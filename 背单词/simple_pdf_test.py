import PyPDF2

# Simple PDF text extraction
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            print(f"Number of pages: {len(pdf_reader.pages)}")
            for i, page in enumerate(pdf_reader.pages):
                print(f"\n=== Page {i+1} ===")
                page_text = page.extract_text()
                print(page_text[:2000])  # Print first 2000 characters per page
                text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""
    return text

# Test with list1.pdf
pdf_path = "list1.pdf"
extract_text_from_pdf(pdf_path)
