from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy_garden.graph import LinePlot
from kivy.properties import StringProperty, ObjectProperty
from sqlalchemy.orm import sessionmaker
from db import engine
from models import DadoCLP
from datetime import datetime
from timeseriesgraph import TimeSeriesGraph
from kivy.uix.spinner import Spinner

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
  def __init__(self):
      super().__init__()
      self._acel_st = str(10)
      self._desacel_st = str(10)

  def notFreq(self):
    self.ids.slides_freq.opacity = 0
    self.ids.slides_freq.disabled = True
    
  def freq(self):
    self.ids.slides_freq.opacity = 80
    self.ids.slides_freq.disabled = False
      
  def setAcel(self, acel, desacel):
    # Acessa o GridLayout já definido no arquivo .kv
    grid_layout = self.ids.grid_part  # Certifique-se que o id está correto no .kv

    # Remove widgets antigos (opcional, se quiser atualizar valores)
    grid_layout.clear_widgets()

    # Adiciona os Labels e TextInputs manualmente
    grid_layout.add_widget(Label(text="ACELERAÇÃO"))
    self._acel_st = TextInput(text=str(acel), font_size=14, halign='center', valign='middle')
    grid_layout.add_widget(self._acel_st)

    grid_layout.add_widget(Label(text="DESACELERAÇÃO"))
    self._desacel_st = TextInput(text=str(desacel), font_size=14, halign='center', valign='middle')
    grid_layout.add_widget(self._desacel_st)
  
  def clearAcel(self):
    grid = self.ids.get('grid_part')  # Obtém o GridLayout
    if grid is None:
        print("Erro: grid_part não encontrado!")
        return
    # Remove apenas os filhos do grid, sem apagar o layout principal
    grid.clear_widgets()
  
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

# class HistoricalDataGraphPopup(Popup):
#     def __init__(self, xmax, tags, **kwargs):
#         super().__init__(**kwargs)
#         self.tags = tags
#         self.current_variable = 'torque'
#         self.sensor_names = [
#             "Reserv. Sup. Nível Alto (Bit 0)",
#             "Reserv. Sup. Nível Baixo (Bit 1)",
#             "Reserv. Inf. Nível Alto (Bit 2)",
#             "Reserv. Inf. Nível Baixo (Bit 3)",
#             "Indicador Nível Muito Alto (Bit 4)",
#             "Válvula XP-01 (Bit 5)",
#             "Válvula XP-02 (Bit 6)",
#             "Indicador Nível Muito Alto (Bit 7)"  
#         ]
        
#         # Configuração inicial do gráfico
#         initial_unid = self.tags[self.current_variable]['unidade']
#         initial_ymax = self.tags[self.current_variable]['ymax']
#         initial_y_ticks = self.tags[self.current_variable]['y_ticks_major']
#         self.plot = LinePlot(line_width=1.5, color=self.tags[self.current_variable]['color'])
#         self.ids.graph.add_plot(self.plot)
#         self._update_axis(initial_unid,initial_ymax,initial_y_ticks)
#         # Filtra as chaves originais (remove 'sensores') e adiciona sensores virtuais
#         original_keys = [key for key in self.tags.keys() if key != 'sensores']
#         spinner_values = original_keys + [f"sensor_{i}" for i in range(8)]
#         self.ids.spinner.values = spinner_values

#     def _update_axis(self, unid,ymax,y_ticks_major):
#         self.ids.graph.ylabel = f"{self.current_variable} [ {unid} ]"
#         self.ids.graph.ymax = ymax
#         self.ids.graph.y_ticks_major = y_ticks_major


#     def on_spinner_select(self, selected_text):
#         if selected_text in self.tags:
#             self.current_variable = selected_text
#             selected_unid = self.tags[self.current_variable]['unidade']
#             selected_ymax = self.tags[self.current_variable]['ymax']
#             selected_y_ticks = self.tags[self.current_variable]['y_ticks_major']
#             self._update_axis(selected_unid,selected_ymax,selected_y_ticks)
#         elif selected_text.startswith('sensor_'):  # Sensor binário
#             self.current_variable = selected_text
#             # Configura o gráfico para modo binário (0 ou 1)
#             self._update_axis('', 1, 1)  # ymax=1, y_ticks_major=1
            
