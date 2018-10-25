from app import db

class IDCAResult(db.Model):
    __tablename__ = "IDCAResults"
    Id = db.Column(db.Integer, primary_key=True)
    IDCAnalysisId = db.Column(db.Integer, db.ForeignKey("IDCAnalysis.Id"), nullable=False)
    StartSegment = db.Column(db.Integer, nullable=False)
    EndSegment = db.Column(db.Integer, nullable=False)
    EquationId = db.Column(db.Integer, db.ForeignKey("Equations.Id"), nullable=False)
    ParameterA = db.Column(db.Float, nullable=False)
    ParameterB = db.Column(db.Float, nullable=False)
        
    def __repr__(self):
        return '<IDCAResult {} {} {}>'.format(self.Id, self.IDCAnalysisId, self.EquationId) 