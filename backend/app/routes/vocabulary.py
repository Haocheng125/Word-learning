from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.vocabulary import Vocabulary
from ..models.word import Word

vocabulary_bp = Blueprint('vocabulary', __name__)


@vocabulary_bp.route('', methods=['GET'])
@jwt_required()
def get_vocabulary():
    """获取用户的生词本"""
    user_id = int(get_jwt_identity())
    
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    wordbook_id = request.args.get('wordbook_id', type=int)
    
    query = Vocabulary.query.filter_by(user_id=user_id)
    
    if wordbook_id:
        query = query.join(Word).filter(Word.wordbook_id == wordbook_id)
    
    total = query.count()
    vocabulary_items = query.order_by(Vocabulary.added_at.desc()).offset((page - 1) * limit).limit(limit).all()
    
    result = []
    for item in vocabulary_items:
        item_dict = item.to_dict()
        if item.word and item.word.wordbook:
            item_dict['wordbook_name'] = item.word.wordbook.name
        result.append(item_dict)
    
    return jsonify({
        'success': True,
        'vocabulary': result,
        'total': total,
        'page': page,
        'limit': limit
    })


@vocabulary_bp.route('', methods=['POST'])
@jwt_required()
def add_to_vocabulary():
    """添加单词到生词本"""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data or 'word_id' not in data:
        return jsonify({'success': False, 'message': '请提供单词ID'}), 400
    
    word_id = data['word_id']
    
    # 检查单词是否存在
    word = Word.query.get(word_id)
    if not word:
        return jsonify({'success': False, 'message': '单词不存在'}), 404
    
    # 检查是否已在生词本中
    existing = Vocabulary.query.filter_by(user_id=user_id, word_id=word_id).first()
    if existing:
        return jsonify({'success': True, 'message': '该单词已在生词本中'})
    
    vocabulary = Vocabulary(user_id=user_id, word_id=word_id)
    db.session.add(vocabulary)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '已加入生词本', 'id': vocabulary.id}), 201


@vocabulary_bp.route('/<int:vocabulary_id>', methods=['DELETE'])
@jwt_required()
def remove_from_vocabulary(vocabulary_id):
    """从生词本移除"""
    user_id = int(get_jwt_identity())
    
    vocabulary = Vocabulary.query.filter_by(id=vocabulary_id, user_id=user_id).first()
    if not vocabulary:
        return jsonify({'success': False, 'message': '记录不存在'}), 404
    
    db.session.delete(vocabulary)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '已从生词本移除'})


@vocabulary_bp.route('/word/<int:word_id>', methods=['DELETE'])
@jwt_required()
def remove_word_from_vocabulary(word_id):
    """通过单词ID从生词本移除"""
    user_id = int(get_jwt_identity())
    
    vocabulary = Vocabulary.query.filter_by(word_id=word_id, user_id=user_id).first()
    if not vocabulary:
        return jsonify({'success': False, 'message': '该单词不在生词本中'}), 404
    
    db.session.delete(vocabulary)
    db.session.commit()
    
    return jsonify({'success': True, 'message': '已从生词本移除'})
