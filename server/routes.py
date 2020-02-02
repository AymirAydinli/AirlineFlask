from sqlalchemy.orm import Session
import random as rnd
from server import app, db, bcrypt, forms
from server.forms import MainPageForm, RegistrationForm, LoginForm
from server.models import User, Psngr_Adrs_Dtls, Psngr_Doc_Dtls, Flight_Details, Airport
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/main', methods=['GET', 'POST'])
def main():
    form = MainPageForm()
    if form.is_submitted():
        airport = Airport(departure=form.departure.data, arrival=form.arrival.data)
        #airp = Airport.query.get(current_user.id)
        flight = Flight_Details(departure_date=form.departure_date.data, arrival_date=form.arrival_date.data,
                                passenger_count=form.passenger_count.data, fare=rnd.randint(150, 300),
                                user1=current_user, user2=airport)
        db.session.add(airport)
        db.session.add(flight)
        db.session.commit()
        return redirect(url_for('available'))
    return render_template('main.html', title="Search", form=form)


@app.route('/ticket')
@login_required
def ticket():
    f = Flight_Details.query.get(current_user.id)
    return render_template('ticket.html', title='Ticket', f=f)


@app.route('/available')
def available():
    form = MainPageForm()
    # max = db.session.query(db.func.max(Flight_Details.id)).scalar()
    # flights = db.session.query(Flight_Details).filter(Flight_Details.id == max).first()
    # flights = Flight_Details.query.all()
    flights = Flight_Details.query.get(current_user.id)
    if form.validate_on_submit():
        return redirect(url_for('ticket'))
    return render_template('available.html', title="Available Flights", form=form, flights=flights)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You have been logged in successfully", 'success')
            return redirect(url_for('main'))
        else:
            flash("Login Unsuccessful,Please check your email and password", 'danger')
    return render_template('login.html', title="Login", form=form)


@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.is_submitted():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, second_name=form.last_name.data, email=form.email.data,
                    password=hashed_password, document_number=form.document_number.data,
                    dateOfBirth=form.dateOfBirth.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account have been created, now You can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login2'))


@app.route('/TEST')
def TEST():
    airport = Airport.query.get(current_user.id)
    flight = Flight_Details.query.get(current_user.id)
    return render_template('TEST.html', title="TEST", flight=flight, airport=airport)


@app.route('/login2', methods=['GET', 'POST'])
def login2():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You have been logged in successfully", 'success')
            return redirect(url_for('ticket'))
        else:
            flash("Login Unsuccessful,Please check your email and password", 'danger')
    return render_template('login2.html', title="Login2", form=form)
