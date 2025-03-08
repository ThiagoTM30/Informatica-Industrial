from pyModbusTCP.client import ModbusClient
from sqlalchemy import engine
from time import sleep
from datetime import datetime
from threading import Thread, Lock
from tabulate import tabulate
from db import Session, Base, engine
from models import DadoCLP
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

class ModbusPersistencia():
    """
    Classe que implementa funcionalidade de persistência de dados
    lidos a partir do protocolo Modbus e também permite a busca de dados históricos
    """
    def __init__(self, server_ip, porta, tags_addrs, scan_time=1):
        """
        Construtor
        """
        self._cliente = ModbusClient(host=server_ip, port=porta)
        self._scan_time = scan_time
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
            while True:
                data = {'timestamp': datetime.now()}
                for tag in self._tags_addrs:
                # Trate a tag 'bits_controle' separadamente
                    if tag == 'nivel_reservatorio':
                        leitura = self._cliente.read_holding_registers(self._tags_addrs[tag], 1)
                        if leitura:
                            valor = leitura[0]
                            # Extraia cada bit (0 a 7)
                            data['nivel_sup_alto'] = (valor >> 0) & 1
                            data['nivel_sup_baixo'] = (valor >> 1) & 1
                            data['nivel_inf_alto'] = (valor >> 2) & 1
                            data['nivel_inf_baixo'] = (valor >> 3) & 1
                            data['nivel_muito_alto'] = (valor >> 4) & 1
                            data['valvula_xp01'] = (valor >> 5) & 1
                            data['valvula_xp02'] = (valor >> 6) & 1
                            data['indicador_alto'] = (valor >> 7) & 1
                        else:
                            # Defina valores padrão em caso de erro
                            for i in range(8):
                                data[f'bit{i}'] = None
                    else:
                        # Leitura normal para as outras tags (float)
                        leitura = self._cliente.read_holding_registers(self._tags_addrs[tag], 2)
                        if leitura:
                            decoder = BinaryPayloadDecoder.fromRegisters(leitura, byteorder=Endian.Big, wordorder=Endian.Big)
                            data[tag] = decoder.decode_32bit_float()
                        else:
                            data[tag] = None
                dado = DadoCLP(**data)
                with self._lock:
                    self._session.add(dado)
                    self._session.commit()
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
                with self._lock:
                    result = self._session.query(DadoCLP).filter(DadoCLP.timestamp.between(init, final)).all()
                result_fmt_list = [obj.get_attr_printable_list() for obj in result]
                print(tabulate(result_fmt_list,
                headers=[
                "ID", "Timestamp", 
                "nivel_sup_alto", "nivel_sup_baixo", "nivel_inf_alto", "nivel_inf_baixo", "nivel_muito_alto",
                "valvula_xp01", "valvula_xp02", "indicador_alto",
                "Temp R", "Temp S", "Temp T", "Temp Carcaça", 
                "Pressão", "Vazão", "Nível Superior", 
                "Rotação Motor", "Torque Motor", 
                "Potência R", "Potência S", "Potência T", "Potência Total", 
                "FP R", "FP S", "FP T", "FP Total"
                        ]
                ))
        except Exception as e:
            print("Erro: busca de dados ", e.args)

    def run(self):
        self._threads.append(Thread(target=self.guardar_dados))
        self._threads.append(Thread(target=self.acesso_dados_historicos))
        for t in self._threads:
            t.start()
