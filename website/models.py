from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(50))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    access_level = db.Column(db.Integer)
    notes = db.relationship('Note')
   
class Trv(db.Model):
    __tablename__ = 'trv'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    temp = db.Column(db.Float)
    extend_existing=True

class T1Pre(db.Model):
    __tablename__ = 't1pre'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    temp = db.Column(db.Float)
    extend_existing=True

class T2Pre(db.Model):
    __tablename__ = 't2pre'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    temp = db.Column(db.Float)
    extend_existing=True

class T1Chi(db.Model):
    __tablename__ = 't1chi'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    temp = db.Column(db.Float)
    extend_existing=True

class T2Chi(db.Model):
    __tablename__ = 't2chi'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    temp = db.Column(db.Float)
    extend_existing=True

class T3Chi(db.Model):
    __tablename__ = 't3chi'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    temp = db.Column(db.Float)
    extend_existing=True
