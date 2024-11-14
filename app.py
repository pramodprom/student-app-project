from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Reddy%4096320@localhost:5433/amazon_app'

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    USN = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String(1000), nullable=False)
    Branch = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)




# Create the database tables if they don't exist
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    students = Student.query.all()  # Query all students
    return render_template('todo.html', todo=students)  # Pass students directly to the template


@app.route('/add-student')
def add_student():
    return render_template('add-student.html')


@app.route('/submit', methods=['POST'])
def create_user():
    USN = request.form['USN']
    Name = request.form['Name']
    Branch = request.form['Branch']
    contact = request.form['contact']
    email = request.form['email']
    address = request.form['address']
    new_student = Student(USN=USN, Name=Name, Branch=Branch,contact=contact,email=email,address=address)
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:id>', methods=['POST'])  # Keeps POST, but can switch to DELETE for better practices
def delete_user(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': 'Student deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'An error occurred while deleting the student: {str(e)}'}), 500


@app.route('/update_task/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    student = Student.query.get_or_404(id)  # Automatically raises 404 if not found

    if request.method == 'POST':
        student.USN = request.form['USN']
        student.Name = request.form['Name']
        student.Branch = request.form['Branch']
        student.contact = request.form['contact']
        student.email = request.form['email']
        student.email = request.form['address']

        try:
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            return f"There was an issue while updating the record: {str(e)}"

    return render_template('update.html', student=student)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5005, debug=True)
