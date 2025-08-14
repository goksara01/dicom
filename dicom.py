import pydicom
from io import BytesIO
from pydicom.dataset import Dataset
from pydicom.filebase import DicomBytesIO
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

key = bytes.fromhex('8ef72dd8c7e59683829f1a8a09febc6ee87bdfb300e3c18b90f320f8470c0d8a')
iv  = bytes.fromhex('3c0dccb453c688c901fc9e343f21acdb')

def read_file(bytes):
    dicom_file = BytesIO(bytes)
    return pydicom.dcmread(dicom_file) 

def aes256(plain_bytes):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plain_bytes) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return ciphertext

def deidentify(bytes):
    dicom_file = BytesIO(bytes)
    original_ds = pydicom.dcmread(dicom_file)

    patient_name = original_ds[0x0010, 0x0010].value
    patient_id   = original_ds[0x0010, 0x0020].value

    original_ds.PatientName = "John^Doe"
    original_ds.PatientID   = ""

    buffer = DicomBytesIO()
    encrypted_attrs_ds = Dataset()
    encrypted_attrs_ds.PatientName = patient_name
    encrypted_attrs_ds.PatientID   = patient_id
    encrypted_attrs_ds.is_little_endian = True
    encrypted_attrs_ds.is_implicit_VR = False
    encrypted_attrs_ds.save_as(buffer)
    ciphertext = aes256(buffer.getvalue())

    item0 = Dataset()
    item0.add_new((0x0400, 0x0510), 'UI', ExplicitVRLittleEndian)
    item0.add_new((0x0400, 0x0520), 'OB', ciphertext)

    original_ds.add_new((0x0400, 0x0500), 'SQ', [item0])
    
    original_ds.file_meta.MediaStorageSOPClassUID = original_ds.SOPClassUID if "SOPClassUID" in original_ds else generate_uid()
    original_ds.file_meta.MediaStorageSOPInstanceUID = original_ds.SOPInstanceUID if "SOPInstanceUID" in original_ds else generate_uid()
    original_ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    original_ds.file_meta.ImplementationClassUID = generate_uid()
    original_ds.is_little_endian = True
    original_ds.is_implicit_VR   = False
        
    original_ds.save_as("dicom_files/deidentified_file.dcm", write_like_original=False)

    return original_ds 