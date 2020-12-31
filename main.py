import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

df = pd.read_csv("marks.csv")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Names:"),
    dcc.Dropdown(
        id='names', 
        value='name', 
        options=[{'value': x, 'label': x} 
                 for x in df.name ],
        clearable=False
    ),
    html.P("Values:"),
    dcc.Dropdown(
        id='values', 
        value='subject', 
        options=[{'value': x, 'label': x} 
                 for x in ['Maths' ,' Physics' ,' Chemistry', ' English'  ,'Biology' , 'Economics' , 'History' , 'Civics' , 'total'  ,'percentage']],
        clearable=False
    ),
    dcc.Graph(id="pie-chart"),
])

@app.callback(
    Output("pie-chart", "figure"), 
    [Input("names", "value"), 
     Input("values", "value")])
def generate_chart(names, values):
    fig = px.pie(df.percentage,df.name)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)