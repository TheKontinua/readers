import SwiftUI
import PDFKit

struct PDFView: View {
    let fileName: String
    let startingPage: Int
    @State private var pdfDocument: PDFDocument? = nil
    @State private var currentPageIndex: Int = 0

    //State variables for zoom.
    @State private var resetZoom = false;
    @State private var zoomedIn = false;
    
    // State variables for timer.
    @State private var selectedDuration: TimeInterval = 0
    @State private var progress: Double = 0
    @State private var timer: Timer?
    @State private var timerIsRunning: Bool = false
    @State private var remainingDuration: TimeInterval = 0
    @State private var isPaused: Bool = false

    
    // Variables for scribble
    @State private var scribbleEnabled: Bool = false
    @State private var pageChangeEnabled: Bool = true
    @State private var currentPath = UIBezierPath()
    @State private var pagePaths: [Int: [UIBezierPath]] = [:]
    @State private var eraseEnabled: Bool = false
    @State private var selectedScribbleTool: String = "Pen"
    
    @State private var isBookmarked: Bool = false
    

    var body: some View {
        VStack {
            HStack {
                // UI Section
                if timerIsRunning {
                    // Pause button
                    Button(action: pauseTimer) {
                        Image(systemName: "pause.circle")
                            .resizable()
                            .frame(width: 24, height: 24)
                            .foregroundColor(.yellow)
                            .padding()
                    }

                    // Restart button
                    Button(action: restartTimer) {
                        Image(systemName: "arrow.clockwise.circle")
                            .resizable()
                            .frame(width: 24, height: 24)
                            .foregroundColor(.green)
                            .padding()
                    }

                    // Cancel button
                    Button(action: cancelTimer) {
                        Image(systemName: "xmark.circle")
                            .resizable()
                            .frame(width: 24, height: 24)
                            .foregroundColor(.red)
                            .padding()
                    }
                } else if isPaused {
                    // Unpause button
                    Button(action: unpauseTimer) {
                        Image(systemName: "play.circle")
                            .resizable()
                            .frame(width: 24, height: 24)
                            .foregroundColor(.green)
                            .padding()
                    }
                    // Restart button
                    Button(action: restartTimer) {
                        Image(systemName: "arrow.clockwise.circle")
                            .resizable()
                            .frame(width: 24, height: 24)
                            .foregroundColor(.green)
                            .padding()
                    }


                    // Cancel button
                    Button(action: cancelTimer) {
                        Image(systemName: "xmark.circle")
                            .resizable()
                            .frame(width: 24, height: 24)
                            .foregroundColor(.red)
                            .padding()
                    }
                } else {
                    // Start Timer menu
                    Menu {
                        Button("15 Minutes") { startTimer(duration: 15 * 60) }
                        Button("20 Minutes") { startTimer(duration: 20 * 60) }
                        Button("25 Minutes") { startTimer(duration: 25 * 60) }
                    } label: {
                        Text("Start Timer")
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(8)
                    }
                }
                
                Menu {
                    Button("Pen") { selectScribbleTool("Pen") }
                    Button("Highlight") { selectScribbleTool("Highlight") }
                    Button("Erase") { selectScribbleTool("Erase") }
                } label: {
                    Text("Markup: \(selectedScribbleTool)")
                        .padding()
                        .background(scribbleEnabled ? Color.red : Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                Button(action: {
                    // Placeholder action for now
                    print("Digital Resources button tapped")
                }) {
                    Text("Digital Resources")
                        .padding()
                        .background(Color.purple)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
            }
            
            .padding()

            HStack {
            
                Spacer()
                
                
                // Bookmark toggle button
                Button(action: {
                    isBookmarked.toggle()
                }) {
                    Image(systemName: isBookmarked ? "bookmark.fill" : "bookmark")
                        .resizable()
                        .frame(width: 24, height: 24)
                        .foregroundColor(isBookmarked ? .yellow : .gray)
                        .padding()
                }
                
                // Reset zoom button
                if zoomedIn {
                    Button("Reset Zoom") {
                        resetZoom = true
                    }
                }
            }
            .padding()

            // Progress Bar
            GeometryReader { geometry in
                Rectangle()
                    .fill(progress >= 1 ? Color.green : Color.red)
                    .frame(width: geometry.size.width * CGFloat(progress), height: 4)
                    .animation(.linear(duration: 0.1), value: progress)
            }
            .frame(height: 4)
            
            if let pdfDocument = pdfDocument {
                ZStack {
                    DocumentView(pdfDocument: pdfDocument, currentPageIndex: $currentPageIndex, resetZoom: $resetZoom, zoomedIn: $zoomedIn)
                        .edgesIgnoringSafeArea(.all)
                        .gesture(dragGesture())
                        .onChange(of: currentPageIndex) {
                            loadPathsForPage(currentPageIndex)
                        }
                    if scribbleEnabled {
                        DrawingCanvas(currentPath: $currentPath,
                                      pagePaths: $pagePaths,
                                      currentPageIndex: currentPageIndex,
                                      eraseEnabled: $eraseEnabled)
                    }
                }
                .onAppear {
                    currentPageIndex = startingPage
                }
            } else {
                ProgressView("Getting Workbook")
                    .onAppear {
                        loadPDFFromURL()
                    }
            }
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
        let baseURL = "http://localhost:8000/"
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
                self.currentPageIndex = startingPage
            }
        }.resume()
    }
    
    private func startTimer(duration: TimeInterval) {
        selectedDuration = duration
        progress = 0
        remainingDuration = duration
        timer?.invalidate() // Stop any existing timer
        timerIsRunning = true
        isPaused = false
        
        timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
            progress += 1 / duration
            remainingDuration -= 1
            if remainingDuration <= 0 {
                timer?.invalidate()
                timer = nil
                timerIsRunning = false
            }
        }
    }
    // Pause Timer function
    private func pauseTimer() {
        timer?.invalidate()
        timer = nil
        timerIsRunning = false
        isPaused = true
    }
    // Unpause Timer function
    private func unpauseTimer() {
        timerIsRunning = true
        isPaused = false

        timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
            progress += 1 / selectedDuration
            remainingDuration -= 1
            if remainingDuration <= 0 {
                timer?.invalidate()
                timer = nil
                timerIsRunning = false
            }
        }
    }
    // Restart Timer function
    private func restartTimer() {
        startTimer(duration: selectedDuration)
    }
    
    // Cancel Timer function
    private func cancelTimer() {
        timer?.invalidate()
        timer = nil
        progress = 0
        remainingDuration = 0
        timerIsRunning = false
        isPaused = false
    }
    
    private func selectScribbleTool(_ tool: String) {
        selectedScribbleTool = tool
        if tool == "Erase" {
            eraseEnabled = true
        } else {
            eraseEnabled = false
        }
    }

    private func loadPathsForPage(_ pageIndex: Int) {
        if pagePaths[pageIndex] == nil {
            pagePaths[pageIndex] = []
        }
    }
}
