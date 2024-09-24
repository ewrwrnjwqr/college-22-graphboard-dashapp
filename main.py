import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_auth
import dash_enterprise_auth as lol
VALID_USERNAME_PASSWORD_PAIRS = {
    'will': 'X',
    'mason': 'X',
    'tieran':'X',
    'jackson':'X',
    'ethan':'X',
    'luke':'X',
    'damon':'X',
    'dylan':'X',
    'Kyle':'X',
    'kyle':'X',
    'Keith' :'X',
    'keith':'X',
    'Dylan':'X',
    'brian':'X'
}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
csv_files_path = os.path.join('tm2.csv')
tm = pd.read_csv(csv_files_path)
tm = tm.drop(columns=['Unnamed: 0'])
pitchtype = tm['Pitchtype'].unique()
players = tm['Name'].unique()
DATA = tm
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
app.title = '2022 College TM Pitcher Graph-board'
app._favicon = ("assets/favicon_io/favicon.ico")
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
server = app.server
def create_figure(column_x, column_y):
    return px.scatter(DATA,x=column_x,y=column_y)
app.layout = html.Div([
                       html.H1('Welcome to the 2022 College TM Pitcher Graph-board'),
                       html.P('Select X & Y Axis. You can also choose color of data points, filter by pitch type and by player names!'),
                       html.H2(id='show-output', children=''),
                       html.Button(" Add Graph", id="ajout-graphe", n_clicks=0),
                       html.Div(),
                       html.Div(id='bloc_graphe', children=[]) 
                     ])

@app.callback( Output('bloc_graphe', 'children'),
               [Input('ajout-graphe', 'n_clicks')],
               [State('bloc_graphe', 'children')])
def ajouter_graphe(n_clicks, children):
    nouvelle_zone_graphe = html.Div(
        style={'width': '50%', 'display': 'inline-block', 'outline': 'thin lightgrey solid', 'padding': 10},
        children=[
                  dcc.Graph(
                            id ={'type': 'Graphique',
                                 'index': n_clicks}
                            ),
                dcc.Dropdown(
                               id='pitch-type',
                               options=[{'label':i, 'value':i} for i in pitchtype],
                               value = None,
                               multi=True,
                               placeholder='Pitchtype'
                              ),
                  dcc.Dropdown(
                               id={
                                   'type':'Selection_variable_X',
                                   'index': n_clicks
                                   },
                               options=[{'label':i, 'value':i} for i in tm.columns],
                               value = None,
                               placeholder = 'X-Axis'
                              ),
                  dcc.Dropdown(
                               id={
                                   'type':'Selection_variable_Y',
                                   'index': n_clicks
                                   },
                               options=[{'label':i, 'value':i} for i in tm.columns],
                               value = None,
                               placeholder='Y-Axis'
                              ),
                  dcc.Dropdown(
                               id="color",
                               options=[{'label':i, 'value':i} for i in tm.columns],
                               value = None,
                               placeholder='Color by...'
                              ),      
                  dcc.Dropdown(
                               id="player",
                               options=[{'label':i, 'value':i} for i in players],
                               value = None,
                               placeholder='Player Name...',
                               multi=True,
                              )  
                 ])
    children.append(nouvelle_zone_graphe)
    return children
@app.callback(
    Output({'type':'Graphique', 'index':MATCH},'figure'),
    [Input({'type':'Selection_variable_X', 'index':MATCH}, 'value'),
    Input({'type':'Selection_variable_Y', 'index':MATCH}, 'value'),
    Input('pitch-type', 'value'),
    Input('color', 'value'),
    Input('player', 'value'),
    ]
)
def create_figure(column_x, column_y,pitch_type_value,color_value,player_value):
    a = tm.reindex(columns = ['Pitchtype','AVG RelSpeed','AVG SpinRate','AVG HorzBreak','AVG InducedVertBreak','AVG RelSide','AVG RelHeight','AVG Extension'])
    DATA = tm
    print(player_value)
    print(pitch_type_value)
    try:
        if len(player_value) > 0:
            DATA = tm.query("Name == @player_value")
    except TypeError:
        pass
    try:
        if len(pitch_type_value) > 0:
            DATA = tm.query("Pitchtype == @pitch_type_value")
    except TypeError:
        pass
    try:
        if len(pitch_type_value) > 0 and len(player_value) > 0:
            DATA = tm.query("Pitchtype == @pitch_type_value").query("Name == @player_value")
    except TypeError:
        pass
    return px.scatter(DATA,x=column_x,y=column_y,color=color_value, hover_name = "Name", hover_data=a.columns.tolist(),title=f"{column_x} vs {column_y} for 2022 TM")
def display_output(column_x,column_y):
            return create_figure(column_x, column_y)
if __name__ == '__main__':
    app.run_server(debug=True)
