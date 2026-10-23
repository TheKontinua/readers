import PDFKit
import SwiftUI

enum TapConstants {
    /// Fraction of the window width at each edge that turns the page when tapped.
    static let pageTurnTapRatio = 0.25
    /// A touch that moves less than this many points is treated as a tap rather than a swipe.
    static let maxTapMovement: CGFloat = 10
}

struct AnnotationsView: View {
    // MARK: - Bindings

    @Binding var pagePaths: [String: [(path: Path, color: Color)]]
    @Binding var highlightPaths: [String: [(path: Path, color: Color)]]
    @Binding var selectedScribbleTool: AnnotationMode
    @Binding var textOpened: Bool

    // MARK: - Input Parameters

    let key: String
    let nextPage: (() -> Void)?
    let previousPage: (() -> Void)?
    /// The PDF page currently displayed, used to follow links inside the document.
    let pdfPage: PDFPage?
    let goToPage: ((Int) -> Void)?
    @Binding var selectedColor: Color
    @Binding var selectedHighlighterColor: Color
    let zoomedIn: Bool
    let zoomManager: ZoomManager

    // MARK: - Observed Objects

    @ObservedObject var annotationManager: AnnotationStorageManager
    @ObservedObject var textManager: TextManager

    // MARK: - Binding Data

    @Binding var textBoxes: [String: [TextBoxData]]
    @Binding var isHidden: Bool
    let pageFrame: CGRect

    // MARK: - Local State

    @State private var liveDrawingPath: Path = .init()

    @State private var lastDragValue: CGSize = .zero

    // MARK: - Body

    var body: some View {
        GeometryReader { geometry in
            // Catches taps in the margins beside the page, which the page-sized canvas doesn't cover.
            Color.clear
                .contentShape(Rectangle())
                .onTapGesture(count: 1, coordinateSpace: .local) { location in
                    if textOpened {
                        textOpened = false
                        return
                    }
                    handlePageTurnTap(atWindowX: location.x, windowWidth: geometry.size.width)
                }

            ZStack(alignment: .bottomLeading) {
                Canvas { context, _ in
                    if !isHidden {
                        // Draw saved paths
                        if let paths = pagePaths[key] {
                            for pathInfo in paths {
                                context.stroke(Path(pathInfo.path.cgPath),
                                               with: .color(pathInfo.color),
                                               lineWidth: 2)
                            }
                        }
                        if let hPaths = highlightPaths[key] {
                            for pathInfo in hPaths {
                                context.stroke(pathInfo.path,
                                               with: .color(pathInfo.color.opacity(0.2)),
                                               lineWidth: 15)
                            }
                        }
                        // Draw live drawing path
                        context.stroke(Path(liveDrawingPath.cgPath),
                                       with: selectedScribbleTool == .highlight ?
                                           .color(selectedHighlighterColor.opacity(0.2)) :
                                           .color(selectedColor),
                                       lineWidth: selectedScribbleTool == .highlight ? 15 : 2)
                    }
                }
                .gesture(
                    DragGesture(minimumDistance: 0.0001)
                        .onChanged { value in
                            if zoomManager.getZoomedIn(), selectedScribbleTool == .none {
                                // Calculate the incremental translation since the last update.
                                let delta = CGSize(
                                    width: value.translation.width - lastDragValue.width,
                                    height: value.translation.height - lastDragValue.height
                                )
                                zoomManager.panZoomCenter(by: delta, in: geometry.size)
                                lastDragValue = value.translation
                            } else {
                                // Existing logic for drawing/erasing
                                if isHidden { return }
                                if selectedScribbleTool == .erase {
                                    erasePath(at: value.location)
                                } else if selectedScribbleTool == .pen || selectedScribbleTool == .highlight {
                                    updateLivePath(with: value.location)
                                }
                            }
                        }
                        .onEnded { value in
                            // Reset the incremental drag offset
                            lastDragValue = .zero

                            // A touch that barely moved is a tap, handled by the tap gesture below.
                            let isTap = abs(value.translation.width) < TapConstants.maxTapMovement
                                && abs(value.translation.height) < TapConstants.maxTapMovement
                            if isTap, selectedScribbleTool == .none || selectedScribbleTool == .text {
                                return
                            }

                            if !zoomManager.getZoomedIn() || selectedScribbleTool != .none {
                                if selectedScribbleTool == .none || selectedScribbleTool == .text || isHidden {
                                    // Page change logic (swipe left/right) only when not zoomed in.
                                    if value.translation.width < 0 {
                                        nextPage?()
                                    } else if value.translation.width > 0 {
                                        previousPage?()
                                    }
                                    textOpened = false
                                } else if selectedScribbleTool == .pen {
                                    finalizeCurrentPath(for: &pagePaths, using: selectedColor)
                                } else if selectedScribbleTool == .highlight {
                                    finalizeCurrentPath(for: &highlightPaths, using: selectedHighlighterColor)
                                }
                                annotationManager.saveAnnotations(pagePaths: pagePaths, highlightPaths: highlightPaths)
                                textManager.saveTextBoxes(textBoxes: textBoxes)
                            }
                        }
                )
                // Use the updated zoomManager gestures
                .simultaneousGesture(zoomManager.zoomin())
                .simultaneousGesture(zoomManager.zoomout())
                // Runs alongside the drag so taps are recognized even though the drag claims every touch.
                .simultaneousGesture(
                    SpatialTapGesture()
                        .onEnded { value in
                            handleTap(at: value.location, in: geometry.size)
                        }
                )
                if showsVisibilityToggle {
                    Image(systemName: isHidden ? "eye.slash" : "eye")
                        .foregroundStyle(Color.blue)
                        .font(.system(size: 25))
                        .padding()
                        .onTapGesture {
                            isHidden.toggle()
                        }
                        .zIndex(999)
                }
            }
            .frame(width: pageFrame.width, height: pageFrame.height)
            .offset(x: pageFrame.origin.x, y: pageFrame.origin.y)
        }
        // Listen for geometry changes to update zoom manager
        .background(GeometryReader { geometry in
            Color.clear
                .onAppear {
                    zoomManager.updateViewSize(geometry.size)
                }
                .onChange(of: geometry.size) { _, newSize in
                    zoomManager.updateViewSize(newSize)
                }
        })
        .overlay(alignment: .bottomLeading) {
            if showsVisibilityToggle {
                Image(systemName: isHidden ? "eye.slash" : "eye")
                    .foregroundStyle(Color.blue)
                    .font(.system(size: 25))
                    .padding()
                    .onTapGesture {
                        isHidden.toggle()
                    }
                    .zIndex(999)
            }
        }
    }

