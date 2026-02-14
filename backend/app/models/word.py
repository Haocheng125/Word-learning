from ..extensions import db
from datetime import datetime

class Word(db.Model):
    __tablename__ = 'words'
    
    id = db.Column(db.Integer, primary_key=True)
    wordbook_id = db.Column(db.Integer, db.ForeignKey('wordbooks.id'), nullable=False)
    word = db.Column(db.String(100), nullable=False)
    phonetic = db.Column(db.String(100))
    translation = db.Column(db.Text, nullable=False)
    word_order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('wordbook_id', 'word_order', name='unique_wordbook_sequence'),
        db.Index('idx_wordbook_sequence', 'wordbook_id', 'word_order'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'wordbook_id': self.wordbook_id,
            'word': self.word,
            'phonetic': self.phonetic,
            'translation': self.translation,
            'sequence': self.word_order
        }
