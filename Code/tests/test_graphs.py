# -------------------------------------------------
# test_graphs.py
'''
Unit tests for the classes and methods in graphs.py
The Plan:
- Create instances of each class, test only that instance variables are what you expect them to be
- see what coverage is after that and then move forward

- also test get_fig
'''
# --------------------------------------------------
# ==================================================
# ##################################################
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
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
    get_fig_html,
    PastTemperatureFigure,
    PastRainFigure,
    PastWindFigure
)

def test_PastTemperatureFigure_vars(app):
    #temp_fig = PastTemperatureFigure(city_and_dates) #yoo wait this can be a fixture too

    # assert temp_fig.dataframe ...
    # assert temp_fig.fig ...
    pass

# Should this be two different funcs?
def test_PastTemperatureFigure_funcs(app):
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