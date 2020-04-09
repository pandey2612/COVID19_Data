import plotly
from plotly.offline import download_plotlyjs , init_notebook_mode , plot , iplot,plot_mpl
import plotly.graph_objects as graph
from selenium import webdriver
plotly.offline.plot({'data': [{'y': [4, 2, 3, 4]}], 
              'layout': {'title': 'Test Plot', 
                         'font': dict(family='Comic Sans MS', size=16)}},
             auto_open=False, image = 'jpeg', image_filename='plotimage',
             output_type='file', image_width=800, image_height=600, 
             filename='temp-plot.html', validate=False)


