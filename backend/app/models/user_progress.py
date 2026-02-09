from ..extensions import db
from datetime import datetime

class UserProgress(db.Model):
    __tablename__ = 'user_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    wordbook_id = db.Column(db.Integer, db.ForeignKey('wordbooks.id'), nullable=False)
    current_index = db.Column(db.Integer, default=1)
    last_learn_time = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'wordbook_id', name='unique_user_wordbook'),
        db.Index('idx_user_wordbook', 'user_id', 'wordbook_id'),
    )
    
    wordbook = db.relationship('Wordbook', backref='progress')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'wordbook_id': self.wordbook_id,
            'current_index': self.current_index,
            'last_learn_time': self.last_learn_time.isoformat() if self.last_learn_time else None
        }
