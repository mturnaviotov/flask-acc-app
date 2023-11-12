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
    return render_template('/'+route_pref+'/edit.html')

### EDIT ITEM
@block.route('/'+route_pref+'/<uuid:id>/edit')
@auth_required()
@roles_accepted(route_pref)
def edit(id):
    safe = escape(id)
    id = uuid.UUID(safe)
    item = Partner.query.filter_by(id=id).first()
    return render_template('/'+route_pref+'/edit.html', item=item)

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
        return redirect(url_for(route_pref+'.get',id=item.id))

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
        return redirect(url_for(route_pref+'.get',id=newItem.id))

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
        return redirect(url_for(route_pref+'.index'))
