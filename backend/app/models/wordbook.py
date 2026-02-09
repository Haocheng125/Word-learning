from ..extensions import db
from datetime import datetime

class Wordbook(db.Model):
    __tablename__ = 'wordbooks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    pdf_filename = db.Column(db.String(255))
    word_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)  # 上架/下架状态
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    words = db.relationship('Word', backref='wordbook', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'word_count': self.word_count,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
