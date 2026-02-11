import os
import sys
import pandas as pd
import pdfplumber
from openpyxl.styles import Alignment

def clean_cell_content(cell):
    if cell is None:
        return ''
    cell_str = str(cell).strip()
    if not cell_str:
        return ''
    lines = [line.strip() for line in cell_str.split('\n') if line.strip()]
    return '\n'.join(lines)

def merge_two_rows(row1, row2):
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
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"在文件夹 {folder_path} 中未找到PDF文件")
        return
    
    print(f"找到 {len(pdf_files)} 个PDF文件")
    print("-" * 50)
    
    success_count = 0
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        try:
            result = pdf_table_to_excel(pdf_path)
            if result:
                success_count += 1
        except Exception as e:
            print(f"处理 {pdf_file} 时出错: {str(e)}")
    
    print("-" * 50)
    print(f"转换完成！成功处理 {success_count}/{len(pdf_files)} 个文件")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        folder_path = os.getcwd()
        print(f"未指定路径，使用当前文件夹: {folder_path}")
        batch_convert_folder(folder_path)
    else:
        path = sys.argv[1]
        
        if os.path.isdir(path):
            batch_convert_folder(path)
        elif os.path.isfile(path) and path.lower().endswith('.pdf'):
            excel_file = sys.argv[2] if len(sys.argv) > 2 else None
            pdf_table_to_excel(path, excel_file)
        else:
            print(f"错误: {path} 不是有效的PDF文件或文件夹")
            sys.exit(1)
