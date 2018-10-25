from app import db

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