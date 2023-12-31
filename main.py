from flask import Flask, Blueprint, render_template, render_template_string, jsonify
from flask_security import current_user, auth_required, permissions_accepted, roles_accepted

main = Blueprint('main', __name__)

from .warehouse.models_warehouse import Good

# Views

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@auth_required()
#@roles_accepted("user")
#@permissions_accepted("user-read")
#permissions_accepted('Super Administrator')
def profile():
    return render_template('profile.html', user=current_user)

@main.route('/profile/json')
@auth_required()
#@roles_accepted("user")
#@permissions_accepted("user-read")
#permissions_accepted('Super Administrator')
def profile_json():
    return jsonify(current_user.to_dict())
    #return render_template('profile.html', user='')

@main.route('/roles/json')
@auth_required()
#@roles_accepted("user")
#@permissions_accepted("user-read")
#permissions_accepted('Super Administrator')
def roles_json():
    roles = list(map(lambda x: x.to_dict(), current_user.roles))
    return jsonify(roles)

@main.route('/board')
@auth_required()
#@roles_accepted("user")
#@permissions_accepted("user-read")
#permissions_accepted('Super Administrator')
def board():
    return '' #jsonify(current_user.to_dict())
    #return render_template('profile.html', user='')

@main.route('/test')
@auth_required()
def test():
    i = Good.query.all()
    items = []
    for item in i: items.append(item._asdict())
    return jsonify(items)