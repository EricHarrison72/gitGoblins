# ------------------------------------------
# graph.py
'''
Code for the graphs, using plotly.py
'''
'''
Resources used:
- [plotly Docs - bar charts](https://plotly.com/python/bar-charts/)
- [plotly docs - px arguments](https://plotly.com/python/px-arguments/)
- [plotly docs - wind rose charts](https://plotly.com/python/wind-rose-charts/)
- Lots of pandas docs
'''
# ------------------------------------------
import plotly.express as px
from pandas import DataFrame, crosstab, cut
from abc import ABC, abstractmethod
from . import queries

DEFAULT_url_args = {
    'stat' : 'temperature',
    'city_name': 'Canberra', 
    'start_date':'2017-06-14',
    'end_date': '2017-06-24'
}

# GET GRAPH METHODS
# ------------------
def get_graph_html(url_args=DEFAULT_url_args):
    '''
    USE THIS outside of graphs.py
    Note: this function was written this way to make it easier to test the other get graph functions.
    '''
    light_graph = _get_graph(url_args)
    dark_graph = _get_graph(url_args)
    dark_graph.convert_to_darkmode()


    return {
        'light': _get_graph_as_string(light_graph),
        'dark': _get_graph_as_string(dark_graph)
    }

def _date_range_is_valid(dates: dict):
    if dates['start_date'] < dates['end_date']:
        return True
    else:
        return False

def _get_graph(url_args=DEFAULT_url_args):
    '''
    Not the function you should use outside of this module.
    You're thinking of get_graph_html.
    '''
    if not _date_range_is_valid(url_args): 
        return "Date Error"

    stat = url_args['stat']
    
    if stat == "temperature":
        graph = TemperatureGraph(url_args)
    elif stat == "wind":
        graph = WindGraph(url_args)
    elif stat == "rain":
        graph = RainGraph(url_args)
    else:
        graph = None

    return graph

def _get_graph_as_string(graph):
    '''
    Not the function you should use outside of this module.
    You're thinking of get_graph_html.
    '''
    if graph == "Date Error":
        return "<p>Error. You entered an invalid date range.</p>"
    elif graph == None:
        return "There was an error generating this graph."
    else:
        return graph.get_html()

# ==================================
class WeatherGraph(ABC):
    def __init__(self, city_and_dates):
        self.city_and_dates = city_and_dates
        self.dataframe = None
        self.fig = None

        self._initialize_dataframe()
        self._initialize_figure()
        self._update_fonts()
        self._update_margins_and_color()
    
    def get_html(self):
        return self.fig.to_html(full_html=False)
    
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
        self.dataframe = DataFrame(queries.get_data_in_range(db_columns, self.city_and_dates))

    @abstractmethod
    def _rename_columns(self, new_columns):
        self.dataframe.columns = new_columns

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
    
    def _update_margins_and_color(self):
        self.fig.update_layout(
            margin={'t': 20, 'r': 10, 'l': 10, 'b':20},
            plot_bgcolor = '#e1f4ff'
        )
    
    def convert_to_darkmode(self):
        self.fig.update_layout(
            margin={'t': 20, 'r': 10, 'l': 10, 'b':20},
            paper_bgcolor = '#424843',
            plot_bgcolor = '#5a605b',
            font_color = '#fff',
            legend_title_font_color = '#fff',
        )
        self.fig.update_yaxes(
            gridcolor = '#424843',
            zerolinecolor = '#424843'
        )

# =================================
class TemperatureGraph(WeatherGraph):
    def __init__(self, city_and_dates):
        super().__init__(city_and_dates)

    # OVERRIDE: all abstract methods
    # ------------------------------
    def _fetch_and_convert_data(self):
        super()._fetch_and_convert_data(['TempMin', 'TempMax'])

    def _rename_columns(self):
        super()._rename_columns(['Date', 'Low', 'High'])

    def _handle_missing_data(self):
        # This is so 0s still show up
        self.dataframe['Low'].replace(0, 0.1, inplace=True)
        self.dataframe['High'].replace(0, 0.1, inplace=True)

        # This is so NAs don't mess up the graph
        self.dataframe['Low'].replace('NA', 0, inplace=True)
        self.dataframe['High'].replace('NA', 0, inplace=True)

    def _initialize_figure(self):
        self.fig = px.bar(
            self.dataframe,
            x = 'Date',
            y = ['Low', 'High'],
            barmode = 'group',
            labels = {"value": "Temperature (°C)", "variable": "Type"},
        )

        self.fig.update_traces(
            marker_line_width=0.1
        )


# =================================
class RainGraph(WeatherGraph):
    def __init__(self, city_and_dates):
        super().__init__(city_and_dates)
        print(self.fig)

    # OVERRIDE: all abstract methods
    # ------------------------------
    def _fetch_and_convert_data(self):
        super()._fetch_and_convert_data(['Rainfall'])

    def _rename_columns(self):
        super()._rename_columns(['Date', 'Rainfall'])

    def _handle_missing_data(self):
        # This is so NAs don't mess up the graph
        self.dataframe['Rainfall'].replace('NA', 0, inplace=True)

    def _initialize_figure(self):
        self.fig = px.bar(
            self.dataframe,
            x = 'Date',
            y = 'Rainfall',
            labels = {"value": "Rainfall (mm)"},
        )

        self.fig.update_traces(
            marker_line_width=0.1
        )


# ========================
class WindGraph(WeatherGraph):
    def __init__(self, city_and_dates):
        self.freq_table = None
        super().__init__(city_and_dates)

    # Overide parent methods
    def _initialize_dataframe(self):
        super()._initialize_dataframe()
        self._initialize_freq_table()

    def convert_to_darkmode(self):
        super().convert_to_darkmode()
        self.fig.update_polars(
            bgcolor = '#5a605b',
            angularaxis_gridcolor = '#424843',
            radialaxis_gridcolor = '#424843'
        )
    # OVERRIDE: all abstract methods
    # ------------------------------
    def _fetch_and_convert_data(self):
        super()._fetch_and_convert_data(['WindGustSpeed', 'WindGustDir'])

    def _rename_columns(self):
        super()._rename_columns(['Date', 'Speed', 'Direction'])

    def _handle_missing_data(self):
        self.dataframe['Speed'].replace('NA', None, inplace=True)
        self.dataframe['Direction'].replace('NA', None, inplace=True)
        self.dataframe.dropna(inplace=True)

    def _initialize_figure(self):
        self.fig = px.bar_polar(
            self.freq_table, 
            r="Frequency", 
            theta="Direction",
            color="Speed",
            color_discrete_sequence= px.colors.sequential.Plasma_r,
            labels = {"Speed": "Speed (km/h)"},
            width=700,
        )

    # NEW Helper METHODS
    # ------------------
    def _initialize_freq_table(self):

        self._cut_speed_into_bins()

        frequencies = crosstab(self.dataframe['Direction'], self.dataframe['Speed'])
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
        speed_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200]
        speeds_as_intervals = DataFrame(cut(self.dataframe['Speed'], speed_bins, right=True))['Speed']

        speeds_as_strings = []
        for interval in speeds_as_intervals:
            speeds_as_strings.append(
                f'{interval.left + 1}-{interval.right}'
            )

        self.dataframe['Speed'] = speeds_as_strings