from flask import Flask, request, render_template, send_file
import mysql.connector
import io
import PyPDF2

app = Flask(__name__)

# Function to establish a connection to the database
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='MySQL83',
        password='kitty17',
        database='bursary_database'
    )
    return connection

@app.route('/')
def home():
    return render_template('welcome.html')

@app.route('/student')
def student():
    return render_template('student.html')



# Route to save the email and password
@app.route('/save', methods=['POST'])
def save():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Validate email and password
        if ';' in email or ',' in email:
            return 'Error: Email must not contain semicolons or commas'
        if ';' in password or ',' in password:
            return 'Error: Password must not contain semicolons or commas'
        
        # Save email address and password to your database here
        
        return 'Details saved successfully'  
    else:
        return 'Method Not Allowed', 405

    
@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')


# Route for submitting bursary application
@app.route('/bursary', methods=['GET', 'POST'])
def bursary():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        surname = request.form['surname']
        student_number = request.form['student_number']
        id_number = request.form['id_number']
        email = request.form['email']
        qualification = request.form['qualification']
        gender = request.form['gender']
        
        # Perform server-side validation for ID number and other fields
        if len(id_number) != 13 or not id_number.isdigit():
            return "ID number must be 13 digits long."
        # Add more validation for other fields as needed
        
        # Get the uploaded PDF files
        proof_of_registration = request.files['proof_of_registration']
        proof_of_address = request.files['proof_of_address']
        
        # Read the file data
        pdf_data_registration = proof_of_registration.read()
        pdf_data_address = proof_of_address.read()
        
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Execute SQL query to insert data
        # Execute SQL query to insert data
        sql = "INSERT INTO bursary_application (name, surname, student_number, id_number, email, qualification, gender, proof_of_registration_pdf, proof_of_address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (name, surname, student_number, id_number, email, qualification, gender, pdf_data_registration, pdf_data_address)
        cursor.execute(sql, values)

        # Commit changes and close connection
        connection.commit()
        cursor.close()
        connection.close()
        
        return "Bursary Application Submitted Successfully"  
    else:
        return render_template('bursary.html')

# Route to view the uploaded document
@app.route('/view_document/<int:application_id>')
def view_document(application_id):
    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Query to retrieve the document data
    query = "SELECT proof_of_registration_pdf FROM bursary_application WHERE id = %s"
    cursor.execute(query, (application_id,))
    document_data = cursor.fetchone()[0]  # Assuming only one document per row

    # Close database connection
    cursor.close()
    connection.close()

    # Send the document data as a file to the client
    return send_file(io.BytesIO(document_data), mimetype='application/pdf')

@app.route('/scholarship', methods=['GET', 'POST'])
def scholarship():
    if request.method == 'POST':
        # Retrieve form data and save to scholarship table
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Retrieve form data
        name = request.form['name']
        surname = request.form['surname']
        student_number = request.form['student_number']
        id_number = request.form['id_number']
        email = request.form['email']
        qualification = request.form['qualification']
        gender = request.form['gender']
        
        # Perform server-side validation for ID number and other fields
        if len(id_number) != 13 or not id_number.isdigit():
            return "ID number must be 13 digits long."
        # Add more validation for other fields as needed
        
        # Get the uploaded PDF files
        proof_of_registration = request.files['proof_of_registration']
        proof_of_address = request.files['proof_of_address']
        
        # Read the file data
        pdf_data_registration = proof_of_registration.read()
        pdf_data_address = proof_of_address.read()

        # Execute SQL query to insert data into scholarship table
        sql = "INSERT INTO scholarship (name, surname, student_number, id_number, email, qualification, gender, proof_of_registration_pdf, proof_of_address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (name, surname, student_number, id_number, email, qualification, gender, pdf_data_registration, pdf_data_address)
        cursor.execute(sql, values)

        # Commit changes and close connection
        connection.commit()
        cursor.close()
        connection.close()
        
        return "Scholarship Application Submitted Successfully"  
    else:
        return render_template('scholarship.html')



@app.route('/grant', methods=['GET', 'POST'])
def grant():
    if request.method == 'POST':
        # Retrieve form data and save to grant table
        # Establish database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Retrieve form data
        name = request.form['name']
        surname = request.form['surname']
        student_number = request.form['student_number']
        id_number = request.form['id_number']
        email = request.form['email']
        qualification = request.form['qualification']
        gender = request.form['gender']
        
        # Perform server-side validation for ID number and other fields
        if len(id_number) != 13 or not id_number.isdigit():
            return "ID number must be 13 digits long."
        # Add more validation for other fields as needed
        
        # Get the uploaded PDF files
        proof_of_registration = request.files['proof_of_registration']
        proof_of_address = request.files['proof_of_address']
        
        # Read the file data
        pdf_data_registration = proof_of_registration.read()
        pdf_data_address = proof_of_address.read()

        # Execute SQL query to insert data into scholarship table
        sql = "INSERT INTO Grant_Applications (name, surname, student_number, id_number, email, qualification, gender, proof_of_registration_pdf, proof_of_address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (name, surname, student_number, id_number, email, qualification, gender, pdf_data_registration, pdf_data_address)
        cursor.execute(sql, values)

        # Commit changes and close connection
        connection.commit()
        cursor.close()
        connection.close()
        
        return "Grant Application Submitted Successfully"  
    else:
        return render_template('grant.html')

if __name__ == '__main__':
    app.run(debug=True)
