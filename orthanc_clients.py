import requests

ORTHANC_URL = "http://130.61.173.177:8042"
ORTHANC_USERNAME = "orthanc"
ORTHANC_PASSWORD = "orthanc"

auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)

def get_all_patients():
    url = f"{ORTHANC_URL}/patients"
    response = requests.get(url, auth=auth)
        
    return response.json()

def get_patient_info(patient_id):
    url = f"{ORTHANC_URL}/patients/{patient_id}"
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()