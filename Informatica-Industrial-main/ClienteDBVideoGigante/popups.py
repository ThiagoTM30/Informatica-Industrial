from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy_garden.graph import LinePlot
from kivy.properties import StringProperty, ObjectProperty

#correto ok!

class ModbusPopup(Popup):
    """
    Popup da configuração do protocolo MODBUS
    """
    _info_lb = None
    def __init__(self, server_ip,server_port, **kwargs):
        """
        Construtor da classe ModbusPopup
        """
        super().__init__(**kwargs)
        self.ids.txt_ip.text = str(server_ip)
        self.ids.txt_porta.text = str(server_port)
        
    def setInfo(self,message):
       self._info_lb = Label(text=message)
       self.ids.layout.add_widget(self._info_lb)
       
    def clearInfo(self):
        if self._info_lb is not None:
            self.ids.layout.remove_widget(self._info_lb)
            
class ScanPopup(Popup):
  """
    Popup da configuraçao do tempo de varredura
  """
  def __init__(self, scantime, **kwargs):
          """
          Construtor da classe ScanPopup
          """
          super().__init__(**kwargs)
          self.ids.txt_st.text = str(scantime)
          
class AtuacaoPopup(Popup):
  """
    Popup da configuração da atuação e controle da planta
  """

class DataGraphPopup(Popup):
    ylabel = StringProperty("Valor")

    def __init__(self, xmax, plot_color, ylabel="", unid="", ymax= 100,y_ticks=10, title="Gráfico Monitoramento Tempo Real",  **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.ylabel = ylabel
        self.y_ticks= y_ticks
        self.ymax = ymax
        self.plot = LinePlot(line_width=1.5, color=plot_color)
        self.ids.graph.add_plot(self.plot)
        self.ids.graph.xmax = xmax
        self.ids.graph.ylabel = f"{self.ylabel} [{unid}]"  
        self.ids.graph.ymax = self.ymax
        self.ids.graph.y_ticks_major = self.y_ticks
 

class LabeledCheckBoxDataGraph(BoxLayout):    
    graph_reference = ObjectProperty()   

class HistoricalDataGraphPopup(Popup):
    def __init__(self, tags, **kwargs):
        super().__init__(**kwargs)
        for key, value in tags.items():
            cb = LabeledCheckBoxHistoricalDataGraph()
            cb.ids.label.text = key
            cb.ids.label.color = value['color']
            cb.id = key
            self.ids.sensores.add_widget(cb)


       
class LabeledCheckBoxHistoricalDataGraph(BoxLayout):    
    pass      

