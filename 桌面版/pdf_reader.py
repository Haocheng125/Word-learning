import PyPDF2
import re
from typing import List, Dict
import os

class PDFReader:
    def __init__(self):
        pass

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return ""
        return text

    def parse_words(self, text: str) -> List[Dict[str, str]]:
        words = []
        lines = text.split('\n')
        
        # First pass: Identify table structure and column positions
        table_structure = self._identify_table_structure(lines)
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                i += 1
                continue
            
            if self._is_header_line(line):
                i += 1
                continue
            
            # Try to parse using table structure if identified
            if table_structure:
                table_word = self._parse_table_word_with_structure(line, table_structure)
                if table_word:
                    words.append(table_word)
                    i += 1
                    continue
            
            # Fallback to regular parsing
            word_data = self._parse_word_from_line(line, lines, i)
            if word_data:
                words.append(word_data)
                i += 1
            else:
                i += 1
        
        return words

    def _identify_table_structure(self, lines: List[str]) -> Dict[str, int]:
        """
        Identify table structure by looking for header lines with Word and Meaning columns
        Returns a dict with column positions if found
        """
        for line in lines:
            line_lower = line.lower().strip()
            if 'word' in line_lower and 'meaning' in line_lower:
                # Found header line with Word and Meaning columns
                words = line.split()
                structure = {}
                
                for i, word in enumerate(words):
                    if word.lower().strip('.,;:!?') == 'word':
                        structure['word_col'] = i
                    elif word.lower().strip('.,;:!?') == 'meaning':
                        structure['meaning_col'] = i
                
                if 'word_col' in structure:
                    return structure
        
        # If no explicit header found, return a default structure
        return {'word_col': 1, 'meaning_col_start': 2}  # Default: second column is word, third onwards is meaning

    def _is_header_line(self, line: str) -> bool:
        header_keywords = {'vocabulary', 'meaning', 'word', 'n0.', 'no.', '雅思词汇真经', '中英词表', '炭炭背单词'}
        words = line.lower().split()
        for word in words:
            stripped_word = word.strip('.,;:!?')
            if stripped_word in header_keywords:
                return True
        return False

    def _parse_word_from_line(self, line: str, lines: List[str], current_index: int) -> Dict[str, str]:
        # 尝试解析表格格式的单词
        table_word = self._parse_table_word(line)
        if table_word:
            return table_word
        
        # 尝试解析编号格式的单词
        numbered_word = self._parse_numbered_word(lines, current_index)
        if numbered_word:
            return numbered_word
        
        return None

    def _parse_table_word_with_structure(self, line: str, structure: Dict[str, int]) -> Dict[str, str]:
        """
        Parse table word using identified structure
        """
        parts = line.split()
        
        if not parts:
            return None
        
        # Get word from specified column
        if 'word_col' in structure and structure['word_col'] < len(parts):
            # Extract word (may span multiple columns until meaning starts)
            word_start = structure['word_col']
            word_end = structure.get('meaning_col', len(parts))
            
            # Collect all valid English words from word column
            english_parts = []
            for i in range(word_start, word_end):
                if i < len(parts) and self._is_valid_english_word(parts[i]):
                    english_parts.append(parts[i])
            
            if english_parts:
                english = ' '.join(english_parts)
                
                # Extract meaning from meaning column
                meaning_start = structure.get('meaning_col', word_end)
                if meaning_start < len(parts):
                    chinese_part = ' '.join(parts[meaning_start:])
                    chinese = self._clean_chinese(chinese_part)
                    if chinese:
                        return {'english': english, 'chinese': chinese}
        
        return None

    def _parse_table_word(self, line: str) -> Dict[str, str]:
        # 尝试匹配表格格式: 第一列 第二列（英文单词） 第三列（中文释义）
        # 例如: "1 apple 苹果", "2 banana 香蕉 (n.)"
        
        # 尝试按空格分割行
        parts = line.split()
        
        # 情况1: 行以数字开头，第二列为英文单词
        if parts and parts[0].isdigit() and len(parts) >= 2:
            # 找到英文单词部分
            english_index = 1
            while english_index < len(parts):
                if self._is_valid_english_word(parts[english_index]):
                    break
                english_index += 1
            
            if english_index < len(parts):
                # 提取英文单词（可能包含多个部分）
                english_parts = []
                i = english_index
                while i < len(parts):
                    if self._is_valid_english_word(parts[i]):
                        english_parts.append(parts[i])
                    else:
                        break
                    i += 1
                
                if english_parts:
                    english = ' '.join(english_parts)
                    # 提取中文部分
                    chinese_part = ' '.join(parts[i:]) if i < len(parts) else ''
                    if chinese_part:
                        chinese = self._clean_chinese(chinese_part)
                        if chinese:
                            return {'english': english, 'chinese': chinese}
        
        # 情况2: 直接是英文单词 中文释义
        # 例如: "apple 苹果", "banana 香蕉 (n.)"
        english_match = re.match(r'^([a-zA-Z-]+(?:\s+[a-zA-Z-]+)*)', line)
        if english_match:
            english = english_match.group(1).strip()
            if self._is_valid_english_word(english):
                chinese_part = line[len(english_match.group(0)):].strip()
                if chinese_part:
                    chinese = self._clean_chinese(chinese_part)
                    if chinese:
                        return {'english': english, 'chinese': chinese}
        
        # 情况3: 处理可能的列对齐格式（尝试识别Word和Meaning列）
        # 寻找第一个英文单词作为Word列
        english_parts = []
        chinese_start = -1
        
        for i, part in enumerate(parts):
            if self._is_valid_english_word(part):
                english_parts.append(part)
            elif any('\u4e00' <= char <= '\u9fff' for char in part):
                chinese_start = i
                break
        
        if english_parts and chinese_start != -1:
            english = ' '.join(english_parts)
            chinese_part = ' '.join(parts[chinese_start:])
            chinese = self._clean_chinese(chinese_part)
            if chinese:
                return {'english': english, 'chinese': chinese}
        
        return None

    def _parse_numbered_word(self, lines: List[str], current_index: int) -> Dict[str, str]:
        line = lines[current_index].strip()
        
        number_match = re.match(r'^(\d+)$', line)
        if not number_match:
            return None
        
        number = number_match.group(1)
        
        if current_index + 1 >= len(lines):
            return None
        
        english_line = lines[current_index + 1].strip()
        
        if not self._is_valid_english_word(english_line):
            return None
        
        chinese_parts = []
        i = current_index + 2
        
        while i < len(lines):
            next_line = lines[i].strip()
            
            if re.match(r'^\d+$', next_line):
                break
            
            if self._is_header_line(next_line):
                break
            
            if self._is_meaning_line(next_line):
                chinese_parts.append(next_line)
            
            i += 1
        
        chinese = ' '.join(chinese_parts).strip()
        chinese = self._clean_chinese(chinese)
        
        if chinese:
            return {'english': english_line, 'chinese': chinese}
        
        return None

    def _is_meaning_line(self, text: str) -> bool:
        if not text:
            return False
        
        has_chinese = False
        has_pos_tag = False
        has_english = False
        
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                has_chinese = True
            if char.isalpha() and char.islower():
                if char in 'adjnv':
                    has_pos_tag = True
                if char in 'abcdefghijklmnopqrstuvwxyz':
                    has_english = True
        
        return has_chinese and (has_pos_tag or not has_english)

    def _clean_chinese(self, text: str) -> str:
        pos_tags = ['adj', 'adv', 'n', 'v', 'num', 'conj', 'prep', 'pron', 'art', 'interj']
        
        result = []
        i = 0
        while i < len(text):
            char = text[i]
            
            if '\u4e00' <= char <= '\u9fff':
                result.append(char)
            elif char in '，。、；：？！""''（）【】《》·…—':
                result.append(char)
            elif char in ' ,.;:?!':
                result.append(char)
            elif char.isdigit():
                result.append(char)
            elif char.isalpha() and char.islower():
                found_tag = False
                for tag in pos_tags:
                    if i + len(tag) <= len(text) and text[i:i+len(tag)].lower() == tag:
                        result.append(tag)
                        i += len(tag) - 1
                        found_tag = True
                        break
            
            i += 1
        
        cleaned = ''.join(result)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned.strip()
        
        return cleaned

    def _is_valid_english_word(self, text: str) -> bool:
        if not text:
            return False
        
        if len(text) < 2 or len(text) > 50:
            return False
        
        if text.lower() in ['list', 'word', 'meaning', 'no.', 'n0.', 'vocabulary']:
            return False
        
        english_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-')
        return all(c in english_chars for c in text) and any(c.isalpha() for c in text)

    def read_pdf_to_words(self, pdf_path: str) -> List[Dict[str, str]]:
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return []
        
        words = self.parse_words(text)
        return words

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