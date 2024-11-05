import SwiftUI
import PDFKit

struct PDFView: View {
    let fileName: String
    let startingPage: Int
    @State private var pdfDocument: PDFDocument? = nil
    @State private var currentPageIndex: Int = 0

    var body: some View {
        VStack {
            if let pdfDocument = pdfDocument {
                DocumentView(pdfDocument: pdfDocument, currentPageIndex: $currentPageIndex)
                    .edgesIgnoringSafeArea(.all)
                    .gesture(dragGesture())
                    .onAppear {
                        currentPageIndex = startingPage
                    }
            } else {
                ProgressView("Fetching PDF")
                    .onAppear {
                        loadPDFFromURL()
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
}
