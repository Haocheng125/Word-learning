# PDF表格转Excel工具

将PDF文件中的表格提取并转换为Excel文件，特别适用于包含单词和音标的词汇表。

## 功能特点

- 自动读取PDF中的所有表格
- 支持多行内容合并到同一单元格（如单词+音标）
- 读取PDF全部页面，合并到一个Excel工作表
- 自动设置Excel单元格自动换行
- 批量处理文件夹内的所有PDF文件
- 保留页码和表格序号信息

## 安装依赖

```bash
pip install -r requirements.txt
```

或单独安装：

```bash
pip install pdfplumber pandas openpyxl
```

## 使用方法

### 1. 处理当前文件夹内的所有PDF

```bash
python pdf_to_excel.py
```

### 2. 处理指定文件夹

```bash
python pdf_to_excel.py <文件夹路径>
```

### 3. 处理单个PDF文件

```bash
python pdf_to_excel.py <PDF文件路径>
```

### 4. 处理单个PDF并指定输出文件名

```bash
python pdf_to_excel.py <PDF文件路径> <输出Excel文件路径>
```

## 示例

```bash
# 处理当前文件夹
python pdf_to_excel.py

# 处理指定文件夹
python pdf_to_excel.py C:\Users\Documents\PDFs

# 处理单个文件
python pdf_to_excel.py list1.pdf

# 处理单个文件并指定输出
python pdf_to_excel.py list1.pdf output.xlsx
```

## 输出说明

- 每个PDF文件会生成对应的Excel文件（同名，.xlsx后缀）
- Excel包含一个名为"所有数据"的工作表
- 列包括：原表格列 + 页码 + 表格序号
- 包含换行的单元格会自动设置为自动换行

## 注意事项

1. 运行脚本前请关闭正在打开的Excel文件
2. 确保PDF中的表格结构清晰
3. 单词和音标会自动合并到同一单元格显示
