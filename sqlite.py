import datetime
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
            (patient['MainDicomTags']['PatientID'], patient['MainDicomTags']['PatientName'], patient['MainDicomTags']['PatientSex'], 
             patient['Type'], patient['MainDicomTags']['PatientBirthDate']))

    conn.commit()
    conn.close()

def load_study(study):
    conn = sqlite3.connect("dicom.db")
    conn.execute("PRAGMA foreign_keys = ON;")

    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS studies (
                id TEXT PRIMARY KEY,
                description TEXT,
                date TEXT NOT NULL,
                patient_id TEXT NOT NULL,
                
                FOREIGN KEY (patient_id) REFERENCES patients(id)
                   ON DELETE CASCADE
                   ON UPDATE CASCADE
            )
    ''')

    cursor.execute("INSERT INTO studies VALUES(?, ?, ?, ?)",
                   (study['ID'], study['MainDicomTags']['StudyDescription'],
                    study['MainDicomTags']['StudyDate'], study['PatientMainDicomTags']['PatientID']))

    conn.commit()
    conn.close()

def load_series(series):
    conn = sqlite3.connect("dicom.db")
    conn.execute("PRAGMA foreign_keys = ON;")

    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS series (
                id TEXT PRIMARY KEY,
                manufacturer TEXT,
                modality TEXT NOT NULL,
                protocol_name TEXT,
                date TEXT NOT NULL,
                study_id TEXT NOT NULL,
                
                FOREIGN KEY (study_id) REFERENCES studies(id)
                   ON DELETE CASCADE
                   ON UPDATE CASCADE
            )
    ''')

    cursor.execute("INSERT INTO series VALUES(?, ?, ?, ?, ?, ?)",
                   (series['ID'], series['MainDicomTags']['Manufacturer'], series['MainDicomTags']['Modality'], 
                    series['MainDicomTags']['ProtocolName'], series['MainDicomTags']['SeriesDate'], series['ParentStudy']))

    conn.commit()
    conn.close()

def load_instance(instance):
    conn = sqlite3.connect("dicom.db")
    conn.execute("PRAGMA foreign_keys = ON;")

    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS instances (
                id TEXT PRIMARY KEY,
                index_in_series INTEGER NOT NULL,
                creation_date TEXT NOT NULL,
                creation_time TEXT NOT NULL,
                series_id TEXT NOT NULL,
                
                FOREIGN KEY (series_id) REFERENCES series(id)
                   ON DELETE CASCADE
                   ON UPDATE CASCADE
            )
    ''')

    cursor.execute("INSERT INTO instances VALUES(?, ?, ?, ?, ?)",
                (instance['ID'], instance['IndexInSeries'], instance['MainDicomTags']['InstanceCreationDate'], 
                    instance['MainDicomTags']['InstanceCreationTime'], instance['ParentSeries']))

    conn.commit()
    conn.close()    

def get_instances_from_db():
    conn = sqlite3.connect('dicom.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, index_in_series, creation_date, creation_time, series_id FROM instances")
    rows = cursor.fetchall()
    conn.close()

    instances = [{"id": row[0], "index_in_series": row[1], "creation_date": datetime.datetime.strptime(row[2], "%Y%m%d").strftime("%Y-%m-%d"), 
                "creation_time": row[3], "series_id": row[4]} for row in rows]
                
    return instances