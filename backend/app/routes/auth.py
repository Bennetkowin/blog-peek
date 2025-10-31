from flask import request, Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User

bp = Blueprint('auth', __name__)
api = Api(bp)

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already registered'}, 400
        
        user = User(
            username=data['username'],
            email=data['email'],
            role=data.get('role', 'reader')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity=user.id)
        
        return {
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token
        }, 201

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return {'message': 'Invalid credentials'}, 401
        
        access_token = create_access_token(identity=user.id)
        
        return {
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token
        }, 200

class MeResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return {'user': user.to_dict()}, 200

api.add_resource(RegisterResource, '/register')
api.add_resource(LoginResource, '/login')
api.add_resource(MeResource, '/me')
