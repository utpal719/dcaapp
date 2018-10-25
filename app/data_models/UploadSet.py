from app import db

class UploadSet(db.Model):
    __tablename__ = "UploadSets"
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(45), nullable=False)
    CreatedDate = db.Column(db.DateTime, nullable=False)
    Description = db.Column(db.String(21845))
    UserId = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
    
    def __repr__(self):
        return '<UploadSet {} {} {} {} {}>'.format(self.Id, self.Name, self.Description, self.CreatedDate, self.UserId) 