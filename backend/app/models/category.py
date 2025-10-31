from app import db
import re

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    color = db.Column(db.String(7), default='#3b82f6')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.slug and self.name:
            self.slug = self.generate_slug(self.name)
    
    def generate_slug(self, name):
        slug = re.sub(r'[^\w\s-]', '', name.lower())
        return re.sub(r'[-\s]+', '-', slug).strip('-_')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'color': self.color
        }
