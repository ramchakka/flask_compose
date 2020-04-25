from flask import Blueprint, request, session, url_for, render_template, redirect,flash
#from resources.user import  User, UserModel
#from schemas.user import UserSchema
from schemas.store import StoreSchema
from models import requires_login, StoreModel
from werkzeug.security import safe_str_cmp

webmodel_blueprint = Blueprint('webmodels', __name__)
store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


@webmodel_blueprint.route("/new", methods=["GET", "POST"])
@requires_login
def create_model():
    if request.method == "POST":
        name = request.form['name']
        if StoreModel.find_by_name(name):
            return "Model already exists with name. Try another name"

        store = StoreModel(name=name,username=session['username'])
        try:
            store.save_to_db()
        except:
            return "Error creating model"

        return redirect(url_for(".index"))

    return render_template("models/new_model.html")

@webmodel_blueprint.route("/")
@requires_login
def index():
    models = StoreModel.find_by_username(session["username"])
    #print(store_list_schema.dump(models))
    return render_template("models/index.html", models=store_list_schema.dump(models))

@webmodel_blueprint.route("/edit/<string:model_id>", methods=["GET", "POST"])
@requires_login
def edit_model(model_id):
    if request.method == "POST":
        name = request.form['name']
        model = StoreModel.find_by_id(model_id)
        model.name = name
        try:
            model.save_to_db()
        
        except:
            flash('Error renaming model', 'danger')
            #return "Error renaming model"

        return redirect(url_for(".index"))
        
    # What happens if it's a GET request
    return render_template("models/edit_model.html", model=StoreModel.find_by_id(model_id))

@webmodel_blueprint.route("/delete/<string:model_id>")
@requires_login
def delete_model(model_id):
    model = StoreModel.find_by_id(model_id)
    if model.username == session["username"]:
        model.delete_from_db()
    return redirect(url_for(".index"))