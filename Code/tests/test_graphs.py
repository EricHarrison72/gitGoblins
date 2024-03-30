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
        dataframe,
        fig,
    ):
        self.city_and_dates = city_and_dates
        self.dataframe = dataframe
        self.fig = fig

class GraphTest():
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
                assert (expected_df[col][row] == real_df[col][row])
                
    def test_figure(self):
        assert 1 == 2

    def test_get_html(self):
        pass

    def test_get_city_name(self):
        pass

@pytest.fixture()
def given_city_and_dates():
    return {
        'city_name': 'Springfield',
        'start_date': '2023-01-01',
        'end_date': '2023-01-03'
    }
# ======================================

# TEMPERATURE GRAPH - FIXTURES & SUPPORT
# --------------------------------------
@pytest.fixture()
def expected_temp_graph(given_city_and_dates):
    city_and_dates = given_city_and_dates

    expected_dataframe = {
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Low':  [-5.0        , -3.0        , 0           ],
        'High': [10.0        , 0           , 30.0        ]
    }
    expected_fig = None

    return ExpectedGraph(
        city_and_dates,
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

def test_TemperatureGraph_get_html(temp_graph_tests):
    temp_graph_tests.test_get_html()

def test_TemperatureGraph_get_city_name(temp_graph_tests):
    temp_graph_tests.test_get_city_name()




# TODO
'''
- repeat above tests for Wind and Rain 
- actually to make this proper I'm gonna have to do some inheritance with this one boys
- also remember to write test for get_fig_html
    - maybe split into two functions; get_fig and get_fig_html?
'''