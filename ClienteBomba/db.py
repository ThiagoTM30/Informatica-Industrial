import os
"""
Objetos do sqlalchemy core para a realização da conexão e operação do Banco de Dados
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_path = os.path.abspath("C:/Users/Arthur/Documents/GitHub/Informatica-Industrial/ClienteBomba/data/db.data")
DB_CONNECTION = f"sqlite:///{db_path}?check_same_thread=False"
engine = create_engine(DB_CONNECTION, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
