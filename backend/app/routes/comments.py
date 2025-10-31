from flask import request, Blueprint
from flask_restful import Api, Resource
from app import db
from app.models.comment import Comment
from app.models.post import Post

bp = Blueprint('comments', __name__)
api = Api(bp)

class PostCommentsResource(Resource):
    def get(self, post_id):
        comments = Comment.query.filter_by(
            post_id=post_id, 
            is_approved=True,
            parent_id=None
        ).all()
        return {'comments': [comment.to_dict() for comment in comments]}, 200
    
    def post(self, post_id):
        data = request.get_json()
        
        comment = Comment(
            content=data['content'],
            author_name=data['author_name'],
            author_email=data['author_email'],
            post_id=post_id,
            parent_id=data.get('parent_id')
        )
        
        db.session.add(comment)
        db.session.commit()
        
        return {'message': 'Comment submitted', 'comment': comment.to_dict()}, 201

api.add_resource(PostCommentsResource, '/posts/<int:post_id>/comments')
