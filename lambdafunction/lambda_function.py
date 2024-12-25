import json
import boto3
import pyodbc
import psycopg2
from botocore.exceptions import NoCredentialsError

# AWS Redshift Serverless details
REDSHIFT_SERVERLESS_ENDPOINT = "default-workgroup.183295407444.us-east-1.redshift-serverless.amazonaws.com:5439/dev"
REDSHIFT_DATABASE = "meditrackdwh"
REDSHIFT_USER = "admin"
REDSHIFT_PASSWORD = "HWYUDcsypu075%*"

# RDS SQL Server details
RDS_SERVER = "meditrackdb-sql.c1q2cm4givcj.us-east-1.rds.amazonaws.com"
RDS_DATABASE = "meditrackdb-sql"
RDS_USER = "admin"
RDS_PASSWORD = "Pass1234"

# Connect to Redshift Serverless
def get_redshift_serverless_connection():
    conn_string = (
        f"dbname='{REDSHIFT_DATABASE}' user='{REDSHIFT_USER}' "
        f"password='{REDSHIFT_PASSWORD}' host='{REDSHIFT_SERVERLESS_ENDPOINT}' port=5439"
    )
    return psycopg2.connect(conn_string)

# Connect to RDS
rds_conn_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={RDS_SERVER};"
    f"DATABASE={RDS_DATABASE};UID={RDS_USER};PWD={RDS_PASSWORD}"
)
rds_conn = pyodbc.connect(rds_conn_string)

# Lambda handler
def lambda_handler(event, context):
    try:
        # appointment per doctor
        rds_cursor = rds_conn.cursor()
        appointment_metrics_query = """
            SELECT 
                d.doctor_id,
                d.specialization,
                CAST(a.appointment_date AS DATE) AS appointment_date,
                COUNT(a.appointment_id) AS appointment_count
            FROM common.appointments a
            INNER JOIN doctor.doctors d ON d.first_name + ' ' + d.last_name = a.doctor_name
            GROUP BY d.doctor_id, d.specialization, CAST(a.appointment_date AS DATE);
        """
        rds_cursor.execute(appointment_metrics_query)
        appointment_metrics = rds_cursor.fetchall()

        # symptom analysis
        symptom_analysis_query = """
            SELECT 
                d.doctor_id,
                LEFT(n.message, 100) AS symptom,  -- Extract relevant symptom data
                LEFT(n.message, 100) AS condition,
                COUNT(n.notification_id) AS treatment_count
            FROM common.notifications n
            INNER JOIN common.appointments a ON n.patient_email = a.patient_email
            INNER JOIN doctor.doctors d ON d.first_name + ' ' + d.last_name = a.doctor_name
            GROUP BY d.doctor_id, LEFT(n.message, 100);
        """
        rds_cursor.execute(symptom_analysis_query)
        symptom_analysis = rds_cursor.fetchall()

        # doctor performance all the time
        doctor_performance_query = """
            SELECT 
                d.doctor_id,
                d.specialization,
                COUNT(a.appointment_id) AS total_appointments
            FROM common.appointments a
            INNER JOIN doctor.doctors d ON d.first_name + ' ' + d.last_name = a.doctor_name
            WHERE a.status = 'Completed'
            GROUP BY d.doctor_id, d.specialization;
        """
        rds_cursor.execute(doctor_performance_query)
        doctor_performance = rds_cursor.fetchall()

        # Load data into Redshift Serverless
        redshift_conn = get_redshift_serverless_connection()
        redshift_cursor = redshift_conn.cursor()

        # Insert into appointment_metrics table
        redshift_cursor.execute("DELETE FROM appointment_metrics")  # Clear table
        for row in appointment_metrics:
            insert_query = """ 
                INSERT INTO appointment_metrics (doctor_id, specialization, appointment_date, appointment_count)
                VALUES (%s, %s, %s, %s);
                """
            redshift_cursor.execute(insert_query, row)

        # Insert into symptom_analysis table
        redshift_cursor.execute("DELETE FROM symptom_analysis")  # Clear table
        for row in symptom_analysis:
            insert_query = """
                INSERT INTO symptom_analysis (doctor_id, symptom, condition, treatment_count)
                VALUES (%s, %s, %s, %s);
                """
            redshift_cursor.execute(insert_query, row)

        # Insert into doctor_performance table
        redshift_cursor.execute("DELETE FROM doctor_performance")  # Clear table
        for row in doctor_performance:
            insert_query = """
                INSERT INTO doctor_performance (doctor_id, specialization, total_appointments, avg_consultation_time)
                VALUES (%s, %s, %s, %s);
                """
            redshift_cursor.execute(insert_query, row)

        redshift_conn.commit()
        redshift_cursor.close()
        rds_cursor.close()

        return {
            'statusCode': 200,
            'body': json.dumps('Data transfer completed successfully!')
        }

    except NoCredentialsError as e:
        print("Error: ", e)
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid AWS credentials')
        }
    except Exception as e:
        print("Error: ", e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error in data transfer')
        }