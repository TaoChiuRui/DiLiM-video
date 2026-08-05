// OCR bang macOS Vision — doc duong dan anh tu stdin, in "path<TAB>chu doc duoc".
// Bien dich mot lan:  swiftc -O -o ocr ocr.swift
// Dung:               ls *.jpg | ./ocr
import Foundation
import Vision
import AppKit

while let path = readLine(strippingNewline: true) {
    guard !path.isEmpty else { continue }
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("\(path)\t"); continue
    }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    req.minimumTextHeight = 0.02          // bo chu li ti (watermark goc)
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    let txt = (req.results ?? [])
        .compactMap { $0.topCandidates(1).first }
        .filter { $0.confidence > 0.45 }
        .map { $0.string }
    print("\(path)\t\(txt.joined(separator: " | "))")
    fflush(stdout)
}
