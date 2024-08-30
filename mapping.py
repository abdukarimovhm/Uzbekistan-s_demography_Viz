import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import json
import numpy as np

# Load DataFrame and GeoJSON data
df_map = pd.read_csv("/home/abdukarimov/O'zbekistan aholi demografiyasi/deyarli_tayyor_mapga.csv")
Uzbekistan_district = json.load(open("/home/abdukarimov/O'zbekistan aholi demografiyasi/Tumanlar.geojson", 'r'))
print('Geojson file is read')

import plotly.express as px

# Ensure max_value is greater than zero
max_value = df_map['2017'].max()
if max_value <= 0:
    max_value = 1  # Set a default value to avoid division by zero

log_max_value = np.log(max_value)

# Calculate the number of ticks needed based on the logarithm of the maximum value
num_ticks = int(np.ceil(log_max_value))

# Generate tick values as a range from 0 to the number of ticks needed
tick_values = np.arange(num_ticks + 1)

# Generate tick text by exponentiating the tick values
tick_labels = [str(int(np.exp(x))) for x in tick_values]

df_map['Density scale'] = np.log(df_map['2017'])

fig = px.choropleth(df_map, 
                    locations='ADM2_PCODE',
                    geojson=Uzbekistan_district,
                    color='Density scale',
                    hover_name='District_x',
                    hover_data='2017',
                    color_continuous_scale='Blues',
                    labels={'Density scale': 'Aholi soni minglarda:'},
                    )

fig.update_geos(fitbounds='locations', visible=False)
fig.update_layout(coloraxis_colorbar=dict(
    title="Aholi soni:",
    tickvals=tick_values,  # Adjust the tick values as needed
    ticktext=tick_labels# Adjust the corresponding labels
))
fig.show()
