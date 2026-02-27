from flask import Blueprint, render_template, request, jsonify, redirect, url_for, send_from_directory, session, make_response
from app.models.wordbook import Wordbook
from app.models.word import Word
from app.models.user import User
from app.extensions import db, bcrypt
from app.services.PDF_reader import extract_words_from_pdf
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.config import Config
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @jwt_required(locations=['cookies'])
    def decorated_function(*args, **kwargs):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or not user.is_admin:
                return redirect(url_for('admin.login'))
        except:
            return redirect(url_for('admin.login'))
        
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return jsonify({'success': False, 'message': '用户名或密码错误'}), 401
        
        if not user.is_admin:
            return jsonify({'success': False, 'message': '您没有管理员权限'}), 403
        
        access_token = create_access_token(identity=str(user.id))
        
        response = jsonify({'success': True, 'message': '登录成功', 'user': user.to_dict()})
        # 使用标准的set_cookie方法
        response.set_cookie(
            'admin_token',
            access_token,
            httponly=True,
            max_age=3600*24*7,
            samesite='Lax'
        )
        return response
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    response = redirect(url_for('admin.login'))
    response.delete_cookie('admin_token')
    return response

@admin_bp.route('/')
@admin_required
def index():
    total_wordbooks = Wordbook.query.count()
    active_wordbooks = Wordbook.query.filter_by(is_active=True).count()
    total_words = Word.query.count()
    total_users = User.query.count()
    return render_template('admin/index.html', 
                           total_wordbooks=total_wordbooks, 
                           active_wordbooks=active_wordbooks, 
                           total_words=total_words, 
                           total_users=total_users)

@admin_bp.route('/wordbooks')
@admin_required
def wordbooks():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = Wordbook.query.order_by(Wordbook.created_at.desc()).paginate(page=page, per_page=per_page)
    return render_template('admin/wordbooks.html', wordbooks=pagination.items, pagination=pagination)

@admin_bp.route('/wordbooks/<int:wordbook_id>/words')
@admin_required
def wordbook_words(wordbook_id):
    wordbook = Wordbook.query.get_or_404(wordbook_id)
    words = Word.query.filter_by(wordbook_id=wordbook_id).order_by(Word.sort_order).all()
    return render_template('admin/wordbook_words.html', wordbook=wordbook, words=words)

@admin_bp.route('/upload', methods=['GET', 'POST'])
@admin_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': '没有上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'message': '没有选择文件'}), 400
        
        wordbook_name = request.form.get('name', '').strip()
        if not wordbook_name:
            return jsonify({'success': False, 'message': '请输入单词书名称'}), 400
        
        filename = secure_filename(file.filename)
        upload_dir = 'uploads'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        
        try:
            if filename.lower().endswith('.pdf'):
                words = extract_words_from_pdf(file_path)
            else:
                from app.services.excel_parser import parse_excel
                words = parse_excel(file_path)
            
            if not words:
                return jsonify({'success': False, 'message': '未找到有效的单词数据'}), 400
            
            wordbook = Wordbook(name=wordbook_name, word_count=len(words), is_active=True)
            db.session.add(wordbook)
            db.session.flush()
            
            for idx, (word, phonetic, translation) in enumerate(words, 1):
                db_word = Word(
                    wordbook_id=wordbook.id,
                    word=word,
                    phonetic=phonetic,
                    translation=translation,
                    sort_order=idx
                )
                db.session.add(db_word)
            
            db.session.commit()
            
            return jsonify({'success': True, 'message': f'成功导入 {len(words)} 个单词', 'wordbook_id': wordbook.id})
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
        
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)
    
    return render_template('admin/upload.html')

@admin_bp.route('/wordbooks/<int:wordbook_id>/toggle', methods=['POST'])
@admin_required
def toggle_wordbook(wordbook_id):
    wordbook = Wordbook.query.get_or_404(wordbook_id)
    wordbook.is_active = not wordbook.is_active
    db.session.commit()
    return redirect(url_for('admin.wordbooks'))

@admin_bp.route('/wordbooks/<int:wordbook_id>/delete', methods=['POST'])
@admin_required
def delete_wordbook(wordbook_id):
    wordbook = Wordbook.query.get_or_404(wordbook_id)
    Word.query.filter_by(wordbook_id=wordbook_id).delete()
    db.session.delete(wordbook)
    db.session.commit()
    return redirect(url_for('admin.wordbooks'))

@admin_bp.route('/api/wordbooks/<int:wordbook_id>/toggle', methods=['POST'])
def api_toggle_wordbook(wordbook_id):
    wordbook = Wordbook.query.get_or_404(wordbook_id)
    wordbook.is_active = not wordbook.is_active
    db.session.commit()
    action = '上架' if wordbook.is_active else '下架'
    return jsonify({'success': True, 'message': f'词库已{action}'})

@admin_bp.route('/api/wordbooks/<int:wordbook_id>', methods=['DELETE'])
def api_delete_wordbook(wordbook_id):
    wordbook = Wordbook.query.get_or_404(wordbook_id)
    Word.query.filter_by(wordbook_id=wordbook_id).delete()
    db.session.delete(wordbook)
    db.session.commit()
    return jsonify({'success': True, 'message': '词库已删除'})

