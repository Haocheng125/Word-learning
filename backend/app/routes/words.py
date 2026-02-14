from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.word import Word
from ..models.wordbook import Wordbook
from ..models.vocabulary import Vocabulary

words_bp = Blueprint('words', __name__)


@words_bp.route('/<int:wordbook_id>/<int:sequence>', methods=['GET'])
@jwt_required()
def get_word(wordbook_id, sequence):
    """获取指定单词书中指定位置的单词"""
    user_id = int(get_jwt_identity())
    
    wordbook = Wordbook.query.get(wordbook_id)
    if not wordbook:
        return jsonify({'success': False, 'message': '单词书不存在'}), 404
    
    word = Word.query.filter_by(
        wordbook_id=wordbook_id,
        sort_order=sequence
    ).first()
    
    if not word:
        return jsonify({'success': False, 'message': '单词不存在'}), 404
    
    # 检查是否在生词本中
    is_in_vocabulary = Vocabulary.query.filter_by(
        user_id=user_id,
        word_id=word.id
    ).first() is not None
    
    result = word.to_dict()
    result['is_in_vocabulary'] = is_in_vocabulary
    result['total_words'] = wordbook.word_count
    
    return jsonify({'success': True, 'word': result})


@words_bp.route('/batch/<int:wordbook_id>', methods=['GET'])
@jwt_required()
def get_words_batch(wordbook_id):
    """批量获取单词（用于预加载）"""
    from flask import request
    
    start = request.args.get('start', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    wordbook = Wordbook.query.get(wordbook_id)
    if not wordbook:
        return jsonify({'success': False, 'message': '单词书不存在'}), 404
    
    words = Word.query.filter(
        Word.wordbook_id == wordbook_id,
        Word.sort_order >= start,
        Word.sort_order < start + limit
    ).order_by(Word.sort_order).all()
    
    return jsonify({
        'success': True,
        'words': [w.to_dict() for w in words],
        'total': wordbook.word_count
    })
