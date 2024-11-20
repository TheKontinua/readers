import SwiftUI
import PDFKit

struct PDFView: View {
    // The fileName and the page index depend on the navigation split view.
    @Binding var fileName: String?
    @Binding var currentPageIndex: Int
    
    @State private var pdfDocument: PDFDocument? = nil

    //State variables for zoom
    @State private var resetZoom = false;
    @State private var zoomedIn = false;
    
    // Timer class
    @ObservedObject private var timerManager = TimerManager()
    
    // Variables for scribble
    @State private var annotationsEnabled: Bool = false
    @State private var exitNotSelected: Bool = false

    @State private var selectedScribbleTool: String = ""
    
    @State private var pageChangeEnabled: Bool = true
    @State private var pagePaths: [Int: [Path]] = [:]
    @State private var highlightPaths: [Int: [Path]] = [:]
    
    @State private var isBookmarked: Bool = false

    var body: some View {
        VStack {
            HStack() {
                if timerManager.isTimerRunning {
                    // Pause button
                    Button(action: timerManager.pauseTimer) {
                        Image(systemName: "pause.circle")
                            .resizable()
                            .frame(width: 24, height: 24)
                            .foregroundColor(.yellow)
                    }

                    // Restart button
                    Button(action: timerManager.restartTimer) {
                        Image(systemName: "arrow.clockwise.circle")
                            .resizable()
                            .frame(width: 24, height: 24)
                            .foregroundColor(.blue)
                    }

                    // Cancel button
                    Button(action: timerManager.cancelTimer) {
                        Image(systemName: "xmark.circle")
                            .resizable()
                            .frame(width: 24, height: 24)
                            .foregroundColor(.red)
                    }
                } else if timerManager.isPaused {
                    // Unpause button
                    Button(action: timerManager.unpauseTimer) {
                        Image(systemName: "play.circle")
                            .resizable()
                            .frame(width: 24, height: 24)
                            .foregroundColor(.green)
                    }
                    // Restart button
                    Button(action: timerManager.restartTimer) {
                        Image(systemName: "arrow.clockwise.circle")
                            .resizable()
                            .frame(width: 24, height: 24)
                            .foregroundColor(.blue)
                    }

                    // Cancel button
                    Button(action: timerManager.cancelTimer) {
                        Image(systemName: "xmark.circle")
                            .resizable()
                            .frame(width: 24, height: 24)
                            .foregroundColor(.red)
                    }
                } else {
                    // Start Timer menu
                    Menu {
                        Button("15 Minutes") { timerManager.startTimer(duration: 15 * 1) }
                        Button("20 Minutes") { timerManager.startTimer(duration: 20 * 60) }
                        Button("25 Minutes") { timerManager.startTimer(duration: 25 * 60) }
                        Button("Clear Timer") {timerManager.cancelTimer() }
                    } label: {
                        Text("Timer")
                            .padding(10)
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(8)
                    }
                }
                
                Menu {
                    Button("Pen") {
                        selectScribbleTool("Pen")
                        annotationsEnabled = true
                        exitNotSelected = true
                    }
                    Button("Highlight") {
                        selectScribbleTool("Highlight")
                        annotationsEnabled = true
                        exitNotSelected = true
                    }
                    Button("Erase") {
                        selectScribbleTool("Erase")
                        annotationsEnabled = true
                        exitNotSelected = true
                    }
                    Button("Text") {
                        selectScribbleTool("Text")
                        annotationsEnabled = true
                        exitNotSelected = true
                    }
                    Button("Exit") {
                        selectScribbleTool("")
                        exitNotSelected = false
                    }
                } label: {
                    Text(selectedScribbleTool.isEmpty ? "Markup" : selectedScribbleTool)
                        .padding(10)
                        .background(exitNotSelected ? Color.red : Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                Button(action: {
                    // Placeholder action for now
                    print("Digital Resources button tapped")
                }) {
                    Text("Digital Resources")
                        .padding(10)
                        .background(Color.purple)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                // Bookmark toggle button
                Button(action: {
                    isBookmarked.toggle()
                }) {
                    Image(systemName: isBookmarked ? "bookmark.fill" : "bookmark")
                        .resizable()
                        .frame(width: 24, height: 24)
                        .foregroundColor(isBookmarked ? .yellow : .yellow)
                        .padding()
                }
    //            HStack {
    //                Spacer()
                    
                    // Reset zoom button
                    if zoomedIn {
                        Button("Reset Zoom") {
                            resetZoom = true
                        }
                    }
                
            }
            
            
//            }

            // Display the progress bar
            GeometryReader { geometry in
                Rectangle()
                    .fill(timerManager.isPaused ? Color.yellow : (timerManager.progress >= 1 ? Color.green : Color.red))
                    .frame(width: geometry.size.width * CGFloat(timerManager.progress), height: 4)
                    .animation(.linear(duration: 0.1), value: timerManager.progress)
            }
            .frame(height: 4)
            
            if let pdfDocument = pdfDocument {
                ZStack {
                    DocumentView(pdfDocument: pdfDocument, currentPageIndex: $currentPageIndex, resetZoom: $resetZoom, zoomedIn: $zoomedIn
)
                        .edgesIgnoringSafeArea(.all)
                        .gesture(dragGesture())
                        .onChange(of: currentPageIndex) {
                            loadPathsForPage(currentPageIndex)
                        }
                    
                    if annotationsEnabled {
                        DrawingCanvas(pagePaths: $pagePaths,
                                      highlightPaths: $highlightPaths,
                                      currentPageIndex: currentPageIndex,
                                      selectedScribbleTool: $selectedScribbleTool,
                                      nextPage: {goToNextPage()},
                                      previousPage: {goToPreviousPage()})
                    }
                }
            } else {
                ProgressView("Getting Workbook")
                    .onAppear {
                        loadPDFFromURL()
                    }
            }
        }
        .onChange(of: fileName) {
            loadPDFFromURL()
        }
    }
    
    private func dragGesture() -> some Gesture {
        if pageChangeEnabled && !zoomedIn {
            return DragGesture().onEnded { value in
                if value.translation.width < 0 {
                    goToNextPage()
                } else if value.translation.width > 0 {
                    goToPreviousPage()
                }
            }
        } else {
            return DragGesture().onEnded { _ in }
        }
    }

    private func goToNextPage() {
        if let pdfDocument = pdfDocument, currentPageIndex < pdfDocument.pageCount - 1 {
            currentPageIndex += 1
        }
    }

    private func goToPreviousPage() {
        if currentPageIndex > 0 {
            currentPageIndex -= 1
        }
    }

    private func loadPDFFromURL() {
        guard let fileName = fileName else {
            return;
        }
        
        let baseURL = "http://localhost:8000/pdfs/"
        let urlString = baseURL + fileName
        guard let url = URL(string: urlString) else {
            print("Invalid URL for file: \(fileName)")
            return
        }

        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                print("Error downloading PDF: \(error.localizedDescription)")
                return
            }

            guard let data = data, let document = PDFDocument(data: data) else {
                print("No data found or invalid PDF from \(url).")
                return
            }

            DispatchQueue.main.async {
                self.pdfDocument = document
            }
        }.resume()
    }

    private func selectScribbleTool(_ tool: String) {
        selectedScribbleTool = tool
    }

    private func loadPathsForPage(_ pageIndex: Int) {
        if pagePaths[pageIndex] == nil {
            pagePaths[pageIndex] = []
        }
    }
}
