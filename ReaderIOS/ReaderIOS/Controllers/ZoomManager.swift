import SwiftUI

class ZoomManager: ObservableObject {
    @Published private var zoomedIn: Bool = false
    @Published private var currentZoom: CGFloat = 0
    @Published private var totalZoom: CGFloat = 1.2
    @Published private var zoomPoint: UnitPoint = .center

    private let minZoom: CGFloat = 1.2
    private let maxZoom: CGFloat = 2.55

    // Track the view size, used to convert gesture locations to a UnitPoint
    @Published private var lastViewSize: CGSize?

    func zoomin() -> some Gesture {
        // We'll use SimultaneousGesture to track both magnification and location
        SimultaneousGesture(
            MagnifyGesture()
                .onChanged { value in
                    // Apply zoom limits
                    let potentialNewZoom = self.totalZoom * value.magnification
                    if potentialNewZoom <= self.maxZoom {
                        self.currentZoom = value.magnification - 1
                    } else {
                        self.currentZoom = (self.maxZoom / self.totalZoom) - 1
                    }
                    self.zoomedIn = self.totalZoom + self.currentZoom > self.minZoom
                }
                .onEnded { _ in
                    self.totalZoom = min(self.totalZoom + self.currentZoom, self.maxZoom)
                    self.currentZoom = 0
                    self.zoomedIn = self.totalZoom > self.minZoom
                },
            DragGesture(minimumDistance: 0)
                .onChanged { value in
                    // Only set zoom point at the beginning of zoom
                    if !self.zoomedIn {
                        self.updateZoomPointFromGesture(value.location)
                    }
                }
        )
    }

    // Helper method to update zoom point given a screen coordinate
    func updateZoomPointFromGesture(_ location: CGPoint) {
        // We need the view size to convert to UnitPoint
        if let viewSize = lastViewSize {
            zoomPoint = UnitPoint(
                x: location.x / viewSize.width,
                y: location.y / viewSize.height
            )
        }
    }

    // Update this when view appears or changes size
    func updateViewSize(_ size: CGSize) {
        lastViewSize = size
    }

    func zoomout() -> some Gesture {
        TapGesture(count: 2)
            .onEnded { _ in
                self.resetZoom()
            }
    }

    func newZoomPoint(newPoint: CGPoint, width: CGFloat, height: CGFloat) {
        if !zoomedIn {
            zoomPoint = UnitPoint(x: newPoint.x / width, y: newPoint.y / height)
        }
        // Store the view size for future reference
        lastViewSize = CGSize(width: width, height: height)
    }

    func newZoomLevel() -> CGFloat {
        max(min(totalZoom + currentZoom, maxZoom), minZoom)
    }

    func resetZoom() {
        totalZoom = minZoom
        currentZoom = 0
        zoomedIn = false
        zoomPoint = .center
    }

    func getZoomedIn() -> Bool {
        zoomedIn
    }

    func getZoomPoint() -> UnitPoint {
        zoomPoint
    }

    func panZoomCenter(by translation: CGSize, in viewSize: CGSize) {
        // Store view size for reference
        lastViewSize = viewSize

        let zoomLevel = newZoomLevel()
        let speedMultiplier = max(zoomLevel / 1.35, 0.75)

        // Apply a damping factor as we approach max zoom
        let zoomRatio = zoomLevel / maxZoom
        let dampingFactor = 1.0 - (zoomRatio * 0.1)

        let adjustedMultiplier = speedMultiplier * dampingFactor

        let deltaX = (translation.width / viewSize.width) * adjustedMultiplier
        let deltaY = (translation.height / viewSize.height) * adjustedMultiplier

        let newX = min(max(zoomPoint.x - deltaX, 0), 1)
        let newY = min(max(zoomPoint.y - deltaY, 0), 1)

        zoomPoint = UnitPoint(x: newX, y: newY)
    }
}
