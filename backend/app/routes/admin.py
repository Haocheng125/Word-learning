from flask import Blueprint, render_template, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os
import re
import traceback
from datetime import datetime
import uuid
import pandas as pd
import pdfplumber
from openpyxl.styles import Alignment
from ..extensions import db
from ..models.user import User
from ..models.wordbook import Wordbook
from ..models.word import Word
from ..services.excel_parser import parse_excel

admin_bp = Blueprint('admin', __name__, template_folder='../templates')


# PDF 转换核心函数
def clean_cell_content(cell):
    if cell is None:
        return ''
    cell_str = str(cell).strip()
    if not cell_str:
        return ''
    lines = [line.strip() for line in cell_str.split('\n') if line.strip()]
    # 保留更多有用的特殊字符
    cleaned_lines = []
    for line in lines:
        # 保留：字母、数字、空格、中文、常用符号、音标、连字符等
        # 允许的字符：
        # \w - 单词字符
        # \s - 空白字符
        # \u4e00-\u9fff - 中文
        # \[\]\(\)'\".-;:,!?，。！？；：""''（）【】——-
        # 音标符号：ˈˌːˌ
        cleaned_line = re.sub(r"[^\w\s\u4e00-\u9fff\[\]\(\)'\".\-;:,!?，。！？；：\"\"''（）【】——ˈˌːˌ]", '', line)
        cleaned_lines.append(cleaned_line)
    return '\n'.join(cleaned_lines)


def merge_two_rows(row1, row2):
    merged = []
    max_len = max(len(row1), len(row2))
    for j in range(max_len):
        cell1 = row1[j] if j < len(row1) else ''
        cell2 = row2[j] if j < len(row2) else ''
        
        # 处理跨行连字符的单词（例如：hel-lo 合并为 hello）
        if cell1 and cell2:
            cell1_str = str(cell1).strip()
            cell2_str = str(cell2).strip()
            
            # 检查是否是跨行连字符单词
            if cell1_str.endswith('-') or cell1_str.endswith('—'):
                # 移除连字符，合并单词
                merged_word = cell1_str[:-1] + cell2_str
                merged.append(merged_word)
            else:
                merged.append(f'{cell1}\n{cell2}')
        elif cell1:
            merged.append(cell1)
        elif cell2:
            merged.append(cell2)
        else:
            merged.append('')
    
    # 清理合并后的数据
    cleaned_merged = []
    for cell in merged:
        if cell:
            # 清理特殊字符，保留更多有用字符
            cleaned_cell = re.sub(r"[^\w\s\u4e00-\u9fff\[\]\(\)'\".\-;:,!?，。！？；：\"\"''（）【】——ˈˌːˌ]", '', str(cell))
            cleaned_merged.append(cleaned_cell)
        else:
            cleaned_merged.append('')
    
    return cleaned_merged


def has_any_content(row):
    """检查行是否有任何非空内容"""
    return any(cell and str(cell).strip() for cell in row)


def clean_dataframe_value(value):
    """安全清理DataFrame中的值"""
    if value is None:
        return ''
    value_str = str(value)
    return re.sub(r"[^\w\s\u4e00-\u9fff\[\]\(\)'\".\-;:,!?，。！？；：\"\"''（）【】——ˈˌːˌ]", '', value_str)


def pdf_table_to_excel(pdf_path, excel_path=None):
    if excel_path is None:
        excel_path = os.path.splitext(pdf_path)[0] + '.xlsx'
    
    all_rows = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                tables = page.extract_tables()
                if not tables:
                    continue
                    
                for table_idx, table in enumerate(tables, 1):
                    if not table or len(table) == 0:
                        continue
                        
                    i = 0
                    while i < len(table):
                        cleaned_row = [clean_cell_content(cell) for cell in table[i]]
                        
                        if i + 1 < len(table):
                            cleaned_next_row = [clean_cell_content(cell) for cell in table[i + 1]]
                            
                            has_content = has_any_content(cleaned_row)
                            next_has_content = has_any_content(cleaned_next_row)
                            
                            if has_content and next_has_content:
                                merged_row = merge_two_rows(cleaned_row, cleaned_next_row)
                                if has_any_content(merged_row):
                                    all_rows.append(merged_row)
                                i += 2
                                continue
                        
                        if has_any_content(cleaned_row):
                            all_rows.append(cleaned_row)
                        i += 1
    except Exception as e:
        print(f"PDF读取失败: {str(e)}")
        raise Exception(f"PDF读取失败: {str(e)}")
    
    if not all_rows:
        print(f"未在 {os.path.basename(pdf_path)} 中找到表格")
        return None
    
    # 转换为标准格式：Word, Meaning
    standard_data = []
    for row in all_rows:
        if len(row) >= 2:
            word_part = str(row[0]) if row[0] else ''
            meaning_part = str(row[1]) if row[1] else ''
            
            if word_part and meaning_part:
                standard_data.append([word_part, meaning_part])
    
    if not standard_data:
        print(f"未找到有效的单词-释义对")
        return None
    
    # 创建 DataFrame，使用标准列名
    df = pd.DataFrame(standard_data, columns=['Word', 'Meaning'])
    
    # 清理DataFrame中的特殊字符
    for col in df.columns:
        df[col] = df[col].apply(clean_dataframe_value)
    
    try:
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='单词数据', index=False)
            worksheet = writer.sheets['单词数据']
            
            for row in worksheet.iter_rows():
                for cell in row:
                    if cell.value and '\n' in str(cell.value):
                        cell.alignment = Alignment(wrap_text=True)
        
        print(f"成功将 {os.path.basename(pdf_path)} 转换为: {os.path.basename(excel_path)}")
        return excel_path
    except Exception as e:
        print(f"Excel写入失败: {str(e)}")
        # 尝试简化数据后再写入
        try:
            # 移除所有特殊字符，只保留基本字符
            for col in df.columns:
                df[col] = df[col].apply(lambda x: re.sub(r'[^\w\s\u4e00-\u9fff]', '', str(x)) if x is not None else x)
            
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='单词数据', index=False)
            
            print(f"使用简化数据成功转换: {os.path.basename(excel_path)}")
            return excel_path
        except Exception as e2:
            print(f"简化数据写入也失败: {str(e2)}")
            raise Exception(f"无法创建Excel文件: {str(e2)}")


