import requests

ORTHANC_URL = "http://130.61.173.177:8042"
ORTHANC_USERNAME = "orthanc"
ORTHANC_PASSWORD = "orthanc"

auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)

def get_all_studies():
    url = f"{ORTHANC_URL}/studies"
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        return {"error" : "Unauthorized access.", "message" : "Authentication failed. Please check your credentials."}

def get_study(study_id):
    url = f"{ORTHANC_URL}/studies/{study_id}"
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()