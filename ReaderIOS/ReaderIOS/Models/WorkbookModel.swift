//
//  WorkbookModel.swift
//  ReaderIOS
//
//  Created by Ethan Handelman on 2/19/25.
//
import Foundation
import PDFKit

struct Chapter: Identifiable, Codable, Hashable {
    let id: String
    let title: String
    let chapNum: Int
    let startPage: Int
    let covers: [Cover]
    let requires: [String]?

    enum CodingKeys: String, CodingKey {
        case id, title, covers, requires
        case chapNum = "chap_num"
        case startPage = "start_page"
    }

    /// True for back matter such as the answers and index, which cover no topics.
    var isBackMatter: Bool {
        covers.isEmpty
    }
}

extension Chapter {
    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        id = try container.decode(String.self, forKey: .id)
        title = try container.decode(String.self, forKey: .title)
        chapNum = try container.decode(Int.self, forKey: .chapNum)
        startPage = try container.decode(Int.self, forKey: .startPage)
        // Back-matter entries (answers, index) have no covers.
        covers = try container.decodeIfPresent([Cover].self, forKey: .covers) ?? []
        requires = try container.decodeIfPresent([String].self, forKey: .requires)
    }
}

struct Cover: Identifiable, Codable, Hashable {
    let id: String
    let desc: String
    let videos: [Video]?
    let references: [Reference]?

    enum CodingKeys: String, CodingKey {
        case id, desc, videos, references
    }
}

struct Video: Codable, Hashable {
    let link: String
    let title: String

    enum CodingKeys: String, CodingKey {
        case link, title
    }
}

struct Reference: Codable, Hashable {
    let link: String
    let title: String

    enum CodingKeys: String, CodingKey {
        case link, title
    }
}

struct Workbook: Codable, Hashable, Identifiable {
    let id: Int
    let number: Int
    let pdf: String
    let chapters: [Chapter]
    let collection: Int
}

// When we are seeing which workbooks a collection has...
struct WorkbookPreview: Identifiable, Codable {
    let id: Int
    let number: Int
}
