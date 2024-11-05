import SwiftUI

struct Workbook: Codable {
    var name: String
    var fileName: String
    var chapters: [Chapter]
}

struct Chapter: Codable {
    var name: String
    var number: Int
    var firstPage: Int
}

struct OutlineItem: Identifiable {
    let id = UUID()
    var name: String
    var children: [OutlineItem]?
    var chapter: Chapter?
    var workbookFileName: String?
}

struct TableOfContents: View {
    @State private var workbooks: [Workbook]? = nil

    func getOutlineItems(books: [Workbook]?) -> [OutlineItem] {
        if let books = books {
            return books.map { workbook in
                OutlineItem(
                    name: workbook.name,
                    children: workbook.chapters.map { chapter in
                        OutlineItem(
                            name: chapter.name,
                            chapter: chapter,
                            workbookFileName: workbook.fileName
                        )
                    }
                )
            }
        } else {
            return []
        }
    }

    var body: some View {
        if let workbooks = workbooks {
            List {
                OutlineGroup(getOutlineItems(books: workbooks), children: \.children) { item in
                    if let chapter = item.chapter, let fileName = item.workbookFileName {
                        NavigationLink(destination: PDFView(fileName: fileName, startingPage: chapter.firstPage)) {
                            Text(item.name)
                        }
                    } else {
                        Text(item.name)
                    }
                }
            }
            .navigationTitle("Table of Contents")
        } else {
            Text("Fetching workbooks...")
                .onAppear {
                    fetchWorkbooks()
                }
        }
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
                print("Error fetching workbooks from url: \(error)")
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
                }

            } catch {
                print("Error decoding JSON: \(error)")
            }
        }

        task.resume()
    }
}

#Preview {
    NavigationStack {
        TableOfContents()
    }
}
