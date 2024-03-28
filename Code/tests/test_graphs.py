# -------------------------------------------------
# test_graphs.py
'''
Unit tests for the classes and methods in graphs.py
The Plan:
- Create instances of each class, test only that instance variables are what you expect them to be
- test for: range has no missing values
- range has missing values
- range is invalid
- see what coverage is after that and then move forward

- also test get_fig
'''
# --------------------------------------------------
# ==================================================
# ##################################################
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
# __________________________________________________
# ..................................................
# **************************************************
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ++++++++++++++++++++++++++++++++++++++++++++++++++
# ::::::::::::::::::::::::::::::::::::::::::::::::::
# """"""""""""""""""""""""""""""""""""""""""""""""""
import pytest
from weatherApp.graphs import (
    get_graph_html,
    TemperatureGraph,
    RainGraph,
    WindGraph
)

# class Fig:
#     def __init__(self):
#         #......

#     def:

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

@pytest.fixture()
def expected_graph():
    city_and_dates = {
        'city_name': 'Springfield',
        'start_date': '2023-01-01',
        'end_date': '2023-01-03'
    }

    expected_dataframe = {
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Low':  [-5.0        , -3.0        , 0],
        'High': [10.0        , 0           , 30.0]
    }
    expected_fig = None

    return ExpectedGraph(
        city_and_dates,
        expected_dataframe,
        expected_fig
    )

# @pytest.fixture()
# def real_temperature_graph():

#     return TemperatureGraph(city_and_dates)

def test_TemperatureGraph_vars(app, expected_graph):
    with app.app_context():
        real_temp_graph = TemperatureGraph(expected_graph.city_and_dates)

    assert real_temp_graph.city_and_dates == expected_graph.city_and_dates # not really necessary but a good starting point for tests
    
    # Check dataframe (TODO: make this its own test)
    '''
    By checking dataframe attribute, we check the whole _initialize_dataframe sequence... 
    - checks that data is correct (_fetch_and_convert_data)
    - checks that columns are properly renamed (_rename_columns)
    - checks that NA data is properly handled (_handle_missing_data))
    '''
    for col in expected_graph.dataframe.keys():
        for row in range( len(expected_graph.dataframe[col])):
            assert expected_graph.dataframe[col][row] == real_temp_graph.dataframe[col][row]

    # assert temp_fig.fig ...

# Should this be two different funcs?
def test_TemperatureGraph_funcs(app):
    # assert temp_fig.get_html()...
    # assert temp_fig.get_city_name()...
    pass

# TODO
'''
- repeat above tests for Wind and Rain 
- actually to make this proper I'm gonna have to do some inheritance with this one boys
- also remember to write test for get_fig_html
    - maybe split into two functions; get_fig and get_fig_html?
'''