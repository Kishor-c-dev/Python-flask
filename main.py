from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "studentssecretkey"

db = SQLAlchemy(app)

class Students(db.Model):
    id = db.Column('students_id', db.Integer, primary_key = True)
    student_name = db.Column(db.String(256))
    phone_number = db.Column(db.String(16))
    address = db.Column(db.String(1023)) 

    def __init__(self, student_name, phone_number, address):
        self.student_name = student_name
        self.phone_number = phone_number
        self.address = address


@app.route('/') #root
def Home():
    return render_template('index.html', students = Students.query.all())

@app.route('/add-new-student/', methods = ['GET', 'POST'])
def AddNewStudent():
    return render_template('new_student_form.html')

@app.route('/on-submit/', methods = ['POST'])
def OnNewStudentSubmit():
    student_name = request.form['student_name']
    phone_number = request.form['phone_number']
    address = request.form['address']
    if len(student_name) > 0 and len(phone_number) > 0 and len(address) > 0:
        student = Students(student_name, phone_number, address)
        db.session.add(student)
        db.session.commit()
        return redirect('/')
    else: 
        return redirect('/add-new-student/')


if __name__ == '__main__':
    db.create_all()
    app.run(port=8000, debug=True) 
