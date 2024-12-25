

-- Endpoint : meditrackdb-sql.c1q2cm4givcj.us-east-1.rds.amazonaws.com
-- port     : 1433
-- Database : meditrackDB
-- UN/PW    : admin/pass1234
-- ** Publicly accessible SET Yes
-- ** Edit Inblund ruless,
--		Add rules - MSSQL(Default port will pick, And set Source as well)
--app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://admin:nkol6056@meditrackdb-sql.c1q2cm4givcj.us-east-1.rds.amazonaws.com/meditrackDB?driver=ODBC+Driver+17+for+SQL+Server"


CREATE DATABASE meditrackDB;

USE meditrackDB


CREATE SCHEMA [patient]
GO
CREATE SCHEMA [doctor]
GO
CREATE SCHEMA [common]
GO


-- Table: patients
CREATE TABLE patient.patients (
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
CREATE TABLE doctor.doctors (
    doctor_id INT IDENTITY(1,1) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    specialization VARCHAR(100),
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(15)
);

-- Table: appointments
CREATE TABLE common.appointments (
    appointment_id INT IDENTITY(1,1) PRIMARY KEY,
    patient_email VARCHAR(100) NOT NULL,
    doctor_name VARCHAR(100) NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME(7) NOT NULL,
    status VARCHAR(50) DEFAULT 'IsScheduled'
);

-- Table: notifications
CREATE TABLE common.notifications (
    notification_id INT IDENTITY(1,1) PRIMARY KEY, 
    patient_email VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    sent_at DATETIME,
    status VARCHAR(50)
);