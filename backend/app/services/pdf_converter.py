import os
import pandas as pd
import pdfplumber
from openpyxl.styles import Alignment

def clean_cell_content(cell):
    """清理单元格内容，移除Excel不支持的特殊字符"""
    if cell is None:
        return ''
    cell_str = str(cell).strip()
    if not cell_str:
        return ''
    
    # 清理音标中的特殊字符，转换为Excel兼容格式
    # 移除重音符号、长音符号等特殊字符
    import unicodedata
    
    # 标准化Unicode字符
    cell_str = unicodedata.normalize('NFKD', cell_str)
    
    # 移除组合字符（如重音符号）
    cleaned_chars = []
    for char in cell_str:
        # 保留基本ASCII字符和常见中文字符
        if ord(char) < 128 or (0x4e00 <= ord(char) <= 0x9fff):
            cleaned_chars.append(char)
        # 对于音标符号，转换为简单的表示
        elif char in ['ˌ', 'ː', 'ˈ', '̩', '̯', '̈', '̃', '̄', '̆', '̊']:
            # 这些是常见的音标修饰符，可以移除或替换
            continue
        else:
            # 其他特殊字符也移除
            continue
    
    cell_str = ''.join(cleaned_chars)
    
    # 处理换行
    lines = [line.strip() for line in cell_str.split('\n') if line.strip()]
    return '\n'.join(lines)

def merge_two_rows(row1, row2):
    """合并两行数据"""
    merged = []
    max_len = max(len(row1), len(row2))
    for j in range(max_len):
        cell1 = row1[j] if j < len(row1) else ''
        cell2 = row2[j] if j < len(row2) else ''
        if cell1 and cell2:
            merged.append(f'{cell1}\n{cell2}')
        elif cell1:
            merged.append(cell1)
        elif cell2:
            merged.append(cell2)
        else:
            merged.append('')
    return merged

def pdf_table_to_excel(pdf_path, excel_path=None):
    """将PDF表格转换为Excel
    
    Args:
        pdf_path: PDF文件路径
        excel_path: 输出的Excel文件路径，如果为None则自动生成
        
    Returns:
        excel_path: 生成的Excel文件路径，失败返回None
    """
    if excel_path is None:
        excel_path = os.path.splitext(pdf_path)[0] + '.xlsx'
    
    all_data = []
    header = None
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            if not tables:
                continue
                
            for table_idx, table in enumerate(tables, 1):
                if not table or len(table) == 0:
                    continue
                    
                if header is None:
                    header = [clean_cell_content(cell) for cell in table[0]]
                
                i = 1
                while i < len(table):
                    cleaned_row = [clean_cell_content(cell) for cell in table[i]]
                    
                    if i + 1 < len(table):
                        cleaned_next_row = [clean_cell_content(cell) for cell in table[i + 1]]
                        
                        has_content = any(cleaned_row)
                        next_has_content = any(cleaned_next_row)
                        
                        if has_content and next_has_content:
                            merged_row = merge_two_rows(cleaned_row, cleaned_next_row)
                            if any(merged_row):
                                row_with_info = merged_row + [page_num, table_idx]
                                all_data.append(row_with_info)
                            i += 2
                            continue
                    
                    if any(cleaned_row):
                        row_with_info = cleaned_row + [page_num, table_idx]
                        all_data.append(row_with_info)
                    i += 1
    
    if not all_data or not header:
        print(f"未在 {os.path.basename(pdf_path)} 中找到表格")
        return None
    
    header_with_info = header + ['页码', '表格序号']
    df = pd.DataFrame(all_data, columns=header_with_info)
    
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='所有数据', index=False)
        worksheet = writer.sheets['所有数据']
        
        for row in worksheet.iter_rows():
            for cell in row:
                if cell.value and '\n' in str(cell.value):
                    cell.alignment = Alignment(wrap_text=True)
    
    print(f"成功将 {os.path.basename(pdf_path)} 转换为: {os.path.basename(excel_path)}")
    return excel_path

def batch_convert_folder(folder_path):
    """批量转换文件夹中的PDF文件"""
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"在文件夹 {folder_path} 中未找到PDF文件")
        return []
    
    print(f"找到 {len(pdf_files)} 个PDF文件")
    print("-" * 50)
    
    results = []
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        try:
            excel_path = pdf_table_to_excel(pdf_path)
            if excel_path:
                results.append({
                    'pdf_file': pdf_file,
                    'excel_file': os.path.basename(excel_path),
                    'status': 'success'
                })
            else:
                results.append({
                    'pdf_file': pdf_file,
                    'status': 'failed',
                    'error': '未找到表格数据'
                })
        except Exception as e:
            results.append({
                'pdf_file': pdf_file,
                'status': 'failed',
                'error': str(e)
            })
            print(f"处理 {pdf_file} 时出错: {str(e)}")
    
    print("-" * 50)
    success_count = len([r for r in results if r['status'] == 'success'])
    print(f"转换完成！成功处理 {success_count}/{len(pdf_files)} 个文件")
    
    return results