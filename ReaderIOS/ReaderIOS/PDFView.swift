import SwiftUI
import PDFKit

struct PDFView: View {
    // The fileName and the page index depend on the navigation split view.
    @Binding var fileName: String?
    @Binding var currentPage: Int
    @Binding var bookmarkLookup: Dictionary<String, Set<Int>>
    
    @State private var pdfDocument: PDFDocument? = nil

    //State variables for zoom.
    @State private var resetZoom = false;
    @State private var zoomedIn = false;
    
    // State variables for timer.
    @State private var selectedDuration: TimeInterval = 0
    @State private var progress: Double = 0
    @State private var timer: Timer?
    @State private var timerIsRunning: Bool = false
    
    // Variables for scribble
    @State private var scribbleEnabled: Bool = false
    @State private var pageChangeEnabled: Bool = true
    @State private var currentPath = UIBezierPath()
    @State private var pagePaths: [Int: [UIBezierPath]] = [:]
    @State private var eraseEnabled: Bool = false
    
    
    var isCurrentPageBookmarked: Bool {
        // TODO: Use file ID here instead when applicable!
        if let fileName = fileName {
            if let valueSet = bookmarkLookup[fileName] {
                return valueSet.contains(currentPage)
            }
            return false
        }
        return false;
    }
    
    private func toggleCurrentPageInBookmarks() {
        if let fileName = fileName {
            if var valueSet = bookmarkLookup[fileName] {
                if valueSet.contains(currentPage) {
                    valueSet.remove(currentPage)
                } else {
                    valueSet.insert(currentPage)
                }
                bookmarkLookup[fileName] = valueSet
            } else {
                bookmarkLookup[fileName] = Set([currentPage])
            }
        }
    }


    var body: some View {
        VStack {
            ZStack{
                HStack{
                    Spacer()
                }
                
                HStack {
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
                    
                    
                    if timerIsRunning {
                        Button(action: cancelTimer) {
                            Text("Cancel")
                                .padding()
                                .background(Color.red)
                                .foregroundColor(.white)
                                .cornerRadius(8)
                        }
                    }
                    
                    Button(action: enableScribble) {
                        Text(scribbleEnabled ? "Scribble Off" : "Scribble")
                            .padding()
                            .background(scribbleEnabled ? Color.red : Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    
                    if scribbleEnabled{
                        Button(action: eraseScribble){
                            Text("Erase")
                                .padding()
                                .background(eraseEnabled ? Color.red : Color.blue)
                                .foregroundColor(.white)
                                .cornerRadius(10)
                        }
                    }
                 
                }.padding()
                
                HStack{
                    Spacer()
                    
                    // Bookmark toggle button
                    Button(action: {
                        toggleCurrentPageInBookmarks()
                    }) {
                        Image(systemName: isCurrentPageBookmarked ? "bookmark.fill" : "bookmark")
                            .resizable()
                            .frame(width: 24, height: 24)
                            .foregroundColor(isCurrentPageBookmarked ? .yellow : .gray)
                            .padding()
                    }
                    
                    //Reset zoom button
                    if zoomedIn{
                        Button("Reset Zoom") {
                            resetZoom = true
                        }
                    }
                }.padding()
            }


            // Progress Bar
            GeometryReader { geometry in
                Rectangle()
                    .fill(progress >= 1 ? Color.green : Color.red)
                    .frame(width: geometry.size.width * CGFloat(progress), height: 4)
                    .animation(.linear(duration: 0.1), value: progress)
            }
            .frame(height: 4)
            
            if let pdfDocument = pdfDocument {

                ZStack{
                    DocumentView(pdfDocument: pdfDocument, currentPageIndex: $currentPage, resetZoom: $resetZoom, zoomedIn: $zoomedIn)
                        .edgesIgnoringSafeArea(.all)
                        .gesture(dragGesture())
                        .onChange(of: currentPage) {
                            loadPathsForPage(currentPage)
                        }
                    if scribbleEnabled {
                        DrawingCanvas(currentPath: $currentPath,
                                      pagePaths: $pagePaths,
                                      currentPageIndex: currentPage,
                                      eraseEnabled: $eraseEnabled)
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
        if pageChangeEnabled && !zoomedIn{
            DragGesture().onEnded { value in
                if value.translation.width < 0 {
                    goToNextPage()
                } else if value.translation.width > 0 {
                    goToPreviousPage()
                }
            }
        } else{
            DragGesture().onEnded {_ in}
        }
    }

    private func goToNextPage() {
        if let pdfDocument = pdfDocument, currentPage < pdfDocument.pageCount - 1 {
            currentPage += 1
        }
    }

    private func goToPreviousPage() {
        if currentPage > 0 {
            currentPage -= 1
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
    
    private func startTimer(duration: TimeInterval) {
           selectedDuration = duration
           progress = 0
           timer?.invalidate() // Stop any existing timer
            timerIsRunning = true

           timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
               progress += 1 / duration
               if progress >= 1 {
                   timer?.invalidate()
                   timer = nil
                   timerIsRunning = false
               }
           }
       }
    
    private func cancelTimer() {
           timer?.invalidate()
           timer = nil
           progress = 0
           timerIsRunning = false
       }
    
    private func enableScribble(){
        scribbleEnabled = !scribbleEnabled
        pageChangeEnabled = !pageChangeEnabled
        if eraseEnabled {
            eraseEnabled = !eraseEnabled
        }
    }
    
    private func loadPathsForPage(_ pageIndex: Int) {
            if pagePaths[pageIndex] == nil {
                pagePaths[pageIndex] = []
            }
    }
    
    private func eraseScribble(){
        eraseEnabled = !eraseEnabled
    }

}
