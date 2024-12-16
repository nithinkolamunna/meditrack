from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from datetime import datetime

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

# Define Notification Model
class NotificationModel(db.Model):
    __tablename__  = 'notifications'
    __table_args__ = {'schema': 'common'}

    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_email   = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status  = db.Column(db.String(50), nullable=False, default="Pending")

# Notification
class Notification(Resource):

    def get(self):
    # Retrieve notifications for a patient by email or list all notifications    
        try:
            email = request.args.get("email")
            if email:
            # If email is provided in query parameters
                notifications = NotificationModel.query.filter_by(patient_email=email).first()
                if not notifications:
                    return {"message": "No notifications found for the provided email."}, 404
                return [
                    {
                        "notification_id": note.notification_id,
                        "patient_email"  : note.patient_email,
                        "message"   : note.message,
                        "sent_at"   : note.sent_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "status"    : note.status,
                    }
                    for note in notifications
                ], 200
            else:
            # If no email is provided, return all
                notifications = NotificationModel.query.all()
                return [
                    {
                        "notification_id": notifi.notification_id,
                        "patient_email"  : notifi.patient_email,
                        "message"   : notifi.message,
                        "sent_at"   : notifi.sent_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "status"    : notifi.status,
                    }
                    for notifi in notifications
                ], 200
        except Exception as e:
            return {"error": str(e)}, 500

    def post(self):
        # Create a new notification
        try:
            data = request.json
            new_notification = NotificationModel(
                patient_email= data["patient_email"],
                message      = data["message"],
                sent_at      = datetime.strptime(data["sent_at"], "%Y-%m-%d %H:%M:%S"),
                status       = data.get("status", "Pending"),
            )
            db.session.add(new_notification)
            db.session.commit()
            return {"message": "Notification created successfully."}, 201
        except Exception as e:
            return {"error": str(e)}, 500


# Register the resource with an endpoint
api.add_resource(Notification, "/notifications")

if __name__ == "__main__":
    # Create the tables in the database
    # with app.app_context():
    #    db.create_all()
    app.run(debug=True)
