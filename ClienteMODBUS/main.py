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
        self._widget = MainWidget()
        return self._widget
    
if __name__ == '__main__':
    
    Builder.load_string(open("Trabalhoinf/mainwidget.kv",encoding="utf-8").read(),rulesonly=True)
    MainApp().run()