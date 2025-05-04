from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# In-memory database for student records
students = {}

# Helper function to generate a unique ID for new students
def generate_id():
    return str(uuid.uuid4())


# API for managing student records
#--------------------------------------------------#
# GET /students - Returns a list of all students
# GET /students/<student_id> - Returns details of a specific student by ID
# POST /students - Adds a new student record
# PUT /students/update - Updates a student's details using query parameters
# DELETE /students/<student_id> - Deletes a student from the list using path parameter
#--------------------------------------------------#

@app.route('/')
def index():
    return "Welcome to the Student Management API!"

# --------------------------------------------------#
# GET all students
# This endpoint retrieves and returns a complete list of all student records stored in the database.
# It is accessible via a GET request to the /students endpoint.
# The response is formatted as a JSON array, where each element represents a student record.
# --------------------------------------------------#
@app.route('/students', methods=['GET'])
def get_all_students():
    """Returns a list of all students"""
    return jsonify(list(students.values()))


# --------------------------------------------------#
# GET /students/<student_id> - Returns details of a specific student by ID
# This endpoint returns the details of a specific student based on the provided student ID.
# It can be accessed via a GET request to /students/<student_id>, where <student_id> is the ID of the student.
# --------------------------------------------------#
@app.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    """Returns details of a specific student by ID"""
    student = students.get(student_id)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404


# --------------------------------------------------#
# POST /students - Adds a new student record
# This endpoint allows the user to add a new student record to the database.
# It can be accessed via a POST request to /students.
# The request body should contain the student details in JSON format.
# The required fields are 'name', 'age', and 'course'.
# The endpoint will generate a unique ID for the new student and store the record in the database.
# --------------------------------------------------#
@app.route('/students', methods=['POST'])
def add_student():
    """Adds a new student record"""
    # Handle both JSON and form/query parameters
    data = {}
    
    if request.is_json:
        data = request.json
    elif request.args:  # Handle query parameters
        data = request.args.to_dict()
    elif request.form:  # Handle form data
        data = request.form.to_dict()
    else:
        return jsonify({"error": "No data provided. Send data as JSON, form or query parameters"}), 400
    
    required_fields = ['name', 'age', 'course']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Generate a unique ID for the new student
    student_id = generate_id()
    
    # Create student record
    # Convert age to integer if it's a string (from query/form parameters)
    try:
        age = int(data['age'])
    except ValueError:
        return jsonify({"error": "Age must be a number"}), 400
        
    student = {
        'id': student_id,
        'name': data['name'],
        'age': age,
        'course': data['course']
    }
    
    # Store in our "database"
    students[student_id] = student
    
    return jsonify(student), 201

# --------------------------------------------------#
# PUT /students/update - Updates a student's details using query parameters
# This endpoint allows the user to update the details of an existing student record.
# It can be accessed via a PUT request to /students/update.
# The request should include the student ID as a query parameter (e.g., /students/update?id=<student_id>).
# The request body can contain the fields to be updated (e.g., 'name', 'age', 'course').
# The endpoint will update the specified fields for the student with the given ID.
# --------------------------------------------------#
@app.route('/students/update', methods=['PUT', 'GET'])  # Also allow GET for browser testing
def update_student_by_param():
    """Updates a student's details using query parameters"""
    student_id = request.args.get('id')
    if not student_id:
        return jsonify({"error": "Missing student ID parameter"}), 400
    
    if student_id not in students:
        return jsonify({"error": "Student not found"}), 404
    
    student = students[student_id]
    
    # Update fields if they exist in the request
    for field in ['name', 'age', 'course']:
        if field in request.args:
            # Convert age to integer if it exists
            if field == 'age' and request.args.get('age'):
                try:
                    student[field] = int(request.args.get('age'))
                except ValueError:
                    return jsonify({"error": "Age must be a number"}), 400
            else:
                student[field] = request.args.get(field)
    
    return jsonify("UPDATED ", student)


# --------------------------------------------------#
# DELETE /students/<student_id> - Deletes a student from the list using path parameter
# This endpoint allows the user to delete a student record from the database.
# It can be accessed via a DELETE request to /students/<student_id>, where <student_id> is the ID of the student to be deleted.
# The endpoint will remove the student record from the database.
# --------------------------------------------------#
@app.route('/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Deletes a student from the list using path parameter"""
    if student_id not in students:
        return jsonify({"error": "Student not found"}), 404
    
    # Remove the student
    deleted_student = students.pop(student_id)
    
    return jsonify({"message": f"Student {deleted_student['name']} has been deleted"})

# Add some sample data for testing
def add_sample_data():
    sample_students = [
        {
            'name': 'Juan Dela Cruz',
            'age': 20,
            'course': 'BSIT'
        },
        {
            'name': 'Maria Santos',
            'age': 21,
            'course': 'BSCS'
        },
        {
            'name': 'Pedro Penduko',
            'age': 19,
            'course': 'BSIS'
        }
    ]
    
    for student_data in sample_students:
        student_id = generate_id()
        student_data['id'] = student_id
        students[student_id] = student_data

if __name__ == '__main__':
    # Add some sample data
    add_sample_data()
    # Run the Flask app
    app.run(debug=True)
