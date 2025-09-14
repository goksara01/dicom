// scripts.js

function viewPatients(){
    fetch(`http://127.0.0.1:5000/patients`, {
        method: 'GET'
    })  
    .then(response => response.json())
    .then(data => {
        const table = document.querySelector("#patient-table tbody")
        console.log(data)
        table.innerHTML = ""

        data.forEach(element => {
            fetch(`http://127.0.0.1:5000/patients/${element}`, {
                method: 'GET'
            })
            .then(response1 => response1.json())
            .then(patient => {
                row = document.createElement("tr")

                const nameCell = document.createElement("td")
                nameCell.textContent = patient['MainDicomTags']['PatientName']

                const birthdayCell = document.createElement("td")
                rawDate = patient['MainDicomTags']['PatientBirthDate']
                birthdayCell.textContent = `${rawDate.slice(0, 4)}-${rawDate.slice(4, 6)}-${rawDate.slice(6, 8)}`;

                const patientSexCell = document.createElement("td")
                patientSexCell.textContent = patient['MainDicomTags']['PatientSex']

                const patientTypeCell = document.createElement("td")
                patientTypeCell.textContent = patient['Type']

                row.appendChild(nameCell)
                row.appendChild(birthdayCell)
                row.appendChild(patientSexCell)
                row.appendChild(patientTypeCell)

                table.appendChild(row)
            })
            .catch(error1 => {
                console.error("Error fetching patient data: ", error1);
            });
        });
    })
    .catch(error => {
        console.error('Error fetching patients:', error)
    })
}

document.addEventListener('DOMContentLoaded', () => {
    const tbody = document.querySelector('#instance-table tbody');
    
    tbody.addEventListener('click', (event) => {
        if (event.target && event.target.matches('.action-btn')) {
            
            const instance_id = event.target.dataset.id;

            alert(instance_id)
            
        }
    });
});