from modbuspersistencia import ModbusPersistencia

tags_addrs = {
    'nivel_reservatorio': 716,
    'temperatura_r': 700,
    'temperatura_s': 702,
    'temperatura_t': 704,
    'temperatura_carcaca': 706,
    'pressao': 710,
    'vazao': 712,
    'nivel_superior': 714,
    'rotacao_motor': 727,
    'torque_motor': 1334,
    'potencia_r': 852,
    'potencia_s': 853,
    'potencia_t': 854,
    'potencia_total': 855,
    'fp_r': 868,
    'fp_s': 869,
    'fp_t': 870,
    'fp_total': 871,
}

c = ModbusPersistencia('localhost', 502, tags_addrs)
c.run()