from app import db
from app.data_models.MeasurementType import MeasurementType
from app.data_models.User import User

def seed_measurement_types():
    db.session.add(MeasurementType(Id="oil_production"))
    db.session.add(MeasurementType(Id="water_production"))
    db.session.add(MeasurementType(Id="gas_production"))
    db.session.add(MeasurementType(Id="co2_production"))
    db.session.add(MeasurementType(Id="water_injection"))
    db.session.add(MeasurementType(Id="co2_injection"))
    
    try:
        db.session.commit()
        print("commit sucessfull - MeasurementTypes - 6 rows inserted")
    except Exception as exIdentifier:
        print(exIdentifier)

def seed_user():
    user = User(username = "admin", email="admin@admin.com")
    user.set_password("admin")
    db.session.add(user)
    db.session.commit()

def seed_all():
    seed_measurement_types()
    seed_user()
    
