import os
from os import environ
from datetime import datetime
from dotenv import load_dotenv, dotenv_values
from flask import Flask, render_template, render_template_string
from flask_security import Security, current_user, auth_required, hash_password, \
     SQLAlchemySessionUserDatastore, permissions_accepted, roles_accepted

from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
from .database import db_session, init_db

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

load_dotenv('.env')

# Create app
def create_app():
    app = Flask(__name__)
    config = dotenv_values()
    app.config.from_mapping(config)

    ##
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False
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

    from .models_warehouse import Warehouse, Partner, Agreement, Item, DeliveryOperation, Delivery

    # one time setup
    with app.app_context():
        init_db()
        # Create a user and role to test with
        app.security.datastore.find_or_create_role(
            name="user", permissions={"user-read", "user-write"}
        )
        app.security.datastore.find_or_create_role(
            name="warehouse", permissions={"warehouse-read", "warehouse-write"}
        )
        app.security.datastore.find_or_create_role(
            name="partner", permissions={"partner-read", "partner-write"}
        )
        app.security.datastore.find_or_create_role(
            name="agreement", permissions={"agreement-read", "agreement-write"}
        )
        app.security.datastore.find_or_create_role(
            name="deliveryoperation", permissions={"deliveryoperation-read", "deliveryoperation-write"}
        )
        app.security.datastore.find_or_create_role(
            name="delivery", permissions={"delivery-read", "delivery-write"}
        )
        db_session.commit()
        if not app.security.datastore.find_user(email="test@me.com"):
            app.security.datastore.create_user(email="test@me.com",
            password=hash_password("password"), roles=["user","warehouse", "partner","agreement","deliveryoperation","delivery"])        
        db_session.commit()

############## warehouse #############
        if not Warehouse.query.filter_by(warehouse_name='1').count() == 1:
            db_session.add(Warehouse(warehouse_name='1'))
            db_session.commit()
        if not Partner.query.filter_by(partner_name='1').count() == 1:
            db_session.add(Partner(partner_name='1'))
            db_session.commit()
        if not Agreement.query.filter_by(partner_id=1,agreement_name='1').count() == 1:
            db_session.add(Agreement(partner_id=1,agreement_name='1'))
            db_session.commit()
        if not DeliveryOperation.query.filter_by(delivery_operation_name='Income').count() == 1:
            db_session.add(DeliveryOperation(delivery_operation_name='Income'))
            db_session.commit()
        if not DeliveryOperation.query.filter_by(delivery_operation_name='Outcome').count() == 1:
            db_session.add(DeliveryOperation(delivery_operation_name='Outcome'))
            db_session.commit()

        if not Delivery.query.filter_by(delivery_id='1').count() == 1:
            db_session.add(Delivery(delivery_id='1',delivery_num='1',delivery_type='1',delivery_date=datetime.now(),partner_id='1',warehouse_id='1'))
            db_session.commit()
        if not Item.query.filter_by(item_id='1').count() == 1:
            db_session.add(Item(item_id='1',item_name='eggs',item_count='20',item_units='pcs',item_price='20',item_price_vat='20', delivery_id='1'))
            db_session.commit()

##### insert into deliveries values ('1','1','8.11.2023 0:0:0','1','1','1','1')
##### insert into items values('1','eggs','50','pcs','20','20','1')
#        if not Delivery.query.filter_by(delivery_operation_name='Outcome').count() == 1:
#            db_session.add(DeliveryOperation(delivery_operation_name='Outcome'))
#            db_session.commit()

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #blueprint for non-auth parts of app
    from .warehouse import warehouse as warehouse_blueprint
    app.register_blueprint(warehouse_blueprint)

    #blueprint for non-auth parts of app
    from .partner import partner as partner_blueprint
    app.register_blueprint(partner_blueprint)
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