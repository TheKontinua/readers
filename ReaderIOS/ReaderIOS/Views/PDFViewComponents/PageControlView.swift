//
//  PageControlView.swift
//  ReaderIOS
//
//  Created by Ethan Handelman on 2/4/25.
//
import SwiftUI

struct PageControlView: View {
    // Binding to the external currentPage variable.
    @Binding var currentPage: Int
    // Total number of pages available.
    let totalPages: Int
    /// The current workbook's chapters, in page order.
    let chapters: [Chapter]
    /// Bookmarked page indexes for the current workbook, in page order.
    let bookmarkedPages: [Int]

    @State private var showPagePicker = false

    var body: some View {
        HStack(spacing: 8) {
            Button(action: decrementPage) {
                Image(systemName: "chevron.left")
                    .font(.title)
                    .frame(width: 10, height: 24)
            }
            .disabled(currentPage == 0)

            // Tapping the page number opens a custom picker instead of the system keyboard.
            Button {
                showPagePicker = true
            } label: {
                Text("\(currentPage + 1)")
                    .monospacedDigit()
                    .frame(minWidth: 50)
                    .padding(.vertical, 4)
                    .background(Color(UIColor.secondarySystemBackground), in: RoundedRectangle(cornerRadius: 6))
            }
            .accessibilityLabel("Page \(currentPage + 1) of \(totalPages)")
            .accessibilityHint("Choose a page to go to")
            .disabled(totalPages == 0)
            .popover(isPresented: $showPagePicker) {
                PagePickerView(
                    currentPage: $currentPage,
                    totalPages: totalPages,
                    chapters: chapters,
                    bookmarkedPages: bookmarkedPages,
                    isPresented: $showPagePicker
                )
                .presentationCompactAdaptation(.popover)
            }

            Text("/ \(totalPages)")

            Button(action: incrementPage) {
                Image(systemName: "chevron.right")
                    .font(.title)
                    .frame(width: 24, height: 24)
            }
            .disabled(currentPage >= totalPages - 1)
        }
    }

    private func incrementPage() {
        if currentPage < totalPages - 1 {
            currentPage += 1
        }
    }

    private func decrementPage() {
        if currentPage > 0 {
            currentPage -= 1
        }
    }
}

/// Lets the user pick a page with a slider or a keypad, then jump to it with Go,
/// or jump straight to one of the workbook's chapters or bookmarks.
struct PagePickerView: View {
    @Binding var currentPage: Int
    let totalPages: Int
    /// The workbook's chapters, in page order.
    let chapters: [Chapter]
    /// Bookmarked page indexes (0-based), in page order.
    let bookmarkedPages: [Int]
    @Binding var isPresented: Bool

    /// The page number being entered (1-based), as typed digits.
    @State private var entry = ""
    /// The first digit typed replaces the shown number rather than appending to it.
    @State private var replaceOnNextDigit = true

    private var maxDigits: Int {
        String(totalPages).count
    }

    private var enteredPage: Int? {
        guard let page = Int(entry), (1 ... totalPages).contains(page) else { return nil }
        return page
    }

    var body: some View {
        // Grow to fit every bookmark, but scroll if there are more than fit on screen.
        ViewThatFits(in: .vertical) {
            pickerContent
            ScrollView { pickerContent }
        }
        .frame(width: 280)
        .onAppear {
            entry = "\(currentPage + 1)"
            replaceOnNextDigit = true
        }
    }

    private var pickerContent: some View {
        VStack(spacing: 16) {
            HStack(alignment: .firstTextBaseline, spacing: 6) {
                Text(entry.isEmpty ? " " : entry)
                    .font(.system(size: 40, weight: .semibold))
                    .monospacedDigit()
                    .foregroundStyle(enteredPage == nil ? .red : .primary)
                Text("/ \(totalPages)")
                    .font(.title3)
                    .foregroundStyle(.secondary)
            }
            .accessibilityElement(children: .combine)

            if totalPages > 1 {
                // No `step:` here, since it draws a tick mark per page; `sliderValue` rounds to whole pages instead.
                Slider(value: sliderValue, in: 1 ... Double(totalPages)) {
                    Text("Page")
                } minimumValueLabel: {
                    Text("1")
                } maximumValueLabel: {
                    Text("\(totalPages)")
                }
            }

            Grid(horizontalSpacing: 10, verticalSpacing: 10) {
                GridRow { digitKey(1); digitKey(2); digitKey(3) }
                GridRow { digitKey(4); digitKey(5); digitKey(6) }
                GridRow { digitKey(7); digitKey(8); digitKey(9) }
                GridRow {
                    keypadButton(action: deleteDigit) {
                        Image(systemName: "delete.left")
                    }
                    .accessibilityLabel("Delete")
                    .disabled(entry.isEmpty)

                    digitKey(0)

                    keypadButton(prominent: true, action: go) {
                        Text("Go").bold()
                    }
                    .disabled(enteredPage == nil)
                }
            }

            if !chapters.isEmpty {
                chaptersSection
            }

            bookmarksSection
        }
        .padding()
    }

