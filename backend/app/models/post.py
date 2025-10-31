from app import db
from datetime import datetime
import re

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    featured_image = db.Column(db.String(500))
    read_time = db.Column(db.Integer, default=5)
    
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    status = db.Column(db.String(20), default='draft')
    is_featured = db.Column(db.Boolean, default=False)
    is_pinned = db.Column(db.Boolean, default=False)
    
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    category = db.relationship('Category', backref='posts')
    comments = db.relationship('Comment', backref='post', lazy=True)
    tags = db.relationship('Tag', secondary='post_tags', backref='posts')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.slug and self.title:
            self.slug = self.generate_slug(self.title)
        if not self.excerpt and self.content:
            self.excerpt = self.content[:150] + '...'
    
    def generate_slug(self, title):
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        return re.sub(r'[-\s]+', '-', slug).strip('-_')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'excerpt': self.excerpt,
            'content': self.content,
            'featured_image': self.featured_image,
            'read_time': self.read_time,
            'status': self.status,
            'is_featured': self.is_featured,
            'author': self.author.to_dict() if self.author else None,
            'category': self.category.to_dict() if self.category else None,
            'tags': [tag.to_dict() for tag in self.tags],
            'comments_count': len(self.comments),
            'created_at': self.created_at.isoformat(),
            'published_at': self.published_at.isoformat() if self.published_at else None
        }
