//
//  MarkupMenuView.swift
//  ReaderIOS
//
//  Created by Ethan Handelman on 2/19/25.
//
import SwiftUI

struct MarkupMenu: View {
    // MARK: - Bindings

    @Binding var selectedScribbleTool: AnnotationMode
    @Binding var exitNotSelected: Bool
    @Binding var showClearAlert: Bool
    @Binding var selectedPenColor: Color
    @Binding var selectedHighlighterColor: Color
    @Binding var textBoxes: [String: [TextBoxData]]

    // MARK: - Observed Objects

    @ObservedObject var annotationManager: AnnotationStorageManager
    @ObservedObject var textManager: TextManager

    // MARK: - Input Data

    let pagePaths: [String: [(path: Path, color: Color)]]
    let highlightPaths: [String: [(path: Path, color: Color)]]

    // MARK: - Body

    var body: some View {
        Menu {
            // Pen Color Submenu
            Menu {
                colorButton(color: .black, label: "Black", tool: .pen, selection: $selectedPenColor)
                colorButton(color: .green, label: "Green", tool: .pen, selection: $selectedPenColor)
                colorButton(color: .red, label: "Red", tool: .pen, selection: $selectedPenColor)
                colorButton(color: .blue, label: "Blue", tool: .pen, selection: $selectedPenColor)
            } label: {
                HStack {
                    Text("Pen")
                    if selectedScribbleTool == .pen {
                        Circle()
                            .fill(selectedPenColor)
                            .frame(width: 10, height: 10)
                    }
                }
            }

            // Highlighter Color Submenu
            Menu {
                colorButton(color: .yellow, label: "Yellow", tool: .highlight, selection: $selectedHighlighterColor)
                colorButton(color: .pink, label: "Pink", tool: .highlight, selection: $selectedHighlighterColor)
                colorButton(color: .blue, label: "Blue", tool: .highlight, selection: $selectedHighlighterColor)
                colorButton(color: .green, label: "Green", tool: .highlight, selection: $selectedHighlighterColor)
            } label: {
                HStack {
                    Text("Highlight")
                    if selectedScribbleTool == .highlight {
                        Circle()
                            .fill(selectedHighlighterColor)
                            .frame(width: 10, height: 10)
                    }
                }
            }

            Button("Erase") {
                selectedScribbleTool = .erase
                exitNotSelected = true
            }
            Button("Text") {
                selectedScribbleTool = .text
                exitNotSelected = true
            }
            Button("Clear Screen") {
                showClearAlert = true
            }
            Button("Exit Markup") {
                selectedScribbleTool = .none
                exitNotSelected = false
                annotationManager.saveAnnotations(pagePaths: pagePaths, highlightPaths: highlightPaths)
                textManager.saveTextBoxes(textBoxes: textBoxes)
            }
        } label: {
            Text(selectedScribbleTool == .none ? "Markup" : "Markup: \(String(describing: selectedScribbleTool))")
                .padding(5)
                .foregroundColor(exitNotSelected ? .pink : .blue)
                .cornerRadius(8)
        }
    }

    // MARK: - Private Helpers

    /// A menu item that selects `tool` and stores `color` in `selection`, showing a checkmark when selected.
    private func colorButton(
        color: Color,
        label: String,
        tool: AnnotationMode,
        selection: Binding<Color>
    ) -> some View {
        Button {
            selection.wrappedValue = color
            selectedScribbleTool = tool
            exitNotSelected = true
        } label: {
            HStack {
                Text(label)
                if selection.wrappedValue == color {
                    Image(systemName: "checkmark")
                }
            }
        }
    }
}
