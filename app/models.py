from app import db

class DriverModel(db.Model):
    __tablename__ = "driver"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    x_location = db.Column(db.Float)
    y_location = db.Column(db.Float)

    def __repr__(self):
        return '<User {}>'.format(self.name)

class RiderModel(db.Model):
    __tablename__ = "rider"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index = True)
     
    def __repr__(self):
        return '<Post {}>'.format(self.name)



class AdminModel(db.Model):

    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)

    def __repr__(self):
        return '<Admin {}>'.format(self.name)
