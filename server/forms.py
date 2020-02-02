from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from server.models import User


class MainPageForm(FlaskForm):
    departure = SelectField('DepartureCity', validators=[DataRequired()], choices=[('Warsaw', 'Warsaw'), ('Rome', 'Rome'), ('Tokyo', 'Tokyo')])
    arrival = SelectField('ArrivalCity', validators=[DataRequired()], choices=[('Warsaw', 'Warsaw'), ('Rome', 'Rome'), ('Tokyo', 'Tokyo')])
    departure_date = DateField('Departure', validators=[DataRequired()])
    arrival_date = DateField('Arrival', validators=[DataRequired()])
    class1 = SelectField('Class', choices=[('1', 'First'), ('E', 'Economy'), ('B', 'Business')])
    passenger_count = SelectField('Passenger', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')])
    search = SubmitField('Search')


class RegistrationForm(FlaskForm):
    first_name = StringField('FirstName', validators=[DataRequired()])
    last_name = StringField('LastName', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('man', 'Male'), ('woman', 'Female')])
    dateOfBirth = DateField('Date of Birth', validators=[DataRequired()])

    document_type = SelectField('Document Type',
                                choices=[('GC', '(Document)Green card'), ('PS', 'Passport'), ('BC', 'Interim Card')])

    document_number = StringField('Document Number', validators=[DataRequired(), Length(min=8)])
    nationality = SelectField('Nationality', choices=[('Az', 'Azerbaijan'), ('PL', 'Poland')])
    dateOfDocExp = DateField('Date of Document Expiry', validators=[DataRequired()])
    phoneNumber = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=25)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    country = SelectField('Country', choices=[('Az', 'Azerbaijan'), ('PL', 'Poland')])
    city = StringField('City', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    building = StringField('Building', validators=[DataRequired()])
    apartment = StringField('Apartment', validators=[DataRequired()])
    zip = StringField('Zip Code', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken, please choose another one')

    def validate_document_number(self, document_number):
        user = User.query.filter_by(document_number=document_number.data).first()
        if user:
            raise ValidationError('This email is taken, please choose another one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=25)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')
