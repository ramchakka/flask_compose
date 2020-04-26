""" Get encrypted file"""
from flask_restful import Resource, request
from flask import current_app, send_from_directory, after_this_request
from flask_jwt_extended import jwt_required, fresh_jwt_required
from models.store import StoreModel
from schemas.store import StoreSchema

from models.item import ItemModel
from schemas.item import ItemSchema

import traceback
import os
from commons.pycrypto_file import encrypt_file
from tempfile import mkstemp

NAME_ALREADY_EXISTS = "A store with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the store."
STORE_NOT_FOUND = "Store not found."
ITEM_NOT_FOUND = "Item not found."
FILE_NOT_FOUND = "File not found."
STORE_DELETED = "Store deleted."

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)
item_schema = ItemSchema()


class GetEncodedFile(Resource):
    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            
            itemname = request.args.get('itemname')
            if itemname is None or itemname  == '':
                return {"message": ITEM_NOT_FOUND}, 404

            item = ItemModel.find_by_storeid_and_itemname(store.id,itemname)
            if item is None:
                return {"message": ITEM_NOT_FOUND}, 404
            
            try:
                uploads = os.path.join( current_app.config['UPLOADED_IMAGES_DEST'], os.path.dirname(item.objname))
                
                key = b'1' * 32
                print('key=',key)
                uploads = os.path.join( current_app.config['UPLOADED_IMAGES_DEST'])
                #out_filename=encrypt_file(key,os.path.basename(item.objname))
                #out_filename=encrypt_file(key,os.path.join(uploads,item.objname))
                _, temp_path = mkstemp()
                out_filename=encrypt_file_orig(key,os.path.join(uploads,item.objname),out_filename=temp_path)
                print('out_filename=',out_filename)
                print('dirname=',os.path.dirname(out_filename))
                print('basename=',os.path.basename(out_filename))

                @after_this_request
                def cleanup(response):
                    print('===cleanup called===')
                    print(out_filename)
                    if out_filename:
                        os.remove(out_filename)
                    return response
                #return send_from_directory(directory=uploads, filename=os.path.basename(item.objname),attachment_filename=item.filename,as_attachment=True)
                return send_from_directory(directory=os.path.dirname(out_filename), filename=os.path.basename(out_filename),attachment_filename=item.filename+'.enc',as_attachment=True)
            except:
                traceback.print_exc()
                return {"message": FILE_NOT_FOUND}, 404

            return item_schema.dump(item), 200



        return {"message": STORE_NOT_FOUND}, 404




