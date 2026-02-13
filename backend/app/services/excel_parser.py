import openpyxl
import logging
import re

logger = logging.getLogger(__name__)

def parse_excel(excel_path):
    words = []
    try:
        workbook = openpyxl.load_workbook(excel_path, read_only=True, data_only=True)
        sheet = workbook.active
        
        logger.info(f'解析Excel: {sheet.title}, {sheet.max_row}行, {sheet.max_column}列')
        
        serial_col = None
        word_col = None
        meaning_col = None
        
        for row_idx in range(1, min(6, sheet.max_row + 1)):
            row = list(sheet.iter_rows(min_row=row_idx, max_row=row_idx, values_only=True))[0]
            for col_idx, cell in enumerate(row, 1):
                if cell is None:
                    continue
                
                cell_str = str(cell).strip()
                
                if not serial_col and cell_str.isdigit():
                    serial_col = col_idx
                    continue
                
                if serial_col and not word_col:
                    if re.search(r'[a-zA-Z]', cell_str):
                        word_col = col_idx
                        continue
                
                if serial_col and word_col and not meaning_col:
                    if any(char >= '\u4e00' and char <= '\u9fff' for char in cell_str):
                        meaning_col = col_idx
                        break
            
            if serial_col and word_col and meaning_col:
                break
        
        if not serial_col:
            serial_col = 1
        if not word_col:
            word_col = 2
        if not meaning_col:
            meaning_col = 3
        
        logger.info(f'序列号列: {serial_col}, 单词列: {word_col}, 释义列: {meaning_col}')
        
        max_serial = 0
        for row_idx in range(1, sheet.max_row + 1):
            try:
                row = list(sheet.iter_rows(min_row=row_idx, max_row=row_idx, values_only=True))[0]
                
                serial_cell = row[serial_col - 1] if serial_col <= len(row) else None
                if serial_cell:
                    serial_str = str(serial_cell).strip()
                    if serial_str.isdigit():
                        current_serial = int(serial_str)
                        max_serial = max(max_serial, current_serial)
        
        logger.info(f'最大序列号: {max_serial}')
        
        for row_idx in range(1, sheet.max_row + 1):
            try:
                row = list(sheet.iter_rows(min_row=row_idx, max_row=row_idx, values_only=True))[0]
                
                serial_cell = row[serial_col - 1] if serial_col <= len(row) else None
                word_cell = row[word_col - 1] if word_col <= len(row) else None
                meaning_cell = row[meaning_col - 1] if meaning_col <= len(row) else None
                
                if not word_cell or not meaning_cell:
                    continue
                
                word_str = str(word_cell).strip()
                meaning_str = str(meaning_cell).strip()
                
                if not word_str or not meaning_str:
                    continue
                
                word = ''
                phonetic = ''
                
                phonetic_match = re.search(r'\[([^\]]+)\]', word_str)
                if phonetic_match:
                    word = word_str.replace(phonetic_match.group(0), '').strip()
                    phonetic = phonetic_match.group(1).strip()
                else:
                    word = word_str
                
                if word:
                    words.append((word, phonetic, meaning_str))
        
        logger.info(f'完成，共{len(words)}个单词')
        
    except FileNotFoundError:
        raise Exception(f'找不到文件: {excel_path}')
    except Exception as e:
        logger.error(f'解析失败: {e}', exc_info=True)
        raise Exception(f'解析失败: {e}')
    
    return words
