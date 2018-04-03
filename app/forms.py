from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField, TextAreaField, HiddenField, IntegerField, FormField, PasswordField, SelectMultipleField, FileField, DateTimeField, DecimalField, validators
from wtforms.validators import Required, Length, Email, EqualTo, ValidationError
from app import db

from models import User, ROLE_ADMIN, INACTIVE_USER, Phone, Department, Member_Department, Family_Relationship,Family


DAYS = [
    ('', '-- Choose a Day --'),
    ('Mon', 'Mon'),
    ('Tues', 'Tues'),
    ('Wed', 'Wed'),
    ('Thur', 'Thur'),
    ('Fri', 'Fri'),
    ('Sat', 'Sat')
]

TIMES = [
    ("08-09[am]", "08-09[am]"),
    ("09-10[am]", "09-10[am]"),
    ("10-11[am]", "10-11[am]"),
    ("11-12[am]", "11-12[am]"),
    ("12-01[pm]", "12-01[pm]"),
    ("01-02[pm]", "01-02[pm]"),
    ("02-03[pm]", "02-03[pm]"),
    ("03-04[pm]", "03-04[pm]"),
    ("04-05[pm]", "04-05[pm]"),
    ("05-06[pm]", "05-06[pm]"),
    ("06-07[pm]", "06-07[pm]"),
    ("07-08[pm]", "07-08[pm]"),
    ("08-09[pm]", "08-09[pm]")
]

SEM = [
    ('', '-- Choose a Semester --'),
    ('1', 'Semester 1'),
    ('2', 'Semester 2'),
    ('3', 'Semester 3')
]

STATUS = [
    ('0', '0'),
    ('1', '1')
]

SALUTATION = [
    ('DR', 'DR'),
    ('MS', 'MS'),
    ('MR', 'MR'),
    ('MRS', 'MRS'),
    ('NA', 'NA'),
    ('TBA1', 'TBA1'),
    ('TBA2', 'TBA2')
]

ANSWER = [
    ('YES', 'YES'),
    ('NO', 'NO')
]

PRIMARY_SECONDARY=[
    ('', '-- Choose Primary or Secondary --'),
    ('PRIMARY', 'PRIMARY'),
    ('SECONDARY', 'SECONDARY')
]

NETWORK=[
    ('', '-- Choose Digicel or Lime --'),
    ('DIGICEL','DIGICEL'),
    ('LIME','LIME')
]


def getDepartments():
    result = []
    result = [("", "-- Choose a Department --")]
    departments = Department.query.order_by(Department.dept_name).all()
    for department in departments:
        result.append((str(department.id), department.dept_name))
    return result

def getUsers():
    result = []
    result = [("", "-- Choose a Member --")]
    users = User.query.order_by(User.lastname).all()
    for user in users:
        result.append((str(user.id), user.firstname + ' ' + user.lastname))
    return result

def getFamilyTypes():
    result = []
    result = [("", "-- Choose a Relationship --")]
    relationships = Family.query.order_by(Family.type).all()
    for relationship in relationships:
        result.append((str(relationship.id), relationship.type))
    return result


DEPT=getDepartments()
USERS=getUsers()
TYPES=getFamilyTypes()

class DepartmentForm(Form):
    dept_name = SelectField('Department Name',choices=DEPT,validators=[Required()])

class FamilyForm(Form):
    user = SelectField('Member Name',choices=USERS,validators=[Required()])
    type = SelectField('Relationship',choices=TYPES,validators=[Required()])


class LoginForm(Form):
    email = TextField('email', [Required(), Email()])
    password = PasswordField('password', [Required()])

    remember_me = BooleanField('remember_me', default=False)


class UploadForm(Form):
    filexl = FileField(validators=[Required()])


class ChangePasswordForm(Form):
    oldpassword = PasswordField('oldpassword', [Required()])
    password = PasswordField('password', [Required()])
    confirm = PasswordField('confirm', [
        Required(),
        EqualTo('password', message='Passwords must match')
    ])


class ManageUserForm(Form):
    password = PasswordField('password')
    confirm = PasswordField(
        'confirm', [
            EqualTo(
                'password', message='Passwords must match')])
    status = SelectField('status', choices=STATUS, validators=[Required()])
    uwiId = TextField('uwiId', validators=[Required()])
    userInitial = TextField('userInitial', validators=[Required()])
    salutation = SelectField(
        'salutation',
        choices=SALUTATION,
        validators=[
            Required()])
    marker = SelectField('marker', choices=ANSWER, validators=[Required()])
    tutor = SelectField('tutor', choices=ANSWER, validators=[Required()])
    lecturer = SelectField('lecturer', choices=ANSWER, validators=[Required()])


class EditUserForm(Form):
    firstname = TextField('firstname', [Required()])
    lastname = TextField('lastname', [Required()])
    middlename = TextField('middlename')
    picture = FileField('picture')
    occupation = TextField('occupation')
    place_of_employment = TextField('place_of_employment')
    certification = TextField('certification')
    street = TextField('street')
    city = TextField('city')
    state = TextField('state')
    zip = TextField('zip')


class AddUserForm(Form):
    firstname = TextField('firstname', [Required()])
    lastname = TextField('lastname', [Required()])
    middlename = TextField('middlename')
    picture = FileField('picture')
    occupation = TextField('occupation')
    place_of_employment = TextField('place_of_employment')
    certification = TextField('certification')
    street = TextField('street')
    city = TextField('city')
    state = TextField('state')
    zip = TextField('zip')




class EditPhoneForm(Form):
    phone = TextField('Phone',validators=[Required()])
    #primary_secondary = TextField('Primary or Secondary')
    primary_secondary = SelectField('Primary or Secondary',choices=PRIMARY_SECONDARY,validators=[Required()])
    network = SelectField('Network',choices=NETWORK,validators=[Required()])

#class EditDepartmentForm(Form):


class RegistrationForm(Form):
    firstname = TextField('firstname', [Required()])
    lastname = TextField('lastname', [Required()])
    email = TextField('email', [Required(), Email()])
    password = PasswordField('password', [Required()])
    confirm = PasswordField('confirmpassword', [
        Required(),
        EqualTo('password', message='Passwords must match')
    ])
