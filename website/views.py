import datetime
from datetime import date, datetime
from multiprocessing import cpu_count
from sqlite3 import Date
from turtle import bgcolor
from xmlrpc.client import DateTime
from flask import Blueprint, render_template, request, flash, jsonify, url_for, abort, redirect
from flask_login import login_required, current_user
from .models import Note, Trv, User
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

    return render_template("t_trv.html", user=current_user, trv_data=chart_data)




def generate_simulated_data():
    start_date = datetime.datetime.now() - datetime.timedelta(days=5)
    end_date = datetime.datetime.now()
    current_date = start_date

    while current_date <= end_date:
        # Generate a random temperature between -40 and -20
        temp = round(random.uniform(-40, -20), 2)

        # Create a new Trv record
        trv = Trv(time=current_date, temp=temp)
        db.session.add(trv)

        current_date += datetime.timedelta(minutes=5)

    db.session.commit()




@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    trv_data = Trv.query.order_by(Trv.time.desc()).limit(20).all()
    #generate_simulated_data()

    return render_template("home.html", user=current_user, trv_data=trv_data)



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
