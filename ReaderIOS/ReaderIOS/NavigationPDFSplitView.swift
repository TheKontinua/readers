//
//  TableOfContentsSplitView.swift
//  ReaderIOS
//
//  Created by Devin Hadley on 11/10/24.
//
import SwiftUI

struct Workbook: Codable, Identifiable, Hashable {
    let id: UUID = UUID()
    var name: String
    var fileName: String
    var chapters: [Chapter]
    
    private enum CodingKeys: String, CodingKey {
        case name, fileName, chapters
    }
}

struct Chapter: Codable, Identifiable, Hashable {
    let id: UUID = UUID()
    var name: String
    var number: Int
    var firstPage: Int
    
    private enum CodingKeys: String, CodingKey {
        case name, number, firstPage
    }
}


struct NavigationPDFSplitView: View {
    
    @State private var workbooks: [Workbook]? = nil
    @State private var selectedWorkbookID: UUID?
    @State private var selectedChapterID: UUID?
    
    var body: some View {
        NavigationSplitView {
            // Workbook selection
            if let workbooks = workbooks {
                List(workbooks, selection: $selectedWorkbookID) { workbook in
                    Text(workbook.name)
                        .tag(workbook.id)
                }
            } else {
                ProgressView("Fetching Workbooks")
                    .onAppear {
                        fetchWorkbooks()
                    }
            }
            
        } content: {
            // Chapter selection
            if let workbook = selectedWorkbook {
                List(workbook.chapters, selection: $selectedChapterID) { chapter in
                    Text(chapter.name)
                        .tag(chapter.id)
                }
            } else {
                ProgressView()
            }
        } detail: {
            // Detail view for PDF
            if let selectedWorkbook {
                if let selectedChapter {
                    PDFView(fileName: selectedWorkbook.fileName, startingPage: selectedChapter.firstPage)
                } else {
                    Text("Select a chapter.")
                }
            } else {
                ProgressView("Getting the latest workbook.")
            }
        }
    }
    
    var selectedWorkbook: Workbook? {
        workbooks?.first(where: { $0.id == selectedWorkbookID })
    }
    
    var selectedChapter: Chapter? {
        selectedWorkbook?.chapters.first(where: { $0.id == selectedChapterID })
    }
    
    func fetchWorkbooks() {
        guard let url = URL(string: "http://localhost:8000/workbooks.json") else {
            print("Invalid workbooks url.")
            return
        }

        var request = URLRequest(url: url)
        request.cachePolicy = .reloadIgnoringLocalCacheData

        let config = URLSessionConfiguration.default
        config.urlCache = nil
        config.requestCachePolicy = .reloadIgnoringLocalCacheData

        let session = URLSession(configuration: config)

        let task = session.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error fetching workbooks: \(error)")
                return
            }

            guard let data = data else {
                print("No data received from url.")
                return
            }

            do {
                let decoder = JSONDecoder()
                let workbookResponse = try decoder.decode([Workbook].self, from: data)

                DispatchQueue.main.async {
                    self.workbooks = workbookResponse
                    // By default, for now, lets set workbook 1 chapter 1 as default.
                    // Later we should store the last workbook/chapter and load this.
                    
                    if let firstWorkbook = workbooks?.first {
                        if let firstChapter = firstWorkbook.chapters.first {
                            selectedWorkbookID = firstWorkbook.id;
                            selectedChapterID = firstChapter.id;
                        }
                    }
                    
                }

            } catch {
                print("Error decoding JSON: \(error)")
            }
        }

        task.resume()
    }
}
