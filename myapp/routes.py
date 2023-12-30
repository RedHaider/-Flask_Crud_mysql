# myapp/routes.py

from myapp import app
from flask import render_template, request, redirect, url_for 
from flask_mysqldb import MySQL
from flask import jsonify

mysql = MySQL(app)
#-------------------------------------------
#--------------Get Patient------------------
#-------------------------------------------

@app.route('/')
def index():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, name, email, disease, doctor FROM patient_information")  # Replace with your table name
        data = cursor.fetchall()
        cursor.close()
        for patient in data:
            print(patient['name'])
        return render_template('index.html', data=data)
    except Exception as e:
        return f"Error: {str(e)}"
#-------------------------------------------
#--------------Add Patient------------------
#-------------------------------------------
@app.route('/add_patient', methods=['POST'])
def add_patient():
      try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        disease = request.form.get('disease')
        doctor = request.form.get('doctor')

        # Execute SQL INSERT query
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO patient_information (name, email, disease, doctor) VALUES (%s, %s, %s, %s)",
                       (name, email, disease, doctor))
        mysql.connection.commit()
        cursor.close()

        # Fetch data again
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, name, email, disease, doctor FROM patient_information")
        data = cursor.fetchall()
        cursor.close()

        # Redirect to the main page after adding the patient
        return redirect(url_for('index',  data=data))
      except Exception as e:
        error_message = f"Error: {str(e)}"
        # Fetch data to display in the table
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, name, email, disease, doctor FROM patient_information")
        data = cursor.fetchall()
        cursor.close()
        return render_template('index.html', error_message=error_message, data=data)
#-------------------------------------------
#--------------Delete Patient---------------
#-------------------------------------------
      


@app.route('/delete_patient/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM patient_information WHERE id = %s", (patient_id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

#-------------------------------------------
#--------------Edit Patient---------------
#-------------------------------------------


# Add a route to fetch patient data for editing
@app.route('/get_patient/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM patient_information WHERE id = %s", (patient_id,))
        patient = cursor.fetchone()
        cursor.close()

        if patient:
            return jsonify({'success': True, 'patient': patient})
        else:
            return jsonify({'success': False, 'error_message': 'Patient not found'})
    except Exception as e:
        return jsonify({'success': False, 'error_message': str(e)})

