from app import db
from app.data_models.AuditMixin import AuditMixin

class WellOutputMeasurement(AuditMixin, db.Model):
    __tablename__ = "WellOutputMeasurements"
    Id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.DateTime, nullable=False)
    WellId = db.Column(db.Integer, db.ForeignKey("Wells.Id"), nullable=False)
    MeasurementTypeId = db.Column(db.String(45), db.ForeignKey("MeasurementTypes.Id"), nullable=False)
    Value = db.Column(db.Float)
    
    def __repr__(self):
        return '<WellOutputMeasurement {} {} {} {} {}>'.format(self.Id, self.Date, self.WellId, self.MeasurementTypeId, self.Value) 