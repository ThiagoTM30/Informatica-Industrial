from db import Base
from sqlalchemy import Column, Integer, Float, DateTime

class DadoCLP(Base):
    """
    Modelo dos dados do CLP
    """
    __tablename__ = 'dadoclp'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    nivel_sup_alto = Column(Integer)  # Sensor Reservatório Superior Nível Alto
    nivel_sup_baixo = Column(Integer)  # Sensor Reservatório Superior Nível Baixo
    nivel_inf_alto = Column(Integer)  # Sensor Reservatório Inferior Nível Alto
    nivel_inf_baixo = Column(Integer)  # Sensor Reservatório Inferior Nível Baixo
    nivel_muito_alto = Column(Integer)  # Indicador de Nível Muito Alto
    valvula_xp01 = Column(Integer)  # Válvula XP-01
    valvula_xp02 = Column(Integer)  # Válvula XP-02
    indicador_alto = Column(Integer)  # Indicador de Nível Muito Alto (repetido no seu comentário original)
    temperatura_r = Column(Float)
    temperatura_s = Column(Float)
    temperatura_t = Column(Float)
    temperatura_carcaca = Column(Float)
    pressao = Column(Float)
    vazao = Column(Float)
    nivel_superior = Column(Float)
    rotacao_motor = Column(Float)
    torque_motor = Column(Float)
    potencia_r = Column(Float)
    potencia_s = Column(Float)
    potencia_t = Column(Float)
    potencia_total = Column(Float)
    fp_r = Column(Float)
    fp_s = Column(Float)
    fp_t = Column(Float)
    fp_total = Column(Float)

    def get_attr_printable_list(self):
        return [
            self.id,
            self.timestamp.strftime('%d/%m/%Y %H:%M:%S'),
            self.nivel_sup_alto,
            self.nivel_sup_baixo,
            self.nivel_inf_alto,
            self.nivel_inf_baixo,
            self.nivel_muito_alto,
            self.valvula_xp01,
            self.valvula_xp02,
            self.indicador_alto,
            self.temperatura_r,
            self.temperatura_s,
            self.temperatura_t,
            self.temperatura_carcaca,
            self.pressao,
            self.vazao,
            self.nivel_superior,
            self.rotacao_motor,
            self.torque_motor,
            self.potencia_r,
            self.potencia_s,
            self.potencia_t,
            self.potencia_total,
            self.fp_r,
            self.fp_s,
            self.fp_t,
            self.fp_total,
        ]