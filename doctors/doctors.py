from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

# Initialize App
app = Flask(__name__)
api = Api(app)

# Flask DB Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
                                        "mssql+pyodbc://admin:nkol6056@"
                                        "meditrackdb-sql.c1q2cm4givcj.us-east-1.rds.amazonaws.com:1433/meditrackDB?"
                                        "driver=ODBC+Driver+18+for+SQL+Server&"
                                        "Encrypt=yes&"
                                        "TrustServerCertificate=yes"
                                        )
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Database
db = SQLAlchemy(app)

# Define Doctor Model
class DoctorModel(db.Model):
    __tablename__  = 'doctors'
    __table_args__ = {'schema': 'doctor'}    

    doctor_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name  = db.Column(db.String(100), nullable=False)
    last_name   = db.Column(db.String(100), nullable=False)
    specialization  = db.Column(db.String(100))
    email           = db.Column(db.String(150), nullable=False, unique=True)
    phone           = db.Column(db.String(15))

# Doctor
class Doctor(Resource):

    # Retrieve doctors or search by email
    def get(self):
        try:        
            email = request.args.get("email")
            if email:
            # If email is provided in query parameters    
                doctor = DoctorModel.query.filter_by(email=email).first()
                if doctor:
                    return {
                        "doctor_id" : doctor.doctor_id,
                        "first_name": doctor.first_name,
                        "last_name" : doctor.last_name,
                        "specialization": doctor.specialization,
                        "email" : doctor.email,
                        "phone" : doctor.phone,
                    }, 200
                else:
                    return {"message": "Doctor not found."}, 404
            else:
            # If no email is provided, return all    
                doctors = DoctorModel.query.all()
                return [
                    {
                        "doctor_id" : doctor.doctor_id,
                        "first_name": doctor.first_name,
                        "last_name" : doctor.last_name,
                        "specialization": doctor.specialization,
                        "email" : doctor.email,
                        "phone" : doctor.phone,
                    }
                    for doctor in doctors
                ], 200
        except Exception as e:
            return {"error": str(e)}, 500

    
    def post(self):
    # Add a new doctor    
        try:
            data = request.json
            new_doctor = DoctorModel(
                first_name  = data["first_name"],
                last_name   = data["last_name"],
                specialization = data.get("specialization"),
                email       = data["email"],
                phone       = data.get("phone"),
            )
            db.session.add(new_doctor)
            db.session.commit()
            return {"message": "Doctor added successfully."}, 201
        except Exception as e:
            return {"error": str(e)}, 500

# Register the resource with an endpoint
api.add_resource(Doctor, "/doctors")

if __name__ == "__main__":
    # Create the tables in the database
    # with app.app_context():
    #    db.create_all()
    app.run(debug=True)
