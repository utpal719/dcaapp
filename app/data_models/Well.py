from app import db
from app.data_models.AuditMixin import AuditMixin

class Well(AuditMixin, db.Model):
    __tablename__ = "Wells"
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(45), nullable=False)
    Latitude = db.Column(db.Numeric(precision=11, scale=8, asdecimal=True))
    Longitude = db.Column(db.Numeric(precision=11, scale=8, asdecimal=True))
    UserId = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
    UploadSetId = db.Column(db.Integer, db.ForeignKey("UploadSets.Id"), nullable=True)
    PerforationTopDepth = db.Column(db.Float)
    PerforationBottomDepth = db.Column(db.Float)
    WellIOMeasurements = db.relationship('WellOutputMeasurement', lazy='select', 
        cascade = 'all, delete-orphan',
        backref=db.backref('Well', lazy='select'))
    MeasurementFormats = db.relationship('MeasurementFormat', lazy='select', 
        cascade = 'all, delete-orphan',
        backref=db.backref('Well', lazy='select'))

    
    def __repr__(self):
        return '<Well {} {} {} {}>'.format(self.Id, self.Name, self.UserId, self.UploadSetId) 


