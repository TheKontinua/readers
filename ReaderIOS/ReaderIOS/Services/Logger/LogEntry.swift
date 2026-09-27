//
//  LogEntry.swift
//  ReaderIOS
//
//  Created by Jonas Schiessl on 5/13/25.
//

import Foundation

struct LogEntry: Codable {
    let timestamp: Date
    let level: LogLevel
    let category: String
    let message: String
    let file: String
    let function: String
    let line: Int
}
