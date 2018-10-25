"""
from app import create_app

app = create_app()

"""

from app import create_app, db
from app.data_models import *

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Casedata': Casedata}