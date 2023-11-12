import os
from os import environ
from datetime import datetime
from dotenv import load_dotenv, dotenv_values
from flask import Flask, render_template, render_template_string
from flask_security import Security, current_user, auth_required, hash_password, \
     SQLAlchemySessionUserDatastore, permissions_accepted, roles_accepted
from flask_wtf.csrf import CSRFProtect
from .database import db_session, init_db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import uuid
csrf = CSRFProtect()

load_dotenv('.env')

# Create app
def create_app():
    app = Flask(__name__)
    config = dotenv_values()
    app.config.from_mapping(config)

    ##
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False
    app.config['SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS'] = True
    app.config['SECURITY_CSRF_PROTECT_MECHANISMS'] = ["session", "basic"]
    ##

    from .models import User, Role
    csrf.init_app(app)

    # Don't worry if email has findable domain
    app.config["SECURITY_EMAIL_VALIDATOR_ARGS"] = {"check_deliverability": False}

    # manage sessions per request - make sure connections are closed and returned
    app.teardown_appcontext(lambda exc: db_session.close())

    # Setup Flask-Security
    user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
    app.security = Security(app, user_datastore)

    from .warehouse.models_warehouse import Warehouse, Partner, Agreement, Item, Delivery

    # one time setup
    with app.app_context():
        init_db()
        # Create a user and role to test with
        app.security.datastore.find_or_create_role(
            name="user", permissions={"user-read", "user-write"}
        )
        app.security.datastore.find_or_create_role(
            name="warehouses", permissions={"warehouses-read", "warehouses-write"}
        )
        app.security.datastore.find_or_create_role(
            name="partners", permissions={"partners-read", "partners-write"}
        )
        app.security.datastore.find_or_create_role(
            name="agreements", permissions={"agreements-read", "agreements-write"}
        )
        app.security.datastore.find_or_create_role(
            name="deliveries", permissions={"deliveries-read", "deliveries-write"}
        )
        db_session.commit()
        if not app.security.datastore.find_user(email="test@me.com"):
            app.security.datastore.create_user(email="test@me.com",
            password=hash_password("password"), roles=["user","warehouses", "partners","agreements","deliveries"])
        db_session.commit()

############## warehouse #############
        if not Warehouse.query.filter_by(name='1').count() == 1:
            db_session.add(Warehouse(name='1'))
            db_session.commit()

        partner = Partner(name='1')
        if not Partner.query.filter_by(name='1').count() == 1:
            db_session.add(partner)
            db_session.commit()
        agr = Agreement(partner_id=Partner.query.filter_by(name='1').first().id,name='1')
        if not Agreement.query.filter_by(name='1').count() == 1:
            db_session.add(agr)
            db_session.commit()

        deliveryIn = Delivery(num='1',date=datetime.now(), type=True, \
            partner_id=Partner.query.filter_by(name='1').first().id, \
            warehouse_id=Warehouse.query.filter_by(name='1').first().id,
            )
        if not Delivery.query.filter_by(num='1').count() == 1:
            db_session.add(deliveryIn)                           
            db_session.commit()

        deliveryOut = Delivery(id=uuid.uuid4(),num='2',date=datetime.now(), type=False, \
            partner_id=Partner.query.filter_by(name='1').first().id, \
            warehouse_id=Warehouse.query.filter_by(name='1').first().id
            )
        if not Delivery.query.filter_by(num='2').count() == 1:
            db_session.add(deliveryOut)                           
            db_session.commit()

        itemIn = Item(name='eggs',count='20',units='pcs',price='20', \
            price_vat='20', delivery_id=Delivery.query.filter_by(num='1').first().id)
        if not Item.query.filter_by(name='eggs',count='20').count() == 1:
            db_session.add(itemIn)
            db_session.commit()
        
        itemOut = Item(id=uuid.uuid4(),name='eggs',count='10',units='pcs',price='20', \
            price_vat='10', delivery_id=Delivery.query.filter_by(num='2').first().id)
        if not Item.query.filter_by(name='eggs',count='q0').count() == 1:
            db_session.add(itemOut)
            db_session.commit()

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #blueprint for non-auth parts of app
    from .warehouse.warehouses import block as warehouses_blueprint
    app.register_blueprint(warehouses_blueprint)

    #blueprint for non-auth parts of app
    from .warehouse.partners import block as partners_blueprint
    app.register_blueprint(partners_blueprint)
    #blueprint for non-auth parts of app

    from .agreement import agreement as agreement_blueprint
    app.register_blueprint(agreement_blueprint)

    from .delivery import delivery as delivery_blueprint
    app.register_blueprint(delivery_blueprint)

### Error hanlders 

    @app.errorhandler(401)
    def unauthorized_page(error):
        return render_template("errors/401.html"), 401

    @app.errorhandler(403)
    def page_not_found(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/500.html"), 500

    if __name__ == '__main__':
        # run application (can also use flask run)
        app.run()
    
    return app