from flask import Flask
from flask_bootstrap import Bootstrap, WebCDN
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
app.extensions["bootstrap"]["cdns"]["jquery"] = WebCDN(
    "https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/"
)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
socketio = SocketIO(app)

from app import routes, models

if __name__ == '__main__':
    socketio.run(app)
