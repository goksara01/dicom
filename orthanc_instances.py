import requests

ORTHANC_URL = "http://130.61.173.177:8042"
ORTHANC_USERNAME = "orthanc"
ORTHANC_PASSWORD = "orthanc"

auth = (ORTHANC_USERNAME, ORTHANC_PASSWORD)

def get_all_instances():
    url = f"{ORTHANC_URL}/instances"
    response = requests.get(url, auth=auth)
        
    return response.json()

def get_instance(instance_id):
    url = f"{ORTHANC_URL}/instances/{instance_id}"
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    return response.json()

def get_preview(instance_id):
    url = f"{ORTHANC_URL}/instances/{instance_id}/preview"
    auth = ('orthanc', 'orthanc')
    response = requests.get(url, auth=auth)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to get preview for instance {instance_id}, status: {response.status_code}")