import SwiftUI
import PDFKit

struct DrawingCanvas: View {
    @Binding var currentPath: UIBezierPath
    @Binding var pagePaths: [Int: [UIBezierPath]]
    var currentPageIndex: Int
    @Binding var eraseEnabled: Bool

    var body: some View {
        Canvas { context, size in
            if let paths = pagePaths[currentPageIndex] {
                for path in paths {
                    context.stroke(Path(path.cgPath), with: .color(.black), lineWidth: 2)
                }
            }
            context.stroke(Path(currentPath.cgPath), with: .color(.black), lineWidth: 2)
        }
        .gesture(
            DragGesture(minimumDistance: 0)
                .onChanged { value in
                    if eraseEnabled {
                        erasePath(at: value.location)
                    } else{
                        if currentPath.isEmpty {
                            currentPath.move(to: value.location)
                        } else {
                            currentPath.addLine(to: value.location)
                        }
                    }
                }
                .onEnded { _ in
                    if pagePaths[currentPageIndex] == nil {
                        pagePaths[currentPageIndex] = []
                    }
                    pagePaths[currentPageIndex]?.append(currentPath)
                    currentPath = UIBezierPath()
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
}
