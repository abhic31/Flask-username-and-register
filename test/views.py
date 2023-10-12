from flask import render_template, request, redirect, url_for, flash
from app import app, db
from models import User , EmployeeForm , Employee

@app.route('/')
def home():
    return 'Welcome to the home page!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # Compare plain text passwords directly
            flash('Logged in successfully.', 'success')
            return redirect(url_for('profile', username=username))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            # Store the plain text password directly
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully. You can now log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profile/<username>')
def profile(username):
    return render_template('profile.html', username=username)

@app.route('/logout')
def logout():
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/employees/create', methods=['GET', 'POST'])
def create_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        new_employee = Employee(
            user_id=form.user_id.data,
            password=form.password.data,
            email=form.email.data,
            department=form.department.data,
            date_of_joining=form.date_of_joining.data
        )
        db.session.add(new_employee)
        db.session.commit()
        flash('Employee created successfully.', 'success')
        return redirect(url_for('employee_list'))
    return render_template('create_employee.html', form=form)

@app.route('/employees/update/<int:id>', methods=['GET', 'POST'])
def update_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        flash('Employee not found.', 'danger')
        return redirect(url_for('employee_list'))

    form = EmployeeForm(obj=employee)  # Pre-populate form fields with existing data
    if form.validate_on_submit():
        form.populate_obj(employee)  # Update the employee object with form data
        db.session.commit()
        flash('Employee updated successfully.', 'success')
        return redirect(url_for('employee_list'))

    return render_template('update_employee.html', form=form, employee=employee)

@app.route('/employees/delete/<int:id>', methods=['GET'])
def delete_employee(id):
    employee = Employee.query.get(id)
    if not employee:
        flash('Employee not found.', 'danger')
        return redirect(url_for('employee_list'))

    db.session.delete(employee)
    db.session.commit()

    flash('Employee deleted successfully.', 'success')
    return redirect(url_for('employee_list'))

@app.route('/employee_list', methods=['GET'])
def employee_list():
    search_keyword = request.args.get('search_keyword', default='', type=str)
    
    if search_keyword:
        employees = Employee.query.filter(
            (Employee.user_id.like(f"%{search_keyword}%")) |
            (Employee.email.like(f"%{search_keyword}%")) |
            (Employee.department.like(f"%{search_keyword}%"))
        ).all()
    else:
        employees = Employee.query.all()
    
    return render_template('employee_list.html', employees=employees)

