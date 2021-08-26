from IRDO import db
import datetime


class BaseModel(db.Model):
    __abstract__ = True
    # id = db.Column(db.Integer,
    #                primary_key=True,
    #                autoincrement=True)
    created_at = db.Column(db.DateTime(timezone=True), 
    default=lambda: datetime.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)
