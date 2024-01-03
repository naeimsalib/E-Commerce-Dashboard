import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, current_user
from flask_mail import Mail



basedir = os.path.abspath(os.path.dirname(__file__))
login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = '0e97339fb919eafaa1f4fa00351c0249'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'salibnaeim@gmail.com'
app.config['MAIL_PASSWORD'] = "uwix fnln lfvn nllq"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
db = SQLAlchemy(app)
Migrate(app,db)
app.app_context().push()


login_manager.init_app(app)
login_manager.login_view = "signin"
login_manager.login_message_category = 'info'

from mypython import routes