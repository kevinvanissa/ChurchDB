from flask import render_template, jsonify
from app import app, db, lm
from models import User, ROLE_ADMIN, INACTIVE_USER, Phone, Department, Member_Department, Family_Relationship, Church, Member_Church,Family
from forms import LoginForm, UploadForm, ChangePasswordForm, RegistrationForm,EditUserForm,EditPhoneForm,DepartmentForm,FamilyForm,AddUserForm
from werkzeug import check_password_hash, generate_password_hash, secure_filename
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, send_from_directory, abort
import uuid
from flask.ext.login import login_user, logout_user, current_user, login_required
from config import ALLOWED_EXTENSIONS
from functools import wraps
import os
import csv
import time as pytime


def active_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.status == INACTIVE_USER:
            flash("Please wait for activation", category='danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.errorhandler(413)
def internal_error(error):
    db.session.rollback()
    return render_template('413.html'), 413


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def login():
    # if g.user is not None:
    # if g.user is not None and g.user.is_authenticated():
        # return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash(
                'The username or password you entered is incorrect!',
                category='danger')
            return redirect(url_for('login'))
        if user.password is None or user.password == "":
            flash(
                'The username or password you entered is incorrect!',
                category='danger')
            return redirect(url_for('login'))
        if user and check_password_hash(
                user.password,
                form.password.data) and user.is_active():
            session['remember_me'] = form.remember_me.data
            if 'remember_me' in session:
                remember_me = session['remember_me']
                session.pop('remember_me', None)
            login_user(user, remember=remember_me)
            flash('You have successfully logged in', category='success')
            return redirect(request.args.get('next') or url_for('main'))

        if user and not check_password_hash(
                user.password, form.password.data) and user.is_active():
            flash('Please check your username and password!', category='danger')
            return redirect(url_for('login'))

        if user and check_password_hash(
                user.password,
                form.password.data) and not user.is_active():
            flash("Your account needs activation!", category='warning')
            return redirect(url_for('login'))

        if user and not check_password_hash(
                user.password,
                form.password.data) and not user.is_active():
            flash("Your account needs activation!", category='warning')
            return redirect(url_for('login'))

    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('There is already a user with this email!', category='danger')
            return redirect(url_for('register'))
        user = User(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data,
            password=generate_password_hash(
                form.password.data))
        db.session.add(user)
        db.session.commit()
        flash(
            'Thanks for registering. Your account will need activation.',
            category='info')
        return redirect(url_for('login'))
    return render_template(
        'register.html',
        title='Register',
        form=form,
        )

@app.route('/main', methods=['GET', 'POST'])
@login_required
def main():
    users = User.query.all()

    return render_template(
            'main.html',
            title='Members',
            users=users
            )


@app.route('/detail/<int:id>', methods=['GET', 'POST'])
@login_required
def detail(id):
    user = User.query.get_or_404(id)

    departments = db.session.query(Department,Member_Department).filter(Department.id==Member_Department.department_id,
           Member_Department.user_id==user.id).all()


    relatives = db.session.query(Family,User,Family_Relationship).filter(User.id==Family_Relationship.family_member,Family_Relationship.user_id==user.id,Family.id==Family_Relationship.relationship).all()

    phones = db.session.query(Phone,User).filter(Phone.user_id==User.id,User.id==user.id).all()

    return render_template(
            'detail.html',
            title='User Information',
            user=user,
            departments=departments,
            relatives=relatives,
            phones=phones
            )


@app.route('/editrelative/<int:id>',methods=['GET','POST'])
@login_required
def editrelative(id):
    title = 'Edit Relatives'
    user = User.query.get_or_404(id)
    form = FamilyForm()
    if form.validate_on_submit():
        family = Family_Relationship(user_id=id,family_member=form.user.data,relationship=form.type.data)
        db.session.add(family)
        db.session.commit()
        flash('Family member successfully added',category='success')
    relatives = db.session.query(Family,User,Family_Relationship).filter(User.id==Family_Relationship.family_member,Family_Relationship.user_id==user.id,Family.id==Family_Relationship.relationship).all()
    return render_template('editrelative.html',title=title,relatives=relatives,user=user,form=form)



