from datetime import datetime
from flask import Blueprint, url_for, request, jsonify, render_template, redirect, flash
from flask_security import auth_required, permissions_accepted, roles_accepted
from markupsafe import escape
import uuid
from .database import db_session
from .models_warehouse import Warehouse
warehouses = Blueprint('warehouses', __name__)

route_pref='warehouses'

### GET ALL

@warehouses.route('/'+route_pref+'/', methods = ['GET'])
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

@warehouses.route('/'+route_pref+'/<uuid:id>')
@auth_required()
@roles_accepted(route_pref)
def get(id):
    safe = escape(id)
    id = uuid.UUID(safe)
    item = Warehouse.query.filter_by(id=id).first()
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

@warehouses.route('/'+route_pref+'/', methods = ['POST','PATCH','UPDATE'])
@auth_required()
@roles_accepted(route_pref)
def create():
    if 'Content-Type' in request.headers and 'application/x-www-form-urlencoded' in request.headers['Content-Type']:
        data = request.form.to_dict()
    if 'Content-Type' in request.headers and 'application/json' in request.headers['Content-Type']:
        data = request.get_json()
    newitem = Warehouse(name=escape(data['name']))
    db_session.add(newitem)
    db_session.commit()
    item = Warehouse.query.filter_by(name=escape(data['name'])).first()
    if 'Accept' in request.headers and 'application/json' in request.headers['Accept']:
        return jsonify(item.to_dict())
    elif 'Content-Type' in request.headers and 'application/json' in request.headers['Content-Type']:
        return jsonify(item.to_dict())
    elif 'text/html'in request.headers['Accept']:
        flash('Item created')
        return redirect(url_for('warehouses.get',id=item.id))

### DELETE ITEM 
@warehouses.route('/'+route_pref+'/<uuid:id>/delete', methods=['POST','DELETE'])
@auth_required()
@roles_accepted(route_pref)
def delete(id):
    safe = escape(id)
    id = uuid.UUID(safe)
    item =Warehouse.query.filter_by(id=id).first()
    db_session.delete(item)
    db_session.commit()
    if 'Accept' in request.headers and 'application/json' in request.headers['Accept']:
        return '' #jsonify(item.to_dict())
    elif 'Content-Type' in request.headers and 'application/json' in request.headers['Content-Type']:
        return '' #jsonify(item.to_dict())
    elif 'text/html'in request.headers['Accept']:
        flash('Item Deleted')
        return redirect(url_for('warehouses.index'))
    return '' #redirect(url_for('warehouses.index'))