from flask import request, Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.post import Post
from app.models.user import User
from app.models.category import Category
from sqlalchemy import or_

bp = Blueprint('posts', __name__)
api = Api(bp)

class PostsResource(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        category = request.args.get('category')
        search = request.args.get('search')
        
        query = Post.query.filter_by(status='published')
        
        if category:
            query = query.join(Category).filter(Category.slug == category)
        
        if search:
            query = query.filter(
                or_(
                    Post.title.ilike(f'%{search}%'),
                    Post.content.ilike(f'%{search}%')
                )
            )
        
        posts = query.order_by(Post.published_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return {
            'posts': [post.to_dict() for post in posts.items],
            'total': posts.total,
            'pages': posts.pages,
            'current_page': page
        }, 200

class PostResource(Resource):
    def get(self, slug):
        post = Post.query.filter_by(slug=slug).first_or_404()
        return {'post': post.to_dict()}, 200

class AdminPostsResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user.role != 'admin':
            return {'message': 'Admin access required'}, 403
        
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return {'posts': [post.to_dict() for post in posts]}, 200
    
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user.role != 'admin':
            return {'message': 'Admin access required'}, 403
        
        data = request.get_json()
        
        post = Post(
            title=data['title'],
            content=data['content'],
            excerpt=data.get('excerpt'),
            author_id=user_id,
            category_id=data.get('category_id'),
            status=data.get('status', 'draft')
        )
        
        if data.get('status') == 'published':
            from datetime import datetime
            post.published_at = datetime.utcnow()
        
        db.session.add(post)
        db.session.commit()
        
        return {'message': 'Post created', 'post': post.to_dict()}, 201

api.add_resource(PostsResource, '/posts')
api.add_resource(PostResource, '/posts/<string:slug>')
api.add_resource(AdminPostsResource, '/admin/posts')
