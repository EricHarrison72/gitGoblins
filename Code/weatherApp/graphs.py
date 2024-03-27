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
'''
Other graphs we want:
- rainfall amount
- wind: gust, 9am, 3am, direction?
 - https://plotly.com/python/wind-rose-charts/
'''
# ------------------------------------------
import plotly.express as px
import plotly.data as plotly_data
from pandas import DataFrame, crosstab, cut
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
        
        case "wind":
            fig = PastWindFigure(city_and_dates)

        case _:
            pass

    return fig.get_html()

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
    
    def get_city_name(self):
        return queries.add_space(self.city_and_dates['city_name'])
   
    # DATAFRAME METHODS
     # ----------------
    def _initialize_dataframe(self):
        self._fetch_and_convert_data()
        self._rename_columns()
        self._handle_missing_data()

    @abstractmethod
    def _fetch_and_convert_data(self, db_columns: list):
        self.df = DataFrame(queries.get_data_in_range(db_columns, self.city_and_dates))

    @abstractmethod
    def _rename_columns(self, new_columns):
        self.df.columns = new_columns

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
        super()._fetch_and_convert_data(['TempMin', 'TempMax'])

    def _rename_columns(self):
        super()._rename_columns(['Date', 'Low', 'High'])

    def _handle_missing_data(self):
        # TODO: use .fillna method?
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
            title = "Temperature Over Time — "+ self.get_city_name(),
            labels = {"value": "Temperature (°C)", "variable": "Type"},
        )


# ========================
class PastWindFigure(PastWeatherFigure):
    def __init__(self, city_and_dates):
        self.freq_table = None
        super().__init__(city_and_dates)

    # Overide parent method
    def _initialize_dataframe(self):
        super()._initialize_dataframe()
        self._initialize_freq_table()

    # OVERRIDE: all abstract methods
    # ------------------------------
    def _fetch_and_convert_data(self):
        super()._fetch_and_convert_data(['WindGustSpeed', 'WindGustDir'])

    def _rename_columns(self):
        super()._rename_columns(['Date', 'Speed', 'Direction'])

    def _handle_missing_data(self):
        # TODO use fillna
        pass

    def _initialize_figure(self):
        self.fig = px.bar_polar(
            self.freq_table, 
            r="Frequency", 
            theta="Direction",
            color="Speed",
            color_discrete_sequence= px.colors.sequential.Plasma_r,
            title = "Wind Gust Data — "+ self.get_city_name()
        )

    # NEW Helper METHODS
    #-----------
    def _initialize_freq_table(self):

        self._cut_speed_into_bins()

        frequencies = crosstab(self.df['Direction'], self.df['Speed'])
        frequencies_rows = frequencies.index.to_list()
        frequencies_columns = frequencies.columns.to_list()

        directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        bins = ['1-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100', '101-200']

        freq_data = []
        for dir in directions:
            for bin in bins:
                if ((dir in frequencies_rows) and (bin in frequencies_columns)):
                    freq_data.append([dir, bin, frequencies.at[dir, bin]])
                else:
                    freq_data.append([dir, bin, 0])

        self.freq_table = DataFrame(freq_data)
        self.freq_table.columns = ['Direction', 'Speed', 'Frequency']

    def _cut_speed_into_bins(self):
        speed_bins = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200]
        speeds_as_intervals = DataFrame(cut(self.df['Speed'], speed_bins))['Speed']

        speeds_as_strings = []
        for interval in speeds_as_intervals:
            speeds_as_strings.append(
                f'{interval.left + 1}-{interval.right}'
            )

        self.df['Speed'] = speeds_as_strings