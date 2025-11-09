-- Table `Patient`
-- Stores personal information about the patient.
CREATE TABLE Patient (
  PatientID SERIAL PRIMARY KEY,
  Name VARCHAR(255) NOT NULL,
  Age INT,
  Gender VARCHAR(50),
  ContactInfo VARCHAR(255)
);

-- Table `Medication`
-- Stores details about medications prescribed to a patient.
CREATE TABLE Medication (
  MedicationID SERIAL PRIMARY KEY,
  PatientID INT NOT NULL,
  Name VARCHAR(255) NOT NULL,
  Dosage VARCHAR(100),
  Frequency VARCHAR(100),
  StartDate DATE,
  EndDate DATE,
  FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

-- Table `Symptom`
-- Stores information about symptoms reported by a patient.
CREATE TABLE Symptom (
  SymptomID SERIAL PRIMARY KEY,
  PatientID INT NOT NULL,
  Description VARCHAR(255) NOT NULL,
  Severity INT, -- A rating, e.g., from 1 to 10
  Duration VARCHAR(100),
  ReportDate TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

-- Table `Symptom_Medical_Correlation`
-- This is the linking table to track the effectiveness of a medication on a symptom.
CREATE TABLE Symptom_Medical_Correlation (
  CorrelationID SERIAL PRIMARY KEY,
  SymptomID INT NOT NULL,
  MedicationID INT NOT NULL,
  ObservationDate DATE,
  EffectiveRating INT, -- A rating, e.g., from 1 to 5, on how well the med worked
  FOREIGN KEY (SymptomID) REFERENCES Symptom(SymptomID),
  FOREIGN KEY (MedicationID) REFERENCES Medication(MedicationID)
);

-- Table `Vitals`
-- Stores patient vital signs and health metrics over time for tracking and visualization.
CREATE TABLE Vitals (
  VitalID SERIAL PRIMARY KEY,
  PatientID INT NOT NULL,
  RecordedAt TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  -- Blood Pressure
  SystolicBP INT, -- Systolic blood pressure (mmHg)
  DiastolicBP INT, -- Diastolic blood pressure (mmHg)
  -- Heart Rate
  HeartRate INT, -- Heart rate in beats per minute (BPM)
  -- Temperature
  Temperature DECIMAL(4,2), -- Body temperature in Celsius or Fahrenheit
  -- Oxygen Saturation
  OxygenSaturation DECIMAL(5,2), -- SpO2 percentage (0-100)
  -- Respiratory Rate
  RespiratoryRate INT, -- Breaths per minute
  -- Weight
  Weight DECIMAL(5,2), -- Weight in kg or lbs
  -- Blood Glucose (optional)
  BloodGlucose DECIMAL(5,2), -- Blood glucose level (mg/dL or mmol/L)
  -- Notes
  Notes TEXT, -- Additional notes or observations
  FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE
);

-- Index for faster queries on patient vitals by time
CREATE INDEX idx_vitals_patient_time ON Vitals(PatientID, RecordedAt);