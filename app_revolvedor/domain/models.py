import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DATE, DATETIME, NUMERIC, TIME, Boolean
from app_revolvedor.db import Base
from werkzeug.security import generate_password_hash, check_password_hash

class Revolvedor(Base):
  __tablename__ = 'revolvedor'
  id_revolvedor = Column(Integer, primary_key=True)
  nome = Column(String(50))
  login = Column(String(20), unique=True)
  senha = Column(String(80))
  medida = relationship('Medida')

  def __init__(self, id_revolvedor=None, nome=None, login=None, senha=None):
    super().__init__()
    self.id_revolvedor = id_revolvedor
    self.nome = nome
    self.login = login
    self.senha = generate_password_hash(senha)

  def as_dict(self):
    return {
      'id_revolvedor': self.id_revolvedor,
      'nome': self.nome,
      'login': self.login,
      'senha': self.senha
    }

  def get_medidas(self):
    return Medida.query.filter(Medida.id_revolvedor == self.id_revolvedor).order_by(Medida.time.asc())
  
  def get_medidas_by_date(self, date):
    if isinstance(date, datetime.datetime):
      date_time = date.date()
    else:
      date_time = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    return Medida.query.filter(Medida.id_revolvedor == self.id_revolvedor, Medida.date == date_time)

  def verificar_senha(self , senha):
    return check_password_hash(self.senha, senha)


class Medida(Base):
  __tablename__ = 'medida'
  id_medida = Column(Integer, primary_key=True)
  date = Column(DATE)
  time = Column(TIME)
  t1 = Column(NUMERIC(3, 1, asdecimal=False))
  t2 = Column(NUMERIC(3, 1, asdecimal=False))
  t3 = Column(NUMERIC(3, 1, asdecimal=False))
  t4 = Column(NUMERIC(3, 1, asdecimal=False))
  t5 = Column(NUMERIC(3, 1, asdecimal=False))
  media = Column(NUMERIC(3, 1, asdecimal=False))
  ligado = Column(Boolean)
  motivo = Column(String(20))
  id_revolvedor = Column(Integer, ForeignKey('revolvedor.id_revolvedor'))

  def __init__(self, id_medida, id_revolvedor=None, temperaturas=[], ligado=False, motivo='', datetime=None) -> None:
    super().__init__()
    self.id_medida = id_medida
    self.id_revolvedor = id_revolvedor
    self.media = sum(temperaturas) / 5
    self.t1 = temperaturas[0]
    self.t2 = temperaturas[1]
    self.t3 = temperaturas[2]
    self.t4 = temperaturas[3]
    self.t5 = temperaturas[4]
    self.ligado = ligado
    self.motivo = motivo
    self.date = datetime.date()
    self.time = datetime.time()
  
  def as_dict(self):
    return {
      'id_medida': self.id_medida,
      'id_revolvedor': self.id_revolvedor,
      'media': self.media,
      'temperaturas': [self.t1, self.t2, self.t3, self.t4, self.t5],
      'ligado': self.ligado,
      'motivo': self.motivo,
      'date': self.date
    }