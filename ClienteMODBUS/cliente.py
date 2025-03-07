from pyModbusTCP.client import ModbusClient
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian
from time import sleep
from datetime import datetime

_tags = {}

class ClienteMODBUS():
    """
    Classe Cliente MODBUS
    """
    def __init__(self,server_ip,porta,scan_time=1):
        """
        Construtor
        """
        self.cliente = ModbusClient(host=server_ip,port=porta)
        self.scan_time = scan_time
        self._meas = {}
        self._meas['timestamp'] = None
        self._meas['values'] = {}
        self._tags = {
            'sensores': {'addr': 716, 'float': False, 'mult': 1, 'lista': True},
            'temp_rmotor': {'addr': 700, 'float': True, 'mult': 10, 'lista': False},
            'temp_smotor': {'addr': 702, 'float': True, 'mult': 10, 'lista': False},
            'temp_tmotor': {'addr': 704, 'float': True, 'mult': 10, 'lista': False},
            'temp_carcaca': {'addr': 706, 'float': True, 'mult': 10, 'lista': False},
            'pressao': {'addr': 710, 'float': True, 'mult': 1, 'lista': False},
            'vazao': {'addr': 712, 'float': True, 'mult': 1, 'lista': False},
            'nivel': {'addr': 714, 'float': True, 'mult': 1, 'lista': False},
            'rot_rpm': {'addr': 727, 'float': True, 'mult': 1, 'lista': False},
            'torque': {'addr': 1334, 'float': True, 'mult': 1, 'lista': False},
            'pot_r': {'addr': 852, 'float': False, 'mult': 1, 'lista': False},
            'pot_s': {'addr': 853, 'float': False, 'mult': 1, 'lista': False},
            'pot_t': {'addr': 854, 'float': False, 'mult': 1, 'lista': False},
            'pot_total': {'addr': 855, 'float': False, 'mult': 1, 'lista': False},
            'fp_r': {'addr': 868, 'float': False, 'mult': 1000, 'lista': False},
            'fp_s': {'addr': 869, 'float': False, 'mult': 1000, 'lista': False},
            'fp_t': {'addr': 870, 'float': False, 'mult': 1000, 'lista': False},
            'fp_tot': {'addr': 871, 'float': False, 'mult': 1000, 'lista': False}
        }

    def readData(self):
        """
        Método de leitura dos dados via MODBUS
        """
        if not self.cliente.is_open():
            self.cliente.open()
        self._meas['timestamp'] = datetime.now()
        for key,value in self._tags.items():
            if 'float' in value and value['float'] is True:
                self._meas['values'][key] = self.readFloat(value['addr']) * value['mult']
            elif 'lista' in value and value['lista'] is True:
                self._meas['values'][key] = self.readLista(value['addr']) * value['mult']
            else: 
                self._meas['values'][key] = self.readInt(value['addr']) * value['mult']
        for key, val in self._meas['values'].items():
            print(f"{key}: {val}")
    
    def readFloat(self,addr):
        """  
        Método auxiliar para a leitura de valores com ponto flutuante
        """
        leitura = self.cliente.read_holding_registers (addr,2)
        decoder = BinaryPayloadDecoder.fromRegisters(leitura, byteorder=Endian.Big, wordorder=Endian.Big)
        return decoder.decode_32bit_float()  
    
    def readLista(self, addr):
        """
        Método auxiliar para a leitura de todos os valores individuais de uma lista
        """
        leitura = self.cliente.read_holding_registers(addr, 1)[0]
        lista_bits = [int(x) for x in "{0:016b}".format(leitura)]
        # Imprime todas as posições com seus respectivos índices (começando em 1)
        return lista_bits[::-1]
    
    def readInt(self,addr):
        """
        Método auxiliar para a leitura de inteiros
        """
        return self.cliente.read_holding_registers(addr,1)[0]   
