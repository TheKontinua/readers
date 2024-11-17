//
//  TableOfContentsSplitView.swift
//  ReaderIOS
//
//  Created by Devin Hadley on 11/10/24.
//
import SwiftUI

struct Chapter: Identifiable, Codable {
    let id: String
    let title: String
    let book: String
    let chapNum: Int
    let covers: [Cover]
    let startPage: Int
    let requires: [String]?
    
    enum CodingKeys: String, CodingKey {
        case id, title, book, covers, requires
        case chapNum = "chap_num"
        case startPage = "start_page"
    }
}

struct Cover: Identifiable, Codable {
    let id: String
    let desc: String
    let videos: [Video]?
    let references: [Reference]?
}

struct Video: Identifiable, Codable {
    let id = UUID()
    let link: String
    let title: String
}

struct Reference: Identifiable, Codable {
    let id = UUID()
    let link: String
    let title: String
}

struct Workbook: Codable, Hashable, Identifiable {
    let id: String;
    let metaName: String;
    let pdfName: String;
}

struct NavigationPDFSplitView: View {
    
    @State private var workbooks: [Workbook]? = nil
    @State private var chapters: [Chapter]? = nil
    @State private var selectedWorkbookID: String?
    @State private var selectedChapterID: String?
    
    @State private var currentPage: Int = 0
    @State private var currentPdfFileName: String? = nil;
    
    var body: some View {
        NavigationSplitView {
            // Workbook selection
            if let workbooks = workbooks {
                List(workbooks, selection: $selectedWorkbookID) { workbook in
                    Text(workbook.id)
                        .tag(workbook.id)
                }
            } else {
                ProgressView("Fetching Workbooks")
                    .onAppear {
                        fetchWorkbooks()
                    }
            }
            
            
        }
        content: {
            // Chapter selection
            if let chapters = chapters {
                List(chapters, selection: $selectedChapterID) { chapter in
                    Text(chapter.title)
                        .tag(chapter.id)
                }
            } else {
                ProgressView()
                    .onAppear(perform: fetchChapters)
            }
        } detail: {
            // Detail view for PDF
            if let currentPdfFileName = currentPdfFileName {
                    PDFView(fileName: $currentPdfFileName, currentPageIndex: $currentPage)
            } else {
                ProgressView("Getting the latest workbook.")
            }
        }
        
        .onChange(of: selectedWorkbookID) {
            fetchChapters()
            if let selectedWorkbook = selectedWorkbook {
                currentPdfFileName = selectedWorkbook.pdfName;
                print("Opened \(String(describing: currentPdfFileName))")
            }
        }
        .onChange(of: selectedChapterID){
            if let chapter = selectedChapter {
                currentPage = chapter.startPage - 1;
            }
        }
        
    }
    
    var selectedWorkbook: Workbook? {
        workbooks?.first(where: { $0.id == selectedWorkbookID })
    }
    
    var selectedChapter: Chapter? {
        chapters?.first(where: { $0.id == selectedChapterID })
    }
    
    func fetchChapters() {
        
        guard let fileName = selectedWorkbook?.metaName else {
            return;
        }

        guard let url = URL(string: "http://localhost:8000/meta/\(fileName)") else {
            print("Invalid chapter meta url.")
            return
        }
        
        var request = URLRequest(url: url)
        request.cachePolicy = .reloadIgnoringLocalCacheData

        let config = URLSessionConfiguration.default
        config.urlCache = nil
        config.requestCachePolicy = .reloadIgnoringLocalCacheData

        let session = URLSession(configuration: config)

        let task = session.dataTask(with: request, completionHandler: { data, response, error in
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
                let chapterResponse = try decoder.decode([Chapter].self, from: data)

                DispatchQueue.main.async {
                    chapters = chapterResponse
                    selectedChapterID = chapters?.first?.id
                }

            } catch {
                print("Error decoding chapters: \(error)")
            }
        })

        task.resume()

        
        
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

        let task = session.dataTask(with: request, completionHandler: { data, response, error in
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
                    workbooks = workbookResponse
                    if let id = workbooks?.first?.id {
                        selectedWorkbookID = id
                    }
                }

            } catch {
                print("Error decoding workbooks: \(error)")
            }
        })

        task.resume()
    }

}

#Preview {
    NavigationPDFSplitView()
}
