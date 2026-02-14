import pdfplumber
import re
from typing import List, Dict
import os

PATTERN_VOCAB = re.compile(
    r'([a-zA-Z\s\-\.]+?)\s*\[([^\]]+)\]\s*(.+)',
    re.IGNORECASE
)

PATTERN_HEADER = re.compile(r'Vocabulary List|Word|Meaning|N0\.|中英词表|雅思词汇真经', re.IGNORECASE)

class PDFReader:
    def __init__(self):
        pass
    
    def extract_words_from_pdf(self, pdf_path):
        words = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if not row or all(cell is None or (isinstance(cell, str) and cell.strip() == '') for cell in row):
                            continue
                        cols = [cell.strip() if cell else '' for cell in row]
                        
                        row_text = ' '.join(cols)
                        if PATTERN_HEADER.search(row_text):
                            continue
                        
                        if len(cols) >= 3 and cols[1] and cols[2]:
                            word_phonetic = cols[1]
                            meaning = cols[2].replace('\n', ' ').strip()
                            
                            match = PATTERN_VOCAB.search(word_phonetic)
                            if match:
                                word = match.group(1).strip()
                                phonetic = match.group(2).strip()
                                words.append({'english': word, 'chinese': meaning})
                            else:
                                word = word_phonetic.strip()
                                if word:
                                    words.append({'english': word, 'chinese': meaning})
                        
                        if len(cols) >= 6 and cols[4] and cols[5]:
                            word_phonetic = cols[4]
                            meaning = cols[5].replace('\n', ' ').strip()
                            
                            match = PATTERN_VOCAB.search(word_phonetic)
                            if match:
                                word = match.group(1).strip()
                                phonetic = match.group(2).strip()
                                words.append({'english': word, 'chinese': meaning})
                            else:
                                word = word_phonetic.strip()
                                if word:
                                    words.append({'english': word, 'chinese': meaning})
        
        return words

    def read_pdf_to_words(self, pdf_path: str) -> List[Dict[str, str]]:
        return self.extract_words_from_pdf(pdf_path)

    def read_folder_pdfs(self, folder_path: str) -> Dict[str, List[Dict[str, str]]]:
        result = {}
        
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            return result
        
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder_path, pdf_file)
            list_name = os.path.splitext(pdf_file)[0]
            words = self.read_pdf_to_words(pdf_path)
            
            if words:
                result[list_name] = words
                print(f"Loaded {len(words)} words from {pdf_file}")
        
        return result
