import os

basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    #MYSQL_DATABASE_USER = 'root'
    #MYSQL_DATABASE_PASSWORD = 'admin'
    #MYSQL_DATABASE_DB = 'dcaapp'
    #MYSQL_DATABASE_HOST = 'localhost'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, os.environ.get('UPLOAD_FOLDER'))
    TOKEN_EXPIRATION_TIME = os.environ.get('TOKEN_EXPIRATION_TIME', 3600)