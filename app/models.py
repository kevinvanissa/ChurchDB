# coding: utf-8
from hashlib import md5
from app import db
from app import app

ROLE_USER = 0
ROLE_ADMIN = 1
ACTIVE_USER = 1
INACTIVE_USER = 0

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    middlename = db.Column(db.String(120))
    password = db.Column(db.String(140))
    status = db.Column(db.SmallInteger, default=INACTIVE_USER)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    picture = db.Column(db.String(100))
    occupation = db.Column(db.String(120))
    place_of_employment = db.Column(db.String(120))
    certification = db.Column(db.String(120))
    street = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    zip = db.Column(db.String(120))


    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return True


    def is_active(self):
        return self.status == ACTIVE_USER

    def is_admin(self):
        return self.role == ROLE_ADMIN

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Member %r %r>' % (self.firstname, self.lastname)


class Family(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(120),nullable=False)


class Church(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    conference = db.Column(db.String(120), nullable=False)


class Member_Church(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    church_id = db.Column(db.Integer, db.ForeignKey('church.id'))


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    phone = db.Column(db.String(120),nullable=False)
    primary_secondary = db.Column(db.String(120))
    network = db.Column(db.String(120))

class Department(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        dept_name = db.Column(db.String(120))

class Member_Department(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

class Family_Relationship(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        family_member = db.Column(db.Integer, db.ForeignKey('user.id'))
        relationship = db.Column(db.String(120))



