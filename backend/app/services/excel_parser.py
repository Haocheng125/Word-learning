import openpyxl
import logging
import re

logger = logging.getLogger(__name__)

def parse_excel(excel_path):
    """
    解析Excel文件，提取单词信息
    支持多种格式：
    1. 简单两列格式：第一列单词，第二列释义
    2. 复杂多列格式：包含单词+音标在同一单元格
    
    返回: [(word, phonetic, translation), ...]
    """
    words = []
    
    try:
        workbook = openpyxl.load_workbook(excel_path, read_only=True, data_only=True)
        sheet = workbook.active
        
        logger.info(f'开始解析Excel，工作表: {sheet.title}，共 {sheet.max_row} 行，{sheet.max_column} 列')
        
        # 检查第一行是否为表头
        first_row = list(sheet.iter_rows(min_row=1, max_row=1, values_only=True))[0]
        has_header = False
        start_row = 1
        
        # 检测表头
        if first_row and len(first_row) >= 2:
            first_row_str = [str(cell or '').lower().strip() for cell in first_row]
            if any('word' in s or 'meaning' in s or '单词' in s or '释义' in s for s in first_row_str):
                has_header = True
                start_row = 2
                logger.info('检测到表头，从第二行开始解析')
        
        # 查找 Word 和 Meaning 列的索引
        word_cols = []
        meaning_cols = []
        
        if has_header:
            for idx, cell in enumerate(first_row, 1):
                cell_str = str(cell or '').lower().strip()
                if 'word' in cell_str or '单词' in cell_str:
                    word_cols.append(idx)
                elif 'meaning' in cell_str or '释义' in cell_str:
                    meaning_cols.append(idx)
        
        # 如果没有找到列，假设第一列是单词，第二列是释义
        if not word_cols:
            word_cols = [1, 2] if sheet.max_column >= 2 else [1]
            logger.info(f'未找到Word列标识，使用默认列: {word_cols}')
        
        if not meaning_cols and sheet.max_column >= 2:
            meaning_cols = [2, 3] if sheet.max_column >= 3 else [2]
            logger.info(f'未找到Meaning列标识，使用默认列: {meaning_cols}')
        
        logger.info(f'Word 列: {word_cols}, Meaning 列: {meaning_cols}')
        
        # 遍历所有行
        for row_idx, row in enumerate(sheet.iter_rows(min_row=start_row, values_only=True), start_row):
            try:
                if not row:
                    continue
                
                # 处理每一对 Word-Meaning 列
                for word_col_idx in word_cols:
                    if word_col_idx > len(row):
                        continue
                    
                    word_cell = row[word_col_idx - 1]
                    if not word_cell:
                        continue
                    
                    # 查找对应的 meaning 列
                    meaning_cell = None
                    for meaning_col_idx in meaning_cols:
                        if meaning_col_idx > len(row):
                            continue
                        if meaning_col_idx > word_col_idx:
                            meaning_cell = row[meaning_col_idx - 1]
                            break
                    
                    if not meaning_cell:
                        continue
                    
                    word_str = str(word_cell).strip()
                    meaning_str = str(meaning_cell).strip()
                    
                    if not word_str or not meaning_str:
                        continue
                    
                    # 解析单词和音标（处理换行符分隔的情况）
                    word = ''
                    phonetic = ''
                    
                    # 如果单词包含换行符，第一行是单词，第二行可能是音标
                    if '\n' in word_str:
                        parts = word_str.split('\n', 1)
                        word = parts[0].strip()
                        if len(parts) > 1:
                            phonetic_part = parts[1].strip()
                            # 提取音标（去除方括号）
                            phonetic_match = re.search(r'\[([^\]]+)\]', phonetic_part)
                            if phonetic_match:
                                phonetic = phonetic_match.group(1)
                    else:
                        # 尝试从单个字符串中提取单词和音标
                        phonetic_match = re.search(r'([a-zA-Z\s\-]+)\s*\[([^\]]+)\]', word_str)
                        if phonetic_match:
                            word = phonetic_match.group(1).strip()
                            phonetic = phonetic_match.group(2).strip()
                        else:
                            word = word_str
                    
                    # 验证单词是否为英文（允许空格、连字符和常见的特殊字符）
                    # 放宽限制，允许重音符和其他特殊字符（如 El Niño）
                    if not re.match(r'^[a-zA-ZÀ-ſ\s\-]+$', word):
                        logger.warning(f'第 {row_idx} 行：单词包含非法字符，已跳过: {word}')
                        continue
                    
                    # 验证长度
                    if len(word) > 100 or len(meaning_str) > 1000:
                        logger.warning(f'第 {row_idx} 行：数据长度超限，已跳过')
                        continue
                    
                    # 验证翻译包含中文或英文
                    translation = meaning_str
                    
                    # 添加到结果
                    words.append((word, phonetic, translation))
                    logger.debug(f'解析成功 #{len(words)}: {word} [{phonetic}] -> {translation[:50]}...')
            
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
