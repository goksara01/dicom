import requests
from flask import session

ORTHANC_URL = "http://130.61.173.177:8042"

def get_all_studies():
    url = f"{ORTHANC_URL}/studies"
    ORTHANC_USERNAME = session.get('username')
    ORTHANC_PASSWORD = session.get('password')
    auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        return {"error" : "Unauthorized access.", "message" : "Authentication failed. Please check your credentials."}

def get_study(study_id):
    url = f"{ORTHANC_URL}/studies/{study_id}"
    ORTHANC_USERNAME = session.get('username')
    ORTHANC_PASSWORD = session.get('password')
    auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()
