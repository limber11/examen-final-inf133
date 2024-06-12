# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('app.config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from app.routes import users, restaurants, reservations
app.register_blueprint(users.bp)
app.register_blueprint(restaurants.bp)
app.register_blueprint(reservations.bp)

# Swagger setup
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Restaurant Reservation API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
