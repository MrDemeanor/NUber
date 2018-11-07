from app import db

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    x_location = db.Column(db.Float)
    y_location = db.Column(db.Float)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Rider(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Post {}>'.format(self.body)



class AdminModel(db.Model):

    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)

    def __repr__(self):
        return '<Admin {}>'.format(self.name)