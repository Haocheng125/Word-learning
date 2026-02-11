from pdf_reader import PDFReader

# Test PDF extraction
reader = PDFReader()
pdf_path = "c:\\Users\\18896\\Desktop\\背单词\\list1.pdf"

# Extract text from PDF
text = reader.extract_text_from_pdf(pdf_path)
print("Extracted text:")
print(text[:5000])  # Print first 5000 characters to see the structure

# Try to parse words
words = reader.read_pdf_to_words(pdf_path)
print("\nParsed words:")
for i, word in enumerate(words[:20]):  # Print first 20 words
    print(f"{i+1}. English: {word['english']}, Chinese: {word['chinese']}")
