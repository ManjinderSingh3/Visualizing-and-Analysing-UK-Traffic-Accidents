# Import all the necessary dependencies
import dash
from dash.dependencies import Output, Input, State

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from data_preprocessing import pre_processing
from clustering import *

mapbox_token = 'pk.eyJ1IjoibWFuamluZGVyLTMiLCJhIjoiY2t3aGkyZGkyMHlsbjJzbzRwYmZwM3AzdSJ9.f46G3mIn5OvpVLjKsWCUsw'
def visualization():
    dataframe = pre_processing()
    df = dataframe.copy()
    numeric_features = df[['accident_severity','speed_limit','urban_or_rural_area']]
    app_layout = dbc.Container([
        # < ----------------- Task 1: Accidents per month at a Geographical Locations ----------------->
        # Area to show SLIDER
        dbc.FormGroup([
            dbc.Label("Select the month to see accidents that occurred in that month."),
            dcc.Slider(id="months_slider", min=df['Month'].min(), max=df['Month'].max(), step=1,
                       # value=[df['Month'].min(), df['Month'].max()],
                       value=1,
                       marks={1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July',
                              8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'},
                       ),
        ]),
        html.Br(),

        dbc.FormGroup([
            dbc.Card([
                dbc.CardBody([
                    dbc.Label(['Choose Columns to decide Size of GPS points'],
                              style={'font-weight': 'bold', "text-align": "center"}),
                    dcc.Dropdown(id="gps_points_size",
                                 options=[{'label': i, 'value': i} for i in numeric_features],
                                 value=numeric_features.columns[0],
                                 searchable=True,
                                 placeholder='Please select...',
                                 clearable=True,
                                 style={'width': "90%"},
                                 ),
                    html.Br(),
                ]),
            ],
                style={"width": "32rem"}
            )
        ]),
        html.Br(),

        # Area to show GRAPHS
        html.H4(children='Geographic Location of Accidents', style={'text-align': 'center'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='accidents_map', figure={})),
        ]),
        html.Br(),

        html.H2(children='DBSCAN Clustering Algorithm'),
        html.Br(),
        # <-----------Select Features on which size of gps points will depend ---------->
        dbc.FormGroup([
            dbc.Label("Choose the EPS value for DBSCAN Algorithm"),
            dcc.Slider(id="eps_value", min=0.1, max=1, step=0.1,
                       value=0.2,
                       marks={0.1: '0.1', 0.2: '0.2', 0.3: '0.3', 0.4: '0.4', 0.5: '0.5', 0.6: '0.6', 0.7: '0.7',
                              0.8: '0.8', 0.9: '0.9', 1: '1.0'}
                       ),
        ]),
        html.Br(),

        dbc.Button('Show Map', id='map_button', color='primary'),
        html.Br(),

        html.H4(children='CLUSTERS of accident locations', style={'text-align': 'center'}),
        html.Br(),
        # <--------- Area to show GRAPHS ---------->
        dcc.Graph(id='accidents_map1', figure={}),
        html.Br(),
    ])
    return app_layout


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
dataframe = pre_processing()
df = dataframe.copy()
numeric_features = df[['accident_severity', 'speed_limit', 'urban_or_rural_area']]
app.layout = dbc.Container([
    html.H1(children='Traffic Accidents in UK', style={'text-align': 'center'}),
    html.Hr(),
    visualization()
])

