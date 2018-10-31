from app import db
#from sqlalchemy.ext.declarative import declared_attr

class AuditMixin(object):
    IsDeleted = db.Column(db.Boolean, nullable=False, default=False)
    CreatedOn = db.Column(db.DateTime, nullable=True)
    CreatedBy = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=True)
    ModifiedOn = db.Column(db.DateTime, nullable=True)
    ModifiedBy = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=True)