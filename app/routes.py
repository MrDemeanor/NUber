from app import app, db
from flask_restful import Resource, Api, reqparse
from app.models import AdminModel, RiderModel, DriverModel
from flask import jsonify, abort
from sqlalchemy.exc import DatabaseError
from app.serializers import admin_schema_many, rider_schema_many, driver_schema_many
from haversine import haversine

api = Api(app)

'''
    Given a rider id and a radius, display all the available drivers within the specified radius. 
    To calculate distance, we will use the haversine formula, which takes in two sets of longitude
    and latitude and displays the distance in miles.  
'''
class GetDrivers(Resource):

    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('radius', type=int)

        self.args = parser.parse_args()

        super().__init__()

    def get(self):
        rider = RiderModel.query.filter_by(id=self.args['id']).first()

        if rider is None:
            return abort(502, 'The rider was not in the database')

        else:

            drivers = DriverModel.query.all()

            rider_coordinates = (rider.lat, rider.long)

            for driver in drivers:
                driver_coordinates = (driver.lat, driver.long)
                if haversine(rider_coordinates, driver_coordinates, miles=True) > self.args['radius'] \
                        or not driver.available:
                    drivers.remove(drivers)

            return jsonify(available_drivers=driver_schema_many.dump(drivers).data)

class Driver(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)

        self.args = parser.parse_args()

        super().__init__()

    def get(self):
        drivers = DriverModel.query.all()
        print(drivers)
        return jsonify(drivers=driver_schema_many.dump(drivers).data)

class Rider(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)

        self.args = parser.parse_args()

        super().__init__()

    def post(self):
        try:
            new_rider = RiderModel(**self.args)
            db.session.add(new_rider)
            db.session.commit()

        except DatabaseError:
            return abort(500, 'Rider was not added to the database!')

        return jsonify(message='Rider successfully created!')

    def delete(self):
        rider = RiderModel.query.filter_by(id=self.args['id']).first()

        if rider:
            try:
                db.session.delete(rider)
                db.session.commit()
            except DatabaseError:
                return abort(502, 'The item was not deleted')

            return jsonify(message="The rider was successfully deleted")

        else:
            return abort(503, 'The rider did not exist')


    def get(self):
        riders = RiderModel.query.all()
        print(riders)
        return jsonify(riders=rider_schema_many.dump(riders).data)



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
                return abort(501, 'The admin was not updated!')

            return jsonify(message="Admin was successfully updated!")

        else:
            return abort(500, 'The admin did not exist')

    def delete(self):
        admin = AdminModel.query.filter_by(id=self.args['id']).first()

        if admin:
            try:
                db.session.delete(admin)
                db.session.commit()
            except DatabaseError:
                return abort(502, 'The item was not deleted')

            return jsonify(message="The admin was successfully deleted")

        else:
            return abort(503, 'The admin did not exist')

        
api.add_resource(Driver, '/admin/driver')
api.add_resource(Rider, '/admin/rider')
api.add_resource(Admin, '/admin')
api.add_resource(GetDrivers, '/rider/get_drivers')
