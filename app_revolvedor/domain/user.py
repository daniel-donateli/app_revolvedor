
from app_revolvedor.domain.revolvedor import Revolvedor


class User:
  def __init__(self, id, login, revolvedor: Revolvedor) -> None:
    self.id = id
    self.login = login
    self.revolvedor = revolvedor