from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import BIGINT
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    access_level = db.Column(db.Integer)
   
class Trv(db.Model):
    __tablename__ = 'trv'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime(timezone=True), default=func.now())
    temp = db.Column(db.Float)
    extend_existing=True

class CHILLER_INST(db.Model):
    ID = db.Column(db.BIGINT, primary_key=True)
    DATA = db.Column(db.DateTime)
    T1_PRE = db.Column(db.Float)
    T2_PRE = db.Column(db.Float)
    T1_CHILLER = db.Column(db.Float)
    T2_CHILLER = db.Column(db.Float)
    T3_CHILLER = db.Column(db.Float)
    ENCH_PRE = db.Column(db.Float)
    RENOV_PRE = db.Column(db.Float)
    ENCH_CHILLER = db.Column(db.Float)
    RENOV_CHILLER = db.Column(db.Float)
    L_CHEIA_INTEIROS = db.Column(db.BIGINT)
    RETORNO_INTEIROS = db.Column(db.BIGINT)
    TOTALIZ_INTEIROS = db.Column(db.BIGINT)
    L_EVISCERACAO = db.Column(db.BIGINT)
    VELOCIDADE = db.Column(db.BIGINT)
    RENOV_PRE_M = db.Column(db.Float)
    RENOV_CHILLER_M = db.Column(db.Float)
    T1_PRE_M = db.Column(db.Float)
    T2_PRE_M = db.Column(db.Float)
    T1_CHILLER_M = db.Column(db.Float)
    T2_CHILLER_M = db.Column(db.Float)
    T3_CHILLER_M = db.Column(db.Float)
    L_PENDURA = db.Column(db.BIGINT)
    T_AT_H_P_CURVA = db.Column(db.BIGINT)
    T_AT_H_P_ESTRADA = db.Column(db.BIGINT)
    T_AT_H_P_AQUIFERO = db.Column(db.BIGINT)
    T_AT_H_P_LIMOEIRO = db.Column(db.BIGINT)
    T_AT_H_P_CONSUMO = db.Column(db.BIGINT)
    T_AN_H_P_CURVA = db.Column(db.BIGINT)
    T_AN_H_P_ESTRADA = db.Column(db.BIGINT)
    T_AN_H_P_AQUIFERO = db.Column(db.BIGINT)
    T_AN_H_P_LIMOEIRO = db.Column(db.BIGINT)
    T_AN_H_P_CONSUMO = db.Column(db.BIGINT)
    P_HORA_P_CURVA = db.Column(db.BIGINT)
    P_HORA_P_ESTRADA = db.Column(db.BIGINT)
    P_HORA_P_AQUIFERO = db.Column(db.BIGINT)
    P_HORA_P_LIMOEIRO = db.Column(db.BIGINT)
    P_HORA_P_CONSUMO = db.Column(db.BIGINT)
    NIVEL_POCO = db.Column(db.Integer)
