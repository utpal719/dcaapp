from app import db

class MeasurementType(db.Model):
    __tablename__ = "MeasurementTypes"
    Id = db.Column(db.String(45), primary_key=True)
        
    def __repr__(self):
        return '<MeasurementType {}>'.format(self.Id) 