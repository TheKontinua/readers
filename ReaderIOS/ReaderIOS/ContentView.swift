import SwiftUI
import PDFKit

// Step 1: Create a UIViewRepresentable for PDFView
struct PDFKitRepresentedView: UIViewRepresentable {
    var url: URL
    
    func makeUIView(context: Context) -> PDFView {
        let pdfView = PDFView()
        pdfView.autoScales = true
        pdfView.document = PDFDocument(url: url)
        return pdfView
    }
    
    func updateUIView(_ uiView: PDFView, context: Context) {
        // No updates needed for this simple use case
    }
}

struct ContentView: View {
    var body: some View {
        VStack {
            // Horizontal Stack for icon and text
            HStack {
                Image(systemName: "book")
                    .imageScale(.large)
                    .foregroundStyle(.tint)
                Text("E-reader")
            }
            .padding()

            // PDF viewer with dynamic frame adjustment
            if let url = Bundle.main.url(forResource: "ac", withExtension: "pdf") {
                GeometryReader { geometry in
                    PDFKitRepresentedView(url: url)
                        .frame(width: geometry.size.width, height: 1050) // Adjust width to fit the view
                        .padding(.top, 10.0)
                }
                .frame(height: 1050) // Set the height for GeometryReader
            } else {
                Text("PDF file not found")
            }
        }
        .padding()
    }
}

// Step 2: Add a preview provider
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
