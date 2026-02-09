from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.wordbook import Wordbook
from ..models.user_progress import UserProgress

wordbooks_bp = Blueprint('wordbooks', __name__)


@wordbooks_bp.route('', methods=['GET'])
@jwt_required()
def get_wordbooks():
    """获取所有已上架的单词书列表"""
    try:
        user_id = int(get_jwt_identity())
        
        # 只获取已上架的词库
        wordbooks = Wordbook.query.filter_by(is_active=True).all()
        
        result = []
        for wb in wordbooks:
            wb_dict = wb.to_dict()
            
            # 获取用户学习进度
            progress = UserProgress.query.filter_by(
                user_id=user_id, 
                wordbook_id=wb.id
            ).first()
            
            if progress:
                wb_dict['user_progress'] = {
                    'current_index': progress.current_index,
                    'last_learn_time': progress.last_learn_time.isoformat() if progress.last_learn_time else None
                }
            else:
                wb_dict['user_progress'] = None
            
            result.append(wb_dict)
        
        return jsonify({'success': True, 'wordbooks': result})
    
    except Exception as e:
        current_app.logger.error(f'获取词库列表失败: {str(e)}')
        return jsonify({'success': False, 'message': '服务器错误'}), 500


@wordbooks_bp.route('/<int:wordbook_id>', methods=['GET'])
@jwt_required()
def get_wordbook(wordbook_id):
    """获取单词书详情"""
    wordbook = Wordbook.query.get(wordbook_id)
    if not wordbook:
        return jsonify({'success': False, 'message': '单词书不存在'}), 404
    
    return jsonify({'success': True, 'wordbook': wordbook.to_dict()})
