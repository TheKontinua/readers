import PDFKit
import SwiftUI

struct URLItem: Identifiable {
    let id = UUID()
    let url: URL
}

struct PDFView: View {
    @Binding var fileName: String?
    @Binding var currentPage: Int
    @Binding var bookmarkLookup: [String: Set<Int>]
    @Binding var covers: [Cover]?

    @State private var pdfDocument: PDFDocument?
    @State private var selectedLink: URLItem?
    @State private var resetZoom = false
    @State private var zoomedIn = false
    @State private var showingFeedback = false

    @ObservedObject private var timerManager = TimerManager()
    @State private var annotationsEnabled: Bool = false
    @State private var exitNotSelected: Bool = false
    @State private var selectedScribbleTool: String = ""
    @State private var pageChangeEnabled: Bool = true
    @State private var pagePaths: [String: [Path]] = [:]
    @State private var highlightPaths: [String: [Path]] = [:]

    @ObservedObject private var annotationManager = AnnotationManager()

    var body: some View {
        NavigationStack {
            ZStack {
                VStack {
                    if let pdfDocument = pdfDocument {
                        ZStack {
                            DocumentView(
                                pdfDocument: pdfDocument,
                                currentPageIndex: $currentPage,
                                resetZoom: $resetZoom,
                                zoomedIn: $zoomedIn
                            )
                            .edgesIgnoringSafeArea(.all)
                            .gesture(dragGesture())
                            .onChange(of: currentPage) {
                                loadPathsForPage(currentPage)
                            }
                            if annotationsEnabled {
                                AnnotationsView(
                                    pagePaths: $pagePaths,
                                    highlightPaths: $highlightPaths,
                                    key: uniqueKey(for: currentPage),
                                    selectedScribbleTool: $selectedScribbleTool,
                                    nextPage: { goToNextPage() },
                                    previousPage: { goToPreviousPage() }
                                )
                            }
                        }
                        .toolbar(content: {
                            ToolbarItemGroup(placement: .navigationBarTrailing, content: {
                                if timerManager.isTimerRunning {
                                    Button(action: timerManager.pauseTimer, label: {
                                        Image(systemName: "pause.circle")
                                            .foregroundColor(.yellow)
                                    })
                                    Button(action: timerManager.restartTimer, label: {
                                        Image(systemName: "arrow.clockwise.circle")
                                            .foregroundColor(.blue)
                                    })
                                    Button(action: timerManager.cancelTimer, label: {
                                        Image(systemName: "xmark.circle")
                                            .foregroundColor(.red)
                                    })
                                } else if timerManager.isPaused {
                                    Button(action: timerManager.unpauseTimer, label: {
                                        Image(systemName: "play.circle")
                                            .foregroundColor(.green)
                                    })
                                    Button(action: timerManager.restartTimer, label: {
                                        Image(systemName: "arrow.clockwise.circle")
                                            .foregroundColor(.blue)
                                    })
                                    Button(action: timerManager.cancelTimer, label: {
                                        Image(systemName: "xmark.circle")
                                            .foregroundColor(.red)
                                    })
                                } else {
                                    Menu(content: {
                                        Button("15 Minutes", action: { timerManager.startTimer(duration: 15 * 60) })
                                        Button("20 Minutes", action: { timerManager.startTimer(duration: 20 * 60) })
                                        Button("25 Minutes", action: { timerManager.startTimer(duration: 25 * 60) })
                                        Button("Clear Timer", action: { timerManager.cancelTimer() })
                                    }, label: {
                                        Text("Timer")
                                            .padding(5)
                                            .foregroundColor(.blue)
                                            .cornerRadius(8)
                                    })
                                }
                            })

                            ToolbarItemGroup(placement: .navigationBarTrailing, content: {
                                Menu(content: {
                                    Button("Pen", action: {
                                        selectScribbleTool("Pen")
                                        annotationsEnabled = true
                                        exitNotSelected = true
                                    })
                                    Button("Highlight", action: {
                                        selectScribbleTool("Highlight")
                                        annotationsEnabled = true
                                        exitNotSelected = true
                                    })
                                    Button("Erase", action: {
                                        selectScribbleTool("Erase")
                                        annotationsEnabled = true
                                        exitNotSelected = true
                                    })
                                    Button("Text", action: {
                                        selectScribbleTool("Text")
                                        annotationsEnabled = true
                                        exitNotSelected = true
                                    })
                                    Button("Exit", action: {
                                        selectScribbleTool("")
                                        exitNotSelected = false
                                        annotationManager.saveAnnotations(
                                            pagePaths: pagePaths,
                                            highlightPaths: highlightPaths
                                        )
                                    })
                                }, label: {
                                    Text(selectedScribbleTool.isEmpty ? "Markup" : "Markup: " + selectedScribbleTool)
                                        .padding(5)
                                        .foregroundColor(exitNotSelected ? .pink : .gray)
                                        .cornerRadius(8)
                                })

                                Menu(content: {
                                    if let covers = covers, !covers.isEmpty {
                                        ForEach(covers) { cover in
                                            Menu(content: {
                                                if let videos = cover.videos, !videos.isEmpty {
                                                    Section(header: Text("Videos"), content: {
                                                        ForEach(videos) { video in
                                                            Button(action: {
                                                                if let url = URL(string: video.link) {
                                                                    selectedLink = URLItem(url: url)
                                                                }
                                                            }, label: {
                                                                Text(video.title)
                                                            })
                                                        }
                                                    })
                                                }
                                                if let references = cover.references, !references.isEmpty {
                                                    Section(header: Text("References"), content: {
                                                        ForEach(references) { reference in
                                                            Button(action: {
                                                                if let url = URL(string: reference.link) {
                                                                    selectedLink = URLItem(url: url)
                                                                }
                                                            }, label: {
                                                                Text(reference.title)
                                                            })
                                                        }
                                                    })
                                                }
                                                if cover.videos?.isEmpty ?? true,
                                                   cover.references?.isEmpty ?? true
                                                {
                                                    Text("No Videos or References Available")
                                                }
                                            }, label: {
                                                Text(cover.desc)
                                            })
                                        }
                                    } else {
                                        Text("No Digital Resources Available")
                                    }
                                }, label: {
                                    Text("Digital Resources")
                                        .padding(5)
                                        .foregroundColor((covers?.isEmpty ?? true) ? .gray : .purple)
                                        .cornerRadius(8)
                                })
                                .disabled(covers?.isEmpty ?? true)

                                Button(action: {
                                    toggleCurrentPageInBookmarks()
                                }, label: {
                                    Image(systemName: isCurrentPageBookmarked ? "bookmark.fill" : "bookmark")
                                        .foregroundColor(.yellow)
                                })

                                if zoomedIn {
                                    Button("Reset Zoom", action: {
                                        resetZoom = true
                                    })
                                }
                                if annotationsEnabled {
                                    Button("Clear", action: {
                                        clearMarkup()
                                    })
                                }
                            })

                            ToolbarItem(placement: .bottomBar, content: {
                                GeometryReader { geometry in
                                    Rectangle()
                                        .fill(timerManager.isPaused ?
                                            .yellow : (timerManager.progress >= 1 ? .green : .red))
                                        .frame(width: geometry.size.width * CGFloat(timerManager.progress),
                                               height: 4)
                                        .animation(.linear(duration: 0.1), value: timerManager.progress)
                                }
                                .frame(maxWidth: .infinity, maxHeight: 4)
                            })
                        })
                    } else {
                        ProgressView("Getting Workbook")
                            .onAppear {
                                loadPDFFromURL()
                                annotationManager.loadAnnotations(
                                    pagePaths: &pagePaths,
                                    highlightPaths: &highlightPaths
                                )
                                if !pagePaths.isEmpty || !highlightPaths.isEmpty {
                                    annotationsEnabled = true
                                }
                            }
                    }
                }
                VStack {
                    Spacer()
                    HStack {
                        Spacer()
                        Button(action: {
                            showingFeedback = true
                        }, label: {
                            Image(systemName: "message.fill")
                                .font(.system(size: 24))
                                .foregroundColor(.white)
                                .padding(15)
                                .background(Color.blue)
                                .clipShape(Circle())
                                .shadow(radius: 4)
                        })
                        .padding(.trailing, 70)
                        .padding(.bottom, 30)
                    }
                }
            }
            .sheet(isPresented: $showingFeedback, content: {
                FeedbackView()
            })
        }
        .sheet(item: $selectedLink, onDismiss: {
            print("WebView dismissed. Cleaning up resources.")
        }, content: { linkItem in
            WebView(url: linkItem.url)
        })
        .onChange(of: fileName) {
            loadPDFFromURL()
        }
    }

