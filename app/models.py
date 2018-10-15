import os
import base64
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask import current_app
from datetime import datetime, timedelta

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    well = db.Column(db.String(64), index=True)
    date = db.Column(db.String(15))
    prod = db.Column(db.Float)
    WATER_PROD = db.Column(db.Float)
    GWG_PROD = db.Column(db.Float)
    CO2_PROD = db.Column(db.Float)
    WATER_INJ = db.Column(db.Float)
    CO2_INJ = db.Column(db.Float)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    user = db.Column(db.String(64), index=True)
    datasetname = db.Column(db.String(64), index=True)
    
    def __repr__(self):
        return '<Dataset {} {} {}>'.format(self.well, self.prod, self.date) 

class Proddata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wellid = db.Column(db.String(64), index=True, nullable=False)
    atttype = db.Column(db.String(64), nullable=False)
    attvalue = db.Column(db.Float)
    readdate = db.Column(db.DateTime, nullable=False)
    datasetid = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Proddata {} {} {} {} {}>'.format(self.wellid, self.atttype, self.attvalue, self.readdate, self.datasetid) 

class Casedata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    well = db.Column(db.String(64), index=True)
    readdate = db.Column(db.String(15))
    oilrate = db.Column(db.Float)
    waterrate = db.Column(db.Float)
    gasrate = db.Column(db.Float)
    #CO2_PROD = db.Column(db.Float)
    #WATER_INJ = db.Column(db.Float)
    #CO2_INJ = db.Column(db.Float)
    user = db.Column(db.String(64), index=True)
    datasetname = db.Column(db.String(64))
    
    def __repr__(self):
        return '<Casedata {} {} {} {} {}>'.format(self.AUTOMATION_NAME, self.OIL_PROD, self.BOOK_DATE, self.user, self.datasetname) 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return '<User {}>'.format(self.username) 

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        print("getting token")
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        db.session.commit()
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

@login.user_loader
def load_user(id):
    return User.query.get(int(id))