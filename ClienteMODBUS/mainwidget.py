from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup, ScanPopup, AtuacaoPopup, DataGraphPopup, QueryHistoricalDataPopup
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window
from threading import Thread, Lock
from time import sleep
import random
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian
from datetime import datetime
from kivy.properties import ListProperty
from timeseriesgraph import TimeSeriesGraph
from sqlalchemy.orm import sessionmaker
from db import engine, Base
from models import DadoCLP

class BoxAlerta(BoxLayout):
    corAlertaT = ListProperty([1, 1, 1, 0.09])
    corAlertaQ = ListProperty([1, 1, 1, 0.09])

class MainWidget(BoxLayout):
    """
    Widget principal
    """
    _updateThread = None
    _updateWidgets = True
    _tags = {}
    _max_points = 20

    def __init__(self, **kwargs):
        """
        Construtor do widget principal
        """
        super().__init__()
        self._scan_time = kwargs.get('scan_time')
        self._serverIP = kwargs.get('server_ip')
        self._serverPort = kwargs.get('server_port')        
        self._modbusPopup = ModbusPopup(self._serverIP, self._serverPort) 
        self._scanPopup = ScanPopup(scantime=self._scan_time)
        self._atuacaoPopup = AtuacaoPopup()
        self._modbusClient = ModbusClient(host=self._serverIP, port=self._serverPort)
        self._addrPartida = None
        self._lock = Lock()
        self._meas = {}
        self._meas['timestamp'] = None
        self._meas['values'] = {}
        for key, value in kwargs.get('modbus_addr').items():
            if key == 'sensores':
                plot_color = (1, 0, 0, 1)
            else:
                plot_color = (random.random(), random.random(), random.random(), 1)            
            self._tags[key] = value.copy()  # Cria uma cópia do dicionário original
            self._tags[key]['color'] = plot_color
        # Plotar gráficos em tempo real    
        self._torque_graph = DataGraphPopup(self._max_points, self._tags['torque']['color'], 'Torque', self._tags['torque']['unidade'], self._tags['torque']['ymax'], self._tags['torque']['y_ticks_major'])
        self._nivel_graph = DataGraphPopup(self._max_points, self._tags['nivel']['color'], 'Nível', self._tags['nivel']['unidade'], self._tags['nivel']['ymax'], self._tags['nivel']['y_ticks_major'])
        self._rot_rpm_graph = DataGraphPopup(self._max_points, self._tags['rot_rpm']['color'], 'Rotações', self._tags['rot_rpm']['unidade'], self._tags['rot_rpm']['ymax'], self._tags['rot_rpm']['y_ticks_major'])
        self._pressao_graph = DataGraphPopup(self._max_points, self._tags['pressao']['color'], 'Pressão', self._tags['pressao']['unidade'], self._tags['pressao']['ymax'], self._tags['pressao']['y_ticks_major'])
        self._vazao_graph = DataGraphPopup(self._max_points, self._tags['vazao']['color'], 'Vazão', self._tags['vazao']['unidade'], self._tags['vazao']['ymax'], self._tags['vazao']['y_ticks_major'])
        # self._graph = HistoricalDataGraphPopup(self._max_points, self._tags)        
        self._queryPopup = QueryHistoricalDataPopup(xmax=self._max_points, tags=self._tags)
        Base.metadata.create_all(engine)
        self._session = sessionmaker(bind=engine)()

    def startDataRead(self, ip, port):
        """
        Método utilizado para configurar IP e porta do servidor MODBUS e
        inicializar uma thread para a leitura dos dados e atualização da interface 
        gráfica.
        """
        self._addrPartida = 1319 if self._addrPartida is None else self._addrPartida
        self._serverIP = ip
        self._serverPort = port
        self._modbusClient.host = self._serverIP
        self._modbusClient.port = self._serverPort
        try:
            Window.set_system_cursor("wait")
            self._modbusClient.open()
            Window.set_system_cursor("arrow")
            if self._modbusClient.is_open:
                self._updateThread = Thread(target=self.updater)
                self._updateThread.start()
                self.ids.img_con.source = '../imgs/conectado.png'
                self._modbusPopup.dismiss()
            else:
                self._modbusPopup.setInfo("Falha na conexão com o servidor")
        except Exception as e:
            print("Erro:", e.args)
        
    def save_to_db(self):
        data_to_store = {'timestamp': self._meas['timestamp']}
        for key, value in self._meas['values'].items():
            if key == "sensores":
                # Extrai os bits e os armazena individualmente
                for i, bit in enumerate(value):
                    data_to_store[f'sensor_{i}'] = bit
            else:
                data_to_store[key] = value
        with self._lock:
            dado = DadoCLP(**data_to_store)
            self._session.add(dado)
            self._session.commit()
    
    def readData(self):
        """
        Método de leitura dos dados via MODBUS.
        """
        self._meas['timestamp'] = datetime.now()
        for key, value in self._tags.items():
            if 'float' in value and value['float'] is True:
                self._meas['values'][key] = self.readFloat(value['addr']) / value['mult']
            elif 'lista' in value and value['lista'] is True:
                self._meas['values'][key] = self.readLista(value['addr'])
            else: 
                self._meas['values'][key] = self.readInt(value['addr']) / value['mult']
        self.save_to_db()
        # print(self._meas)
    
    def readFloat(self, addr):
        """
        Método auxiliar para a leitura de valores com ponto flutuante.
        """
        with self._lock:
            leitura = self._modbusClient.read_holding_registers(addr, 2)
        decoder = BinaryPayloadDecoder.fromRegisters(leitura, byteorder=Endian.Big, wordorder=Endian.Big)
        return decoder.decode_32bit_float()
    
    def readLista(self, addr):
        """
        Método auxiliar para a leitura de todos os valores individuais de uma lista.
        """
        with self._lock:
            leitura = self._modbusClient.read_holding_registers(addr, 1)[0]
        lista_bits = [int(x) for x in "{0:016b}".format(leitura)]
        return lista_bits[::-1]
    
    def readInt(self, addr):
        """
        Método auxiliar para a leitura de inteiros.
        """
        with self._lock:
            leitura = self._modbusClient.read_holding_registers(addr, 1)
        if leitura is None:
            print(f"[DEBUG] readInt retornou None para o endereço {addr}")
            return 0  # ou outra estratégia de tratamento
        return leitura[0]
    
    def updater(self):
        """
        Método que invoca as rotinas de leitura dos dados, atualização da interface
        e inserção dos dados no Banco de dados.
        """
        try:
            while self._updateWidgets:
                self.readData()
                self.updateGUI()
                sleep(self._scan_time / 1000)
        except Exception as e:
            self._modbusClient.close()
            print("Erro:", e.args)
            
    def updateGUI(self):
        """
        Método para atualização de interface gráfica a partir dos dados lidos.
        """
        # Atualização dos labels
        for key, value in self._tags.items():
            if key in self.ids and key in self._meas['values']:
                valor = round(self._meas['values'][key], 2)
                self.ids[key].text = str(valor)
                
        # Atualização do Nível da Água
        self.ids.lb_nivel.size = (self.ids.lb_nivel.size[0], (self._meas['values']['nivel'] / 100) * 50)
        
        # Atualização da Medida da Pressão
        self.ids.lb_pressao.size = ((self._meas['values']['pressao'] / self._tags['pressao']['ymax']) * 85, self.ids.lb_pressao.size[1])
        
        # Atualização da Medida da Vazão
        self.ids.lb_vazao.size = ((self._meas['values']['vazao'] / self._tags['vazao']['ymax']) * 85, self.ids.lb_vazao.size[1])
        
        # Atualização dos Gráficos em tempo real
        self._torque_graph.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['torque']), 0)
        self._nivel_graph.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['nivel']), 0)
        self._vazao_graph.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['vazao']), 0)
        self._rot_rpm_graph.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['rot_rpm']), 0)
        self._pressao_graph.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['pressao']), 0) 

        # # Atualização do gráfico histórico
        # current_var = self._graph.current_variable
        # if current_var in self._meas['values']:
        #     raw_value = self._meas['values'][current_var]
        #     self._graph.ids.graph.updateGraph((self._meas['timestamp'], raw_value), 0)
        # elif current_var.startswith('sensor_'):
        #     bit_index = int(current_var.split('_')[1])
        #     sensor_values = self._meas['values'].get('sensores', [0] * 8)
        #     if 0 <= bit_index < 8:
        #         bit_value = sensor_values[bit_index]
        #         self._graph.ids.graph.updateGraph((self._meas['timestamp'], bit_value), 0)
        
        # Atualiza o visor de apoio ao acionamento de motor
        self.atualizaVisor(self._addrPartida)
        
        # Atualiza a cor dos triângulos de alerta
        self.mudaCor()
    
    def atualizaVisor(self, addr):
        """ 
        Método que modifica a string mostrada no visor.
        """
        with self._lock:
            if addr == 1312:
                self.ids.visor_part.text = 'Inversor'
               
            elif addr == 1316:
                
                self.ids.visor_part.text = 'Soft-start'
            elif addr == 1319:
                
                self.ids.visor_part.text = 'Partida Direta'

    def stopRefresh(self):
        self._updateWidgets = False
    
    def ligaMotor(self, addr):
        """
        Aciona a partida do motor selecionado.
        """
        with self._lock:
            self._modbusClient.write_single_register(addr, 1)
    
    def desligaMotor(self, addr):
        """ 
        Desliga o motor selecionado.
        """
        with self._lock:
            self._modbusClient.write_single_register(addr, 0)
        
    def defineVel(self, vel):
        """
        Define a frequência do inversor.
        """
        with self._lock:
            if self._addrPartida == 1312:
                self._modbusClient.write_single_register(1313, vel * 10)
    
    def defineAcel(self,acel,desacel):
        """
        Define a curva de aceleração e desaceleração
        """
        with self._lock:
            if self._addrPartida ==1312:
                self._modbusClient.write_single_register(self._addrPartida + 2, int(acel))
                self._modbusClient.write_single_register(self._addrPartida + 3, int(desacel))
            else:
                self._modbusClient.write_single_register(self._addrPartida + 1, int(acel))
                self._modbusClient.write_single_register(self._addrPartida + 2, int(desacel))
    
    def mudaCor(self):
        for key, value in self._tags.items():
            if key in self.ids and key in self._meas['values']:
                id_correto = f"alerta_{key}"
                if self._meas['values'][key] / self._tags[key]['ymax'] > 0.8 and self._meas['values'][key] / self._tags[key]['ymax'] <= 0.9:
                    self.ids[id_correto].corAlertaT = (1, 0.9, 0, 1)
                elif self._meas['values'][key] / self._tags[key]['ymax'] > 0.9:
                    self.ids[id_correto].corAlertaQ = (1, 0, 0, 1)
                    self.ids[id_correto].corAlertaT = (1, 0, 0, 1)
                else:
                    self.ids[id_correto].corAlertaQ = (1, 1, 1, 0.09) 
                    self.ids[id_correto].corAlertaT = (1, 1, 1, 0.09)