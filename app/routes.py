from app import app, db
from flask_restful import Resource, Api, reqparse
from app.models import AdminModel, RiderModel, DriverModel
from flask import jsonify, abort
from sqlalchemy.exc import DatabaseError
from app.serializers import admin_schema_many, rider_schema_many, driver_schema_many
from app.haversine import Haversine

api = Api(app)

class SelectDriver(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('driver_id', type=int)
        parser.add_argument('rider_id', type=int)

        self.args = parser.parse_args()

        super().__init__()
    
    def put(self):

        # Query both the driver and the rider
        driver = DriverModel.query.filter_by(id=self.args['driver_id']).first()
        rider = RiderModel.query.filter_by(id=self.args['rider_id']).first()

        # Check if the driver is not in the database
        if driver is None:
            abort(502, 'Driver was not found')
        
        # Check to see if the rider is not in the database
        elif rider is None:
            abort(502, 'Rider was not found')
        
        # Check driver availability
        elif not driver.available:
            abort(502, 'Driver is not available')
        
        else:
            try:
                rider.selected_driver = self.args['driver_id']
                driver.selected_rider = self.args['rider_id']
                driver.available = False
                db.session.commit()
            
            except:
                abort(502, 'Driver was not assigned to rider')
        
        return jsonify(message='Driver was successfully added to rider')

    def get(self):
        # Query both the driver and the rider
        driver = DriverModel.query.filter_by(id=self.args['driver_id']).first()
        rider = RiderModel.query.filter_by(id=self.args['rider_id']).first()

        # Check if the driver is not in the database
        if driver is None:
            abort(502, 'Driver was not found')

        # Check to see if the rider is not in the database
        elif rider is None:
            abort(502, 'Rider was not found')

        # Check driver availability
        elif not driver.available:
            abort(502, 'Driver is not available')

        else:
            try:
                '''
                I need to figure out if we want to output an ETA here as well
                '''

            except:
                abort(502, 'Destination and ETA could not be determined')

        '''Confused on if i need to jsonify output or print output'''
        return jsonify(message='This is the location and time till driver arrives')

class SetRiderDest(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('destination', type=str)

        self.args = parser.parse_args()

        super().__init__()

    def put(self):
        rider = RiderModel.query.filter_by(id=self.args['id']).first()

        if rider is None:
            abort(502, 'Rider was not found')
        
        else:
            try:
                rider.destination = self.args['destination']
                db.session.commit()
            
            except:
                abort(503, 'Rider destination was not updated')
        
        return jsonify(message='Rider destination successfully updated')

'''
    Given a driver id and a new set of coordinates, update the driver with the set of new coordinates
'''
class UpdateDriverPosition(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('lat', type=float)
        parser.add_argument('long', type=float)

        self.args = parser.parse_args()

        super().__init__()

    def put(self):
        driver = DriverModel.query.filter_by(id=self.args['id']).first()

        if driver is None:
            abort(502, 'Driver was not found')

        else:
            try:
                driver.lat = self.args['lat']
                driver.long = self.args['long']
                db.session.commit()

            except:
                abort(502, 'Driver coordinates were not updated')

        return jsonify(message='Driver coordinates successfully updated')

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

            for driver in drivers:
                if Haversine.calculate_distance(rider.lat, rider.long, driver.lat, driver.long) > self.args['radius'] \
                        or not driver.available:
                    drivers.remove(drivers)

            return jsonify(available_drivers=driver_schema_many.dump(drivers).data)

'''
Driver class allows drivers to be added, removed, and modified in the database.
'''
class Driver(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)

        self.args = parser.parse_args()

        super().__init__()

    def get(self):
        drivers = DriverModel.query.all()
        return jsonify(drivers=driver_schema_many.dump(drivers).data)

    def post(self):
        try:
            new_driver = DriverModel(**self.args)
            new_driver.available = True
            db.session.add(new_driver)
            db.session.commit()

        except DatabaseError:
            return abort(500, 'Driver was not added to the database!')

        return jsonify(message='Driver successfully created!')

    def put(self):

        driver = DriverModel.query.filter_by(id=self.args['id']).first()

        if driver:
            try:
                driver.id = self.args['id']
                driver.name = self.args['name']
                driver.lat = self.args['driver']
                driver.long = self.args['long']
                db.session.commit()
            except DatabaseError:
                return abort(501, 'The admin was not updated!')

            return jsonify(message="Admin was successfully updated!")

        else:
            return abort(500, 'The admin did not exist')

    def delete(self):
        driver = DriverModel.query.filter_by(id=self.args['id']).first()

        if driver:
            try:
                db.session.delete(driver)
                db.session.commit()
            except DatabaseError:
                return abort(502, 'The item was not deleted')

            return jsonify(message="The driver was successfully deleted")

        else:
            return abort(503, 'The driver did not exist')

'''
Rider class allows drivers to be added, removed, and modified in the database.
'''
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

    def put(self):

        rider = RiderModel.query.filter_by(id=self.args['id']).first()

        if rider:
            try:
                rider.id = self.args['id']
                rider.name = self.args['name']
                rider.lat = self.args['lat']
                rider.long = self.args['long']
                db.session.commit()
            except DatabaseError:
                return abort(501, 'The admin was not updated!')

            return jsonify(message="Admin was successfully updated!")

        else:
            return abort(500, 'The admin did not exist')


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


api.add_resource(Admin, '/admin')
api.add_resource(Driver, '/admin/driver')
api.add_resource(Rider, '/admin/rider')
api.add_resource(GetDrivers, '/rider/get_drivers')
api.add_resource(SetRiderDest, '/rider/set_destination')
api.add_resource(SelectDriver, '/rider/select_driver')
api.add_resource(UpdateDriverPosition, '/driver/update_position')
