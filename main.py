from flask import Flask, render_template, jsonify
import orthanc_clients, orthanc_studies

app = Flask(__name__)

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

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)