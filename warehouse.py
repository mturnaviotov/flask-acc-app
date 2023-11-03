from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, render_template_string, jsonify
from flask_security import auth_required, permissions_accepted, roles_accepted
import uuid
from .database import db_session
from .models_warehouse import Warehouse
warehouse = Blueprint('warehouse', __name__)

wh='/warehouse'
@warehouse.route(wh+'/all')
def all():
    i = db_session.query(Warehouse).all()
    print('i',i)
    return jsonify(i)

# @auth.route('/login', methods=['POST'])
# def login_post():
#     # login code goes here
#     email = request.form.get('email')
#     password = request.form.get('password')
#     remember = True if request.form.get('remember') else False

#     user = User.query.filter_by(email=email).first()

#     # check if the user actually exists
#     # take the user-supplied password, hash it, and compare it to the hashed password in the database
#     if not user or not check_password_hash(user.password, password):
#         flash('Please check your login details and try again.')
#         return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

#     # if the above check passes, then we know the user has the right credentials
#     login_user(user, remember=remember)
#     return redirect(url_for('main.profile'))

#@auth.route('/signup')
#def signup():
#    return render_template('auth/signup.html')

# @auth.route('/signup', methods=['POST'])
# def signup_post():
#     # code to validate and add user to database goes here
#     email = request.form.get('email')
#     name = request.form.get('name')
#     password = request.form.get('password')
#     is_active = True

#     user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

#     if user: # if a user is found, we want to redirect back to signup page so user can try again
#         flash('Email address already exists')
#         return redirect(url_for('auth.signup'))

#     # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#     new_user = User(id=uuid.uuid4(), email=email, name=name, is_active = is_active, created_at = datetime.now(), password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))

#     # add the new user to the database
#     db.session.add(new_user)
#     db.session.commit()

#     return redirect(url_for('auth.login'))

#@auth.route('/logout')
#@login_required
#def logout():
#    logout_user()
#    return redirect(url_for('main.index'))
