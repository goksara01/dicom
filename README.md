# DICOM Attribute Confidentiality Profiles Implementacija

&nbsp;&nbsp;&nbsp;&nbsp;Ideja projekta jeste implementacija jednog (za sada) bezbednosnog profila definisanog u "__DICOM PS3.15 2025c - Security and System
Management Profiles__", konkretno Attribute Confidentiality profila. Ovaj profil, kao i većina ostalih u ovom poglavlju, ima za cilj očuvanje ključnih činioca informacione bezbednosti: integritetu, tajnosti i pouzdanosti podataka. Ovo pogotovo važi kada su u pitanju medicinski podaci, CT slike, MRI skenovi i slično.

&nbsp;&nbsp;&nbsp;&nbsp;Projekat je započeo dizanjem 2 Docker kontejnera. Na jednom je podignut portainer (__portainer/portainer-ce__) za lakšu konfiguraciju postojećih kontejnera (i ukoliko se pojavi potreba za još jednim izolovanim sistemom), a na drugom je podignut __urosss/orthanc__, kontejner na kojem je podignuta verzija Orthanc DICOMweb servera kompatibilna sa ARM arhitekturama. Nakon ovoga je usledilo pravljenje Python web-servera uz pomoć __Flask__ biblioteke. Sajt je dignut na lokalu, a u pozadi komunicira sa Orthanc serverom putem njegove javne IP adrese, (za sada) statički definisanih login kredencijala i RESTful zahteva. Biblioteke korišćene tokom implementacije i njihove verzije su: 
- _cryptography__45.0.5
- __dicom_ 0.9.9.post1
- __Flask_ 3.1.1
- __pydicom_ 3.0.1


