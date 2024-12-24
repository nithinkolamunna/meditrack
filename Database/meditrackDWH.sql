-- Create the appointment_metrics table
CREATE TABLE appointment_metrics (
    doctor_id INT NOT NULL,
    specialization VARCHAR(100),
    appointment_date DATE,
    appointment_count INT
);

-- Create the symptom_analysis table
CREATE TABLE symptom_analysis (
    doctor_id INT NOT NULL,
    symptom VARCHAR(100),
    condition VARCHAR(100),
    treatment_count INT
);

-- Create the doctor_performance table
CREATE TABLE doctor_performance (
    doctor_id INT NOT NULL,
    specialization VARCHAR(100),
    total_appointments INT,
    avg_consultation_time FLOAT
);
