import SwiftUI
import PDFKit

struct PDFView: View {
    // The fileName and the page index depend on the navigation split view.
    @Binding var fileName: String?
    @Binding var currentPageIndex: Int
    
    @State private var pdfDocument: PDFDocument? = nil

    //State variables for zoom
    @State private var resetZoom = false
    @State private var zoomedIn = false
    
    // Timer class
    @ObservedObject private var timerManager = TimerManager()
    
    // Variables for scribble
    @State private var annotationsEnabled: Bool = false
    @State private var exitNotSelected: Bool = false

    @State private var selectedScribbleTool: String = ""
    
    @State private var pageChangeEnabled: Bool = true
    @State private var pagePaths: [String: [Path]] = [:]
    @State private var highlightPaths: [String: [Path]] = [:]
    
    @State private var isBookmarked: Bool = false

    var body: some View {
        NavigationStack {
            VStack {
                if let pdfDocument = pdfDocument {
                    ZStack {
                        DocumentView(pdfDocument: pdfDocument, currentPageIndex: $currentPageIndex, resetZoom: $resetZoom, zoomedIn: $zoomedIn)
                            .edgesIgnoringSafeArea(.all)
                            .gesture(dragGesture())
                            .onChange(of: currentPageIndex) {
                                loadPathsForPage(currentPageIndex)
                            }
                        
                        if annotationsEnabled {
                            DrawingCanvas(pagePaths: $pagePaths,
                                          highlightPaths: $highlightPaths,
                                          key: uniqueKey(for: currentPageIndex),
                                          selectedScribbleTool: $selectedScribbleTool,
                                          nextPage: {goToNextPage()},
                                          previousPage: {goToPreviousPage()})
                        }
                    }
                    .toolbar {
                        // Timer Controls
                        ToolbarItemGroup(placement: .navigationBarTrailing) {
                            if timerManager.isTimerRunning {
                                Button(action: timerManager.pauseTimer) {
                                    Image(systemName: "pause.circle")
                                        .foregroundColor(.yellow)
                                }
                                Button(action: timerManager.restartTimer) {
                                    Image(systemName: "arrow.clockwise.circle")
                                        .foregroundColor(.blue)
                                }
                                Button(action: timerManager.cancelTimer) {
                                    Image(systemName: "xmark.circle")
                                        .foregroundColor(.red)
                                }
                            } else if timerManager.isPaused {
                                Button(action: timerManager.unpauseTimer) {
                                    Image(systemName: "play.circle")
                                        .foregroundColor(.green)
                                }
                                Button(action: timerManager.restartTimer) {
                                    Image(systemName: "arrow.clockwise.circle")
                                        .foregroundColor(.blue)
                                }
                                Button(action: timerManager.cancelTimer) {
                                    Image(systemName: "xmark.circle")
                                        .foregroundColor(.red)
                                }
                            } else {
                                Menu {
                                    Button("15 Minutes") { timerManager.startTimer(duration: 15 * 1) }
                                    Button("20 Minutes") { timerManager.startTimer(duration: 20 * 60) }
                                    Button("25 Minutes") { timerManager.startTimer(duration: 25 * 60) }
                                    Button("Clear Timer") { timerManager.cancelTimer() }
                                } label: {
                                    Text("Timer")
                                        .padding(5)
                                        .foregroundColor(.blue)
                                        .cornerRadius(8)
                                }
                            }
                        }
                        
                        // Markup Tools
                        ToolbarItemGroup(placement: .navigationBarTrailing) {
                            // Markup Tools
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
                               Text(selectedScribbleTool.isEmpty ? "Markup" : "Markup: " + selectedScribbleTool)
                               .padding(5)
                               .foregroundColor(exitNotSelected ? Color.pink : Color.gray)
                               .cornerRadius(8)
                             }
                            
                            // Digital Resources
                            Button(action: {
                                print("Digital Resources button tapped")
                            }) {
                                Text("Digital Resources")
                                    .padding(5)
                                    .foregroundColor(.purple)
                                    .cornerRadius(8)
                            }
                            
                            // Bookmark
                            Button(action: {
                                isBookmarked.toggle()
                            }) {
                                Image(systemName: isBookmarked ? "bookmark.fill" : "bookmark")
                                    .foregroundColor(.yellow)
                            }
                            
                            // Reset Zoom
                            if zoomedIn {
                                Button("Reset Zoom") {
                                    resetZoom = true
                                }
                            }
                            if annotationsEnabled{
                                Button("Clear"){
                                    clearMarkup()
                                }
                            }
                        }
                        // Progress Bar as a Toolbar Item
                        ToolbarItem(placement: .bottomBar) {
                            GeometryReader { geometry in
                                Rectangle()
                                    .fill(timerManager.isPaused ? Color.yellow : (timerManager.progress >= 1 ? Color.green : Color.red))
                                    .frame(width: geometry.size.width * CGFloat(timerManager.progress), height: 4)
                                    .animation(.linear(duration: 0.1), value: timerManager.progress)
                            }
                            .frame(maxWidth: .infinity, maxHeight: 4)
                        }
                    }
                } else {
                    ProgressView("Getting Workbook")
                        .onAppear {
                            loadPDFFromURL()
                        }
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
        let key = uniqueKey(for: pageIndex)
        if pagePaths[key] == nil {
            pagePaths[key] = []
        }
        if highlightPaths[key] == nil {
            highlightPaths[key] = []
        }
    }
    
    private func uniqueKey(for pageIndex: Int) -> String {
        guard let fileName = fileName else { return "\(pageIndex)" }
        return "\(fileName)-\(pageIndex)"
    }
    
    private func clearMarkup() {
        highlightPaths.removeValue(forKey: uniqueKey(for: currentPageIndex))
        pagePaths.removeValue(forKey: uniqueKey(for: currentPageIndex))
    }
}
