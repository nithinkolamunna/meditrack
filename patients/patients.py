from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_cors import CORS

# Initialize App
app = Flask(__name__)
api = Api(app)
CORS(app)

# Flask DB Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = (
                                        "mssql+pyodbc://admin:nkol6056@"
                                        "meditrackdb-sql.c1q2cm4givcj.us-east-1.rds.amazonaws.com:1433/meditrackDB?"
                                        "driver=ODBC+Driver+18+for+SQL+Server&"
                                        "Encrypt=yes&"
                                        "TrustServerCertificate=yes"
                                        )
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Initialize DatabaseDB
db = SQLAlchemy(app)

# define Patient Model
class PatientModel(db.Model):
    __tablename__  = 'patients'
    __table_args__ = {'schema': 'patient'}
            
    patient_id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name  = db.Column(db.String(100), nullable=False)
    last_name   = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email       = db.Column(db.String(100), unique=True, nullable=False)
    phone       = db.Column(db.String(10))
    address     = db.Column(db.Text)
    medical_history = db.Column(db.Text)


# Patient 
class Patient(Resource):

    def get(self):
    # Retrieve all patients or a specific patient by email
        try:
            email = request.args.get("email")
            if email:  
            # If email is provided in query parameters
                patient = PatientModel.query.filter_by(email=email).first()
                if patient:
                    return {
                        "patient_id"    : patient.patient_id,
                        "first_name"    : patient.first_name,
                        "last_name"     : patient.last_name,
                        "date_of_birth" : str(patient.date_of_birth),
                        "email"         : patient.email,
                        "phone"         : patient.phone,
                        "address"       : patient.address,
                        "medical_history": patient.medical_history,
                    }, 200
                else:
                    return {"message": "Patient not found."}, 404
            else:  
            # If no email is provided, return all patients
                patients = PatientModel.query.all()
                return [
                    {
                        "patient_id"    : patient.patient_id,
                        "first_name"    : patient.first_name,
                        "last_name"     : patient.last_name,
                        "date_of_birth" : str(patient.date_of_birth),
                        "email"         : patient.email,
                        "phone"         : patient.phone,
                        "address"       : patient.address,
                        "medical_history": patient.medical_history,
                    }
                    for patient in patients
                ], 200
        except Exception as e:
            return {"error": str(e)}, 500


    def post(self):
    # Add a new patient
        data        = request.json
        new_patient = PatientModel(
            first_name  = data["first_name"],
            last_name   =   data["last_name"],
            date_of_birth=data["date_of_birth"],
            email       = data["email"],
            phone       = data.get("phone"),
            address     = data.get("address"),
            medical_history=data.get("medical_history"),
        )
        db.session.add(new_patient)
        db.session.commit()
        return {"message": "Patient added successfully."}, 201


# Register the resource with an endpoint
api.add_resource(Patient, "/patients")

if __name__ == "__main__":
    # Create the tables in the database
    #with app.app_context():
    #    db.create_all()
    app.run(debug=True)
