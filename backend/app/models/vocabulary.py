from ..extensions import db
from datetime import datetime

class Vocabulary(db.Model):
    __tablename__ = 'vocabulary'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'word_id', name='unique_user_word'),
    )
    
    word = db.relationship('Word', backref='in_vocabulary')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'word_id': self.word_id,
            'added_at': self.added_at.isoformat() if self.added_at else None,
            'word': self.word.to_dict() if self.word else None
        }
