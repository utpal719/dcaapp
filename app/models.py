import os
import base64
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import current_app
from datetime import datetime, timedelta



# class Dataset(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     well = db.Column(db.String(64), index=True)
#     date = db.Column(db.String(15))
#     prod = db.Column(db.Float)
#     WATER_PROD = db.Column(db.Float)
#     GWG_PROD = db.Column(db.Float)
#     CO2_PROD = db.Column(db.Float)
#     WATER_INJ = db.Column(db.Float)
#     CO2_INJ = db.Column(db.Float)
#     year = db.Column(db.Integer)
#     month = db.Column(db.Integer)
#     user = db.Column(db.String(64), index=True)
#     datasetname = db.Column(db.String(64), index=True)
    
#     def __repr__(self):
#         return '<Dataset {} {} {}>'.format(self.well, self.prod, self.date) 



@login.user_loader
def load_user(id):
    return User.query.get(int(id))

