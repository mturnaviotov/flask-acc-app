from flask import Flask, Blueprint, render_template, render_template_string
from flask_security import current_user, auth_required, permissions_accepted, roles_accepted

main = Blueprint('main', __name__)

# Views

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@auth_required()
@roles_accepted("user")
#@permissions_accepted("user-read")
#permissions_accepted('Super Administrator')
def profile():
    return render_template('profile.html', user=current_user)

