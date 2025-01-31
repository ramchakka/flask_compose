from typing import List

from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=False)
    filename = db.Column(db.String(1024), nullable=True, unique=False,default=None)
    objname = db.Column(db.String(2048), nullable=True, unique=False,default=None)

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("StoreModel")

    @classmethod
    def find_by_name(cls, name: str) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id: int) -> "ItemModel":
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def find_by_storeid_and_itemname(cls, storeid:int, name: str) -> "ItemModel":
        return cls.query.filter_by(name=name,store_id=storeid).first()

    @classmethod
    def find_all(cls) -> List["ItemModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
