import os
from os import environ
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
#    warehouse_datastore = db_session.connection
    #.add_all( Warehouse, Partner, Agreement, Item, DeliveryOperation, Delivery)

    # one time setup
    with app.app_context():
        init_db()
        # Create a user and role to test with
        app.security.datastore.find_or_create_role(
            name="user", permissions={"user-read", "user-write"}
        )
        db_session.commit()
        if not app.security.datastore.find_user(email="test@me.com"):
            app.security.datastore.create_user(email="test@me.com",
            password=hash_password("password"), roles=["user"])        
        db_session.commit()

        db_session.add(Warehouse(warehouse_name='1'))
        db_session.commit()
        db_session.add(Partner(partner_name='1'))
        db_session.commit()
        db_session.add(Agreement(partner_id=1,agreement_name='1'))
        db_session.commit()
        db_session.add(DeliveryOperation(delivery_operation_name='Income'))
        db_session.commit()
        db_session.add(DeliveryOperation(delivery_operation_name='Outcome'))
        db_session.commit()

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #blueprint for non-auth parts of app
    from .warehouse import warehouse as warehouse_blueprint
    app.register_blueprint(warehouse_blueprint)

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