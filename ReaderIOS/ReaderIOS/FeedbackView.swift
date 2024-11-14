//
//  FeedbackView.swift
//  ReaderIOS
//
//  Created by Jonas Schiessl on 11/13/24.
//

import SwiftUI

struct FeedbackView: View {
    @Environment(\.dismiss) var dismiss
    @State private var email: String = ""
    @State private var feedback: String = ""
    @State private var isSubmitting = false
    @State private var isValid = false
    
    var body: some View {
        NavigationView {
            Form {
                Section {
                    TextField("Email", text: $email)
                        .keyboardType(.emailAddress)
                    TextEditor(text: $feedback)
                        .frame(height: 200)
                }
                
                Button(action: submitFeedback) {
                    HStack {
                        Text(isSubmitting ? "Submitting..." : "Submit Feedback")
                        if isSubmitting {
                            ProgressView()
                        }
                    }
                }
                .disabled(isSubmitting || email.isEmpty || feedback.isEmpty)
            }
            .navigationTitle("Feedback")
            .navigationBarItems(trailing: Button("Cancel") { dismiss() })
        }
    }
    
    private func submitFeedback() {
        isSubmitting = true
        DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
            isSubmitting = false
            dismiss()
        }
        
    }
}
