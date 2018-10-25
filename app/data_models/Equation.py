from app import db

class Equation(db.Model):
    __tablename__ = "Equations"
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(45), nullable=False)
    Description = db.Column(db.String(21845))    
        
    def __repr__(self):
        return '<Equation {} {} {}>'.format(self.Id, self.Name, self.Description) 