from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy_garden.graph import LinePlot
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
#teste

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

class DataGraphPopup(Popup):
    def __init__(self, xmax, tags, **kwargs):
        super().__init__(**kwargs)
        self.tags = {k:v for k,v in tags.items() if k != 'sensores'}  # Remove sensores do dicionário
        self.current_variable = 'torque'
        self.sensor_popup = None
        
        # Configuração inicial do gráfico
        initial_mult = self.tags[self.current_variable]['mult']
        self.plot = LinePlot(line_width=1.5, color=self.tags[self.current_variable]['color'])
        self.ids.graph.add_plot(self.plot)
        self._update_axis(initial_mult)
        self.ids.spinner.values = list(self.tags.keys())

    def _update_axis(self, mult):
        self.ids.graph.ylabel = f"{self.current_variable} [x{mult}]"

    def on_spinner_select(self, selected_text):
        if selected_text in self.tags:
            self.current_variable = selected_text
            selected_mult = self.tags[self.current_variable]['mult']
            
            self.ids.graph.reset_data()
            self.ids.graph.clearPlots()
            
            new_color = self.tags[self.current_variable]['color']
            self.plot = LinePlot(line_width=1.5, color=new_color)
            self.ids.graph.add_plot(self.plot)
            self._update_axis(selected_mult)

    def show_sensor_popup(self):
        if not hasattr(self, 'sensor_popup') or not self.sensor_popup:
            self.sensor_popup = SensorPopup()
        self.sensor_popup.open()
        
class LabeledCheckBoxDataGraph(BoxLayout):    
    pass      

class SensorPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Estado dos Sensores"
        self.sensor_states = {}
        self._create_sensor_grid()
        
    def _create_sensor_grid(self):
      sensor_names = [
          "Reserv. Sup. Nível Alto (Ativo=1)",
          "Reserv. Sup. Nível Baixo (Ativo=0)",
          "Reserv. Inf. Nível Alto (Ativo=1)",
          "Reserv. Inf. Nível Baixo (Ativo=0)",
          "Indicador Nível Muito Alto",
          "Válvula XP-01",
          "Válvula XP-02",
          "Indicador Nível Muito Alto",
          "Bit 8", "Bit 9", "Bit 10", "Bit 11",
          "Bit 12", "Bit 13", "Bit 14", "Bit 15"
      ]
      
      grid = self.ids.sensor_grid
      
      for name in sensor_names:
          box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, padding=5)

          lbl_name = Label(text=name, halign='left', size_hint_x=0.7, text_size=(None, None), markup=True)

          btn_state = Button(text='[b]INATIVO[/b]', 
                            background_color=(0.85, 0.35, 0.35, 1),  # Vermelho inicial (inativo)
                            size_hint_x=0.3,
                            markup=True)
          
          self.sensor_states[name] = btn_state

          box.add_widget(lbl_name)
          box.add_widget(btn_state)
          grid.add_widget(box)

    def update_states(self, states):
      colors = {
          1: (0.35, 0.75, 0.35, 1),  # Verde (ATIVO)
          0: (0.85, 0.35, 0.35, 1)   # Vermelho (INATIVO)
      }

      states = states[:16]  

      for (name, btn), state in zip(self.sensor_states.items(), states):
          btn.text = '[b]ATIVO[/b]' if state else '[b]INATIVO[/b]'
          btn.background_color = colors[state]  # Alterando a cor corretamente