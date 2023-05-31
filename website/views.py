import datetime
from datetime import date, datetime
from multiprocessing import cpu_count
from sqlite3 import Date
from turtle import bgcolor
from xmlrpc.client import DateTime
from flask import Blueprint, render_template, request, flash, jsonify, url_for, abort, redirect
from flask_login import login_required, current_user
from .models import Note, Trv, User, T1Pre, T2Pre, T1Chi, T2Chi, T3Chi, AlarmGroup, AlarmMessage
from . import db
import json
import psutil
import plotly.graph_objects as go
import plotly.utils


import random
import datetime
from sqlalchemy.sql import func

views = Blueprint('views', __name__)

@views.route('/t_trv', methods=['GET', 'POST'])
@login_required
def trv():
    
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    trv_data = Trv.query.order_by(Trv.time.desc()).limit(20).all()

    if request.method == 'POST':
        if start_date == '' and end_date == '':
            trv_data = Trv.query.all()
        else:
            trv_data = Trv.query.filter(Trv.time.between(start_date, end_date)).order_by(Trv.time.desc()).all()

    # Convert data to the desired format for the chart and reverse the order
    chart_data = []
    for data_point in trv_data[::-1]:
        chart_data.append({
            'x': data_point.time.strftime('%Y-%m-%d %H:%M'),  # Format the time as desired
            'y': data_point.temp
        })

    if current_user.access_level == 5:
        print("test")
        return render_template("t_trv.html", user=current_user, trv_data=chart_data)
    else:
        abort(403)




def generate_simulated_data():
    start_date = datetime.datetime.now() - datetime.timedelta(days=5)
    end_date = datetime.datetime.now()
    current_date = start_date

    while current_date <= end_date:
        # Generate a random temperature between -40 and -20
        temptrv = round(random.uniform(-40.0, -38.1), 2)
        tempt1pre = round(random.uniform(3.0, 5.1), 2)
        tempt2pre = round(random.uniform(3.0, 5.1), 2)
        tempt1chi = round(random.uniform(3.0, 5.1), 2)
        tempt2chi = round(random.uniform(3.0, 5.1), 2)
        tempt3chi = round(random.uniform(3.0, 5.1), 2)

        # Create a new Trv record
        trv = Trv(time=current_date, temp=temptrv)
        t1pre = T1Pre(time=current_date, temp=tempt1pre)
        t2pre = T2Pre(time=current_date, temp=tempt2pre)
        t1chi = T1Chi(time=current_date, temp=tempt1chi)
        t2chi = T2Chi(time=current_date, temp=tempt2chi)
        t3chi = T3Chi(time=current_date, temp=tempt3chi)
        db.session.add(trv)
        db.session.add(t1pre)
        db.session.add(t2pre)
        db.session.add(t1chi)
        db.session.add(t2chi)
        db.session.add(t3chi)
        current_date += datetime.timedelta(minutes=5)

    db.session.commit()




@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    trv_data = Trv.query.order_by(Trv.time.desc()).limit(20).all()
    t1pre_data = T1Pre.query.order_by(T1Pre.time.desc()).limit(10).all()
    t2pre_data = T2Pre.query.order_by(T2Pre.time.desc()).limit(10).all()
    t1chi_data = T1Chi.query.order_by(T1Chi.time.desc()).limit(10).all()
    t2chi_data = T2Chi.query.order_by(T2Chi.time.desc()).limit(10).all()
    t3chi_data = T3Chi.query.order_by(T3Chi.time.desc()).limit(10).all()
    #generate_simulated_data()

    # Convert data to the desired format for the chart and reverse the order
    chart_data = []
    for data_point in trv_data[::-1]:
        chart_data.append({
            'x': data_point.time.strftime('%Y-%m-%d %H:%M'),  # Format the time as desired
            'y': data_point.temp
        })
    
    chart_data1 = []
    for data_point in t1pre_data[::-1]:
        chart_data1.append({
            'x': data_point.time.strftime('%Y-%m-%d %H:%M'),  # Format the time as desired
            'y': data_point.temp
        })
    
    chart_data2 = []
    for data_point in t2pre_data[::-1]:
        chart_data2.append({
            'x': data_point.time.strftime('%Y-%m-%d %H:%M'),  # Format the time as desired
            'y': data_point.temp
        })
    
    chart_data3 = []
    for data_point in t1chi_data[::-1]:
        chart_data3.append({
            'x': data_point.time.strftime('%Y-%m-%d %H:%M'),  # Format the time as desired
            'y': data_point.temp
        })

    chart_data4 = []
    for data_point in t2chi_data[::-1]:
        chart_data4.append({
            'x': data_point.time.strftime('%Y-%m-%d %H:%M'),  # Format the time as desired
            'y': data_point.temp
        })
    
    chart_data5 = []
    for data_point in t3chi_data[::-1]:
        chart_data5.append({
            'x': data_point.time.strftime('%Y-%m-%d %H:%M'),  # Format the time as desired
            'y': data_point.temp
        })

    return render_template("home.html", user=current_user, trv_data=chart_data, t1pre_data=chart_data1, t2pre_data=chart_data2, t1chi_data=chart_data3, t2chi_data=chart_data4, t3chi_data=chart_data5)



@views.route('/t_caldeira')
def t_caldeira():
    
    cpu_usage = psutil.cpu_percent()

    return render_template('t_caldeira.html', user=current_user, cpu_usage=cpu_usage)

@views.route('/realtime')
def realtime():
    
    cpu_usage = psutil.cpu_percent()

    return render_template('realtime.html', user=current_user, cpu_usage=cpu_usage)



@views.route('/get_updated_value')
def get_updated_value():
    # Retrieve the CPU usage percentage
    cpu_usage = psutil.cpu_percent()          

    return jsonify(cpu_usage=cpu_usage)

@views.route('/get_updated_value1')
def get_updated_value1():
    # Retrieve the CPU usage percentage
    cpu_usage1 = psutil.cpu_percent()          

    return jsonify(cpu_usage1=cpu_usage1)

@views.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if current_user.access_level != 5:
        abort(403)  # Access denied for non-admin users
    
    user_data = User.query.all()
    return render_template("users.html", user=current_user, user_data=user_data)

@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if current_user.access_level != 5:
        #abort(403)  # Access denied for non-admin users
        return render_template("access_denied.html", user=current_user)
    user_data = User.query.all()
    return render_template("settings.html", user=current_user, user_data=user_data)

@views.route('/access_denied', methods=['GET', 'POST'])
def access_denied():
    
    return render_template("access_denied.html", user=current_user)
    

@views.route('/alarms', methods=['GET', 'POST'])
@login_required
def alarms():
    
    #alarm_data = Alarms.query.all()
    alarm_group_data = AlarmGroup.query.order_by(AlarmGroup.id.desc()).all()
    alarm_message_data = AlarmMessage.query.order_by(AlarmMessage.id.desc()).all()
    return render_template("alarms.html", user=current_user, alarm_group_data=alarm_group_data, alarm_message_data=alarm_message_data)

@views.route('/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    if current_user.access_level != 5:
        abort(403)  # Access denied for non-admin users
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('users'))


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
