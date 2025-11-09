from flask import Flask, render_template, request, redirect, url_for
from db_connector import (
    create_db_connection, 
    add_patient, 
    get_all_patients, 
    delete_patient,
    find_symptom_correlation,
    add_symptom,
    get_all_symptoms,
    add_medication,
    get_all_medications,
    add_vitals,
    get_all_vitals
)

app = Flask(__name__)

# Global connection - in production, use connection pooling
connection = None

def get_connection():
    """Gets or creates a database connection."""
    global connection
    try:
        if connection is None:
            connection = create_db_connection()
        # Check if connection is still valid
        elif hasattr(connection, 'closed') and connection.closed:
            connection = create_db_connection()
        else:
            # Check if connection is in an aborted transaction state
            # Try a simple query to test the connection
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
            except Exception:
                # Connection is in bad state, rollback and create new connection
                try:
                    connection.rollback()
                except:
                    pass
                connection = create_db_connection()
    except:
        connection = create_db_connection()
    return connection

@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@app.route('/patients')
def patients():
    """Display all patients."""
    conn = get_connection()
    if not conn:
        return render_template('patients.html', patients=[], error="Database connection failed")
    
    patients_list = get_all_patients(conn)
    return render_template('patients.html', patients=patients_list)

@app.route('/add_patient', methods=['POST'])
def add_patient_route():
    """Add a new patient."""
    conn = get_connection()
    if not conn:
        return redirect(url_for('patients'))
    
    name = request.form.get('name')
    age = int(request.form.get('age'))
    gender = request.form.get('gender')
    contact = request.form.get('contact')
    
    add_patient(conn, name, age, gender, contact)
    return redirect(url_for('patients'))

@app.route('/delete_patient/<int:patient_id>')
def delete_patient_route(patient_id):
    """Delete a patient."""
    conn = get_connection()
    if conn:
        delete_patient(conn, patient_id)
    return redirect(url_for('patients'))

@app.route('/symptoms_manage')
def symptoms_manage():
    """Display all symptoms."""
    conn = get_connection()
    if not conn:
        return render_template('symptoms_manage.html', symptoms=[], error="Database connection failed")
    
    symptoms_list = get_all_symptoms(conn)
    return render_template('symptoms_manage.html', symptoms=symptoms_list)

@app.route('/add_symptom', methods=['POST'])
def add_symptom_route():
    """Add a new symptom."""
    conn = get_connection()
    if not conn:
        return redirect(url_for('symptoms_manage'))
    
    try:
        patient_id = int(request.form.get('patient_id'))
        description = request.form.get('description')
        severity = int(request.form.get('severity'))
        duration = request.form.get('duration')
        
        add_symptom(conn, patient_id, description, severity, duration)
    except ValueError:
        pass  # Handle error silently or add flash message
    
    return redirect(url_for('symptoms_manage'))

@app.route('/medications_manage')
def medications_manage():
    """Display all medications."""
    conn = get_connection()
    if not conn:
        return render_template('medications_manage.html', medications=[], error="Database connection failed")
    
    medications_list = get_all_medications(conn)
    return render_template('medications_manage.html', medications=medications_list)

@app.route('/add_medication', methods=['POST'])
def add_medication_route():
    """Add a new medication."""
    conn = get_connection()
    if not conn:
        return redirect(url_for('medications_manage'))
    
    try:
        patient_id = int(request.form.get('patient_id'))
        name = request.form.get('name')
        dosage = request.form.get('dosage')
        frequency = request.form.get('frequency')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date') if request.form.get('end_date') else None
        
        add_medication(conn, patient_id, name, dosage, frequency, start_date, end_date)
    except ValueError:
        pass  # Handle error silently or add flash message
    
    return redirect(url_for('medications_manage'))

@app.route('/vitals_manage')
def vitals_manage():
    """Display all vitals."""
    conn = get_connection()
    if not conn:
        return render_template('vitals_manage.html', vitals=[], error="Database connection failed")
    
    vitals_list = get_all_vitals(conn)
    return render_template('vitals_manage.html', vitals=vitals_list)

@app.route('/add_vitals', methods=['POST'])
def add_vitals_route():
    """Add new vital signs."""
    conn = get_connection()
    if not conn:
        return redirect(url_for('vitals_manage'))
    
    try:
        patient_id = int(request.form.get('patient_id'))
        systolic_bp = int(request.form.get('systolic_bp')) if request.form.get('systolic_bp') else None
        diastolic_bp = int(request.form.get('diastolic_bp')) if request.form.get('diastolic_bp') else None
        heart_rate = int(request.form.get('heart_rate')) if request.form.get('heart_rate') else None
        temperature = float(request.form.get('temperature')) if request.form.get('temperature') else None
        oxygen_saturation = float(request.form.get('oxygen_saturation')) if request.form.get('oxygen_saturation') else None
        respiratory_rate = int(request.form.get('respiratory_rate')) if request.form.get('respiratory_rate') else None
        weight = float(request.form.get('weight')) if request.form.get('weight') else None
        blood_glucose = float(request.form.get('blood_glucose')) if request.form.get('blood_glucose') else None
        notes = request.form.get('notes') if request.form.get('notes') else None
        
        add_vitals(conn, patient_id, systolic_bp, diastolic_bp, heart_rate, 
                  temperature, oxygen_saturation, respiratory_rate, weight, 
                  blood_glucose, notes)
    except (ValueError, TypeError):
        pass  # Handle error silently or add flash message
    
    return redirect(url_for('vitals_manage'))

@app.route('/symptoms', methods=['GET', 'POST'])
def symptoms():
    """Display symptom correlation search."""
    correlation = None
    
    if request.method == 'POST':
        conn = get_connection()
        if conn:
            symptom = request.form.get('symptom')
            if symptom:
                correlation = find_symptom_correlation(conn, symptom)
    
    return render_template('symptoms.html', correlation=correlation)

if __name__ == '__main__':
    # Initialize database connection
    get_connection()
    app.run(debug=True, host='0.0.0.0', port=5000)