    private var chaptersSection: some View {
        VStack(alignment: .leading, spacing: 4) {
            Divider()
                .padding(.bottom, 8)

            Text("Chapters")
                .font(.headline)

            ForEach(chapters) { chapter in
                // Like bookmarks, a chapter is checked only when the current page is exactly where it starts.
                jumpRow(to: chapter.pageNumber, isCurrent: chapter.pageNumber == currentPage) {
                    Text(chapter.title)
                        .multilineTextAlignment(.leading)
                    Spacer()
                    Text("\(chapter.pageNumber + 1)")
                        .monospacedDigit()
                        .foregroundStyle(.secondary)
                }
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }

    private var bookmarksSection: some View {
        VStack(alignment: .leading, spacing: 4) {
            Divider()
                .padding(.bottom, 8)

            Text("Bookmarks")
                .font(.headline)

            if bookmarkedPages.isEmpty {
                Text("No bookmarks in this workbook")
                    .font(.callout)
                    .foregroundStyle(.secondary)
                    .padding(.vertical, 6)
            } else {
                ForEach(bookmarkedPages, id: \.self) { page in
                    jumpRow(to: page, isCurrent: page == currentPage) {
                        Image(systemName: "bookmark.fill")
                            .foregroundStyle(.yellow)
                        Text("Page \(page + 1)")
                            .monospacedDigit()
                        Spacer()
                    }
                }
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }

    /// A row that jumps to `page` and dismisses the picker; `isCurrent` adds a checkmark.
    private func jumpRow(
        to page: Int,
        isCurrent: Bool,
        @ViewBuilder content: () -> some View
    ) -> some View {
        Button {
            currentPage = page
            isPresented = false
        } label: {
            HStack {
                content()
                Image(systemName: "checkmark")
                    .foregroundStyle(.secondary)
                    .opacity(isCurrent ? 1 : 0)
                    .accessibilityHidden(!isCurrent)
                    .accessibilityLabel("Current")
            }
            .padding(.vertical, 8)
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
    }

    /// Drives the slider from the entered page, falling back to the current page while the entry is invalid.
    /// Moving the slider turns the document immediately so the user can see the page they're choosing.
    private var sliderValue: Binding<Double> {
        Binding(
            get: { Double(enteredPage ?? currentPage + 1) },
            set: { newValue in
                let page = Int(newValue.rounded())
                entry = "\(page)"
                replaceOnNextDigit = true
                if currentPage != page - 1 {
                    currentPage = page - 1
                }
            }
        )
    }

    private func digitKey(_ digit: Int) -> some View {
        keypadButton(action: { appendDigit(digit) }, label: { Text("\(digit)") })
    }

    @ViewBuilder
    private func keypadButton(
        prominent: Bool = false,
        action: @escaping () -> Void,
        @ViewBuilder label: () -> some View
    ) -> some View {
        let button = Button(action: action) {
            label()
                .font(.title2)
                .frame(maxWidth: .infinity, minHeight: 44)
        }
        if prominent {
            button.buttonStyle(.borderedProminent)
        } else {
            button.buttonStyle(.bordered)
        }
    }

    private func appendDigit(_ digit: Int) {
        if replaceOnNextDigit {
            entry = ""
            replaceOnNextDigit = false
        }
        // Ignore leading zeros and digits beyond the length of the last page number.
        guard entry.count < maxDigits, !(entry.isEmpty && digit == 0) else { return }
        entry += "\(digit)"
    }

    private func deleteDigit() {
        replaceOnNextDigit = false
        if !entry.isEmpty {
            entry.removeLast()
        }
    }

    private func go() {
        guard let page = enteredPage else { return }
        currentPage = page - 1
        isPresented = false
    }
}

#Preview {
    PagePickerView(
        currentPage: .constant(4),
        totalPages: 41,
        chapters: [
            Chapter(id: "a", title: "Introduction", chapNum: 1, startPage: 1, covers: [], requires: nil),
            Chapter(id: "b", title: "Adding and Subtracting Fractions", chapNum: 2, startPage: 3, covers: [], requires: nil),
            Chapter(id: "c", title: "Ratios", chapNum: 3, startPage: 13, covers: [], requires: nil),
            Chapter(id: "answers", title: "Answers", chapNum: 4, startPage: 37, covers: [], requires: nil),
            Chapter(id: "index", title: "Index", chapNum: 5, startPage: 40, covers: [], requires: nil),
        ],
        bookmarkedPages: [0, 4, 11, 27],
        isPresented: .constant(true)
    )
}
