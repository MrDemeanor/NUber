#from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema
from app.models import DriverModel, RiderModel, AdminModel, RatingModel

#ma = Marshmallow()

class DriverSchema(ModelSchema):
    class Meta:
        model = DriverModel

class RiderSchema(ModelSchema):
    class Meta:
        model = RiderModel

class AdminSchema(ModelSchema):
    class Meta:
        model = AdminModel

class RatingSchema(ModelSchema):
    class Meta:
        model = RatingModel

driver_schema_many = DriverSchema(many=True)
driver_schema = DriverSchema()

rider_schema_many = RiderSchema(many=True)
rider_schema = RiderSchema()

admin_schema_many = AdminSchema(many=True)
admin_schema = AdminSchema()

rating_schema_many = RatingSchema(many=True)
rating_schema = RatingSchema()