    private func dragGesture() -> some Gesture {
        if pageChangeEnabled, !zoomedIn {
            return DragGesture().onEnded { value in
                if value.translation.width < 0 {
                    goToNextPage()
                } else if value.translation.width > 0 {
                    goToPreviousPage()
                }
            }
        } else {
            return DragGesture().onEnded { _ in }
        }
    }

    private func goToNextPage() {
        if let pdfDocument = pdfDocument, currentPage < pdfDocument.pageCount - 1 {
            currentPage += 1
        }
    }

    private func goToPreviousPage() {
        if currentPage > 0 {
            currentPage -= 1
        }
    }

    private func loadPDFFromURL() {
        guard let fileName = fileName else { return }

        let baseURL = "http://localhost:8000/pdfs/"
        let urlString = baseURL + fileName
        guard let url = URL(string: urlString) else {
            print("Invalid URL for file: \(fileName)")
            return
        }

        URLSession.shared.dataTask(with: url) { data, _, error in
            if let error = error {
                print("Error downloading PDF: \(error.localizedDescription)")
                return
            }
            guard let data = data, let document = PDFDocument(data: data) else {
                print("No data found or invalid PDF from \(url).")
                return
            }
            DispatchQueue.main.async {
                pdfDocument = document
            }
        }.resume()
    }

    private func selectScribbleTool(_ tool: String) {
        selectedScribbleTool = tool
    }

    private func loadPathsForPage(_ pageIndex: Int) {
        let key = uniqueKey(for: pageIndex)
        if pagePaths[key] == nil {
            pagePaths[key] = []
        }
        if highlightPaths[key] == nil {
            highlightPaths[key] = []
        }
    }

    private func uniqueKey(for pageIndex: Int) -> String {
        guard let fileName = fileName else { return "\(pageIndex)" }
        return "\(fileName)-\(pageIndex)"
    }

    private func clearMarkup() {
        highlightPaths.removeValue(forKey: uniqueKey(for: currentPage))
        pagePaths.removeValue(forKey: uniqueKey(for: currentPage))
    }

    var isCurrentPageBookmarked: Bool {
        if let fileName = fileName {
            if let valueSet = bookmarkLookup[fileName] {
                return valueSet.contains(currentPage)
            }
            return false
        }
        return false
    }

    private func toggleCurrentPageInBookmarks() {
        if let fileName = fileName {
            if var valueSet = bookmarkLookup[fileName] {
                if valueSet.contains(currentPage) {
                    valueSet.remove(currentPage)
                } else {
                    valueSet.insert(currentPage)
                }
                bookmarkLookup[fileName] = valueSet
            } else {
                bookmarkLookup[fileName] = Set([currentPage])
            }
        }
    }
}

#Preview {
    NavigationPDFSplitView()
}
