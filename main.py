from flask import Flask, flash, redirect, render_template, jsonify, Response, request, session, url_for
import orthanc_clients, orthanc_studies, orthanc_series, orthanc_instances, sqlite

app = Flask(__name__)
app.secret_key = 'b0f1b6f71c2f9f4e6a7da38b1c6b4c2b37c47b7801540b869d6c3fbdc2b490b9'

@app.route('/patients')
def list_patients():
    try:
        data = orthanc_clients.get_all_patients()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/patients/<patient_id>')
def patient_info(patient_id):
    try:
        data = orthanc_clients.get_patient_info(patient_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/patients/<patient_id>/add-patient')
def save_patient(patient_id):
    try:
        data = orthanc_clients.get_patient_info(patient_id)
        sqlite.add_patient(data)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/studies')
def list_studies():
    try:
        data = orthanc_studies.get_all_studies()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/studies/<study_id>')
def get_study(study_id):
    try:
        data = orthanc_studies.get_study(study_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/studies/load-studies')
def load_studies():
    try:
        data = orthanc_studies.get_all_studies()
        for study in data:
            sqlite.load_study(get_study(study).get_json())
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/series')
def list_series():
    try:
        data = orthanc_series.get_all_series()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/series/<series_id>')
def get_series(series_id):
    try:
        data = orthanc_series.get_series_info(series_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/series/load-series')
def load_series():
    try:
        data = orthanc_series.get_all_series()
        for series in data:
            sqlite.load_series(get_series(series).get_json())
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500    

@app.route('/instances')
def list_instances():
    try:
        data = orthanc_instances.get_all_instances()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/instances-db')
def list_instances_from_db():
    data = sqlite.get_instances_from_db()
    return jsonify(data)

@app.route('/instances/<instance_id>')
def get_instance(instance_id):
    try:
        data = orthanc_instances.get_instance(instance_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/instances/load-instances')
def load_instances():
    try:
        data = orthanc_instances.get_all_instances()
        for instance in data:
            sqlite.load_instance(get_instance(instance).get_json())
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500    

@app.route('/instances/<instance_id>/file')
def get_instance_file(instance_id):
    try:
        data = orthanc_instances.get_instance_file(instance_id)
        return jsonify(str(data))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/instances/<instance_id>/deidentify')
def get_deidentified_file(instance_id):
    try:
        data = orthanc_instances.create_deidentified_instance(instance_id)
        return jsonify(str(data))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/instances/<instance_id>/reidentify')
def get_reidentified_file(instance_id):
    try:
        data = orthanc_instances.create_reidentified_instance(instance_id)
        #print(data)
        return jsonify(str(data))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/instances/<instance_id>/preview')
def get_preview(instance_id):
    try:
        data = orthanc_instances.get_preview(instance_id)
        return Response(data, mimetype="image/jpeg")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/instances/<instance_id>/secure')
def get_secure(instance_id):
    try:
        data = orthanc_instances.create_secure_DICOM_enveloped(instance_id)
        #print(data)
        return jsonify({'status': "success"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/instances/<instance_id>/rsa-signature')
def get_rsa_signature(instance_id):
    try:
        data = orthanc_instances.create_RSA_digital_signature(instance_id)
        #print(data)
        return jsonify({'status': "success"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500    

@app.route('/instances/<instance_id>/creator-rsa-signature')
def get_creator_rsa_signature(instance_id):
    try:
        data = orthanc_instances.create_creator_RSA_digital_signature(instance_id)
        #print(data)
        return jsonify({'status': "success"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        if orthanc_instances.authenticate(username=username, password=password):
            session['logged_in'] = True
            session['username']  = username
            session['password']  = password
            return redirect(url_for('home'))
        else:
            session['logged_in'] = False
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route("/")
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    return render_template("index.html")

@app.route('/patient-portal')
def patient_portal():
    return render_template("patient.html")

@app.route('/instance-portal')
def instance_portal():
    return render_template("instance_page.html")

if __name__ == "__main__":
    app.run(debug=True)