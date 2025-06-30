from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder


class MainApp3(App):
    """
    classe com o aplicativo
    """
    def build(self):
        """
        Metodo que gera o app com base no widget
        """
        self._widget = MainWidget(scan_time=1000,server_ip='127.0.0.1',server_port=502,
        modbus_addr = {
            'sensores': {'addr': 716, 'float': False, 'mult': 1, 'lista': True},
            'temp_rmotor': {'addr': 700, 'float': True, 'mult': 10, 'lista': False, 'ymax': 150, 'y_ticks_major': 30, 'unidade' : '°C'},
            'temp_smotor': {'addr': 702, 'float': True, 'mult': 10, 'lista': False, 'ymax': 150, 'y_ticks_major': 30, 'unidade' : '°C'},
            'temp_tmotor': {'addr': 704, 'float': True, 'mult': 10, 'lista': False, 'ymax': 150, 'y_ticks_major': 30, 'unidade' : '°C'},
            'temp_carcaca': {'addr': 706, 'float': True, 'mult': 10, 'lista': False, 'ymax': 150, 'y_ticks_major': 30, 'unidade' : '°C'},
            'pressao': {'addr': 710, 'float': True, 'mult': 1, 'lista': False, 'ymax': 500, 'y_ticks_major': 100, 'unidade' : 'Kgf/cm²'},
            'vazao': {'addr': 712, 'float': True, 'mult': 1, 'lista': False, 'ymax': 500, 'y_ticks_major': 100, 'unidade' : 'm²/h'},
            'nivel': {'addr': 714, 'float': True, 'mult': 1, 'lista': False, 'ymax': 500, 'y_ticks_major': 100, 'unidade' : '%'},
            'rot_rpm': {'addr': 727, 'float': True, 'mult': 1, 'lista': False, 'ymax': 500, 'y_ticks_major': 100, 'unidade' : 'RPM'},
            'torque': {'addr': 1334, 'float': True, 'mult': 1, 'lista': False, 'ymax': 500, 'y_ticks_major': 100, 'unidade' : 'N/m'},
            'pot_r': {'addr': 852, 'float': False, 'mult': 1, 'lista': False, 'ymax': 500, 'y_ticks_major': 100, 'unidade' : 'W'},
            'pot_s': {'addr': 853, 'float': False, 'mult': 1, 'lista': False, 'ymax': 500, 'y_ticks_major': 100, 'unidade' : 'W'},
            'pot_t': {'addr': 854, 'float': False, 'mult': 1, 'lista': False, 'ymax': 500, 'y_ticks_major': 100, 'unidade' : 'W'},
            'pot_total': {'addr': 855, 'float': False, 'mult': 1, 'lista': False, 'ymax': 1.2, 'y_ticks_major': 0.1, 'unidade' : 'W'},
            'fp_r': {'addr': 868, 'float': False, 'mult': 1000, 'lista': False, 'ymax': 1.2, 'y_ticks_major': 0.1, 'unidade' : ''},
            'fp_s': {'addr': 869, 'float': False, 'mult': 1000, 'lista': False, 'ymax': 1.2, 'y_ticks_major': 0.1, 'unidade' : ''},
            'fp_t': {'addr': 870, 'float': False, 'mult': 1000, 'lista': False, 'ymax': 1.2, 'y_ticks_major': 0.1, 'unidade' : ''},
            'fp_tot': {'addr': 871, 'float': False, 'mult': 1000, 'lista': False, 'ymax': 1.2, 'y_ticks_major': 0.1, 'unidade' : ''}
        }
        )
        return self._widget
    def on_stop(self):
        """
        Método executado quando a aplicação é fechada
        """
        self._widget.stopRefresh()
    
if __name__ == '__main__':
    
    Builder.load_string(open("Trabalhoinf/mainwidget.kv",encoding="utf-8").read(),rulesonly=True)
    Builder.load_string(open("Trabalhoinf/popups.kv",encoding="utf-8").read(),rulesonly=True)

    MainApp().run()
