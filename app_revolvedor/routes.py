from app_revolvedor.domain import revolvedor
from app_revolvedor.domain.models import Medida, Revolvedor
from flask.helpers import url_for
from flask import Response
from werkzeug.utils import redirect

import os
import datetime

from flask import session
from flask import request
from flask.templating import render_template

from app_revolvedor import app
from app_revolvedor import db

app.secret_key = os.getenv('SECRET_KEY')

LIGAR = False

date_time = datetime.datetime.today()

@app.route('/api/<int:revolvedor_id>', methods=['GET','POST'])
def api_revolvedor(revolvedor_id):
  if request.method == 'POST':
    request_time = datetime.datetime.now()
    data = request.get_json()
    if data:
      if data['temperaturas'] and data['motivo']:
        revolvedor = db.get_revolvedor(revolvedor_id)
        if revolvedor == None:
          return Response(status=404)
        novo_id = 1
        novo_id += len(Medida.query.all())
        global LIGAR
        LIGAR = data['ligado']
        m = Medida(id_medida=novo_id, id_revolvedor=revolvedor_id, temperaturas=data['temperaturas'], ligado=LIGAR, motivo=data['motivo'], datetime=request_time)
        db.db_session.add(m)
        db.db_session.commit()
        return Response(status=200)
    return Response(status=400)
  if request.method == 'GET':
    if LIGAR:
      return 'Ligar'
    else:
      return 'Desligar'

@app.route('/')
def index():
  if 'revolvedor_id' in session:
    revolvedor = db.get_revolvedor(session['revolvedor_id'])
    return render_template('user_dashboard.html', date=date_time, revolvedor=revolvedor, ligado=LIGAR , medidas=revolvedor.get_medidas_by_date(date_time))
  return redirect(url_for('user_login'))

@app.route('/login', methods=['GET', 'POST'])
def user_login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    revolvedor_id = int(request.form['revolvedor_select'])
    if validate_login(username, password, revolvedor_id):
      session['revolvedor_id'] = db.get_revolvedor(revolvedor_id).id_revolvedor
      return redirect(url_for('index'))
  return render_template('user_login.html', revolvedores=Revolvedor.query.all())

@app.route('/logout')
def user_logout():
  session.pop('revolvedor_id')
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
      return render_template('admin_dashboard.html', revolvedores=Revolvedor.query.all())
  return render_template('admin_login.html')

@app.route('/create_user', methods=['POST'])
def create_user():
  nome = request.form['nome']
  login = request.form['login']
  password = request.form['password']
  if validate_new_user(nome, login, password):
    novo_id = 1
    novo_id += len(Revolvedor.query.all())
    r = Revolvedor(id_revolvedor=novo_id, nome=nome, login=login, senha=password)
    db.db_session.add(r)
    db.db_session.commit()
  return redirect(url_for('admin_login'))

@app.route('/admin_logout')
def admin_logout():
  session.pop('admin')
  return redirect(url_for('admin_login'))

@app.route('/turn_on_off', methods=['POST'])
def on_off():
  value = request.form['switch-btn']
  if value == 'Ligar':
    LIGAR = True
  else:
    LIGAR = False
  #return redirect(url_for('index'))
  return render_template('user_dashboard.html', date=date_time, revolvedor=revolvedor, ligado=LIGAR , medidas=db.get_revolvedor(session['revolvedor_id']).get_medidas_by_date(date_time))

@app.route('/change_date', methods=['POST'])
def change_date():
  value = request.form['date-picker']
  date = datetime.datetime.strptime(value, '%Y-%m-%d')
  return render_template('user_dashboard.html', date=date, revolvedor=revolvedor, ligado=LIGAR , medidas=db.get_revolvedor(session['revolvedor_id']).get_medidas_by_date(date))

@app.route('/api/<int:revolvedor_id>/get_date/<string:date>')
def get_by_date(revolvedor_id, date):
  revolvedor = db.get_revolvedor(revolvedor_id)
  return {'data': date, 'medidas': [r.as_dict() for r in revolvedor.get_medidas_by_date(date)]}

@app.route('/api/<int:revolvedor_id>/delete')
def delete_revolvedor(revolvedor_id):
  revolvedor = db.get_revolvedor(revolvedor_id)
  db.db_session.delete(revolvedor)
  db.db_session.commit()
  #return Response(status=200)
  return redirect(url_for('admin_login'))

def validate_login(username, password, id_revolvedor):
  revolvedor = db.get_revolvedor(id_revolvedor)
  if revolvedor.verificar_senha(senha=password):
    return True
  return False

def validate_admin(username, password):
  if username == 'admin' and password == '123456':
    return True
  return False

def validate_new_user(nome, username, password):
  return True
