from app import db
from sqlalchemy.ext.declarative import declared_attr
from flask import g
import datetime

class AuditMixin(object):
    IsDeleted = db.Column(db.Boolean, nullable=False, default=False)
    CreatedOn = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)
    ModifiedOn = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)
    
    @declared_attr
    def CreatedById(cls):
        return db.Column(db.Integer, 
            db.ForeignKey("Users.id"), 
            default=cls.get_user_id, 
            nullable=True)

    
    @declared_attr
    def ModifiedById(cls):
        return db.Column(db.Integer, 
            db.ForeignKey("Users.id"), 
            default=cls.get_user_id, 
            nullable=True)

    @declared_attr
    def CreatedBy(cls):
        return db.relationship('User', 
            primaryjoin='%s.CreatedById == User.id' % cls.__name__, 
            enable_typechecks=False)


    @declared_attr
    def ModifiedBy(cls):
        return db.relationship('User', 
            primaryjoin='%s.ModifiedById == User.id' % cls.__name__, 
            enable_typechecks=False)
                        
                        

    @classmethod
    def get_user_id(cls):
        try:
            return g.current_user.id
        except Exception as e:
            return None