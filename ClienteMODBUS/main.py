from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder


class MainApp(App):
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
        )
        return self._widget
    
if __name__ == '__main__':
    
    Builder.load_string(open("Trabalhoinf/mainwidget.kv",encoding="utf-8").read(),rulesonly=True)
    Builder.load_string(open("Trabalhoinf/popups.kv",encoding="utf-8").read(),rulesonly=True)

    MainApp().run()