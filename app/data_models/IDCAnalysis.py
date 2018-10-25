from app import db

class IDCAnalysis(db.Model):
    __tablename__ = "IDCAnalysis"
    Id = db.Column(db.Integer, primary_key=True)
    WellId = db.Column(db.Integer, db.ForeignKey("Wells.Id"), nullable=False)
    Date = db.Column(db.DateTime, nullable=False)
    TotalError = db.Column(db.Float)
    PredictedProduction = db.Column(db.Float)
    ActualProduction = db.Column(db.Float)
    Difference = db.Column(db.Float)
        
    def __repr__(self):
        return '<IDCAnalysis {} {} {}>'.format(self.Id, self.WellId, self.Date) 