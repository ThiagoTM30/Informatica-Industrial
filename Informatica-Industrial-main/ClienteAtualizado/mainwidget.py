from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup, ScanPopup, AtuacaoPopup, DataGraphPopup, HistoricalDataGraphPopup
from pyModbusTCP.client import ModbusClient
from kivy.core.window import Window
from threading import Thread
from time import sleep
import random
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian
from datetime import datetime
from timeseriesgraph import TimeSeriesGraph

#não apagar ok

class MainWidget(BoxLayout):
    """
    widget principal
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
        self._modbusPopup = ModbusPopup(self._serverIP,self._serverPort) 
        self._scanPopup = ScanPopup(scantime= self._scan_time)
        self._atuacaoPopup = AtuacaoPopup()
        self._modbusClient = ModbusClient(host=self._serverIP,port=self._serverPort)
        self._meas = {}
        self._meas['timestamp'] = None
        self._meas['values'] = {}
        for key, value in kwargs.get('modbus_addr').items():
            if key == 'torque':
                plot_color = (1, 0, 0, 1)
            else:
                plot_color = (random.random(), random.random(), random.random(), 1)            
            self._tags[key] = value.copy() #Cria uma cópia do dicionário original e adiciona a chave 'color'
            self._tags[key]['color'] = plot_color
        #plotar graficos tempo real    
        self._torque_graph = DataGraphPopup(self._max_points,self._tags['torque']['color'],'Torque',self._tags['torque']['unidade'],self._tags['torque']['ymax'],self._tags['torque']['y_ticks_major'])
        self._nivel_graph = DataGraphPopup(self._max_points, self._tags['nivel']['color'],'Nível',self._tags['nivel']['unidade'],self._tags['nivel']['ymax'],self._tags['nivel']['y_ticks_major'])
        self._rot_rpm_graph = DataGraphPopup(self._max_points, self._tags['rot_rpm']['color'],'Rotações',self._tags['rot_rpm']['unidade'],self._tags['rot_rpm']['ymax'],self._tags['rot_rpm']['y_ticks_major'])
        self._pressao_graph = DataGraphPopup(self._max_points, self._tags['pressao']['color'],'Pressão',self._tags['pressao']['unidade'],self._tags['pressao']['ymax'],self._tags['pressao']['y_ticks_major'])
        self._vazao_graph = DataGraphPopup(self._max_points, self._tags['vazao']['color'],'Vazão',self._tags['vazao']['unidade'],self._tags['vazao']['ymax'],self._tags['vazao']['y_ticks_major'])
        #plotar grafico dados historicos
        self._graph = HistoricalDataGraphPopup(self._max_points,self._tags)
    
    def startDataRead(self, ip, port):
        """
        Metodo utilizado para a configuração do IP e porta do servidor MODBUS e
        inicializar uma thread para a leitura dos dados e atualizaçao da interface 
        gráfica
        """
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
                self.ids.img_con.source = 'imgs/conectado.png'
                self._modbusPopup.dismiss()
            else:
              self._modbusPopup.setInfo("Falha na conexão com o servidor")
        except Exception as e:
            print("Erro:",e.args)
    
    def readData(self):
        """
        Método de leitura dos dados via MODBUS
        """
        self._meas['timestamp'] = datetime.now()
        for key,value in self._tags.items():
            if 'float' in value and value['float'] is True:
                self._meas['values'][key] = self.readFloat(value['addr']) / value['mult']
            elif 'lista' in value and value['lista'] is True:
                self._meas['values'][key] = self.readLista(value['addr']) 
            else: 
                self._meas['values'][key] = self.readInt(value['addr']) / value['mult']
        print(self._meas)
    
    def readFloat(self,addr):
        """  
        Método auxiliar para a leitura de valores com ponto flutuante
        """
        leitura = self._modbusClient.read_holding_registers (addr,2)
        decoder = BinaryPayloadDecoder.fromRegisters(leitura, byteorder=Endian.Big, wordorder=Endian.Little)
        return decoder.decode_32bit_float()  
    
    def readLista(self, addr):
        """
        Método auxiliar para a leitura de todos os valores individuais de uma lista
        """
        leitura = self._modbusClient.read_holding_registers(addr, 1)[0]
        lista_bits = [int(x) for x in "{0:016b}".format(leitura)]
        # Imprime todas as posições com seus respectivos índices (começando em 1)
        return lista_bits[::-1]
    
    def readInt(self,addr):
        """
        Método auxiliar para a leitura de inteiros
        """
        return self._modbusClient.read_holding_registers(addr,1)[0] 
    
    def updater(self):
        """
        Metodo que invoca as rotinas de leitura dos dados, atualizaçao da 
        interface e inserção dos dados no Banco de dados
        """
        try:
            while self._updateWidgets:
                self.readData()
                self.updateGUI()
                #ler os dados MODBUS, atualizar interface e inserir os dados
                sleep(self._scan_time/1000)
        except Exception as e:
            self._modbusClient.close()
            print("Erro:",e.args)
            
    def updateGUI(self):
        """
        Método para atualização de interface gráfica a partir dos dados lidos
        """
        #Atualização dos labels
        for key, value in self._tags.items():
            if key in self.ids and key in self._meas['values']:  # Verifica se o ID e a chave existem
                valor = round(self._meas['values'][key], 2)  # Limita a 2 casas decimais
                self.ids[key].text = str(valor)
                
        #Atualização do Nivel da Agua
        self.ids.lb_nivel.size = (self.ids.lb_nivel.size[0],(self._meas['values']['nivel']/100)*50) #Acessa o widget lb_nivel no .kv

        #Atualição do Grafico tempo real
        self._torque_graph.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['torque']), 0) 
        self._nivel_graph.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['nivel']), 0)
        self._vazao_graph.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['vazao']), 0)
        self._rot_rpm_graph.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['rot_rpm']), 0)
        self._pressao_graph.ids.graph.updateGraph((self._meas['timestamp'], self._meas['values']['pressao']), 0) 

        # Atualização do gráfico histórico
        current_var = self._graph.current_variable
        if current_var in self._meas['values']:  # Sensores normais
            raw_value = self._meas['values'][current_var]
            self._graph.ids.graph.updateGraph((self._meas['timestamp'], raw_value), 0)
        elif current_var.startswith('sensor_'):  # Sensores binários
            bit_index = int(current_var.split('_')[1])
            sensor_values = self._meas['values'].get('sensores', [0]*8)
            if 0 <= bit_index < 8:
                bit_value = sensor_values[bit_index]
                self._graph.ids.graph.updateGraph((self._meas['timestamp'], bit_value), 0)

    def stopRefresh(self):
        self._updateWidgets = False