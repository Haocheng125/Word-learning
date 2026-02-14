import pdfplumber
import re

PATTERN_VOCAB = re.compile(
    r'([a-zA-Z\s\-\.]+?)\s*\[([^\]]+)\]\s*(.+)',
    re.IGNORECASE
)

PATTERN_HEADER = re.compile(r'Vocabulary List|Word|Meaning|N0\.|中英词表|雅思词汇真经', re.IGNORECASE)

def extract_words_from_pdf(pdf_path):
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
                            words.append((word, phonetic, meaning))
                        else:
                            word = word_phonetic.strip()
                            if word:
                                words.append((word, '', meaning))
                    
                    if len(cols) >= 6 and cols[4] and cols[5]:
                        word_phonetic = cols[4]
                        meaning = cols[5].replace('\n', ' ').strip()
                        
                        match = PATTERN_VOCAB.search(word_phonetic)
                        if match:
                            word = match.group(1).strip()
                            phonetic = match.group(2).strip()
                            words.append((word, phonetic, meaning))
                        else:
                            word = word_phonetic.strip()
                            if word:
                                words.append((word, '', meaning))
    
    return words
