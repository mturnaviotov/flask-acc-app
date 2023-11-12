from datetime import datetime
from flask import Blueprint, url_for, request, jsonify, render_template, redirect, flash
from flask_security import auth_required, permissions_accepted, roles_accepted
from markupsafe import escape
import uuid
from ..database import db_session
from .models_warehouse import Partner
block = Blueprint('partners', __name__)

route_pref='partners'

### GET ALL

@block.route('/'+route_pref+'/', methods = ['GET'])
@auth_required()
@roles_accepted(route_pref)
def index():
    all = Partner.query.all()
    arr = []
    if 'Accept' in request.headers and 'application/json' in request.headers['Accept']:
        for item in all:
            arr.append(item.to_dict())
        return jsonify(arr)
    if 'text/html'in request.headers['Accept']:
        return render_template('/'+route_pref+'/index.html', items=all)
    return ''
### GET ID

@block.route('/'+route_pref+'/<uuid:id>')
@auth_required()
@roles_accepted(route_pref)
def get(id):
    safe = escape(id)
    id = uuid.UUID(safe)
    item = Partner.query.filter_by(id=id).first()
    if 'Accept' in request.headers and 'application/json' in request.headers['Accept']:
        return jsonify(item.to_dict())
    elif 'Content-Type' in request.headers and 'application/json' in request.headers['Content-Type']:
        return jsonify(item.to_dict())
    elif 'text/html'in request.headers['Accept']:
        return render_template('/'+route_pref+'/item.html', item=item)

### CREATE ITEM 
@block.route('/'+route_pref+'/new')
@auth_required()
@roles_accepted(route_pref)
def new():
    return render_template('/'+route_pref+'/new.html')

@block.route('/'+route_pref+'/', methods = ['POST'])
@auth_required()
@roles_accepted(route_pref)
def create():
    if 'Content-Type' in request.headers and 'application/x-www-form-urlencoded' in request.headers['Content-Type']:
        data = request.form.to_dict()
    if 'Content-Type' in request.headers and 'application/json' in request.headers['Content-Type']:
        data = request.get_json()
    newitem = Partner(name=escape(data['name']))
    db_session.add(newitem)
    db_session.commit()
    item = Partner.query.filter_by(name=escape(data['name'])).first()
    if 'Accept' in request.headers and 'application/json' in request.headers['Accept']:
        return jsonify(item.to_dict())
    elif 'Content-Type' in request.headers and 'application/json' in request.headers['Content-Type']:
        return jsonify(item.to_dict())
    elif 'text/html'in request.headers['Accept']:
        flash('Item created')
        return redirect(url_for('partners.get',id=item.id))

### UPDATE ITEM 
@block.route('/'+route_pref+'/<uuid:id>', methods=['UPDATE','PATCH','POST'])
@auth_required()
@roles_accepted(route_pref)
def update(id):
    safe = escape(id)
    id = uuid.UUID(safe)
    item = Partner.query.filter_by(id=id).first()#.to_dict()
    dict = item.to_dict()
    db_session.delete(item)
    #s = dict(item.__table__.columns)
    #props= (list(s))
    if 'Content-Type' in request.headers and 'application/x-www-form-urlencoded' in request.headers['Content-Type']:
        data = request.form.to_dict()
    if 'Content-Type' in request.headers and 'application/json' in request.headers['Content-Type']:
        data = request.get_json()
#    for prop in props:
#        if prop != 'id': item['{prop}'] = data[prop] 
    for field in data:
        dict[field] = escape(data[field])
    newItem = Partner(**dict)
    db_session.add(newItem)
    db_session.commit()
    if 'Accept' in request.headers and 'application/json' in request.headers['Accept']:
        return jsonify(newItem.to_dict())
    elif 'Content-Type' in request.headers and 'application/json' in request.headers['Content-Type']:
        return jsonify(newItem.to_dict())
    elif 'text/html'in request.headers['Accept']:
        flash('Item Updated')
        return redirect(url_for('partners.get',id=newItem.id))

### DELETE ITEM 
@block.route('/'+route_pref+'/<uuid:id>/delete', methods=['POST','DELETE'])
@auth_required()
@roles_accepted(route_pref)
def delete(id):
    safe = escape(id)
    id = uuid.UUID(safe)
    item =Partner.query.filter_by(id=id).first()
    db_session.delete(item)
    db_session.commit()
    if 'Accept' in request.headers and 'application/json' in request.headers['Accept']:
        return '' #jsonify(item.to_dict())
    elif 'Content-Type' in request.headers and 'application/json' in request.headers['Content-Type']:
        return '' #jsonify(item.to_dict())
    elif 'text/html'in request.headers['Accept']:
        flash('Item Deleted')
        return redirect(url_for('partners.index'))

#################
# from datetime import datetime
# from flask import Blueprint, url_for, request, jsonify, render_template, redirect, flash
# from flask_security import auth_required, permissions_accepted, roles_accepted
# from markupsafe import escape

# from ..database import db_session
# from .models_warehouse import Partner
# partner = Blueprint('partner', __name__)

# route_pref='partner'

# @partner.route('/'+route_pref+'/<int:id>')
# @auth_required()
# @roles_accepted(route_pref)
# def get(id):
#     item = Partner.query.filter_by(partner_id=escape(id)).first().to_dict()
#     return render_template(route_pref+'/item.html', item=item)

# @partner.route('/'+route_pref+'/<int:id>/json')
# @auth_required()
# @roles_accepted(route_pref)
# def get_json(id):
#     item = partner.query.filter_by(partner_id=escape(id)).first().to_dict()
#     return jsonify(item)

# @partner.route('/'+route_pref)
# @auth_required()
# @roles_accepted(route_pref)
# def index():
#    i = db_session.query(partner).all()
#     all = Partner.query.all()
#     arr = []
#     for item in all:
#         arr.append(item.to_dict())
#     return render_template('/'+route_pref+'/index.html', items=arr)

# @partner.route('/'+route_pref+'/create') #, methods=['POST'])
# @auth_required()
# @roles_accepted(route_pref)
# def create_page():
#     return render_template('/'+route_pref+'/create.html')

# @partner.route('/'+route_pref+'/json')
# @auth_required()
# @roles_accepted(route_pref)
# def index_json():
#     all = Partner.query.all()
#     arr = []
#     for item in all:
#         arr.append(item.to_dict())
#     return jsonify(arr)

# @partner.route('/'+route_pref, methods=['POST'])
# @auth_required()
# @roles_accepted(route_pref)
# def create():
#     # code to validate before database goes here
#     name = request.form.get('name')
#     item = Partner(partner_name=escape(name))

#     # add the new item to the database
#     db_session.add(item)
#     db_session.commit()
#     flash('Data saved')
#     return redirect(url_for('partner.index'))

# @partner.route('/'+route_pref+'/<int:id>/delete', methods=['POST'])
# @auth_required()
# @roles_accepted(route_pref)
# def delete(id):
#     item = Partner.query.filter_by(partner_id=escape(id)).first()
#     db_session.delete(item)
#     db_session.commit()
#     flash('Data deleted')
#     return redirect(url_for('partner.index'))

#     return redirect(url_for('auth.login'))
# ##########################################
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

# @auth.route('/signup')
# def signup():
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

# @auth.route('/logout')
# @login_required
# def logout():
#    logout_user()
#    return redirect(url_for('main.index'))
