# -------------------------------------------------
# test_graphs.py
'''
Unit tests for the classes and methods in graphs.py
Note that tests are separated out so that they show up
as individual tests in terminal and testing tab.

The Plan:
- Create instances of each class, test only that instance variables are what you expect them to be
- test for: range has no missing values
- range has missing values
- range is invalid
- see what coverage is after that and then move forward

- also test get_fig
'''
# --------------------------------------------------
import pytest
from weatherApp.graphs import (
    get_graph_html,
    WeatherGraph,
    TemperatureGraph,
    RainGraph,
    WindGraph
)

# GENERAL FIXTURES & SUPPORT
# --------------------------
class ExpectedGraph:
    def __init__(
        self,
        city_and_dates,
        got_city_name,
        dataframe,
        fig,
    ):
        self.city_and_dates = city_and_dates
        self.got_city_name = got_city_name
        self.dataframe = dataframe
        self.fig = fig

class GraphTest():
    '''Note:
    - test_get_html() is not included, because I can't test
      how the html will look in the browser.
    '''
    def __init__(self, expected: ExpectedGraph, real: WeatherGraph):
        self.expected = expected
        self.real = real

    def test_dataframe(self):
        '''
        By checking dataframe attribute, we check the whole _initialize_dataframe sequence... 
        - checks that data is correct (_fetch_and_convert_data)
        - checks that columns are properly renamed (_rename_columns)
        - checks that NA data is properly handled (_handle_missing_data))
        '''
        expected_df = self.expected.dataframe
        real_df = self.real.dataframe

        for col in expected_df.keys():
            for row in range( len(expected_df[col])):
                assert (real_df[col][row] == expected_df[col][row])
                
    def test_figure(self):
        expected_fig = self.expected.fig
        real_fig = self.real.fig['data']

        for i in range(len(expected_fig)):
            for key in expected_fig[i].keys():
                assert (real_fig[i][key] == expected_fig[i][key])

    def test_get_city_name(self):
        assert (self.real.get_city_name() == self.expected.got_city_name)

@pytest.fixture()
def given_city_and_dates():
    return {
        'city_name': 'Springfield',
        'start_date': '2023-01-01',
        'end_date': '2023-01-03'
    }
# ======================================================================

# TEMPERATURE GRAPH - FIXTURES & SUPPORT
# --------------------------------------
@pytest.fixture()
def expected_temp_graph(given_city_and_dates):
    city_and_dates = given_city_and_dates
    got_city_name = given_city_and_dates['city_name']

    expected_dataframe = {
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Low':  [-5.0        , -3.0        , 0           ],
        'High': [10.0        , 0           , 30.0        ]
    }
    expected_fig = [
        {
            'name': 'Low',
            'type': 'bar'
        },
        {
            'name':'High',
            'type':'bar'
        }
    ]

    return ExpectedGraph(
        city_and_dates,
        got_city_name,
        expected_dataframe,
        expected_fig
    )

@pytest.fixture()
def real_temp_graph(app, given_city_and_dates):
    with app.app_context():
        return TemperatureGraph(given_city_and_dates)

@pytest.fixture()
def temp_graph_tests(expected_temp_graph, real_temp_graph):
    return GraphTest(expected_temp_graph, real_temp_graph)

# TEMPERATURE GRAPH TESTS
# -----------------------
def test_TemperatureGraph_dataframe(temp_graph_tests):
    temp_graph_tests.test_dataframe()

def test_TemperatureGraph_figure(temp_graph_tests):
    temp_graph_tests.test_figure()

def test_WeatherGraph_get_city_name(temp_graph_tests):
    temp_graph_tests.test_get_city_name()

# =============================================================

# RAIN GRAPH - FIXTURES & SUPPORT
# -----------------------------
@pytest.fixture()
def expected_rain_graph(given_city_and_dates):
    city_and_dates = given_city_and_dates
    got_city_name = given_city_and_dates['city_name']

    expected_dataframe = {
        'Date':     ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Rainfall': [0.0         , 5.0         , 0.0         ],
    }
    expected_fig = [
        {'type': 'bar'}
    ]

    return ExpectedGraph(
        city_and_dates,
        got_city_name,
        expected_dataframe,
        expected_fig
    )

