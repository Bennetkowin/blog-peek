from flask import Blueprint
from flask_restful import Api, Resource
from app.models.category import Category

bp = Blueprint('categories', __name__)
api = Api(bp)

class CategoriesResource(Resource):
    def get(self):
        categories = Category.query.all()
        return {'categories': [category.to_dict() for category in categories]}, 200

api.add_resource(CategoriesResource, '/categories')
