from datetime import datetime
from flask import Blueprint, url_for, request, jsonify, render_template, redirect, flash
from flask_security import auth_required, permissions_accepted, roles_accepted
from markupsafe import escape

from .database import db_session
from .models_warehouse import Warehouse
warehouses = Blueprint('warehouses', __name__)

route_pref='warehouses'

### GET ALL

@warehouses.route('/'+route_pref, methods = ['GET'])
@auth_required()
@roles_accepted(route_pref)
def index():
    all = Warehouse.query.all()
    arr = []
    if 'Accept' in request.headers and 'application/json' in request.headers['Accept']:
        for item in all:
            arr.append(item.to_dict())
        return jsonify(arr)
    if 'text/html'in request.headers['Accept']:
        return render_template('/'+route_pref+'/index.html', items=all)
    return ''
### GET ID

@warehouses.route('/'+route_pref+'/<int:id>')
@auth_required()
@roles_accepted(route_pref)
def get(id):
    item = Warehouse.query.filter_by(warehouse_id=escape(id)).first()
    if 'Accept' in request.headers and 'application/json' in request.headers['Accept']:
        return jsonify(item.to_dict())
    elif 'Content-Type' in request.headers and 'application/json' in request.headers['Content-Type']:
        return jsonify(item.to_dict())
    elif 'text/html'in request.headers['Accept']:
        return render_template('/'+route_pref+'/item.html', item=item)

### CREATE ITEM 
@warehouses.route('/'+route_pref+'/new')
@auth_required()
@roles_accepted(route_pref)
def new():
    return render_template('/'+route_pref+'/new.html')

@warehouses.route('/'+route_pref, methods = ['POST','PATCH','UPDATE'])
@auth_required()
@roles_accepted(route_pref)
def create():
    if 'Content-Type' in request.headers and 'application/x-www-form-urlencoded' in request.headers['Content-Type']:
        data = request.form.to_dict()
        print('x-www-form', data)
    if 'Content-Type' in request.headers and 'application/json' in request.headers['Content-Type']:
        data = request.get_json()
        print('json', data)
    newitem = Warehouse(warehouse_name=escape(data['name']))
    print(newitem)
    db_session.add(newitem)
    db_session.commit()
    item = Warehouse.query.filter_by(warehouse_name=escape(data['name'])).first()
    if 'Accept' in request.headers and 'application/json' in request.headers['Accept']:
        return jsonify(item.to_dict())
    elif 'Content-Type' in request.headers and 'application/json' in request.headers['Content-Type']:
        return jsonify(item.to_dict())
    elif 'text/html'in request.headers['Accept']:
        return redirect(url_for('warehouses.get',id=item.warehouse_id))


### DELETE ITEM 
@warehouses.route('/'+route_pref+'/<int:id>/delete', methods=['POST'])
@auth_required()
@roles_accepted(route_pref)
def delete(id):
    item = Warehouse.query.filter_by(warehouse_id=escape(id)).first()
    db_session.delete(item)
    db_session.commit()
    flash('Data deleted')
    return redirect(url_for('warehouses.index'))

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
