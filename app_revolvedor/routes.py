from flask.helpers import url_for
from flask import Response
from werkzeug.utils import redirect
from app_revolvedor.domain import revolvedor
import os
import datetime

from flask import session
from flask import request
from flask.templating import render_template

from app_revolvedor import app
from app_revolvedor.domain.revolvedor import Revolvedor
from app_revolvedor.domain.user import User
from app_revolvedor import db

app.secret_key = os.getenv('SECRET_KEY')

LIGAR = False

date_time = datetime.datetime.now()
revolvedor1 = Revolvedor(1, 'IFES CAMPUS ITAPINA')
revolvedor1.add_medida('08:30', 24.2, 25.4, 24.6, 25.4, 24.6, 24.5, False, 'Tempo')
revolvedor1.add_medida('08:40', 24.2, 25.4, 24.6, 25.4, 24.6, 24.5, False, 'Tempo')
revolvedor2 = Revolvedor(2, 'SANTA MARIA')
revolvedor2.add_medida('08:30', 24.2, 25.4, 24.6, 25.4, 24.6, 24.5, False, 'Tempo')
revolvedor2.add_medida('08:40', 24.2, 25.4, 24.6, 25.4, 24.6, 24.5, False, 'Tempo')
revolvedores = [revolvedor1, revolvedor2]
user1 = User(1, 'IFESI', revolvedor1)
user2 = User(2, 'SATAM', revolvedor2)
users=[user1, user2]

@app.route('/api/<int:revolvedor_id>', methods=['POST'])
def api_revolvedor(revolvedor_id):
  data = request.get_json()
  if data:
    if data['hora'] and data['temperaturas'] and data['media'] and data['ligado'] and data['motivo']:
      revolvedor = get_revolvedor(revolvedor_id)
      if revolvedor == None:
        return Response(status=404)
      revolvedor.add_medida(data['hora'], data['temperaturas'][0], data['temperaturas'][1], data['temperaturas'][2], 
        data['temperaturas'][3], data['temperaturas'][4], data['media'], data['ligado'], data['motivo'])
      return Response(status=200)
  return Response(status=400)

@app.route('/')
def index():
  if 'user_id' in session:
    user = db.get_user(session['user_id'])
    return render_template('user_dashboard.html', date=date_time, revolvedor=user.revolvedor, ligado=True)
  return redirect(url_for('user_login'))

@app.route('/login', methods=['GET', 'POST'])
def user_login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    if validate_login(username, password):
      session['user_id'] = 1
      return redirect(url_for('index'))
  return render_template('user_login.html', revolvedores=revolvedores)

@app.route('/logout')
def user_logout():
  session.pop('user_id')
  return redirect(url_for('user_login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    if validate_admin(username, password):
      session['admin'] = True
      return redirect(url_for('admin_login'))
  if 'admin' in session:
      return render_template('admin_dashboard.html', users=db.get_users())
  return render_template('admin_login.html')

@app.route('/create_user', methods=['POST'])
def create_user():
  nome = request.form['nome']
  login = request.form['login']
  password = request.form['password']
  if validate_new_user(nome, login, password):
    db.add_user(login, password, nome)
  return redirect(url_for('admin_login'))

@app.route('/admin_logout')
def admin_logout():
  session.pop('admin')
  return redirect(url_for('admin_login'))

def validate_login(username, password):
  if username == 'teste' and password == '123456':
    return True
  return False

def validate_admin(username, password):
  if username == 'admin' and password == '123456':
    return True
  return False

def validate_new_user(nome, username, password):
  return True

def get_user(user_id):
  for user in users:
    if user_id == user.id:
      return user
  return None

def get_revolvedor(revolvedor_id):
  for revolvedor in revolvedores:
    if revolvedor_id == revolvedor.id:
      return revolvedor
  return None