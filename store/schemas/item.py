from ma import ma
from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel

class ItemSchema(ma.ModelSchema):
    class Meta:
        model = ItemModel
        load_only = ("store","store_id","objname",)
        dump_only = ("id",)
        include_fk = True
