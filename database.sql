
CREATE DATABASE IF NOT EXISTS health_tracker_db;
USE health_tracker_db;


-- Table `Patient`
-- Stores personal information about the patient.
CREATE TABLE Patient (
  PatientID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(255) NOT NULL,
  Age INT,
  Gender VARCHAR(50),
  ContactInfo VARCHAR(255)
);

-- Table `Medication`
-- Stores details about medications prescribed to a patient.
CREATE TABLE Medication (
  MedicationID INT AUTO_INCREMENT PRIMARY KEY,
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
  SymptomID INT AUTO_INCREMENT PRIMARY KEY,
  PatientID INT NOT NULL,
  Description VARCHAR(255) NOT NULL,
  Severity INT, -- A rating, e.g., from 1 to 10
  Duration VARCHAR(100),
  ReportDate DATETIME DEFAULT CURRENT_TIMESTAMP, -- Automatically records when the symptom was logged
  FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

-- Table `Reminder`
-- Stores reminders for medications or visits.
CREATE TABLE Reminder (
  ReminderID INT AUTO_INCREMENT PRIMARY KEY,
  PatientID INT NOT NULL,
  MedicationID INT, -- Can be NULL if it's a general visit reminder
  ReminderName VARCHAR(255) NOT NULL,
  ReminderType VARCHAR(100), -- E.g., 'Medication' or 'Visit'
  ReminderTime DATETIME NOT NULL,
  Status VARCHAR(50) DEFAULT 'Active', -- E.g., 'Active', 'Dismissed'
  FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
  FOREIGN KEY (MedicationID) REFERENCES Medication(MedicationID)
);

-- Table `Symptom_Medical_Correlation`
-- This is the linking table to track the effectiveness of a medication on a symptom.
CREATE TABLE Symptom_Medical_Correlation (
  CorrelationID INT AUTO_INCREMENT PRIMARY KEY,
  SymptomID INT NOT NULL,
  MedicationID INT NOT NULL,
  ObservationDate DATE,
  EffectiveRating INT, -- A rating, e.g., from 1 to 5, on how well the med worked
  FOREIGN KEY (SymptomID) REFERENCES Symptom(SymptomID),
  FOREIGN KEY (MedicationID) REFERENCES Medication(MedicationID)
);