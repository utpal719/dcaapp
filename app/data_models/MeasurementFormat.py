from app import db
from app.data_models.AuditMixin import AuditMixin
class MeasurementFormat(AuditMixin, db.Model):
    __tablename__ = "MeasurementFormats"
    WellId = db.Column(db.Integer, db.ForeignKey("Wells.Id"), primary_key=True, nullable=False)
    MeasurementTypeId = db.Column(db.String(45), db.ForeignKey("MeasurementTypes.Id"), primary_key=True, nullable=False)
    Format = db.Column(db.String(45), nullable=False)
        
    def __repr__(self):
        return '<MeasurementFormat {} {} {}>'.format(self.WellId, self.MeasurementTypeId, self.Format) 