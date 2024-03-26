# ------------------------------------------
# graph.py
'''
Code for the graphs, using plotly.py
'''
'''
Resources used:
- [plotly Docs - bar charts](https://plotly.com/python/bar-charts/)
- [plotly docs - px arguments](https://plotly.com/python/px-arguments/)
'''
# ok, let's move it into different grpahs
'''DESIGN TIME
get_figure(type, other params)
type changes... 
- query method
- column names
- replacements
- graph type

type doesn't change...
- general graph formatting
'''
'''
Other graphs we want:
- rainfall amount
- wind: gust, 9am, 3am, direction?
 - https://plotly.com/python/wind-rose-charts/
'''
# ------------------------------------------
import plotly.express as px
from pandas import DataFrame
from abc import ABC, abstractmethod
from . import queries

DEFAULT_stat = "temp"
DEFAULT_city_and_dates = {
    'city_name': 'Canberra', 
    'start_date':'2017-06-14',
    'end_date': '2017-06-24'
}
def get_fig(stat=DEFAULT_stat, city_and_dates=DEFAULT_city_and_dates):

    match stat:
        case "temp":
            fig = PastTemperatureFigure(city_and_dates)
            return fig.get_html()
        case _:
            pass

# ==================================
class PastWeatherFigure(ABC):
    def __init__(self, city_and_dates):
        self.city_and_dates = city_and_dates
        self.dataframe = None
        self.fig = None

        self._initialize_dataframe()
        self._initialize_figure()
        self._update_fonts()
    
    def get_html(self):
        return self.fig.to_html()
   
    # DATAFRAME METHODS
     # ----------------
    def _initialize_dataframe(self):
        self._fetch_and_convert_data()
        self._rename_columns()
        self._handle_missing_data()

    @abstractmethod
    def _fetch_and_convert_data(self):
        pass

    @abstractmethod
    def _rename_columns(self):
        pass

    @abstractmethod
    def _handle_missing_data(self):
        pass
    
    # FIGURE METHODS
    # ----------------------
    @abstractmethod
    def _initialize_figure(self):
        pass

    def _update_fonts(self):
        self.fig.update_layout (
        font_family="Roboto",
        font_color="black",
        title_font_family="Rubik",
        title_font_color="black",
        legend_title_font_color="black"
    )

# =================================
class PastTemperatureFigure(PastWeatherFigure):
    def __init__(self, city_and_dates):
        super().__init__(city_and_dates)

    # OVERRIDE: all abstract methods
    # ------------------------------
    def _fetch_and_convert_data(self):
        self.df = DataFrame(queries.get_temp_in_range(self.city_and_dates))

    def _rename_columns(self):
        self.df.columns=['Date', 'Low', 'High']

    def _handle_missing_data(self):
        # TODO: add message explaining 0s and NAs
        # This is so 0s still show up
        self.df['Low'].replace(0, 0.1, inplace=True)
        self.df['High'].replace(0, 0.1, inplace=True)

        # This is so NAs don't mess up the graph
        self.df['Low'].replace('NA', 0, inplace=True)
        self.df['High'].replace('NA', 0, inplace=True)

    def _initialize_figure(self):
        self.fig = px.bar(
            self.df,
            x = 'Date',
            y = ['Low', 'High'],
            barmode = 'group',
            title = "Temperature Over Time — "+ self.city_and_dates['city_name'],
            labels = {"value": "Temperature (°C)", "variable": "Type"},
        )
