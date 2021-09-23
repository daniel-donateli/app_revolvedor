from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///./banco.db', future=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


from app_revolvedor.domain.models import Revolvedor

def init_db():
  import app_revolvedor.domain.models

  Base.metadata.create_all(bind=engine)
  

def get_revolvedor(revolvedor_id) -> Revolvedor:
  return Revolvedor.query.get(revolvedor_id)
