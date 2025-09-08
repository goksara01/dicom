import sqlite3

def add_patient(patient):
    conn = sqlite3.connect("dicom.db")

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    sex TEXT CHECK (sex IN ('F', 'M')) DEFAULT 'F',
                    type TEXT NOT NULL,
                    birthdate TEXT NOT NULL
            )
    ''')

    cursor.execute("INSERT INTO patients VALUES(?, ?, ?, ?, ?)", 
            (patient['MainDicomTags']['PatientID'], patient['MainDicomTags']['PatientName'], patient['MainDicomTags']['PatientSex'], patient['Type'], patient['MainDicomTags']['PatientBirthDate']))

    conn.commit()
    conn.close()