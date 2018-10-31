from app import db
from app.data_models.AuditMixin import AuditMixin

class UploadSet(AuditMixin, db.Model):
    __tablename__ = "UploadSets"
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(45), nullable=False)
    CreatedDate = db.Column(db.DateTime, nullable=False)
    Description = db.Column(db.String(21845))
    UserId = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
    FileName = db.Column(db.String(45))
    StoredFileName = db.Column(db.String(45))
    Wells = db.relationship('Well', lazy='select', 
        cascade = 'all, delete-orphan',
        backref=db.backref('UploadSet', lazy='select'))

    def __repr__(self):
        return '<UploadSet {} {} {} {} {} {}>'.format(self.Id, self.Name, self.Description, self.CreatedDate, self.UserId, self.FileName)

    @property
    def serialize(self):
        return {
            'id': self.Id,
            'name': self.Name,
            'createdDate': self.CreatedDate.isoformat(),
            'description': self.Description,
            'fileName': self.FileName
        }


