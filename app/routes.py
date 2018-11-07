from app import app, db
from flask_restful import Resource, Api, reqparse
from app.models import AdminModel
from flask import jsonify, abort
from sqlalchemy.exc import DatabaseError
from app.serializers import admin_schema_many

api = Api(app)

'''
class Driver(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)

        self.args = parser.parse_args()

        super().__init__()

    def get(self):
        return {'hello': 'world'}

class Rider(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)

        self.args = parser.parse_args()

        super().__init__()

    def get(self):
        return {'hello': 'world'}
'''
class Admin(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)

        self.args = parser.parse_args()

        super().__init__()

    def get(self):
        admins = AdminModel.query.all()
        print(admins)
        return jsonify(admins=admin_schema_many.dump(admins).data)

    def post(self):
        try:
            #AdminModel.create(**self.args)
            new_admin = AdminModel(**self.args)
            db.session.add(new_admin)
            db.session.commit()

        except DatabaseError:
            return abort(500, 'Admin was not added to the database!')

        return jsonify(message='Admin successfully created!')

    def put(self):

        admin = AdminModel.query.filter_by(id=self.args['id']).first()

        if admin:
            try:
                admin.id = self.args['id']
                admin.name = self.args['name']
                db.session.commit()
            except DatabaseError:
                return abort(501, 'The item was not updated!')

            return jsonify(message="Item was successfully updated!")

        else:
            return abort(500, 'The admin did not exist')

#api.add_resource(Driver, '/driver')
#api.add_resource(Rider, '/rider')
api.add_resource(Admin, '/admin')