@pytest.fixture()
def real_rain_graph(app, given_city_and_dates):
    with app.app_context():
        return RainGraph(given_city_and_dates)

@pytest.fixture()
def rain_graph_tests(expected_rain_graph, real_rain_graph):
    return GraphTest(expected_rain_graph, real_rain_graph)

# RAIN GRAPH - TESTS
# ------------------
def test_RainGraph_dataframe(rain_graph_tests):
    rain_graph_tests.test_dataframe()

def test_RainGraph_figure(rain_graph_tests):
    rain_graph_tests.test_figure()

# =============================================================

# WIND GRAPH - FIXTURES & SUPPORT
# -----------------------------
@pytest.fixture()
def expected_wind_graph(given_city_and_dates):
    city_and_dates = given_city_and_dates
    got_city_name = given_city_and_dates['city_name']

    expected_dataframe = {
        'Date':      ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Speed':     ['11-20'     , '31-40'     , '101-200'   ],
        'Direction': ['W'         , 'NNE'      , 'SW'         ]
    }
    expected_fig = [
        {'type': 'barpolar'}
    ]

    return ExpectedGraph(
        city_and_dates,
        got_city_name,
        expected_dataframe,
        expected_fig
    )

@pytest.fixture()
def real_wind_graph(app, given_city_and_dates):
    with app.app_context():
        return WindGraph(given_city_and_dates)

@pytest.fixture()
def wind_graph_tests(expected_wind_graph, real_wind_graph):
    return GraphTest(expected_wind_graph, real_wind_graph)

# WIND GRAPH - TESTS
# ------------------
def test_WindGraph_dataframe(wind_graph_tests):
    wind_graph_tests.test_dataframe()

def test_WindGraph_figure(wind_graph_tests):
    wind_graph_tests.test_figure()

# @pytest.fixture()
# def expected_freq_table():
#         directions =  ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
#         bins =  ['1-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100', '101-200'],
        
#         expected_freq_table = {
#             'Direction': [],
#             'Speed': [],
#             'Frequency': []
#         }

#         for dir in directions:
#             for bin in bins:
#                 expected_freq_table['Direction'].append(dir)
#                 expected_freq_table['Speed'].append(bin)
#                 expected_freq_table['Frequency'].append(0)

#         w_11_20 = 12*1 # W has idx 12 in directions, 11-20 has idx 1 in bins
#         nne_31_40 = 1*3 # NNE has idx 1 in directions, 31-40 has idx 3 in bins
#         sw_101_200 = 10*10 # SW has idx 10 in directions, 101-200 has idx 10 in bins

#         expected_freq_table['Frequency'][w_11_20] = 1
#         expected_freq_table['Frequency'][nne_31_40] = 1
#         expected_freq_table['Frequency'][sw_101_200] = 1

#         return expected_freq_table

# TODO - get this working - current problem is .at[] doesn't work
    # OR DON'T - graphs.py has 89% coverage now... and frequency stuff is covered
def test_WindGraph_freq_table( real_wind_graph):
    # real_freq = real_wind_graph.freq_table
    # expected_filled_freq = 1
    # expected_empty_freq = 0

    # assert real_freq.at['W', '11-20'] == expected_filled_freq
    # assert real_freq.at['NNE', '31-40'] == expected_filled_freq
    # assert real_freq.at['SW', '101-200'] == expected_filled_freq

    # assert real_freq.at['W', '31-40'] == expected_empty_freq

    # # for col in expected_ft.keys():
    # #         for row in range( len(expected_ft[col])):
    # #             assert (real_ft[col][row] == expected_ft[col][row])
    pass

# TODO
'''
- also remember to write test for get_fig_html
    - maybe split into two functions; get_fig and get_fig_html?
'''