//
//  ReaderIOSApp.swift
//  ReaderIOS
//r
//  Created by Devin Hadley on 10/22/24.
//

import SwiftUI

@main
struct ReaderIOSApp: App {
    var body: some Scene {
        WindowGroup {
            NavigationStack {
                NavigationPDFSplitView()
            }
        }
    }
}

#Preview {
    NavigationPDFSplitView()
}
