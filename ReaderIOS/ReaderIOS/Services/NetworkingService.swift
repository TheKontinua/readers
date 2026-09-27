//
//  NetworkingService.swift
//  ReaderIOS
//
//  Created by Ethan Handelman on 2/19/25.
//

import Foundation
import PDFKit.PDFDocument

enum NetworkError: Error {
    case invalidURL
    case noData
}

final class NetworkingService: ObservableObject {
    static let shared = NetworkingService()

    // Published property so views can observe loading state.
    @Published var isContentLoading: Bool = false
    // Internal counter to handle multiple concurrent requests.
    private var loadingCount = 0

    private init() {}

    // Configure a URLSession with no caching.
    private let session: URLSession = {
        let config = URLSessionConfiguration.default
        config.urlCache = nil
        config.requestCachePolicy = .reloadIgnoringLocalCacheData
        return URLSession(configuration: config)
    }()

    // MARK: - Loading State Helpers

    private func startLoading() {
        loadingCount += 1
        DispatchQueue.main.async {
            self.isContentLoading = true
        }
    }

    private func stopLoading() {
        loadingCount -= 1
        if loadingCount <= 0 {
            loadingCount = 0
            DispatchQueue.main.async {
                self.isContentLoading = false
            }
        }
    }

    // MARK: - Network Methods

    func fetchLatestCollection(completion: @escaping (Result<Collection, Error>) -> Void) {
        fetchJSON(
            Collection.self,
            path: ApplicationConstants.APIEndpoints.collections + "latest?localization=en_US",
            completion: completion
        )
    }

    func fetchWorkbooks(collection: Collection, completion: @escaping (Result<[WorkbookPreview], Error>) -> Void) {
        Logger.info("Fetching workbooks for collection: \(collection.id)", category: "Network")
        fetchJSON(
            DetailedCollection.self,
            path: ApplicationConstants.APIEndpoints.collections + "\(collection.id)/"
        ) { result in
            completion(result.map(\.workbooks))
        }
    }

    func fetchWorkbook(id: Int, completion: @escaping (Result<Workbook, Error>) -> Void) {
        Logger.info("Fetching workbook with ID: \(id)", category: "Network")
        fetchJSON(
            Workbook.self,
            path: ApplicationConstants.APIEndpoints.workbooks + "\(id)/",
            completion: completion
        )
    }

    /// Fetches an API endpoint and decodes its JSON body. The completion is always called on the main queue.
    private func fetchJSON<T: Decodable>(
        _ type: T.Type,
        path: String,
        completion: @escaping (Result<T, Error>) -> Void
    ) {
        guard let url = URL(string: ApplicationConstants.API.baseURLString + path) else {
            Logger.error("Invalid URL for path: \(path)", category: "Network")
            completion(.failure(NetworkError.invalidURL))
            return
        }
        Logger.Network.request(url.absoluteString)
        startLoading()

        let task = session.dataTask(with: url) { data, response, error in
            // Ensure stopLoading is called when this closure exits.
            defer { self.stopLoading() }

            let result: Result<T, Error>
            if let error = error {
                Logger.Network.error(error, url: url.absoluteString)
                result = .failure(error)
            } else if let httpResponse = response as? HTTPURLResponse, let data = data {
                Logger.Network.response(url.absoluteString, statusCode: httpResponse.statusCode)
                do {
                    result = try .success(JSONDecoder().decode(T.self, from: data))
                    Logger.info("Successfully decoded \(T.self)", category: "Network")
                } catch {
                    Logger.error("Failed to decode \(T.self): \(error)", category: "Network")
                    result = .failure(error)
                }
            } else {
                Logger.error("Invalid response or no data received", category: "Network")
                result = .failure(NetworkError.noData)
            }
            DispatchQueue.main.async { completion(result) }
        }
        task.resume()
    }

    func fetchPDF(workbook: Workbook, completion: @escaping (Result<PDFDocument, Error>) -> Void) {
        guard let url = URL(string: workbook.pdf) else {
            Logger.error("Invalid PDF URL for workbook: \(workbook.id) - \(workbook.pdf)", category: "Network")
            completion(.failure(NetworkError.invalidURL))
            return
        }
        Logger.info("Downloading PDF for workbook: \(workbook.id)", category: "Network")
        Logger.Network.request(url.absoluteString)
        startLoading()

        let task = session.dataTask(with: url) { data, response, error in
            defer { self.stopLoading() }

            if let error = error {
                Logger.Network.error(error, url: url.absoluteString)
                DispatchQueue.main.async { completion(.failure(error)) }
                return
            }
            if let httpResponse = response as? HTTPURLResponse {
                Logger.Network.response(url.absoluteString, statusCode: httpResponse.statusCode)
            }
            guard let data = data, let document = PDFDocument(data: data) else {
                Logger.error("Failed to create PDF document from data", category: "Network")
                DispatchQueue.main.async { completion(.failure(NetworkError.noData)) }
                return
            }
            Logger.info("Successfully loaded PDF for workbook: \(workbook.id)", category: "Network")
            DispatchQueue.main.async { completion(.success(document)) }
        }
        task.resume()
    }
}
