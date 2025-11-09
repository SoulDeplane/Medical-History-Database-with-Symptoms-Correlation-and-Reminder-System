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

def get_all_patients(connection):
    """
    Retrieves all patients from the database.
    """
    cursor = connection.cursor()
    patients = []
    try:
        query = "SELECT PatientID, Name, Age, Gender, ContactInfo FROM Patient ORDER BY PatientID;"
        
        cursor.execute(query)
        patients = cursor.fetchall()
        print(f" Found {len(patients)} patient(s).")
        
    except Exception as e:
        print(f" The error '{e}' occurred")
    finally:
        cursor.close()
    return patients

def delete_patient(connection, patient_id):
    """
    Deletes a patient from the database.
    Note: This will fail if there are foreign key constraints (symptoms, medications, etc.)
    """
    cursor = connection.cursor()
    success = False
    try:
        query = "DELETE FROM Patient WHERE PatientID = %s;"
        
        cursor.execute(query, (patient_id,))
        connection.commit()
        if cursor.rowcount > 0:
            success = True
            print(f" Patient with ID {patient_id} deleted successfully.")
        else:
            print(f" No patient found with ID {patient_id}.")
        
    except Exception as e:
        print(f" The error '{e}' occurred")
        connection.rollback()
    finally:
        cursor.close()
    return success

def find_symptom_correlation(connection, symptom_description):
    """
    Finds patients who have a specific symptom and returns their names and symptoms.
    """
    cursor = connection.cursor()
    correlations = []
    try:
        query = """
        SELECT p.Name, s.Description
        FROM Patient p
        INNER JOIN Symptom s ON p.PatientID = s.PatientID
        WHERE LOWER(s.Description) LIKE LOWER(%s)
        ORDER BY p.Name;
        """
        
        cursor.execute(query, (f'%{symptom_description}%',))
        correlations = cursor.fetchall()
        print(f" Found {len(correlations)} correlation(s) for symptom '{symptom_description}'.")
        
    except Exception as e:
        print(f" The error '{e}' occurred")
    finally:
        cursor.close()
    return correlations

def get_all_symptoms(connection):
    """
    Retrieves all symptoms with patient information.
    """
    cursor = connection.cursor()
    symptoms = []
    try:
        query = """
        SELECT s.SymptomID, s.PatientID, p.Name, s.Description, s.Severity, s.Duration, s.ReportDate
        FROM Symptom s
        INNER JOIN Patient p ON s.PatientID = p.PatientID
        ORDER BY s.ReportDate DESC;
        """
        
        cursor.execute(query)
        symptoms = cursor.fetchall()
        print(f" Found {len(symptoms)} symptom(s).")
        
    except Exception as e:
        print(f" The error '{e}' occurred")
    finally:
        cursor.close()
    return symptoms

def get_all_medications(connection):
    """
    Retrieves all medications with patient information.
    """
    cursor = connection.cursor()
    medications = []
    try:
        query = """
        SELECT m.MedicationID, m.PatientID, p.Name, m.Name, m.Dosage, m.Frequency, m.StartDate, m.EndDate
        FROM Medication m
        INNER JOIN Patient p ON m.PatientID = p.PatientID
        ORDER BY m.StartDate DESC;
        """
        
        cursor.execute(query)
        medications = cursor.fetchall()
        print(f" Found {len(medications)} medication(s).")
        
    except Exception as e:
        print(f" The error '{e}' occurred")
    finally:
        cursor.close()
    return medications

def add_vitals(connection, patient_id, systolic_bp=None, diastolic_bp=None, heart_rate=None, 
               temperature=None, oxygen_saturation=None, respiratory_rate=None, 
               weight=None, blood_glucose=None, notes=None):
    """
    Adds vital signs for a specific patient.
    """
    cursor = connection.cursor()
    try:
        query = """
        INSERT INTO Vitals (PatientID, SystolicBP, DiastolicBP, HeartRate, Temperature, 
                           OxygenSaturation, RespiratoryRate, Weight, BloodGlucose, Notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        vital_data = (patient_id, systolic_bp, diastolic_bp, heart_rate, temperature,
                     oxygen_saturation, respiratory_rate, weight, blood_glucose, notes)
        
        cursor.execute(query, vital_data)
        connection.commit()
        print(f" Vitals added successfully for patient ID {patient_id}.")
        
    except Exception as e:
        print(f" The error '{e}' occurred")
        # Rollback the transaction to clear the error state
        try:
            connection.rollback()
        except:
            pass
    finally:
        cursor.close()

def get_all_vitals(connection):
    """
    Retrieves all vitals with patient information.
    """
    cursor = connection.cursor()
    vitals = []
    try:
        query = """
        SELECT v.VitalID, v.PatientID, p.Name, v.RecordedAt, v.SystolicBP, v.DiastolicBP, 
               v.HeartRate, v.Temperature, v.OxygenSaturation, v.RespiratoryRate, 
               v.Weight, v.BloodGlucose, v.Notes
        FROM Vitals v
        INNER JOIN Patient p ON v.PatientID = p.PatientID
        ORDER BY v.RecordedAt DESC;
        """
        
        cursor.execute(query)
        vitals = cursor.fetchall()
        print(f" Found {len(vitals)} vital record(s).")
        
    except Exception as e:
        print(f" The error '{e}' occurred")
        # Rollback the transaction to clear the error state
        try:
            connection.rollback()
        except:
            pass
    finally:
        cursor.close()
    return vitals

def get_patient_vitals(connection, patient_id):
    """
    Retrieves all vitals for a specific patient.
    """
    cursor = connection.cursor()
    vitals = []
    try:
        query = """
        SELECT VitalID, RecordedAt, SystolicBP, DiastolicBP, HeartRate, Temperature, 
               OxygenSaturation, RespiratoryRate, Weight, BloodGlucose, Notes
        FROM Vitals
        WHERE PatientID = %s
        ORDER BY RecordedAt DESC;
        """
        
        cursor.execute(query, (patient_id,))
        vitals = cursor.fetchall()
        print(f" Found {len(vitals)} vital record(s) for patient ID {patient_id}.")
        
    except Exception as e:
        print(f" The error '{e}' occurred")
    finally:
        cursor.close()
    return vitals

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