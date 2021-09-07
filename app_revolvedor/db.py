from app_revolvedor.domain import revolvedor
from app_revolvedor.domain.revolvedor import Revolvedor
from app_revolvedor.domain.user import User

users = []
revolvedores = []

def init_db():
  revolvedor1 = Revolvedor(1, 'IFES CAMPUS ITAPINA')
  revolvedor1.add_medida('08:30', 24.2, 25.4, 24.6, 25.4, 24.6, 24.5, False, 'Tempo')
  revolvedor1.add_medida('08:40', 24.2, 25.4, 24.6, 25.4, 24.6, 24.5, False, 'Tempo')
  revolvedor2 = Revolvedor(2, 'SANTA MARIA')
  revolvedor2.add_medida('08:30', 24.2, 25.4, 24.6, 25.4, 24.6, 24.5, False, 'Tempo')
  revolvedor2.add_medida('08:40', 24.2, 25.4, 24.6, 25.4, 24.6, 24.5, False, 'Tempo')
  #revolvedores = [revolvedor1, revolvedor2]
  revolvedores.append(revolvedor1)
  revolvedores.append(revolvedor2)
  user1 = User(1, 'IFESI', revolvedor1)
  user2 = User(2, 'SATAM', revolvedor2)
  #users = [user1, user2]
  users.append(user1)
  users.append(user2)

def get_users():
  return users

def get_user(user_id):
  for user in users:
    if user_id == user.id:
      return user
  return None

def add_user(username, senha, nome_revolvedor):
  id = len(users) + 1
  revolvedor = Revolvedor(len(revolvedores), nome_revolvedor)
  user = User(id, username, revolvedor)
  users.append(user)