@admin_bp.route('/api/wordbooks/<int:wordbook_id>/words', methods=['POST'])
def api_add_word(wordbook_id):
    wordbook = Wordbook.query.get_or_404(wordbook_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': '请提供单词信息'}), 400
    
    word_text = data.get('word', '').strip()
    phonetic = data.get('phonetic', '').strip()
    translation = data.get('translation', '').strip()
    
    if not word_text or not translation:
        return jsonify({'success': False, 'message': '单词和中文翻译不能为空'}), 400
    
    max_sort_order = db.session.query(db.func.max(Word.sort_order)).filter_by(wordbook_id=wordbook_id).scalar() or 0
    
    new_word = Word(
        wordbook_id=wordbook_id,
        word=word_text,
        phonetic=phonetic,
        translation=translation,
        sort_order=max_sort_order + 1
    )
    
    db.session.add(new_word)
    wordbook.word_count = wordbook.word_count + 1
    db.session.commit()
    
    return jsonify({'success': True, 'message': '单词添加成功'})

@admin_bp.route('/api/upload-excel', methods=['POST'])
def api_upload_excel():
    if 'excel_file' not in request.files:
        return jsonify({'success': False, 'message': '没有上传文件'}), 400
    
    file = request.files['excel_file']
    if file.filename == '':
        return jsonify({'success': False, 'message': '没有选择文件'}), 400
    
    wordbook_name = request.form.get('name', '').strip()
    if not wordbook_name:
        return jsonify({'success': False, 'message': '请输入单词书名称'}), 400
    
    filename = secure_filename(file.filename)
    upload_dir = 'uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)
    
    try:
        from app.services.excel_parser import parse_excel
        words = parse_excel(file_path)
        
        if not words:
            return jsonify({'success': False, 'message': '未找到有效的单词数据'}), 400
        
        wordbook = Wordbook(name=wordbook_name, word_count=len(words), is_active=False)
        db.session.add(wordbook)
        db.session.flush()
        
        for idx, (word, phonetic, translation) in enumerate(words, 1):
            db_word = Word(
                wordbook_id=wordbook.id,
                word=word,
                phonetic=phonetic,
                translation=translation,
                sort_order=idx
            )
            db.session.add(db_word)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'成功导入 {len(words)} 个单词', 'word_count': len(words), 'wordbook_id': wordbook.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@admin_bp.route('/download/desktop-app')
@admin_required
def download_desktop_app():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.dirname(os.path.dirname(current_dir))
    downloads_dir = os.path.join(app_dir, 'uploads', 'downloads')
    filename = '单词学习助手.exe'
    return send_from_directory(downloads_dir, filename, as_attachment=True)

@admin_bp.route('/api/convert-pdf', methods=['POST'])
@admin_required
def api_convert_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'success': False, 'message': '没有上传文件'}), 400
    
    file = request.files['pdf_file']
    if file.filename == '':
        return jsonify({'success': False, 'message': '没有选择文件'}), 400
    
    wordbook_name = request.form.get('name', '').strip()
    if not wordbook_name:
        return jsonify({'success': False, 'message': '请输入单词书名称'}), 400
    
    filename = secure_filename(file.filename)
    upload_dir = 'uploads'
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)
    
    try:
        words = extract_words_from_pdf(file_path)
        
        if not words:
            return jsonify({'success': False, 'message': '未找到有效的单词数据'}), 400
        
        wordbook = Wordbook(name=wordbook_name, word_count=len(words), is_active=False)
        db.session.add(wordbook)
        db.session.flush()
        
        for idx, (word, phonetic, translation) in enumerate(words, 1):
            db_word = Word(
                wordbook_id=wordbook.id,
                word=word,
                phonetic=phonetic,
                translation=translation,
                sort_order=idx
            )
            db.session.add(db_word)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'成功导入 {len(words)} 个单词', 'word_count': len(words), 'wordbook_id': wordbook.id})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@admin_bp.route('/api/admin/add', methods=['POST'])
@admin_required
def add_admin():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    if not current_user or not current_user.is_super_admin:
        return jsonify({'success': False, 'message': '只有主管理员才能添加副管理员'}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': '请提供管理员信息'}), 400
    
    admin_key = data.get('admin_key', '').strip()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not admin_key or admin_key != Config.ADMIN_KEY:
        return jsonify({'success': False, 'message': '管理员密钥错误'}), 403
    
    if not username or not email or not password:
        return jsonify({'success': False, 'message': '用户名、邮箱和密码不能为空'}), 400
    
    if len(password) < 6:
        return jsonify({'success': False, 'message': '密码至少6个字符'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': '用户名已存在'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': '邮箱已被注册'}), 400
    
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    new_admin = User(
        username=username,
        email=email,
        password_hash=password_hash,
        is_admin=True,
        is_super_admin=False
    )
    
    db.session.add(new_admin)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '副管理员添加成功', 'admin': new_admin.to_dict()})
