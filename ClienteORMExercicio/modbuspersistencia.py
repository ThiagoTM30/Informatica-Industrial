from pyModbusTCP.client import ModbusClient
from sqlalchemy import engine
from time import sleep
from datetime import datetime
from threading import Thread,Lock
from tabulate import tabulate
from db import Session, Base, engine
from models import DadoCLP

class ModbusPersistencia():
    """
    Classe que implementa funcionalidade de persistência de dados 
    lidos a partir do protocolo Modbus e também permite a busca de dados históricos
    """
    def __init__(self, server_ip,porta, tags_addrs, scan_time=1):
        """
        Construtor
        """
        self._cliente = ModbusClient(host=server_ip, port=porta)
        self._scan_time = 1
        self._tags_addrs = tags_addrs
        self._session = Session()
        Base.metadata.create_all(engine)
        self._lock = Lock()
        self._threads = []

    def guardar_dados(self):
        """
        Método para leitura de um dado da tabela MODBUS
        """
        try:
            print("Persistência iniciada")
            self._cliente.open()
            data = {}
            while True:
                data['timestamp'] = datetime.now()
                for tag in self._tags_addrs:
                    data[tag]= self._cliente.read_holding_registers(self._tags_addrs[tag],1)[0]
                dado = DadoCLP(**data) #inicializa todos os atributos do DadoCLP
                self._lock.acquire()
                self._session.add(dado)
                self._session.commit()
                self._lock.release()
                sleep(self._scan_time)

        except Exception as e:
            print("Erro na persistência dos dados: ", e.args)

    def acesso_dados_historicos(self):
        """
        Método que permite ao usuário acessar dados históricos
        """
        try:
            print("Bem vindo ao sistema de busca de dados históricos")
            while True:
                init = input("Digite o horário inicial para a busca (DD/MM/AAAA HH:MM:SS):")
                final = input("Digite o horário final para a busca (DD/MM/AAAA HH:MM:SS):")
                init = datetime.strptime(init, '%d/%m/%Y %H:%M:%S')
                final = datetime.strptime(final, '%d/%m/%Y %H:%M:%S')
                self._lock.acquire()
                result = self._session.query(DadoCLP).filter(DadoCLP.timestamp.between(init,final)).all()
                self._lock.release()
                result_fmt_list = [obj.get_attr_printable_list() for obj in result] #lista de listas   na interface grafica nao precisa dessas duas linhas           
                print(tabulate(result_fmt_list, headers=DadoCLP.__table__.columns.keys()))


        except Exception as e:
            print("Erro: busca de dados ", e.args)

    def run(self):
        self._threads.append(Thread(target=self.guardar_dados))
        self._threads.append(Thread(target=self.acesso_dados_historicos))
        for t in self._threads:
            t.start()

    