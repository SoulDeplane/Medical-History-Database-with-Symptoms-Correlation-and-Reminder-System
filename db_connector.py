import psycopg2
from psycopg2 import OperationalError
from datetime import date

def create_db_connection():
    """ Creates and returns a connection to the PostgreSQL database. """
    connection = None
    try:
        connection = psycopg2.connect(
            database="Medical_history_db",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        print(" PostgreSQL Database connection successful")
    except OperationalError as e:
        print(f" The error '{e}' occurred")
    return connection

def add_patient(connection, name, age, gender, contact_info):
    """
    Adds a new patient to the Patient table and returns the new patient's ID.
    """
    cursor = connection.cursor()
    new_patient_id = None
    try:
        query = """
        INSERT INTO Patient (Name, Age, Gender, ContactInfo) 
        VALUES (%s, %s, %s, %s) RETURNING PatientID;
        """
        patient_data = (name, age, gender, contact_info)
        
        cursor.execute(query, patient_data)
        new_patient_id = cursor.fetchone()[0] # Fetch the returned ID
        connection.commit()
        print(f"Patient '{name}' added successfully with ID {new_patient_id}.")
        
    except Exception as e:
        print(f" The error '{e}' occurred")
    finally:
        cursor.close()
        return new_patient_id

def add_symptom(connection, patient_id, description, severity, duration):
    """
    Adds a new symptom for a specific patient.
    """
    cursor = connection.cursor()
    try:
        query = """
        INSERT INTO Symptom (PatientID, Description, Severity, Duration)
        VALUES (%s, %s, %s, %s);
        """
        symptom_data = (patient_id, description, severity, duration)
        
        cursor.execute(query, symptom_data)
        connection.commit()
        print(f" Symptom '{description}' added successfully for patient ID {patient_id}.")
        
    except Exception as e:
        print(f" The error '{e}' occurred")
    finally:
        cursor.close()

def add_medication(connection, patient_id, name, dosage, frequency, start_date, end_date=None):
    """
    Adds a new medication for a specific patient. end_date is optional.
    """
    cursor = connection.cursor()
    try:
        query = """
        INSERT INTO Medication (PatientID, Name, Dosage, Frequency, StartDate, EndDate)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        medication_data = (patient_id, name, dosage, frequency, start_date, end_date)
        
        cursor.execute(query, medication_data)
        connection.commit()
        print(f" Medication '{name}' added successfully for patient ID {patient_id}.")
        
    except Exception as e:
        print(f" The error '{e}' occurred")
    finally:
        cursor.close()

def get_patient_symptoms(connection, patient_id):
    """
    Retrieves all symptoms for a specific patient.
    """
    cursor = connection.cursor()
    symptoms = []
    try:
        query = "SELECT Description, Severity, Duration, ReportDate FROM Symptom WHERE PatientID = %s;"
        
        cursor.execute(query, (patient_id,))
        symptoms = cursor.fetchall()
        print(f" Found {len(symptoms)} symptom(s) for patient ID {patient_id}.")
        
    except Exception as e:
        print(f" The error '{e}' occurred")
    finally:
        cursor.close()
        return symptoms

# --- Main Testing Block ---
if __name__ == '__main__':
    conn = create_db_connection()

    if conn:
        print("\n--- Running Database Test Workflow ---")
        
        # Action 1: Add a new patient and get their ID.
        patient_id = add_patient(conn, 'Alice Johnson', 28, 'Female', '555-1122')
        
        # This check ensures we only proceed if the patient was added successfully.
        if patient_id:
            # Action 2: Add a symptom for the new patient using the returned ID.
            add_symptom(conn, patient_id, 'Sore Throat', 5, '2 days')

            # Action 3: Add a medication for the same patient.
            add_medication(conn, patient_id, 'Lozenges', '1 every 4 hours', 'As needed', date.today())
            
            # Action 4: Get and print all symptoms for that patient to verify.
            all_symptoms = get_patient_symptoms(conn, patient_id)
            if all_symptoms:
                print(f"\n--- Symptoms Report for Patient ID {patient_id} ---")
                for symptom in all_symptoms:
                    print(f"  - Description: {symptom[0]}, Severity: {symptom[1]}")

        # Finally, close the connection
        conn.close()
        print("\n PostgreSQL connection is closed.")