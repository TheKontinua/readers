//
//  ChapterSearch.swift
//  ReaderIOS
//
//  Created by Ethan Handelman on 12/11/24.
//

import Foundation
import SwiftUI

// ChapterSearchable protocol to make searching more generic
protocol ChapterSearchable {
    var searchableText: String { get }
    var pageNumber: Int { get }
}

extension Chapter: ChapterSearchable {
    var searchableText: String {
        title
    }

    var pageNumber: Int {
        startPage - 1
    }
}

// Search result with highlighting information
struct SearchResult<T: ChapterSearchable> {
    let item: T
    let highlightRanges: [Range<String.Index>]
}

// Search utility struct
enum ChapterSearch {
    /// Filters chapters based on a search text with match highlighting
    /// - Parameters:
    ///   - chapters: The array of chapters to filter
    ///   - searchText: The text to search for
    /// - Returns: Filtered array of search results with highlight information
    static func filter<T: ChapterSearchable>(
        _ chapters: [T]?,
        by searchText: String
    ) -> [SearchResult<T>] {
        guard let chapters = chapters, !searchText.isEmpty else {
            return chapters?.map { SearchResult(item: $0, highlightRanges: []) } ?? []
        }

        return chapters.compactMap { chapter in
            // Find all case-insensitive matches; searchText is non-empty, so each match advances the search.
            let text = chapter.searchableText
            var ranges: [Range<String.Index>] = []
            var searchStart = text.startIndex

            while let range = text[searchStart...].range(of: searchText, options: .caseInsensitive) {
                ranges.append(range)
                searchStart = range.upperBound
            }

            return ranges.isEmpty ? nil : SearchResult(item: chapter, highlightRanges: ranges)
        }
    }
}

// Extension to create a highlighted text view
extension SearchResult where T == Chapter {
    /// Creates a view with the chapter title, highlighting matching text
    func highlightedTitleView() -> some View {
        VStack(alignment: .leading) {
            if !item.isBackMatter {
                Text("Chapter \(item.chapNum)")
                    .font(.caption)
            }

            Text(highlightAttributedString())
        }
    }

    /// Creates an attributed string with matching text bolded
    private func highlightAttributedString() -> AttributedString {
        var attributedString = AttributedString(item.title)

        for range in highlightRanges {
            if let attributedRange = Range(range, in: attributedString) {
                attributedString[attributedRange].font = .body.bold()
            }
        }

        return attributedString
    }
}
