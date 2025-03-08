from pyModbusTCP.server import DataBank, ModbusServer
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants import Endian
import random
from time import sleep


class ServidorMODBUS():
    """
    Classe Servidor Modbus
    """


    def __init__(self,host_ip,port):
        """
        Construtor
        """
        self._db = DataBank()
        self._server = ModbusServer(host=host_ip,port=port,no_block=True,data_bank = self._db)
       
    def run(self):
        """
        Execução servidor Modbus
        """
        try:
            self._server.start()
            print("Servidor MODBUS em execução")
            while True:
                # Gerar 8 bits aleatórios (0 ou 1)
                bits = [random.randint(0, 1) for _ in range(8)]
                # Converter os bits para um valor inteiro (0-255)
                valor_inteiro = sum(bit << i for i, bit in enumerate(bits))
                self._db.set_holding_registers(716, [valor_inteiro])
                #Lista: bit0 - Sensor de Reservatório Superior Nível Alto (Ativo = 1)
                #Lista: bit1 - Sensor de Reservatório Superior Nível Baixo (Ativo = 0)
                #Lista: bit2 - Sensor de Reservatório Inferior Nível Alto (Ativo = 1)
                #Lista: bit3 - Sensor de Reservatório Inferior Nível Baixo (Ativo = 0)
                #Lista: bit4 - Indicador de Nível Muito Alto
                #Lista: bit5 - Válvula XP-01
                #Lista: bit6 - Válvula XP-02
                #Lista: bit7 - Indicador de Nível Muito Alto
               
                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                builder.add_32bit_float(random.uniform(0.95*400, 1.05*400))
                payload = builder.to_registers()
                self._db.set_holding_registers(700, payload)
                #Temperatura Enrolamento R Motor
                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                builder.add_32bit_float(random.uniform(0.95*400, 1.05*400))
                payload = builder.to_registers()
                self._db.set_holding_registers(702, payload)
                #Temperatura Enrolamento S Motor
                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                builder.add_32bit_float(random.uniform(0.95*400, 1.05*400))
                payload = builder.to_registers()
                self._db.set_holding_registers(704, payload)
                #Temperatura Enrolamento T Motor  
                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                builder.add_32bit_float(random.uniform(0.95*400, 1.05*400))
                payload = builder.to_registers()
                self._db.set_holding_registers(706, payload)
                #Temperatura Carcaça  
               
                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                builder.add_32bit_float(random.uniform(0.95*400, 1.05*400))
                payload = builder.to_registers()
                self._db.set_holding_registers(710, payload)
                #Medida da Pressão PIT-01
                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                builder.add_32bit_float(random.uniform(0.95*400, 1.05*400))
                payload = builder.to_registers()
                self._db.set_holding_registers(712, payload)
                #Medida da Vazão FIT-01
                
                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                builder.add_32bit_float(random.uniform(0.95*400, 1.05*400))
                payload = builder.to_registers()
                self._db.set_holding_registers(714, payload)
                #Medida do Nível do Reservatório superior (Porcentagem)

                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                builder.add_32bit_float(random.uniform(0.95*400, 1.05*400))
                payload = builder.to_registers()
                self._db.set_holding_registers(727, payload)
                #Medida da Rotação do Motor selecionado (RPM)
                builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
                builder.add_32bit_float(random.uniform(0.95*400, 1.05*400))
                payload = builder.to_registers()
                self._db.set_holding_registers(1334, payload)    
                #Medida do Torque no Motor Selecionado
               
               
                self._db.set_holding_registers(852,[random.randrange(int(0.95*400),int(1.05*400))])
                #Medida Potência Ativa Fase R
                self._db.set_holding_registers(853,[random.randrange(int(0.95*400),int(1.05*400))])
                #Medida Potência Ativa Fase S
                self._db.set_holding_registers(854,[random.randrange(int(0.95*400),int(1.05*400))])
                #Medida Potência Ativa Fase T
                self._db.set_holding_registers(855,[random.randrange(int(0.95*400),int(1.05*400))])
                #Medida Potência Ativa Total
             
                self._db.set_holding_registers(868,[random.randrange(int(0.95*400),int(1.05*400))])
                #Medida do Fator de Potência Fase R
                self._db.set_holding_registers(869,[random.randrange(int(0.95*400),int(1.05*400))])
                #Medida do Fator de Potência Fase S
                self._db.set_holding_registers(870,[random.randrange(int(0.95*400),int(1.05*400))])
                #Medida do Fator de Potência Fase T
                self._db.set_holding_registers(871,[random.randrange(int(0.95*400),int(1.05*400))])
                #Medida do Fator de Potência Total              
               
               


               
                leitura = self._db.get_holding_registers(1334,2)
                decoder = BinaryPayloadDecoder.fromRegisters(leitura, byteorder=Endian.Big, wordorder=Endian.Big)
               
                print("=================")
                print("Tabela MODBUS")
                print(f' Holding Register \r \n R1334: {decoder.decode_32bit_float()} \r\n R871: {self._db.get_holding_registers(871)}')
                sleep(1)
        except Exception as e:
            print("Erro: ",e.args)

