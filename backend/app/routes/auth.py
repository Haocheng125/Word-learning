from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from ..extensions import db, bcrypt
from ..models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': '请提供注册信息'}), 400
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not username or not email or not password:
        return jsonify({'success': False, 'message': '用户名、邮箱和密码不能为空'}), 400
    
    if len(password) < 6:
        return jsonify({'success': False, 'message': '密码至少6个字符'}), 400
    
    # 检查用户名和邮箱是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({'success': False, 'message': '用户名已存在'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': '邮箱已被注册'}), 400
    
    # 创建新用户
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password_hash=password_hash)
    
    # 第一个用户设为管理员
    if User.query.count() == 0:
        user.is_admin = True
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '注册成功'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': '请提供登录信息'}), 400
    
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'success': False, 'message': '邮箱和密码不能为空'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({'success': False, 'message': '邮箱或密码错误'}), 401
    
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return jsonify({
        'success': True,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    })


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify({'access_token': access_token})


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'success': False, 'message': '用户不存在'}), 404
    
    return jsonify({'success': True, 'user': user.to_dict()})
