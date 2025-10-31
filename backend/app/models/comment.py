from app import db
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_name = db.Column(db.String(100), nullable=False)
    author_email = db.Column(db.String(120), nullable=False)
    author_website = db.Column(db.String(200))
    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    
    is_approved = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]))
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'author_name': self.author_name,
            'author_email': self.author_email,
            'author_website': self.author_website,
            'post_id': self.post_id,
            'is_approved': self.is_approved,
            'replies': [reply.to_dict() for reply in self.replies],
            'created_at': self.created_at.isoformat()
        }
