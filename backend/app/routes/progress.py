from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from ..extensions import db
from ..models.user_progress import UserProgress
from ..models.wordbook import Wordbook

progress_bp = Blueprint('progress', __name__)


@progress_bp.route('/<int:wordbook_id>', methods=['GET'])
@jwt_required()
def get_progress(wordbook_id):
    """获取用户在指定单词书的学习进度"""
    user_id = int(get_jwt_identity())
    
    wordbook = Wordbook.query.get(wordbook_id)
    if not wordbook:
        return jsonify({'success': False, 'message': '单词书不存在'}), 404
    
    progress = UserProgress.query.filter_by(
        user_id=user_id,
        wordbook_id=wordbook_id
    ).first()
    
    if not progress:
        # 如果没有进度记录，返回默认值
        return jsonify({
            'success': True,
            'progress': {
                'wordbook_id': wordbook_id,
                'current_index': 1,
                'total_words': wordbook.word_count,
                'progress_percentage': 0,
                'last_learn_time': None
            }
        })
    
    percentage = round((progress.current_index - 1) / wordbook.word_count * 100, 1) if wordbook.word_count > 0 else 0
    
    return jsonify({
        'success': True,
        'progress': {
            'wordbook_id': wordbook_id,
            'current_index': progress.current_index,
            'total_words': wordbook.word_count,
            'progress_percentage': percentage,
            'last_learn_time': progress.last_learn_time.isoformat() if progress.last_learn_time else None
        }
    })


@progress_bp.route('/<int:wordbook_id>', methods=['POST'])
@jwt_required()
def update_progress(wordbook_id):
    """更新学习进度"""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or 'current_index' not in data:
        return jsonify({'success': False, 'message': '请提供当前位置'}), 400
    
    current_index = data['current_index']
    
    wordbook = Wordbook.query.get(wordbook_id)
    if not wordbook:
        return jsonify({'success': False, 'message': '单词书不存在'}), 404
    
    # 验证索引范围
    if current_index < 1 or current_index > wordbook.word_count:
        return jsonify({'success': False, 'message': '索引超出范围'}), 400
    
    progress = UserProgress.query.filter_by(
        user_id=user_id,
        wordbook_id=wordbook_id
    ).first()
    
    if progress:
        progress.current_index = current_index
        progress.last_learn_time = datetime.utcnow()
    else:
        progress = UserProgress(
            user_id=user_id,
            wordbook_id=wordbook_id,
            current_index=current_index,
            last_learn_time=datetime.utcnow()
        )
        db.session.add(progress)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'current_index': progress.current_index
    })


@progress_bp.route('/<int:wordbook_id>/reset', methods=['POST'])
@jwt_required()
def reset_progress(wordbook_id):
    """重置学习进度"""
    user_id = int(get_jwt_identity())
    
    progress = UserProgress.query.filter_by(
        user_id=user_id,
        wordbook_id=wordbook_id
    ).first()
    
    if progress:
        progress.current_index = 1
        progress.last_learn_time = datetime.utcnow()
        db.session.commit()
    
    return jsonify({'success': True, 'current_index': 1})
