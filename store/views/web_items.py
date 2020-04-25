from flask import Blueprint, request, session, url_for, render_template, redirect,flash,current_app,send_from_directory
from flask_uploads import UploadNotAllowed
#from resources.user import  User, UserModel
#from schemas.user import UserSchema
from schemas.store import StoreSchema
from schemas.item import ItemSchema
from models import requires_login, StoreModel, ItemModel
from libs.strings import gettext
import logging

from werkzeug.security import safe_str_cmp
from libs import image_helper
from schemas.image import ImageSchema
import traceback
import os

logger = logging.getLogger(__package__)
webitem_blueprint = Blueprint('webitems', __name__)

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)

#image_schema = ImageSchema()

@webitem_blueprint.route("/")
@requires_login
def index():
    model_id  = request.args.get('model_id') 
    model = StoreModel.find_by_id(model_id)
    #print(model)
    #print(store_list_schema.dump(model.items))
    return render_template("items/index.html", items=item_list_schema.dump(model.items), model=model)

@webitem_blueprint.route("/new", methods=["GET", "POST"])
@requires_login
def create_item():
    
    if request.method == "POST":
        name = request.form['name']
        model_id = request.args.get('model_id') 
        
        #image logic
        username = session['username']
        folder = f"user_{username}"
        # validation and sanity checks

        if model_id is None:
            return "Missing model number"

        if 'file1' not in request.files:
            return "Missing file part"
        
        if ItemModel.find_by_name(name):
            return gettext("web_items_alredyexists")
        
        file1 = request.files['file1']
        
        #data = image_schema.load(file1)

        try:
            #image_path = image_helper.save_image(data["image"], folder=folder)
            image_path = image_helper.save_image(file1, folder=os.path.join(folder,model_id))
            logger.info(image_path)
            basename = image_helper.get_basename(image_path)
            logger.info(basename)
        except UploadNotAllowed:  # forbidden file type
            extension = image_helper.get_extension(file1)
            return  f"Unable to upload the extension {extension}"

        #create item in database
        item = ItemModel(name=name,filename=file1.filename,objname=image_path,store_id=model_id)
        print(item)
        try:
            item.save_to_db()
        except:
            return "Error creating item"

        return redirect(url_for(".index",model_id=model_id))
    #Get implementation
    model_id=request.args.get('model_id')
    return render_template("items/new_item.html",model_id=model_id )

@webitem_blueprint.route("/delete/<string:item_id>")
@requires_login
def delete_item(item_id):
    item = ItemModel.find_by_id(item_id)
    model_id = request.args.get('model_id') 
    item.delete_from_db()
    try:
        #uploads = os.path.join(current_app.root_path, current_app.config['UPLOADED_IMAGES_DEST'])
        uploads = os.path.join( current_app.config['UPLOADED_IMAGES_DEST'])
        os.remove(os.path.join(uploads,item.objname))
    except:
        traceback.print_exc()
        return "File deletion failed"

    return redirect(url_for(".index",model_id=model_id))



@webitem_blueprint.route("/download/<string:item_id>")
@requires_login
def download_file(item_id):
    item = ItemModel.find_by_id(item_id)
    model_id = request.args.get('model_id') 
   
    try:
        uploads = os.path.join( current_app.config['UPLOADED_IMAGES_DEST'], os.path.dirname(item.objname))
        return send_from_directory(directory=uploads, filename=os.path.basename(item.objname),attachment_filename=item.filename,as_attachment=True)
    except:
        traceback.print_exc()
        return "File not found!"

    return redirect(url_for(".index",model_id=model_id))
