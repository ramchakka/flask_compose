from flask import Flask, jsonify,render_template, request, session, make_response
from flask_restful import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_migrate import Migrate
from marshmallow import ValidationError
from werkzeug.security import safe_str_cmp
from flask_uploads import configure_uploads, patch_request_class

from marshmallow import ValidationError
import logging
import logging.config

from db import db
from ma import ma
from blacklist import BLACKLIST
#from resources.user import UserRegister, UserLogin, User, UserModel, TokenRefresh, UserLogout
#from schemas.user import UserSchema
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from views.web_user import webuser_blueprint
from views.web_models import webmodel_blueprint
from views.web_items import webitem_blueprint
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.getfile import Getfile
from resources.getencfile import GetEncodedFile
from libs.image_helper import IMAGE_SET
import os

app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")  # load default configs from default_config.py
app.config.from_envvar(
    "APPLICATION_SETTINGS"
)  # override with config.py (APPLICATION_SETTINGS points to config.py)
logging.config.fileConfig(os.path.join(app.root_path,app.config["LOG_CONFIG_FILE"]))
logger = logging.getLogger()
patch_request_class(app, 25 * 1024 * 1024)  # restrict max upload image size to 20MB
configure_uploads(app, IMAGE_SET)
app.secret_key = app.config["JWT_SECRET_KEY"]
api = Api(app)
jwt = JWTManager(app)
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)



@app.before_first_request
def create_tables():
    db.create_all()

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400

# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST

@app.route('/')
def home():
    return render_template('home.html')

app.register_blueprint(webuser_blueprint, url_prefix="/web/user")
app.register_blueprint(webmodel_blueprint, url_prefix="/web/models")
app.register_blueprint(webitem_blueprint, url_prefix="/web/items")

api.add_resource(Store, "/store/<string:name>")
api.add_resource(Getfile, "/file/<string:name>")
api.add_resource(GetEncodedFile, "/encodedfile/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

if __name__ == "__main__":
    #db.init_app(app)
    #ma.init_app(app)
    #app.run(host='0.0.0.0',port=5000, debug=True)
    app.run(host='0.0.0.0', debug=True)
