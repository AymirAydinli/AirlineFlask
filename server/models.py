from server import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    second_name = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    password = db.Column(db.String(60), nullable=False)
    dateOfBirth = db.Column(db.Date)
    email = db.Column(db.String(20), unique=True, nullable=False)
    document_number = db.Column(db.String(20), unique=True, nullable=False)
    address = db.relationship('Psngr_Adrs_Dtls', backref='adrs', lazy=True)
    docs = db.relationship('Psngr_Doc_Dtls', backref='user', lazy=True)
    ticket_user = db.relationship('Flight_Details', backref='user1', lazy=True)

    def __repr__(self):
        return f"User('{self.first_name}','{self.second_name}','{self.email}','{self.gender}','{self.dateOfBirth}')"


class Psngr_Adrs_Dtls(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phoneNumber = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    street = db.Column(db.String(30), nullable=False)
    building = db.Column(db.String(10), nullable=False)
    apartment = db.Column(db.String(10), nullable=False)
    zip = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Psngr_Adrs_Dtls('{self.country}','{self.city}','{self.street}','{self.building}','{self.zip}')"


class Psngr_Doc_Dtls(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_type = db.Column(db.String(10), nullable=False)
    nationality = db.Column(db.String(30), nullable=False)
    dateOfDocExp = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Psngr_Doc_Dtls('{self.document_type}','{self.nationality}','{self.dateOfDocExp}')"


class Flight_Details(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    departure_date = db.Column(db.Date)
    arrival_date = db.Column(db.Date)
    passenger_count = db.Column(db.Integer, nullable=False)
    fare = db.Column(db.Integer, nullable=True)
    airport_id = db.Column(db.Integer, db.ForeignKey('airport.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Flight_Details('{self.departure_date}','{self.arrival_date}', '{self.fare}', '{self.user_id}', '{self.airport_id}')"


class Airport(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    departure = db.Column(db.String(20), nullable=False, default=datetime.utcnow())
    arrival = db.Column(db.String(20), nullable=False)
    flight_det = db.relationship('Flight_Details', backref='user2', lazy=True)

    def __repr__(self):
        return f"Airport('{self.Airport_name}','{self.departure}','{self.arrival}')"
