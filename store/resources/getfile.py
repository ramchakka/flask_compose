from flask_restful import Resource, request
from flask import current_app, send_from_directory, after_this_request
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.store import StoreModel
from schemas.store import StoreSchema
from models.item import ItemModel
from schemas.item import ItemSchema
from libs.strings import gettext
import logging
import traceback
import os

logger = logging.getLogger(__package__)
store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)
item_schema = ItemSchema()


class Getfile(Resource):
    @classmethod
    def get(cls, name: str):
        logger.debug(request)
        store = StoreModel.find_by_name(name)
        if store:
            itemname = request.args.get('itemname')
            if itemname is None or itemname  == '':
                return {"message": gettext("getfile_item_notfound")}, 404

            item = ItemModel.find_by_storeid_and_itemname(store.id,itemname)
            if item is None:
                return {"message": gettext("getfile_item_notfound")}, 404
            
            try:
                uploads = os.path.join( current_app.config['UPLOADED_IMAGES_DEST'], os.path.dirname(item.objname))
                return send_from_directory(directory=uploads, filename=os.path.basename(item.objname),attachment_filename=item.filename,as_attachment=True)
            except:
                traceback.print_exc()
                return {"message": gettext("getfile_file_notfound")}, 404

            return {"message": gettext("getfile_file_notfound")}, 404

        return {"message": gettext("getfile_store_notfound")}, 404