    // MARK: - Private Helpers

    /// The show/hide-markup eye icon appears when markup is hidden or the page has any markup.
    private var showsVisibilityToggle: Bool {
        isHidden
            || !(textBoxes[key]?.isEmpty ?? true)
            || !(pagePaths[key]?.isEmpty ?? true)
            || !(highlightPaths[key]?.isEmpty ?? true)
    }

    /// Handles a tap on the page canvas. `location` is in canvas coordinates.
    private func handleTap(at location: CGPoint, in size: CGSize) {
        zoomManager.newZoomPoint(newPoint: location, width: size.width, height: size.height)

        if !textOpened, selectedScribbleTool == .text {
            textOpened = true
            textManager.addText(textBoxes: $textBoxes, key: key, width: size.width, height: size.height)
            textManager.saveTextBoxes(textBoxes: textBoxes)
            return
        }
        if textOpened {
            textOpened = false
            return
        }

        // This canvas covers the PDF and takes its touches, so follow PDF links here.
        if selectedScribbleTool == .none, let destination = linkDestination(at: location) {
            goToPage?(destination)
            return
        }

        // The canvas is offset to the page frame, so convert to window coordinates.
        handlePageTurnTap(atWindowX: location.x + pageFrame.origin.x, windowWidth: size.width)
    }

    /// Returns the destination page index of an internal link under `location` (canvas coordinates), if any.
    private func linkDestination(at location: CGPoint) -> Int? {
        guard let page = pdfPage, let document = page.document,
              pageFrame.width > 0, pageFrame.height > 0 else { return nil }

        // The canvas exactly covers the page's crop box; PDF page space has its origin at the bottom left.
        let bounds = page.bounds(for: .cropBox)
        let pagePoint = CGPoint(
            x: bounds.minX + location.x / pageFrame.width * bounds.width,
            y: bounds.maxY - location.y / pageFrame.height * bounds.height
        )

        // Don't compare `annotation.type` to `PDFAnnotationSubtype.link.rawValue`: one is "Link", the other "/Link".
        guard let annotation = page.annotation(at: pagePoint) else { return nil }

        let destination = annotation.destination ?? (annotation.action as? PDFActionGoTo)?.destination
        guard let destinationPage = destination?.page else { return nil }

        let index = document.index(for: destinationPage)
        return index == NSNotFound ? nil : index
    }

    /// Turns the page when a tap lands in the left or right quarter of the window.
    /// Taps in the middle half, in a markup mode, or while zoomed in are ignored.
    private func handlePageTurnTap(atWindowX windowX: CGFloat, windowWidth: CGFloat) {
        guard selectedScribbleTool == .none, !zoomManager.getZoomedIn() else { return }

        if windowX < windowWidth * TapConstants.pageTurnTapRatio {
            previousPage?()
        } else if windowX > windowWidth * (1 - TapConstants.pageTurnTapRatio) {
            nextPage?()
        }
    }

    /// Removes the first pen path and the first highlight path under `location`.
    private func erasePath(at location: CGPoint) {
        if let index = pagePaths[key]?.firstIndex(where: { $0.path.contains(location) }) {
            pagePaths[key]?.remove(at: index)
        }
        if let index = highlightPaths[key]?.firstIndex(where: { $0.path.contains(location) }) {
            highlightPaths[key]?.remove(at: index)
        }
    }

    private func updateLivePath(with point: CGPoint) {
        if liveDrawingPath.isEmpty {
            liveDrawingPath.move(to: point)
        } else {
            liveDrawingPath.addLine(to: point)
        }
    }

    private func finalizeCurrentPath(for paths: inout [String: [(path: Path, color: Color)]],
                                     using color: Color)
    {
        guard !liveDrawingPath.isEmpty else { return }
        paths[key, default: []].append((path: liveDrawingPath, color: color))
        liveDrawingPath = Path()
    }
}
