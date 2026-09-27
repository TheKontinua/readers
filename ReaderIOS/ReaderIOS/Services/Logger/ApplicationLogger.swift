import Foundation
import OSLog
import UIKit

final class ApplicationLogger: LoggerProtocol {
    static let shared = ApplicationLogger()

    private let osLogger: OSLog
    private var logBuffer: [LogEntry] = []
    private let bufferSize: Int
    private let queue = DispatchQueue(label: "com.app.logger", attributes: .concurrent)
    private let subsystem: String

    init(subsystem: String = Bundle.main.bundleIdentifier ?? "ReaderIOS",
         category: String = "Application",
         bufferSize: Int = 500)
    {
        self.subsystem = subsystem
        osLogger = OSLog(subsystem: subsystem, category: category)
        self.bufferSize = bufferSize
    }

    func log(_ message: String,
             level: LogLevel = .info,
             category: String = "General",
             file: String = #file,
             function: String = #function,
             line: Int = #line)
    {
        // Log to OSLog
        os_log("%{public}@", log: osLogger, type: level.osLogType, message)

        // Create log entry
        let entry = LogEntry(
            timestamp: Date(),
            level: level,
            category: category,
            message: message,
            file: file,
            function: function,
            line: line
        )

        // Add to buffer
        queue.async(flags: .barrier) {
            self.logBuffer.append(entry)

            // Maintain buffer size
            if self.logBuffer.count > self.bufferSize {
                self.logBuffer.removeFirst(self.logBuffer.count - self.bufferSize)
            }
        }
    }

    func getRecentLogs(count: Int = 50) -> [LogEntry] {
        queue.sync {
            let startIndex = max(0, logBuffer.count - count)
            return Array(logBuffer[startIndex...])
        }
    }

    func getLogsForFeedbackJSON() -> [String: Any] {
        let recentLogs = getRecentLogs(count: 200)

        // Count errors and warnings
        let groupedLogs = Dictionary(grouping: recentLogs) { $0.level }
        let errorCount = groupedLogs[.error]?.count ?? 0
        let warningCount = groupedLogs[.warning]?.count ?? 0
        let criticalCount = groupedLogs[.critical]?.count ?? 0

        // Convert logs to JSON-friendly format
        let isoFormatter = ISO8601DateFormatter()
        let logEntries = recentLogs.map { log in
            [
                "timestamp": isoFormatter.string(from: log.timestamp),
                "level": String(describing: log.level),
                "category": log.category,
                "message": log.message,
                "file": URL(fileURLWithPath: log.file).lastPathComponent,
                "line": log.line,
                "function": log.function
            ] as [String: Any]
        }

        // Get device info
        let device = UIDevice.current
        let appVersion = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "Unknown"
        let buildNumber = Bundle.main.infoDictionary?["CFBundleVersion"] as? String ?? "Unknown"

        return [
            "device": [
                "model": device.model,
                "systemVersion": device.systemVersion,
                "systemName": device.systemName,
                "appVersion": appVersion,
                "buildNumber": buildNumber,
                "deviceName": device.name
            ],
            "summary": [
                "totalLogs": recentLogs.count,
                "errorCount": errorCount,
                "warningCount": warningCount,
                "criticalCount": criticalCount,
                "timeRange": formatTimeRange(logs: recentLogs)
            ],
            "logs": logEntries,
            "metadata": [
                "exportDate": isoFormatter.string(from: Date()),
                "subsystem": subsystem
            ]
        ]
    }

    private func formatTimeRange(logs: [LogEntry]) -> String {
        guard let first = logs.first?.timestamp,
              let last = logs.last?.timestamp
        else {
            return "No logs"
        }

        let formatter = DateFormatter()
        formatter.dateFormat = "MMM dd, HH:mm:ss"

        return "\(formatter.string(from: first)) - \(formatter.string(from: last))"
    }
}
