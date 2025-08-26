import requests
from flask import session

ORTHANC_URL = "http://130.61.173.177:8042"

def get_all_patients():
    url = f"{ORTHANC_URL}/patients"
    ORTHANC_USERNAME = session.get('username')
    ORTHANC_PASSWORD = session.get('password')
    auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)
    response = requests.get(url, auth=auth)
        
    return response.json()

def get_patient_info(patient_id):
    url = f"{ORTHANC_URL}/patients/{patient_id}"
    ORTHANC_USERNAME = session.get('username')
    ORTHANC_PASSWORD = session.get('password')
    auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()