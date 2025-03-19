from db import Base
from sqlalchemy import Column, Integer, Float, DateTime

class DadoCLP(Base):
    __tablename__ = 'dadoclp'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    sensor_0 = Column(Integer)
    sensor_1 = Column(Integer)
    sensor_2 = Column(Integer)
    sensor_3 = Column(Integer)
    sensor_4 = Column(Integer)
    sensor_5 = Column(Integer)
    sensor_6 = Column(Integer)
    sensor_7 = Column(Integer)
    sensor_8 = Column(Integer)
    sensor_9 = Column(Integer)
    sensor_10 = Column(Integer)
    sensor_11 = Column(Integer)
    sensor_12 = Column(Integer)
    sensor_13 = Column(Integer)
    sensor_14= Column(Integer)
    sensor_15 = Column(Integer)
    temp_rmotor = Column(Float)
    temp_smotor = Column(Float)
    temp_tmotor = Column(Float)
    temp_carcaca = Column(Float)
    pressao = Column(Float)
    vazao = Column(Float)
    nivel = Column(Float)
    rot_rpm = Column(Float)
    torque = Column(Float)
    pot_r = Column(Float)
    pot_s = Column(Float)
    pot_t = Column(Float)
    pot_total = Column(Float)
    fp_r = Column(Float)
    fp_s = Column(Float)
    fp_t = Column(Float)
    fp_tot = Column(Float)

    def get_attr_printable_list(self):
        return [
            self.id,
            self.timestamp.strftime('%d/%m/%Y %H:%M:%S'),
            self.sensor_0,
            self.sensor_1,
            self.sensor_2,
            self.sensor_3,
            self.sensor_4,
            self.sensor_5,
            self.sensor_6,
            self.sensor_7,
            self.sensor_8,
            self.sensor_9,
            self.sensor_10,
            self.sensor_11,
            self.sensor_12,
            self.sensor_13,
            self.sensor_14,
            self.sensor_15,
            self.temp_rmotor,
            self.temp_smotor,
            self.temp_tmotor,
            self.temp_carcaca,
            self.pressao,
            self.vazao,
            self.nivel,
            self.rot_rpm,
            self.torque,
            self.pot_r,
            self.pot_s,
            self.pot_t,
            self.pot_total,
            self.fp_r,
            self.fp_s,
            self.fp_t,
            self.fp_tot,
        ]