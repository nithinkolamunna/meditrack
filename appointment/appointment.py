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

# Define Appointment Model
class AppointmentModel(db.Model):
    __tablename__  = 'appointments'
    __table_args__ = {'schema': 'common'}    

    appointment_id   = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_email    = db.Column(db.String(100), nullable=False)
    doctor_name      = db.Column(db.String(100), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    status           = db.Column(db.String(50), nullable=False, default="Scheduled")


# Appointment
class Appointment(Resource):

    def get(self):
    # Retrieve appointments by patient email or list all appointments.
        try:
            email = request.args.get("email")
            if email:
            # If email is provided in query parameters
                appointments = AppointmentModel.query.filter_by(patient_email=email).first()
                if not appointments:
                    return {"message": "No appointments found for the provided email."}, 404

                return [
                    {
                        "appointment_id": app.appointment_id,
                        "patient_email" : app.patient_email,
                        "doctor_name"   : app.doctor_name,
                        "appointment_date": str(app.appointment_date),
                        "appointment_time": str(app.appointment_time),
                        "status"        : app.status,
                    }
                    for app in appointments
                ], 200
            else:
            # If no email is provided, return all
                appointments = AppointmentModel.query.all()
                return [
                    {
                        "appointment_id": app.appointment_id,
                        "patient_email" : app.patient_email,
                        "doctor_name"   : app.doctor_name,
                        "appointment_date": str(app.appointment_date),
                        "appointment_time": str(app.appointment_time),
                        "status"        : app.status,
                    }
                    for app in appointments
                ], 200
        except Exception as e:
            return {"error": str(e)}, 500


    def post(self):
        # Schedule a new appointment
        try:
            data = request.json
            new_appointment     = AppointmentModel(
                patient_email   = data["patient_email"],
                doctor_name     = data["doctor_name"],
                appointment_date= data["appointment_date"],
                appointment_time= data["appointment_time"],
                status          = data.get("status", "Scheduled"),
            )
            db.session.add(new_appointment)
            db.session.commit()
            return {"message": "Appointment scheduled successfully."}, 201
        except Exception as e:
            return {"error": str(e)}, 500


# Register the resource with an endpoint
api.add_resource(Appointment, "/appointments")

if __name__ == "__main__":
    # Create the tables in the database
    # with app.app_context():
    #    db.create_all()
    app.run(debug=True)
