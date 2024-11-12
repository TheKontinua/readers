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
    
    // Variables for scribble
    @State private var scribbleEnabled: Bool = false
    @State private var pageChangeEnabled: Bool = true
    @State private var currentPath = UIBezierPath()
    @State private var pagePaths: [Int: [UIBezierPath]] = [:]
    @State private var eraseEnabled: Bool = false
    
    @State private var isBookmarked: Bool = false


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
                 
                }
                
                HStack{
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

                ZStack(alignment: .topTrailing) {
                    // The PDF document view
                    DocumentView(pdfDocument: pdfDocument, currentPageIndex: $currentPageIndex, resetZoom: $resetZoom, zoomedIn: $zoomedIn)
                        .edgesIgnoringSafeArea(.all)
                        .gesture(dragGesture())
                        .onChange(of: currentPageIndex) {
                            loadPathsForPage(currentPageIndex)
                        }
                    
                    // Drawing canvas for scribbles
                    if scribbleEnabled {
                        DrawingCanvas(currentPath: $currentPath,
                                      pagePaths: $pagePaths,
                                      currentPageIndex: currentPageIndex,
                                      eraseEnabled: $eraseEnabled)
                    }
                    
                    // Bookmark toggle button in the top-right corner
                    Button(action: {
                        isBookmarked.toggle()
                    }) {
                        Image(systemName: isBookmarked ? "bookmark.fill" : "bookmark")
                            .resizable()
                            .frame(width: 40, height: 60)
                            .padding(20)
                            .foregroundColor(.yellow)
                    }
                }
                .onAppear {
                    currentPageIndex = startingPage
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

#Preview {
    NavigationPDFSplitView()
}