def map_options(selected_month, selected_column):
    if (selected_column == numeric_features.columns[0]):
        required_df = df[df['Month'] == selected_month]

        colors = {1: 'red', 2: 'orange', 3: 'green'}
        required_df['color'] = required_df['accident_severity'].apply(lambda x: colors[x])
        gps_point_size = {1: 11, 2: 8, 3: 5}
        required_df['scatter_size'] = required_df['accident_severity'].apply(lambda x: gps_point_size[x])

        traces = []
        traces.append({
            'type': 'scattermapbox',
            'mode': 'markers',
            'lat': required_df['latitude'],
            'lon': required_df['longitude'],
            'marker': {
                'color': required_df['color'],
                'size': required_df['scatter_size'],
            },
            'hoverinfo': 'text',
            'text': required_df[selected_column]  # Text will show location
        })
        layout = {
            'height': 500,
            'autosize': True,
            'hovermode': 'closest',
            'mapbox': {
                'accesstoken': mapbox_token,
                'center': {  # Set the geographic centre - trial and error
                    'lat': 56.5,
                    'lon': -4
                },
                'zoom': 3.8,
                'style': 'dark',
            },
            'margin': {'t': 0,
                       'b': 0,
                       'l': 0,
                       'r': 0},
            'legend': {
                'font': {'color': 'white'},
                'orientation': 'h',
                'x': 0,
                'y': 1.01
            }
        }
        fig = dict(data=traces, layout=layout)
        return fig

    elif(selected_column == numeric_features.columns[1]):
        required_df = df[df['Month'] == selected_month]

        colors = {-1: 'white', 20: 'red', 30: 'orange', 40: 'green', 50: 'yellow', 60: 'blue', 70: 'coral'}
        required_df['color'] = required_df['speed_limit'].apply(lambda x: colors[x])
        gps_point_size = {-1: 0, 20: 4, 30: 5, 40: 6, 50: 7, 60: 8, 70: 9}
        required_df['scatter_size'] = required_df['speed_limit'].apply(lambda x: gps_point_size[x])

        traces = []
        traces.append({
            'type': 'scattermapbox',
            'mode': 'markers',
            'lat': required_df['latitude'],
            'lon': required_df['longitude'],
            'marker': {
                'color': required_df['color'],
                'size': required_df['scatter_size'],
            },
            'hoverinfo': 'text',
            'text': required_df[selected_column]
        })
        layout = {
            'height': 500,
            'autosize': True,
            'hovermode': 'closest',
            'mapbox': {
                'accesstoken': mapbox_token,
                'center': {
                    'lat': 56.5,
                    'lon': -4
                },
                'zoom': 3.8,
                'style': 'dark',
            },
            'margin': {'t': 0,
                       'b': 0,
                       'l': 0,
                       'r': 0},
            'legend': {
                'font': {'color': 'white'},
                'orientation': 'h',
                'x': 0,
                'y': 1.01
            }
        }
        fig = dict(data=traces, layout=layout)
        return fig

    elif (selected_column == numeric_features.columns[2]):
        required_df = df[df['Month'] == selected_month]

        colors = {1: 'red', 2: 'green'}
        required_df['color'] = required_df['urban_or_rural_area'].apply(lambda x: colors[x])
        gps_point_size = {1: 9, 2: 6}
        required_df['scatter_size'] = required_df['urban_or_rural_area'].apply(lambda x: gps_point_size[x])

        traces = []
        traces.append({
            'type': 'scattermapbox',
            'mode': 'markers',
            'lat': required_df['latitude'],
            'lon': required_df['longitude'],
            'marker': {
                'color': required_df['color'],
                'size': required_df['scatter_size'],
            },
            'hoverinfo': 'text',
            'text': required_df[selected_column]  # Text will show location
        })
        layout = {
            'height': 500,
            'autosize': True,
            'hovermode': 'closest',
            'mapbox': {
                'accesstoken': 'pk.eyJ1IjoibWFuamluZGVyLTMiLCJhIjoiY2t3aGkyZGkyMHlsbjJzbzRwYmZwM3AzdSJ9.f46G3mIn5OvpVLjKsWCUsw',
                'center': {
                    'lat': 56.5,
                    'lon': -4
                },
                'zoom': 3.8
            },
            'margin': {'t': 0,
                       'b': 0,
                       'l': 0,
                       'r': 0},
            'legend': {
                'font': {'color': 'white'},
                'orientation': 'h',
                'x': 0,
                'y': 1.01
            }
        }
        fig = dict(data=traces, layout=layout)
        return fig

# <------------ CALLBACK-1 --------------->
@app.callback(
    Output(component_id='accidents_map', component_property='figure'),
    [Input(component_id='months_slider', component_property='value'),
     Input(component_id='gps_points_size', component_property='value')
     ]
)
def visualization_1(selected_month,selected_column):
    print("Month:\n", selected_month)
    print("Column:\n", selected_column)
    print("--------")
    final_fig = map_options(selected_month, selected_column)
    return final_fig

# <------------ CALLBACK-2 --------------->
@app.callback(
    Output(component_id='accidents_map1', component_property='figure'),
    Input(component_id='map_button', component_property='n_clicks'),
    [State(component_id='months_slider', component_property='value'),
     State(component_id='gps_points_size', component_property='value'),
     State(component_id='eps_value', component_property='value')]
)
def visualization_1(nclicks, selected_month, selected_column, epsValue):

    required_df = df[df['Month'] == selected_month]
    required_df.dropna(inplace=True)

    required_columns = ['longitude', 'latitude', 'accident_severity', 'speed_limit', 'urban_or_rural_area']
    required_df = required_df[required_columns]

    result = dbscan(required_df, epsValue)
    print("*** Number of Unique Clusters ***", result['unique_clusters'])

    print("Month:\n", selected_month)
    print("Column:\n", selected_column)
    print("EPS Value:\n", epsValue)
    print("----------")

    traces = []
    traces.append({
        'type': 'scattermapbox',
        'mode': 'markers',
        'lat': required_df['latitude'],
        'lon': required_df['longitude'],
        'marker': {
            'color': result['clusters'],
        },
        'hoverinfo': 'text',
        'text': required_df[selected_column]
    })
    layout = {
        'height': 500,
        'autosize': True,
        'hovermode': 'closest',
        'mapbox': {
            'accesstoken': mapbox_token,
            'center': {  # Set the geographic centre - trial and error
                'lat': 56.5,
                'lon': -4
            },
            'zoom': 3.8,
        },
        'margin': {'t': 0,
                   'b': 0,
                   'l': 0,
                   'r': 0},
        'legend': {
            'font': {'color': 'white'},
            'orientation': 'h',
            'x': 0,
            'y': 1.01
        }
    }
    fig = dict(data=traces, layout=layout)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
