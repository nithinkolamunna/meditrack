
-- Create the appointment_metrics table
CREATE TABLE "public"."appointment_metrics"(
    "doctor_id" INTEGER NULL,
    "specialization" VARCHAR(100) NULL,
    "appointment_date" DATE NULL,
    "appointment_count" INTEGER NULL
) ENCODE AUTO;


CREATE TABLE "public"."symptom_analysis"(
    "doctor_id" INTEGER NULL,
    "symptom" VARCHAR(100) NULL,
    "condition" VARCHAR(100) NULL,
    "treatment_count" INTEGER NULL
) ENCODE AUTO;


CREATE TABLE "public"."doctor_performance"(
    "doctor_id" INTEGER NULL,
    "specialization" VARCHAR(100) NULL,
    "total_appointments" INTEGER NULL,
    "avg_consultation_time" FLOAT NULL
) ENCODE AUTO;
