from datetime import datetime
from flask import Blueprint, url_for, request, jsonify, render_template, redirect, flash
from flask_security import auth_required, permissions_accepted, roles_accepted
from markupsafe import escape

from .database import db_session
from .models_warehouse import Partner
partner = Blueprint('partner', __name__)

route_pref='partner'

@partner.route('/'+route_pref+'/<int:id>')
@auth_required()
@roles_accepted("partner")
def get(id):
    item = partner.query.filter_by(partner_id=escape(id)).first().to_dict()
    return render_template(route_pref+'/item.html', item=item)

@partner.route('/'+route_pref+'/<int:partner_id>/json')
@auth_required()
@roles_accepted("partner")
def get_json(id):
    item = partner.query.filter_by(partner_id=escape(id)).first().to_dict()
    return jsonify(item)

@partner.route('/'+route_pref)
@auth_required()
@roles_accepted("partner")
def index():
#    i = db_session.query(partner).all()
    all = Partner.query.all()
    arr = []
    for item in all:
        arr.append(item.to_dict())
    return render_template('/'+route_pref+'/index.html', items=arr)

@partner.route('/'+route_pref+'/create') #, methods=['POST'])
@auth_required()
@roles_accepted("partner")
def create_page():
    return render_template('/'+route_pref+'/create.html')

@partner.route('/'+route_pref+'/json')
@auth_required()
@roles_accepted("partner")
def index_json():
    all = Partner.query.all()
    arr = []
    for item in all:
        arr.append(item.to_dict())
    return jsonify(arr)

@partner.route('/'+route_pref, methods=['POST'])
@auth_required()
@roles_accepted("partner")
def create():
#     # code to validate before database goes here
    name = request.form.get('name')
    item = Partner(partner_name=escape(name))

#     # add the new item to the database
    db_session.add(item)
    db_session.commit()
    flash('Data saved')
    return redirect(url_for('partner.index'))

@partner.route('/'+route_pref+'/<int:id>/delete', methods=['POST'])
@auth_required()
@roles_accepted("partner")
def delete(id):
    item = Partner.query.filter_by(partner_id=escape(id)).first()
    db_session.delete(item)
    db_session.commit()
    flash('Data deleted')
    return redirect(url_for('partner.index'))

#     return redirect(url_for('auth.login'))
###########################################
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
