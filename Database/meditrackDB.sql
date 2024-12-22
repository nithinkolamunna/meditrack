

-- Endpoint : meditrackdb-sql.c1q2cm4givcj.us-east-1.rds.amazonaws.com
-- port     : 1433
-- Database : meditrackDB
-- UN/PW    : admin/
-- ** Publicly accessible SET Yes
-- ** Edit Inblund ruless,
--		Add rules - MSSQL(Default port will pick, And set Source as well)
--app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://admin:nkol6056@meditrackdb-sql.c1q2cm4givcj.us-east-1.rds.amazonaws.com/meditrackDB?driver=ODBC+Driver+17+for+SQL+Server"


CREATE DATABASE meditrackDB;

USE meditrackDB


-- Table: patients
CREATE TABLE patients (
    patient_id INT IDENTITY(1,1) PRIMARY KEY, 
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(15),
    address TEXT,
    medical_history TEXT
);

-- Table: doctors
CREATE TABLE doctors (
    doctor_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100),
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(15)
);

-- Table: appointments
CREATE TABLE appointments (
    appointment_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    appointment_date DATETIME NOT NULL,
    status VARCHAR(50) DEFAULT 'IsScheduled',
    notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

-- Table: notifications
CREATE TABLE notifications (
    notification_id INT IDENTITY(1,1) PRIMARY KEY, 
    appointment_id INT NOT NULL,
    message TEXT NOT NULL,
    sent_at DATETIME,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
);




-- Alter Schema

CREATE SCHEMA [patient]
GO
CREATE SCHEMA [doctor]
GO
CREATE SCHEMA [common]
GO


ALTER SCHEMA patient TRANSFER dbo.patients;
GO
ALTER SCHEMA doctor TRANSFER dbo.doctors;
GO
ALTER SCHEMA common TRANSFER dbo.appointments;
GO
ALTER SCHEMA common TRANSFER dbo.notifications;

asd