from cProfile import label
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

nivel_acesso = 0

auth = Blueprint('auth', __name__)

@auth.route('/a_caixa', methods=['GET', 'POST'])
def a_caixa():
    
    return render_template("a_caixa.html", user=current_user)

@auth.route('/a_companhia', methods=['GET', 'POST'])
def a_companhia():
    
    return render_template("a_companhia.html", user=current_user)

@auth.route('/a_consumo', methods=['GET', 'POST'])
def a_consumo():
    
    return render_template("a_consumo.html", user=current_user)

@auth.route('/a_pocos', methods=['GET', 'POST'])
def a_pocos():
    
    return render_template("a_pocos.html", user=current_user)

#-----------------------------------------------------------------------------------------

@auth.route('/e_paletizacao', methods=['GET', 'POST'])
def e_paletizacao():
    
    return render_template("e_paletizacao.html", user=current_user)

@auth.route('/e_salacortes', methods=['GET', 'POST'])
def e_salacortes():
    
    return render_template("e_salacortes.html", user=current_user)

@auth.route('/e_salamaquina', methods=['GET', 'POST'])
def e_salamaquina():
    
    return render_template("e_salamaquina.html", user=current_user)

@auth.route('/e_trv', methods=['GET', 'POST'])
def e_trv():
    
    return render_template("e_trv.html", user=current_user)

#-----------------------------------------------------------------------------------------
@auth.route('/t_caldeira', methods=['GET', 'POST'])
def t_caldeira():
    
    return render_template("t_caldeira.html", user=current_user)

@auth.route('/t_chiller', methods=['GET', 'POST'])
def t_chiller():
    
    return render_template("t_chiller.html", user=current_user)

@auth.route('/t_embsec', methods=['GET', 'POST'])
def t_embsec():
    
    return render_template("t_embsec.html", user=current_user)

@auth.route('/t_paletizacao', methods=['GET', 'POST'])
def t_paletizacao():
    
    return render_template("t_paletizacao.html", user=current_user)

@auth.route('/t_trv', methods=['GET', 'POST'])
def t_trv():
    
    return render_template("t_trv.html", user=current_user)

#-------------------------------------------------------------------------------------------------------------------------------------------------

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                nivel_acesso = user.access_level
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    session.permanent = False

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        access_level = request.form.get('access_level')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, access_level=access_level, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            #login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.users'))

    return render_template("sign_up.html", user=current_user)