@app.route('/editdepartment/<int:id>',methods=['GET','POST'])
@login_required
def editdepartment(id):
    title = 'Edit Department'
    user = User.query.get_or_404(id)
    departments = db.session.query(Department,Member_Department).filter(Department.id==Member_Department.department_id,
           Member_Department.user_id==user.id).all()
    form = DepartmentForm()

    f = request.form.get('dept_name')
    print "hello..."
    print f

    if form.validate_on_submit():
        print "right"
        member_department = Member_Department(user_id=user.id,department_id=form.dept_name.data)
        db.session.add(member_department)
        db.session.commit()
        return redirect(url_for('editdepartment',id=user.id))
    return render_template('editdepartment.html',title=title,departments=departments,user=user,form=form)




@app.route('/editphone/<int:id>',methods=['GET','POST'])
@login_required
def editphone(id):
    title = 'Edit Phone'
    user = User.query.get_or_404(id)
    form = EditPhoneForm()

    if form.validate_on_submit():
        phone = Phone(user_id=id,phone=form.phone.data,primary_secondary=form.primary_secondary.data,network=form.network.data)
        db.session.add(phone)
        db.session.commit()
        flash('Phone number added successfully', category='success')

    phones = Phone.query.filter_by(user_id=id).all()

    return render_template('editphone.html',title=title,phones=phones,form=form,user=user)


@app.route('/edituser/<int:id>',methods=['GET','POST'])
@login_required
def edituser(id):
    title='Edit User'
    user = User.query.get_or_404(id)
    mypic = user.picture
    if not user:
        abort(404)
    form = EditUserForm()
    if form.validate_on_submit():

        filename = ""
        file = request.files['picture']
        if file:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename=str(uuid.uuid4())+filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                user.picture = filename
            else:
                flash('Only jpeg, jpg or png files are accepted',category='danger')
                return redirect(url_for('edituser',id=user.id))

        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.middlename = form.middlename.data
        user.occupation = form.occupation.data
        user.place_of_employment = form.place_of_employment.data
        user.certification = form.certification.data
        user.street = form.street.data
        user.city  = form.city.data
        user.state = form.state.data
        user.zip  = form.zip.data
        db.session.add(user)
        db.session.commit()
        flash('User has been edited',category='success')
        return redirect(url_for('detail',id=user.id))
    else:
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.middlename.data = user.middlename
        form.occupation.data = user.occupation
        form.place_of_employment.data = user.place_of_employment
        form.certification.data = user.certification
        form.street.data = user.street
        form.city.data = user.city
        form.state.data = user.state
        form.zip.data = user.zip

    return render_template('edituser.html',form=form,title=title,id=user.id,user=user)


@app.route('/adduser',methods=['GET','POST'])
@login_required
def adduser():
    title='Add User'
    #user = User.query.get_or_404(id)
#    mypic = user.picture
#    if not user:
#        abort(404)
    form = AddUserForm()
    if form.validate_on_submit():

        filename = ""
        file = request.files['picture']
        if file:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename=str(uuid.uuid4())+filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            else:
                flash('Only jpeg, jpg or png files are accepted',category='danger')
                return redirect(url_for('adduser'))
        user = User(
            firstname = form.firstname.data,
            lastname = form.lastname.data,
            middlename = form.middlename.data,
            picture = filename,
            occupation = form.occupation.data,
            place_of_employment = form.place_of_employment.data,
            certification = form.certification.data,
            street = form.street.data,
            city  = form.city.data,
            state = form.state.data,
            zip  = form.zip.data)
        db.session.add(user)
        db.session.commit()
        flash('User has been Added',category='success')
        return redirect(url_for('detail',id=user.id))
    return render_template('adduser.html',form=form,title=title)



@app.route('/deleteuser/<int:id>',methods=['GET','POST'])
@login_required
def deleteuser(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User successfully deleted!',category='success')
    return redirect(url_for('main'))







@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out!', category='success')
    return redirect(url_for('login'))
