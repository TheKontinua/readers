import SwiftUI
import PDFKit

struct DocumentView: UIViewRepresentable {
    var pdfDocument: PDFDocument?
    // Binding directly connects the PDF components state with the parent, content view.
    @Binding var currentPageIndex: Int

    func makeUIView(context: Context) -> PDFKit.PDFView {
        let pdfView = PDFKit.PDFView()
        configurePDFView(pdfView)
        return pdfView
    }

    func updateUIView(_ uiView: PDFKit.PDFView, context: Context) {
        guard let pdfDocument = pdfDocument else { return }
        if uiView.document != pdfDocument {
            uiView.document = pdfDocument
        }
        goToPage(in: uiView)
    }

    private func configurePDFView(_ pdfView: PDFKit.PDFView) {
        pdfView.autoScales = true
        pdfView.displayMode = .singlePage
        pdfView.displayDirection = .horizontal
        pdfView.document = pdfDocument
        goToPage(in: pdfView)
    }

    private func goToPage(in pdfView: PDFKit.PDFView) {
        if let page = pdfDocument?.page(at: currentPageIndex) {
            pdfView.go(to: page)
        }
    }
}

struct PDFView: View {
    let PDF_URL = "http://localhost:8000/wb1.pdf";
    @State private var pdfDocument: PDFDocument? = nil
    @State private var currentPageIndex: Int = 0

    var body: some View {
        VStack {
            if let pdfDocument = pdfDocument {
                DocumentView(pdfDocument: pdfDocument, currentPageIndex: $currentPageIndex)
                    .edgesIgnoringSafeArea(.all)
                    .gesture(dragGesture())
            } else {
                Text("Loading PDF...")
                    .onAppear {
                        loadPDF(from: PDF_URL)
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

    private func loadPDF(from urlString: String) {
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
                print("No data found or invalid PDF")
                return
            }

            DispatchQueue.main.async {
                self.pdfDocument = document
                self.currentPageIndex = 0
            }
        }.resume()
    }
}