#         self.ids.graph.reset_data()
#         self.ids.graph.clearPlots()
#         if selected_text.startswith('sensor_'):
#             new_color = (0, 1, 0, 1) 
#             line = 3.0 # Verde para sensores binários
#         else:    
#             new_color = self.tags[self.current_variable]['color']
#             line = 1.5
#         self.plot = LinePlot(line_width=line, color=new_color)
#         self.ids.graph.add_plot(self.plot)
            
       
# class LabeledCheckBoxHistoricalDataGraph(BoxLayout):    
#     pass      

class QueryHistoricalDataPopup(Popup):
    def __init__(self, xmax, tags, **kwargs):
        super().__init__(**kwargs)
        self.tags = tags
        self.current_variable = 'torque'
        self.session = sessionmaker(bind=engine)()
        
        # Configuração inicial do gráfico
        initial_unid = self.tags[self.current_variable]['unidade']
        initial_ymax = self.tags[self.current_variable]['ymax']
        initial_y_ticks = self.tags[self.current_variable]['y_ticks_major']
        self.plot = LinePlot(line_width=1.5, color=self.tags[self.current_variable]['color'])
        self.ids.graph.add_plot(self.plot)
        self._update_axis(initial_unid, initial_ymax, initial_y_ticks)
        
        # Configuração do Spinner
        original_keys = [key for key in self.tags.keys() if key != 'sensores']
        spinner_values = original_keys + [f"sensor_{i}" for i in range(8)]
        self.ids.spinner.values = spinner_values
    
    def _update_axis(self, unid, ymax, y_ticks_major):
        self.ids.graph.ylabel = f"{self.current_variable} [ {unid} ]"
        self.ids.graph.ymax = ymax
        self.ids.graph.y_ticks_major = y_ticks_major
    
    def on_spinner_select(self, selected_text):
        if selected_text in self.tags:
            self.current_variable = selected_text
            selected_unid = self.tags[self.current_variable]['unidade']
            selected_ymax = self.tags[self.current_variable]['ymax']
            selected_y_ticks = self.tags[self.current_variable]['y_ticks_major']
            self._update_axis(selected_unid, selected_ymax, selected_y_ticks)
        elif selected_text.startswith('sensor_'):  # Sensor binário
            self.current_variable = selected_text
            # Configura o gráfico para modo binário (0 ou 1)
            self._update_axis('', 1, 1)  # ymax=1, y_ticks_major=1
        self.ids.graph.reset_data()
        self.ids.graph.clearPlots()
        if selected_text.startswith('sensor_'):
            new_color = (0, 1, 0, 1) 
            line = 3.0 # Verde para sensores binários
        else:    
            new_color = self.tags[self.current_variable]['color']
            line = 1.5
        self.plot = LinePlot(line_width=line, color=new_color)
        self.ids.graph.add_plot(self.plot)
         
    def query_data(self):
        try:
            start_time = datetime.strptime(self.ids.start_time_input.text, "%d/%m/%Y %H:%M:%S")
            end_time = datetime.strptime(self.ids.end_time_input.text, "%d/%m/%Y %H:%M:%S")
            selected_variable = self.current_variable
            
            results = self.session.query(DadoCLP).filter(DadoCLP.timestamp.between(start_time, end_time)).all()
            
            if not results:
                print("Nenhum dado encontrado para o intervalo selecionado.")
                return
            
            # Define xmax como o número total de pontos encontrados
            num_points = len(results)
            self.ids.graph.xmax = num_points if num_points > 0 else 20  # Garante no mínimo 20 pontos
                
            data_points = [(r.timestamp, getattr(r, selected_variable, None)) for r in results]
            self.plot.points = [(i, v) for i, (t, v) in enumerate(data_points) if v is not None]
            self.ids.graph.update_x_labels([t for t, v in data_points if v is not None])
        except Exception as e:
            print("Erro na consulta:", e.args)