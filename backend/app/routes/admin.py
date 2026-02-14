import pdfplumber
import re
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.models.wordbook import Wordbook
from app.models.word import Word
from app.extensions import db
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def clean_cell_content(cell):
    if cell is None:
        return ''
    if isinstance(cell, (list, tuple)):
        return ' '.join(str(c) for c in cell if c is not None)
    return str(cell).strip()

def extract_words_from_pdf(pdf_path):
    words_data = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                tables = page.extract_tables()
                if not tables:
                    continue
                    
                for table_idx, table in enumerate(tables, 1):
                    if not table or len(table) == 0:
                        continue
                        
                    serial_col = None
                    word_col = None
                    meaning_col = None
                    
                    for row_idx in range(min(5, len(table))):
                        row = table[row_idx]
                        for col_idx, cell in enumerate(row):
                            if cell is None:
                                continue
                            
                            cell_str = clean_cell_content(cell)
                            
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
                        serial_col = 0
                    if not word_col:
                        word_col = 1
                    if not meaning_col:
                        meaning_col = 2
                    
                    for row in table:
                        if not row:
                            continue
                        
                        serial_cell = row[serial_col] if serial_col < len(row) else None
                        word_cell = row[word_col] if word_col < len(row) else None
                        meaning_cell = row[meaning_col] if meaning_col < len(row) else None
                        
                        if not word_cell or not meaning_cell:
                            continue
                        
                        word_str = clean_cell_content(word_cell)
                        meaning_str = clean_cell_content(meaning_cell)
                        
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
                            words_data.append((word, phonetic, meaning_str))
    
    except Exception as e:
        print(f"PDF读取失败: {str(e)}")
        raise Exception(f"PDF读取失败: {str(e)}")
    
    return words_data

@admin_bp.route('/')
def index():
    total_wordbooks = Wordbook.query.count()
    active_wordbooks = Wordbook.query.filter_by(is_active=True).count()
    total_words = Word.query.count()
    total_users = 0
    return render_template('admin/index.html', 
                           total_wordbooks=total_wordbooks, 
                           active_wordbooks=active_wordbooks, 
                           total_words=total_words, 
                           total_users=total_users)

@admin_bp.route('/wordbooks')
def wordbooks():
    from flask_paginate import Pagination, get_page_args
    
    page, per_page, offset = get_page_args(page_parameter='page',
                                          per_page_parameter='per_page',
                                          count=Wordbook.query.count())
    
    wordbooks = Wordbook.query.offset(offset).limit(per_page).all()
    pagination = Pagination(page=page, per_page=per_page, total=Wordbook.query.count(),
                           css_framework='bootstrap4')
    
    return render_template('admin/wordbooks.html', 
                           wordbooks=wordbooks, 
                           pagination=pagination)

@admin_bp.route('/wordbooks/<int:id>/words')
def wordbook_words(id):
    wordbook = Wordbook.query.get(id)
    if not wordbook:
        return redirect(url_for('admin.wordbooks'))
    
    words = Word.query.filter_by(wordbook_id=id).all()
    return render_template('admin/wordbook_words.html', 
                           wordbook=wordbook, 
                           words=words)

@admin_bp.route('/upload')
def upload():
    return render_template('admin/upload.html')

@admin_bp.route('/api/upload-excel', methods=['POST'])
def api_upload_excel():
    if 'excel_file' not in request.files:
        return jsonify({'success': False, 'message': '请上传Excel文件'}), 400
    
    excel_file = request.files['excel_file']
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    
    if not excel_file.filename:
        return jsonify({'success': False, 'message': '请选择Excel文件'}), 400
    
    if not name:
        return jsonify({'success': False, 'message': '请填写词库名称'}), 400
    
    if Wordbook.query.filter_by(name=name).first():
        return jsonify({'success': False, 'message': '词库名称已存在'}), 400
    
    filename = secure_filename(excel_file.filename)
    filepath = os.path.join('uploads', filename)
    os.makedirs('uploads', exist_ok=True)
    excel_file.save(filepath)
    
    from app.services.excel_parser import parse_excel
    
    try:
        words_data = parse_excel(filepath)
        
        if not words_data:
            os.remove(filepath)
            return jsonify({'success': False, 'message': 'Excel中未找到有效的单词数据'}), 400
        
        wordbook = Wordbook(
            name=name,
            description=description,
            excel_filename=filename,
            word_count=len(words_data),
            is_active=False
        )
        db.session.add(wordbook)
        db.session.commit()
        
        for idx, (word, phonetic, translation) in enumerate(words_data, 1):
            word_obj = Word(
                wordbook_id=wordbook.id,
                word=word,
                phonetic=phonetic,
                translation=translation,
                word_order=idx
            )
            db.session.add(word_obj)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'成功导入{len(words_data)}个单词', 'word_count': len(words_data)}), 200
        
    except Exception as e:
        os.remove(filepath)
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'}), 500

@admin_bp.route('/api/convert-pdf', methods=['POST'])
def api_convert_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'success': False, 'message': '请上传PDF文件'}), 400
    
    pdf_file = request.files['pdf_file']
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    
    if not pdf_file.filename:
        return jsonify({'success': False, 'message': '请选择PDF文件'}), 400
    
    if not name:
        return jsonify({'success': False, 'message': '请填写词库名称'}), 400
    
    if Wordbook.query.filter_by(name=name).first():
        return jsonify({'success': False, 'message': '词库名称已存在'}), 400
    
    filename = secure_filename(pdf_file.filename)
    filepath = os.path.join('uploads', filename)
    os.makedirs('uploads', exist_ok=True)
    pdf_file.save(filepath)
    
    try:
        words_data = extract_words_from_pdf(filepath)
        
        if not words_data:
            os.remove(filepath)
            return jsonify({'success': False, 'message': 'PDF中未找到有效的单词数据'}), 400
        
        wordbook = Wordbook(
            name=name,
            description=description,
            pdf_filename=filename,
            word_count=len(words_data),
            is_active=False
        )
        db.session.add(wordbook)
        db.session.commit()
        
        for idx, (word, phonetic, translation) in enumerate(words_data, 1):
            word_obj = Word(
                wordbook_id=wordbook.id,
                word=word,
                phonetic=phonetic,
                translation=translation,
                word_order=idx
            )
            db.session.add(word_obj)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'成功导入{len(words_data)}个单词', 'word_count': len(words_data)}), 200
        
    except Exception as e:
        os.remove(filepath)
        return jsonify({'success': False, 'message': f'处理失败: {str(e)}'}), 500

@admin_bp.route('/api/wordbooks/<int:id>/toggle', methods=['POST'])
def toggle_wordbook_status(id):
    wordbook = Wordbook.query.get(id)
    if not wordbook:
        return jsonify({'success': False, 'message': '词库不存在'}), 404
    
    wordbook.is_active = not wordbook.is_active
    db.session.commit()
    
    status = '上架' if wordbook.is_active else '下架'
    return jsonify({'success': True, 'message': f'词库已{status}'}), 200

@admin_bp.route('/api/wordbooks/<int:id>', methods=['DELETE'])
def delete_wordbook(id):
    wordbook = Wordbook.query.get(id)
    if not wordbook:
        return jsonify({'success': False, 'message': '词库不存在'}), 404
    
    Word.query.filter_by(wordbook_id=id).delete()
    db.session.delete(wordbook)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '词库已删除'}), 200
