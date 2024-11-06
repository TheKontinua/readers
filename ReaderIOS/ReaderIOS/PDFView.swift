import SwiftUI
import PDFKit

struct PDFView: View {
    //where we are serving the pdfs
    let PDF_URL = "http://localhost:8000/wb1.pdf";
    @State private var pdfDocument: PDFDocument? = nil
    @State private var currentPageIndex: Int = 0
    
    //state variables for timer stuff
    @State private var selectedDuration: TimeInterval = 0
    @State private var progress: Double = 0
    @State private var timer: Timer?
    @State private var timerIsRunning: Bool = false


    var body: some View {
        VStack {
            //set timer button
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
                DocumentView(pdfDocument: pdfDocument, currentPageIndex: $currentPageIndex)
                    .edgesIgnoringSafeArea(.all)
                    .gesture(dragGesture())
            } else {
                Text("Loading PDF...")
                    .onAppear {
                        loadPDFFromURL(from: PDF_URL)
                    }
            }
        }
    }

    private func dragGesture() -> some Gesture {
        DragGesture().onEnded { value in
            if value.translation.width < 0 {
                goToNextPage()
            } else if value.translation.width > 0 {
                goToPreviousPage()
            }
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

    private func loadPDFFromURL(from urlString: String) {
        guard let url = URL(string: urlString) else {
            print("Invalid URL")
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
                self.currentPageIndex = 0
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
}

