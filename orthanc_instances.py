import requests, dicom
from flask import session

ORTHANC_URL = "http://130.61.173.177:8042"

def get_all_instances():
    url = f"{ORTHANC_URL}/instances"
    ORTHANC_USERNAME = session.get('username')
    ORTHANC_PASSWORD = session.get('password')
    auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)
    response = requests.get(url, auth=auth) 
    return response.json()

def authenticate(username, password):
    url = f"{ORTHANC_URL}/instances"
    response = requests.get(url, auth=(username, password))

    if response.status_code == 200:
        return True
    else:
        return False

def get_instance(instance_id):
    url = f"{ORTHANC_URL}/instances/{instance_id}"
    ORTHANC_USERNAME = session.get('username')
    ORTHANC_PASSWORD = session.get('password')
    auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()

def get_full_instance(instance_id):
    url = f"{ORTHANC_URL}/instances/{instance_id}/tags?simplify=false"
    ORTHANC_USERNAME = session.get('username')
    ORTHANC_PASSWORD = session.get('password')
    auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()

def get_instance_file(instance_id):
    url = f"{ORTHANC_URL}/instances/{instance_id}/file"
    ORTHANC_USERNAME = session.get('username')
    ORTHANC_PASSWORD = session.get('password')
    auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return dicom.read_file(response.content)

def get_preview(instance_id):
    url = f"{ORTHANC_URL}/instances/{instance_id}/preview"
    ORTHANC_USERNAME = session.get('username')
    ORTHANC_PASSWORD = session.get('password')
    auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to get preview for instance {instance_id}, status: {response.status_code}")
    
def create_deidentified_instance(instance_id):
    url = f"{ORTHANC_URL}/instances/{instance_id}/file"
    ORTHANC_USERNAME = session.get('username')
    ORTHANC_PASSWORD = session.get('password')
    auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return dicom.deidentify(response.content, instance_id)

def create_reidentified_instance(instance_id):
    url = f"{ORTHANC_URL}/instances/{instance_id}/file"
    ORTHANC_USERNAME = session.get('username')
    ORTHANC_PASSWORD = session.get('password')
    auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return dicom.reidentify(response.content)

def create_secure_DICOM_enveloped(instance_id):
    url = f"{ORTHANC_URL}/instances/{instance_id}/file"
    ORTHANC_USERNAME = session.get('username')
    ORTHANC_PASSWORD = session.get('password')
    auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return dicom.secure_enveloped_data(response.content)

def create_RSA_digital_signature(instance_id):
    url = f"{ORTHANC_URL}/instances/{instance_id}/file"
    ORTHANC_USERNAME = session.get('username')
    ORTHANC_PASSWORD = session.get('password')
    auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return dicom.base_RSA_signature(response.content)

def create_creator_RSA_digital_signature(instance_id):
    url = f"{ORTHANC_URL}/instances/{instance_id}/file"
    ORTHANC_USERNAME = session.get('username')
    ORTHANC_PASSWORD = session.get('password')
    auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return dicom.creator_RSA_signature(response.content)