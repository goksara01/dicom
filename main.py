from flask import Flask, render_template, jsonify, Response
import orthanc_clients, orthanc_studies, orthanc_instances

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

@app.route('/instances')
def list_instances():
    try:
        data = orthanc_instances.get_all_instances()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/instances/<instance_id>')
def get_instance(instance_id):
    try:
        data = orthanc_instances.get_instance(instance_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/instances/<instance_id>/preview')
def get_preview(instance_id):
    try:
        data = orthanc_instances.get_preview(instance_id)
        return Response(data, mimetype="image/jpeg")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)