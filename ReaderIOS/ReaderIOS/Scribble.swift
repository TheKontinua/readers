import SwiftUI
import PDFKit

struct DrawingCanvas: View {
    @Binding var pagePaths: [Int: [Path]]
    var currentPageIndex: Int
    @Binding var selectedScribbleTool: String
    var nextPage: (() -> Void)?
    var previousPage: (() -> Void)?
    @State private var liveDrawingPath: Path = Path()

    var body: some View {
        Canvas { context, size in
            if let paths = pagePaths[currentPageIndex] {
                for path in paths {
                    context.stroke(Path(path.cgPath), with: .color(.black), lineWidth: 2)
                }
            }
            context.stroke(Path(liveDrawingPath.cgPath), with: .color(.blue), lineWidth: 2)
            if let paths = pagePaths[currentPageIndex] {
                for path in paths {
                    context.stroke(Path(path.cgPath), with: .color(.yellow.opacity(0.5)), lineWidth: 5)
                }
            }
            context.stroke(Path(liveDrawingPath.cgPath), with: .color(.blue.opacity(0.5)), lineWidth: 5)
        }
        .gesture(
            DragGesture(minimumDistance: 0)
                .onChanged { value in
                    if selectedScribbleTool == "Erase" {
                        erasePath(at: value.location)
                    } else if selectedScribbleTool == "Pen" || selectedScribbleTool == "Highlight"{
                        updateLivePath(with: value.location)
                    }
                }
                .onEnded { value in
                    if selectedScribbleTool != ""{
                        finalizeCurrentPath()
                    } else {
                        if value.translation.width < 0 {
                            nextPage?()
                        } else if value.translation.width > 0 {
                            previousPage?()
                        }
                    }
                }
        )
    }
    
    private func erasePath(at location: CGPoint) {
        if let pagePathsForCurrentPage = pagePaths[currentPageIndex] {
            for (index, path) in pagePathsForCurrentPage.enumerated() {
                if path.contains(location) {
                    pagePaths[currentPageIndex]?.remove(at: index)
                    break
                }
            }
        }
    }
    
    private func updateLivePath(with point: CGPoint) {
        if liveDrawingPath.isEmpty {
            liveDrawingPath.move(to: point)
        } else {
            liveDrawingPath.addLine(to: point)
        }
    }
    
    private func finalizeCurrentPath() {
        if !liveDrawingPath.isEmpty {
            pagePaths[currentPageIndex, default: []].append(liveDrawingPath)
            liveDrawingPath = Path()
        }
    }
}
