import SwiftUI
import PDFKit

struct DrawingCanvas: View {
    @Binding var pagePaths: [Int: [Path]]
    @Binding var highlightPaths: [Int: [Path]]
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
            if let hPaths = highlightPaths[currentPageIndex] {
                for path in hPaths {
                    context.stroke(Path(path.cgPath), with: .color(.yellow.opacity(0.5)), lineWidth: 5)
                }
            }
            context.stroke(Path(liveDrawingPath.cgPath), with: selectedScribbleTool == "Highlight" ? .color(.blue.opacity(0.5)) : .color(.blue), lineWidth: selectedScribbleTool == "Highlight" ? 5 : 2)
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
                    if selectedScribbleTool == "Pen"{
                        finalizeCurrentPath(for: &pagePaths)
                    } else if selectedScribbleTool == "Highlight"{
                        finalizeCurrentPath(for: &highlightPaths)
                    } else if selectedScribbleTool == ""{
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
    
    private func finalizeCurrentPath(for pathDirectory: inout [Int: [Path]]) {
        if !liveDrawingPath.isEmpty {
            pathDirectory[currentPageIndex, default: []].append(liveDrawingPath)
            liveDrawingPath = Path()
        }
    }
}