@admin_bp.route('/')
def index():
    """管理后台首页"""
    # 统计数据
    total_wordbooks = Wordbook.query.count()
    total_users = User.query.count()
    total_words = Word.query.count()
    active_wordbooks = Wordbook.query.filter_by(is_active=True).count()
    
    return render_template('admin/index.html',
                         total_wordbooks=total_wordbooks,
                         total_users=total_users,
                         total_words=total_words,
                         active_wordbooks=active_wordbooks)


@admin_bp.route('/wordbooks')
def wordbooks():
    """词库管理页面"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = Wordbook.query.order_by(Wordbook.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/wordbooks.html',
                         wordbooks=pagination.items,
                         pagination=pagination)


@admin_bp.route('/upload')
def upload():
    """Excel上传页面"""
    return render_template('admin/upload.html')





@admin_bp.route('/api/convert-pdf', methods=['POST'])
def api_convert_pdf():
    """将PDF转换为Excel，保存到单词库文件夹，然后上传到词库"""
    if 'pdf_file' not in request.files:
        return jsonify({'success': False, 'message': '请上传PDF文件'}), 400
    
    pdf_file = request.files['pdf_file']
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    
    if not pdf_file.filename:
        return jsonify({'success': False, 'message': '请选择文件'}), 400
    
    if not name:
        return jsonify({'success': False, 'message': '请输入单词书名称'}), 400
    
    # 验证文件格式
    if not pdf_file.filename.lower().endswith('.pdf'):
        return jsonify({'success': False, 'message': '只支持PDF文件（.pdf）'}), 400
    
    # 生成唯一文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    original_filename = secure_filename(pdf_file.filename)
    pdf_filename = f"{timestamp}_{unique_id}_{original_filename}"
    excel_filename = f"{timestamp}_{unique_id}_{os.path.splitext(original_filename)[0]}.xlsx"
    
    # 创建单词库文件夹
    wordbooks_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'wordbooks')
    os.makedirs(wordbooks_folder, exist_ok=True)
    
    pdf_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], pdf_filename)
    excel_filepath = os.path.join(wordbooks_folder, excel_filename)
    
    try:
        # 保存PDF文件
        pdf_file.save(pdf_filepath)
        
        # 转换PDF为Excel，保存到单词库文件夹
        result_excel_path = pdf_table_to_excel(pdf_filepath, excel_filepath)
        
        if not result_excel_path:
            if os.path.exists(pdf_filepath):
                os.remove(pdf_filepath)
            return jsonify({
                'success': False, 
                'message': 'PDF中未找到有效的表格数据，请确保PDF包含表格信息'
            }), 400
        
        # 解析Excel
        words_data = parse_excel(excel_filepath)
        
        if not words_data:
            if os.path.exists(pdf_filepath):
                os.remove(pdf_filepath)
            if os.path.exists(excel_filepath):
                os.remove(excel_filepath)
            return jsonify({
                'success': False, 
                'message': 'Excel中未找到有效的单词数据'
            }), 400
        
        # 创建单词书
        wordbook = Wordbook(
            name=name,
            description=description,
            pdf_filename=pdf_filename,
            word_count=len(words_data),
            is_active=False  # 默认下架状态
        )
        db.session.add(wordbook)
        db.session.flush()
        
        # 批量插入单词
        for seq, (word, phonetic, translation) in enumerate(words_data, 1):
            word_obj = Word(
                wordbook_id=wordbook.id,
                word=word,
                phonetic=phonetic,
                translation=translation,
                sequence=seq
            )
            db.session.add(word_obj)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'成功从PDF转换并导入 {len(words_data)} 个单词',
            'wordbook_id': wordbook.id,
            'word_count': len(words_data),
            'excel_path': f'/admin/download/wordbooks/{excel_filename}'
        }), 201
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'PDF转换上传失败: {str(e)}\n{traceback.format_exc()}')
        
        # 清理文件
        if os.path.exists(pdf_filepath):
            os.remove(pdf_filepath)
        if os.path.exists(excel_filepath):
            os.remove(excel_filepath)
        
        return jsonify({
            'success': False, 
            'message': f'处理失败: {str(e)}'
        }), 500

@admin_bp.route('/api/upload-excel', methods=['POST'])
def api_upload_excel():
    """上传 Excel 文件并创建词库"""
    if 'excel_file' not in request.files:
        return jsonify({'success': False, 'message': '请上传Excel文件'}), 400
    
    excel_file = request.files['excel_file']
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    
    if not excel_file.filename:
        return jsonify({'success': False, 'message': '请选择文件'}), 400
    
    if not name:
        return jsonify({'success': False, 'message': '请输入单词书名称'}), 400
    
    # 验证文件格式
    if not excel_file.filename.lower().endswith(('.xlsx', '.xls')):
        return jsonify({'success': False, 'message': '只支持Excel文件（.xlsx 或 .xls）'}), 400
    
    # 生成唯一文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    original_filename = secure_filename(excel_file.filename)
    filename = f"{timestamp}_{original_filename}"
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    try:
        # 保存Excel文件
        excel_file.save(filepath)
        
        # 解析Excel
        words_data = parse_excel(filepath)
        
        if not words_data:
            os.remove(filepath)
            return jsonify({
                'success': False, 
                'message': 'Excel中未找到有效的单词数据'
            }), 400
        
        # 创建单词书
        wordbook = Wordbook(
            name=name,
            description=description,
            pdf_filename=filename,
            word_count=len(words_data),
            is_active=False  # 默认下架状态
        )
        db.session.add(wordbook)
        db.session.flush()
        
        # 批量插入单词
        for seq, (word, phonetic, translation) in enumerate(words_data, 1):
            word_obj = Word(
                wordbook_id=wordbook.id,
                word=word,
                phonetic=phonetic,
                translation=translation,
                sequence=seq
            )
            db.session.add(word_obj)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'成功导入 {len(words_data)} 个单词',
            'wordbook_id': wordbook.id,
            'word_count': len(words_data)
        }), 201
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'上传失败: {str(e)}\n{traceback.format_exc()}')
        
        # 清理文件
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({
            'success': False, 
            'message': f'上传失败: {str(e)}'
        }), 500


@admin_bp.route('/api/wordbooks/<int:wordbook_id>/toggle', methods=['POST'])
def toggle_wordbook_status(wordbook_id):
    """切换词库上架/下架状态"""
    try:
        wordbook = Wordbook.query.get_or_404(wordbook_id)
        wordbook.is_active = not wordbook.is_active
        db.session.commit()
        
        status_text = '上架' if wordbook.is_active else '下架'
        return jsonify({
            'success': True,
            'message': f'词库已{status_text}',
            'is_active': wordbook.is_active
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@admin_bp.route('/api/wordbooks/<int:wordbook_id>', methods=['DELETE'])
def delete_wordbook(wordbook_id):
    """删除词库"""
    try:
        wordbook = Wordbook.query.get_or_404(wordbook_id)
        filename = wordbook.pdf_filename
        
        # 删除数据库记录（级联删除单词）
        db.session.delete(wordbook)
        db.session.commit()
        
        # 删除文件
        if filename:
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(filepath):
                os.remove(filepath)
        
        return jsonify({'success': True, 'message': '词库删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@admin_bp.route('/download/<filename>')
def download_file(filename):
    """下载/查看Excel文件"""
    try:
        return send_from_directory(
            current_app.config['UPLOAD_FOLDER'],
            filename,
            as_attachment=True
        )
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 404


@admin_bp.route('/download/wordbooks/<filename>')
def download_wordbook_file(filename):
    """下载单词库文件夹中的Excel文件"""
    try:
        wordbooks_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'wordbooks')
        return send_from_directory(
            wordbooks_folder,
            filename,
            as_attachment=True
        )
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 404


@admin_bp.route('/download/desktop-app')
def download_desktop_app():
    """下载桌面版应用"""
    try:
        downloads_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'downloads')
        os.makedirs(downloads_folder, exist_ok=True)
        
        exe_filename = '单词学习助手.exe'
        exe_path = os.path.join(downloads_folder, exe_filename)
        
        if os.path.exists(exe_path):
            return send_from_directory(
                downloads_folder,
                exe_filename,
                as_attachment=True
            )
        else:
            return jsonify({
                'success': False,
                'message': '桌面版应用暂未打包，请先运行打包脚本'
            }), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@admin_bp.route('/wordbooks/<int:wordbook_id>/words')
def view_wordbook_words(wordbook_id):
    """查看词库中的单词列表"""
    wordbook = Wordbook.query.get_or_404(wordbook_id)
    
    # 获取该词库的所有单词，按序号排序
    words = Word.query.filter_by(wordbook_id=wordbook_id).order_by(Word.sequence).all()
    
    return render_template('admin/wordbook_words.html',
                         wordbook=wordbook,
                         words=words)
