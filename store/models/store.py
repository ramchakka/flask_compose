from typing import List

from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    username = db.Column(db.String, db.ForeignKey("users.username"), nullable=True)
    user = db.relationship("UserModel",back_populates="store")

    items = db.relationship("ItemModel", lazy="dynamic")

    @classmethod
    def find_by_name(cls, name: str) -> "StoreModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_username(cls, username: str) -> "StoreModel":
        return cls.query.filter_by(username=username)

    @classmethod
    def find_by_id(cls, id: int) -> "StoreModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls) -> List["StoreModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
