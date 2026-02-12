import openpyxl
import logging
import re

logger = logging.getLogger(__name__)

def parse_excel(excel_path):
    """
    解析Excel文件，提取单词信息
    直接读取 Word 和 Meaning 列
    
    返回: [(word, phonetic, translation), ...]
    """
    words = []
    
    try:
        workbook = openpyxl.load_workbook(excel_path, read_only=True, data_only=True)
        sheet = workbook.active
        
        logger.info(f'开始解析Excel，工作表: {sheet.title}，共 {sheet.max_row} 行，{sheet.max_column} 列')
        
        word_col_idx = 1
        meaning_col_idx = 2
        start_row = 1
        
        if sheet.max_row > 0:
            first_row = list(sheet.iter_rows(min_row=1, max_row=1, values_only=True))[0]
            if first_row and len(first_row) >= 2:
                first_row_str = [str(cell or '').lower().strip() for cell in first_row]
                
                for idx, cell in enumerate(first_row_str):
                    if 'word' in cell or '单词' in cell:
                        word_col_idx = idx + 1
                        start_row = 2
                        break
                
                for idx, cell in enumerate(first_row_str):
                    if 'meaning' in cell or '释义' in cell or '中文' in cell:
                        meaning_col_idx = idx + 1
                        break
        
        logger.info(f'Word 列: {word_col_idx}, Meaning 列: {meaning_col_idx}, 从第 {start_row} 行开始')
        
        for row_idx in range(start_row, sheet.max_row + 1):
            try:
                row = list(sheet.iter_rows(min_row=row_idx, max_row=row_idx, values_only=True))[0]
                
                if not row or len(row) <= max(word_col_idx, meaning_col_idx):
                    continue
                
                word_cell = row[word_col_idx - 1] if (word_col_idx - 1) < len(row) else None
                meaning_cell = row[meaning_col_idx - 1] if (meaning_col_idx - 1) < len(row) else None
                
                if not word_cell or not meaning_cell:
                    continue
                
                word_str = str(word_cell).strip()
                meaning_str = str(meaning_cell).strip()
                
                if not word_str or not meaning_str:
                    continue
                
                word = ''
                phonetic = ''
                
                if '\n' in word_str:
                    parts = word_str.split('\n', 1)
                    word = parts[0].strip()
                    if len(parts) > 1:
                        phonetic_part = parts[1].strip()
                        phonetic_match = re.search(r'\[([^\]]+)\]', phonetic_part)
                        if phonetic_match:
                            phonetic = phonetic_match.group(1)
                else:
                    phonetic_match = re.search(r'([a-zA-Z\s\-]+)\s*\[([^\]]+)\]', word_str)
                    if phonetic_match:
                        word = phonetic_match.group(1).strip()
                        phonetic = phonetic_match.group(2).strip()
                    else:
                        word = word_str
                
                if word:
                    words.append((word, phonetic, meaning_str))
                    logger.debug(f'解析成功 #{len(words)}: {word} [{phonetic}] -> {meaning_str[:50]}...')
            
            except Exception as e:
                logger.warning(f'解析第 {row_idx} 行失败: {str(e)}')
                continue
        
        workbook.close()
        logger.info(f'Excel解析完成，共提取 {len(words)} 个单词')
        
    except FileNotFoundError:
        raise Exception(f'找不到Excel文件: {excel_path}')
    except Exception as e:
        logger.error(f'Excel解析失败: {str(e)}', exc_info=True)
        raise Exception(f'Excel解析失败: {str(e)}')
    
    return words
