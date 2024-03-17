# ------------------------------------------
# graph.py
'''
Code for the graphs, using plotly.py
'''
'''
Resources used:
- [BugBytes, "Django & Plotly" video](https://www.youtube.com/watch?v=TcnWEQMT3_A)
- [plotly Docs - bar charts](https://plotly.com/python/bar-charts/)
- [plotly docs - px arguments](https://plotly.com/python/px-arguments/)
'''
# ------------------------------------------
import plotly.express as px
from pandas import DataFrame

from . import queries

# TODO:
'''
- embed graph in template with plotly.js 
- add graphs for different statistics
- write tests for query and graph stuff
    - possibly seperate show_graph into more functions to make this easier
'''

def show_graph(city_name='Albury', start_date='2008-12-01', end_date='2008-12-30'):

    # convert the SQL query to a pandas dataframe format (plotly needs it)
    df = DataFrame(queries.get_temp_in_range(city_name, start_date, end_date))
    df.columns=['Date', 'Low', 'High']

    # generate a bar chart from the dataframe
    fig = px.bar(
        df,
        x = 'Date',
        y = ['Low', 'High'],
        barmode = 'group',
        title = "Past Data for "+ city_name,
        labels = {"value": "Temperature (°C)", "variable": "Type"}
        )

    # show the bar chart
    fig.show()

    # return the chart so it can be passed to the html template somehow
    pass