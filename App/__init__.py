from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from .config import conf  


db=SQLAlchemy()
manager=LoginManager()
bootstrap=Bootstrap5()
mail=Mail()
moment=Moment()
manager.login_view='main.token'
manager.login_message='please login first'

templates='/home/magesajr/JAVA/App/templetes'

def create_app(config_name):
    app=Flask(__name__,template_folder=templates)
    app.config.from_object(conf[config_name])
    conf[config_name].init_app(app)

    #initialize extentions
    db.init_app(app)
    manager.init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    
    #import blueprints
    from .main import main
    from .payment import payment
    from .Ceo import Ceo

    #register blueprints
    app.register_blueprint(main)
    app.register_blueprint(payment)
    app.register_blueprint(Ceo)

    return app