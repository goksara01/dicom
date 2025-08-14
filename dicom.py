import pydicom
from io import BytesIO
from pydicom.dataset import Dataset
from pydicom.uid import ExplicitVRLittleEndian
from pydicom.sequence import Sequence

def read_file(bytes):
    dicom_file = BytesIO(bytes)
    # return a Dataset
    return pydicom.dcmread(dicom_file) 

def deidentify(bytes):
    dicom_file = BytesIO(bytes)
    original_ds = pydicom.dcmread(dicom_file)

    patient_name = original_ds[0x0010, 0x0010].value
    patient_id   = original_ds[0x0010, 0x0020].value

    #encrypted_attributes_sq = Dataset()
    encrypted_content = Dataset() # UID (0400,0520)
    encrypted_content.PatientName = patient_name
    encrypted_content.PatientID   = patient_id
    encrypted_content_transfer_syntax = Dataset() # UID (0400,0510)
    encrypted_content_transfer_syntax.add_new((0x0400, 0x0510), 'UI', ExplicitVRLittleEndian)
    original_ds.add_new((0x0400, 0x0500), 'SQ', [encrypted_content_transfer_syntax, encrypted_content])
    return original_ds 