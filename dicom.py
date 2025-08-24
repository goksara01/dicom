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

def decrypt_aes256(cipher_bytes):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(cipher_bytes) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext

def deidentify(bytes):
    dicom_file = BytesIO(bytes)
    original_ds = pydicom.dcmread(dicom_file)

    patient_name         = original_ds[0x0010, 0x0010].value
    patient_id           = original_ds[0x0010, 0x0020].value
    patient_age          = original_ds[0x0010, 0x1010].value
    patient_birthday     = original_ds[0x0010, 0x0030].value
    patient_weight       = original_ds[0x0010, 0x1030].value
    patient_sex          = original_ds[0x0010, 0x0040].value
    study_instance_UID   = original_ds[0x0020, 0x000D].value
    series_instance_UID  = original_ds[0x0020, 0x000E].value
    institution_address  = original_ds[0x0008, 0x0081].value
    institution_name     = original_ds[0x0008, 0x0080].value
    institution_dep_name = original_ds[0x0008, 0x1040].value
    station_name         = original_ds[0x0008, 0x1010].value
    study_description    = original_ds[0x0008, 0x1030].value
    series_description   = original_ds[0x0008, 0x103E].value
    physician_name       = original_ds[0x0008, 0x1050].value
    inst_creation_date   = original_ds[0x0008, 0x0012].value
    inst_creation_time   = original_ds[0x0008, 0x0013].value
    study_time           = original_ds[0x0008, 0x0030].value
    series_time          = original_ds[0x0008, 0x0031].value
    acquisition_time     = original_ds[0x0008, 0x0032].value
    content_time         = original_ds[0x0008, 0x0033].value

    original_ds.PatientSex          = ""
    original_ds.PatientName         = "John^Doe"
    original_ds.PatientID           = ""
    original_ds.PatientBirthDate    = ""
    original_ds.StudyTime           = ""
    original_ds.ContentTime         = ""
    del original_ds.SeriesTime
    del original_ds.PatientAge
    del original_ds.StationName
    del original_ds.PatientWeight
    del original_ds.AcquisitionTime
    del original_ds.InstitutionName
    del original_ds.StudyDescription
    del original_ds.SeriesDescription
    del original_ds.InstitutionAddress
    del original_ds.InstanceCreationTime
    del original_ds.InstanceCreationDate
    del original_ds.PerformingPhysicianName
    del original_ds.InstitutionalDepartmentName
    original_ds.add_new((0x0012, 0x0062), 'CS', "YES")
    original_ds.add_new((0x0012, 0x0063), 'LO', "Per DICOM PS 3.15 AnnexE. Details in 0012,0064")

    buffer = DicomBytesIO()
    encrypted_attrs_ds = Dataset()
    encrypted_attrs_ds.PatientName      = patient_name
    encrypted_attrs_ds.PatientID        = patient_id
    encrypted_attrs_ds.PatientSex       = patient_sex
    encrypted_attrs_ds.PatientAge       = patient_age
    encrypted_attrs_ds.PatientBirthDate = patient_birthday
    encrypted_attrs_ds.PatientWeight    = patient_weight
    encrypted_attrs_ds.StudyTime        = study_time
    encrypted_attrs_ds.SeriesTime       = series_time
    encrypted_attrs_ds.AcquisitionTime  = acquisition_time
    encrypted_attrs_ds.ContentTime      = content_time
    encrypted_attrs_ds.is_little_endian = True
    encrypted_attrs_ds.is_implicit_VR = False
    encrypted_attrs_ds.save_as(buffer)
    ciphertext = aes256(buffer.getvalue())

    item0 = Dataset()
    item0.add_new((0x0400, 0x0510), 'UI', ExplicitVRLittleEndian)
    item0.add_new((0x0400, 0x0520), 'OB', ciphertext)

    encrypted_attrs_ds.clear()
    encrypted_attrs_ds.StationName                 = station_name   
    encrypted_attrs_ds.InstitutionName             = institution_name
    encrypted_attrs_ds.StudyDescription            = study_description
    encrypted_attrs_ds.SeriesDescription           = series_description
    encrypted_attrs_ds.InstitutionAddress          = institution_address
    encrypted_attrs_ds.InstanceCreationTime        = inst_creation_time
    encrypted_attrs_ds.InstanceCreationDate        = inst_creation_date
    encrypted_attrs_ds.PerformingPhysicianName     = physician_name
    encrypted_attrs_ds.InstitutionalDepartmentName = institution_dep_name
    encrypted_attrs_ds.is_little_endian = True
    encrypted_attrs_ds.is_implicit_VR = False
    encrypted_attrs_ds.save_as(buffer)
    ciphertext = aes256(buffer.getvalue())

    item1 = Dataset()
    item1.add_new((0x0400, 0x0510), 'UI', ExplicitVRLittleEndian)
    item1.add_new((0x0400, 0x0520), 'OB', ciphertext)

    original_ds.add_new((0x0400, 0x0500), 'SQ', [item0, item1])
    
    original_ds.file_meta.MediaStorageSOPClassUID    = original_ds.SOPClassUID if "SOPClassUID" in original_ds else generate_uid()
    original_ds.file_meta.MediaStorageSOPInstanceUID = original_ds.SOPInstanceUID if "SOPInstanceUID" in original_ds else generate_uid()
    original_ds.file_meta.TransferSyntaxUID          = ExplicitVRLittleEndian
    original_ds.file_meta.ImplementationClassUID = generate_uid()
    original_ds.is_little_endian = True
    original_ds.is_implicit_VR   = False
        
    original_ds.save_as("dicom_files/deidentified_file.dcm", write_like_original=False)

    return original_ds 

def reidentify(bytes):
    dicom_file = BytesIO(bytes)
    deidentified_ds = pydicom.dcmread(dicom_file)

    if deidentified_ds[0x0012, 0x0062].value == "YES":
        encrypted_attr_seq = deidentified_ds[0x0400, 0x0500]
        for attribute in encrypted_attr_seq:
            encrypted_content = attribute[0x0400, 0x0520].value
            plain_content     = pydicom.dcmread(BytesIO(decrypt_aes256(encrypted_content)), force=True)
            for entry in plain_content:
                if entry.tag in deidentified_ds:
                    deidentified_ds[entry.tag].value = entry.value
                else:
                    deidentified_ds.add_new(entry.tag, entry.VR, entry.value)

        del deidentified_ds[0x0400, 0x0500]
        deidentified_ds[0x0012, 0x0062].value = "NO"

        deidentified_ds.save_as("dicom_files/reidentified_file.dcm", write_like_original=False)

        return deidentified_ds
    else:
        return deidentified_ds