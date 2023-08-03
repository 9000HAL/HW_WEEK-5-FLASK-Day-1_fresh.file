from flask import Flask
from config import Config
from flask_login import LoginManager

login_manager = LoginManager()


app = Flask(__name__)
app.config.from_object(Config)
login_manager.init_app(app)



from app import routes

