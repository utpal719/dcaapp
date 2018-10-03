"""
from app import create_app

app = create_app()

"""

from app import create_app, db
from app.models import User, Dataset, Casedata

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Dataset': Dataset, 'Casedata': Casedata}