import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
from dash import Dash, dcc, html,Output,Input
import plotly.express as px
import math
df = pd.read_csv("/home/abdukarimov/O'zbekistan aholi demografiyasi/byGender.csv")

df= df.transpose()
df.drop(df.index[0], inplace=True)
df.rename(columns={0: "Ayollar", 1 : "Erkaklar",}, inplace=True)
df.index = df.index.astype('int')
df_age = pd.read_csv("/home/abdukarimov/O'zbekistan aholi demografiyasi/byageGroup.csv")

df_age.set_index('Unnamed: 0', inplace=True)
df_age.index.name = None
df_age = df_age.transpose()
df_age.index = df_age.index.astype(int)





app = Dash(__name__)

@app.callback(
    Output('my-age-graph', 'figure'),
    [Input('my-slider', 'value')]
)
def update_age_graph(years):
    df_filtered_age = df_age[df_age.index == years]
    df_filtered_age = df_filtered_age.transpose()  # Transpose DataFrame to have age groups as rows
    fig_age = px.bar(data_frame=df_filtered_age.reset_index(),
                     y="index",  # Age groups
                     x=df_filtered_age.columns,  # Population counts
                     color="index",  # Use different colors for each age group
                     labels={"index": "Yosh qatlami"},  # Rename legend labels
                     orientation='h'
                     )
    fig_age.update_layout(legend_title_text='Yosh qatlami',
                          xaxis_title='Aholi soni')  # Set legend title
    return fig_age

@app.callback(
    Output('my-gender-graph', 'figure'),
    [Input('my-slider', 'value')]
)
def update_gender_graph(years):
    df_filtered_gender = df[df.index == years]
    if df_filtered_gender.empty:
        fig_gender = px.pie(title="No data available for the selected year")
    else:
        values = df_filtered_gender.iloc[0].values.tolist()  # Convert the values to a list
        fig_gender = px.pie(names=df_filtered_gender.columns,  # Gender groups
                            values=values,  # Population counts for each gender
                            title="Aholining jins kesimda ko'rsatkichi",
                            hole=0.4
                            )
    return fig_gender

app.layout = html.Div(
    [
        html.H1("O'zbekiston aholisining jins va yosh bo'yicha kesimi", style={'textAlign': 'center'}),
        html.Label('Yillar'),
        dcc.Slider(min=df_age.index.min(),
                   max=df_age.index.max(),
                   step=1,
                   value=2023,
                   tooltip={"placement": "bottom", "always_visible": True},
                   updatemode='drag',
                   persistence=True,
                   persistence_type='session',
                   id='my-slider',
                   marks={year: str(year) for year in range(int(df_age.index.min()), int(df_age.index.max()) + 1)}
                   ),
        html.Div([
            dcc.Graph(id='my-age-graph', style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='my-gender-graph', style={'width': '50%', 'display': 'inline-block'})
        ])
    ],
    style={"margin": 30}
)

if __name__ == "__main__":
    app.run(debug=True)
