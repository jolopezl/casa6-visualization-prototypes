from __future__ import absolute_import
# get is_CASA6 and is_python3
from casatasks.private.casa_transition import is_CASA6

if is_CASA6:
    from casatools import table, msmetadata, quanta, ms, measures
    from casatasks import casalog
else:
    from casac import table, msmetadata, quanta, ms, measures
    from taskinit import casalog
    from casa_system import casa

from task_plotants import getPlotantsAntennaInfo

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Center([
    # Welcome message
    html.H1("Dash web application demo", style={'text-align': 'center'}),
    # Input and draw actions
    html.Div([dbc.Input(id="input_path",
                        placeholder="/Users/lopez/temp/CASA/casa-distro/regression/ic2233/ic2233_1.ms", type="text"),
              html.Br(),
              dbc.Button("Draw XY", id="example-button-1", className="mr-1"),
              dbc.Button("Draw Polar", id="example-button-2", className="mr-1"),
              ]),
    # html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='output_graph', figure={}),
    dbc.Alert("This is an info alert. Good to know!", color="info"),
])  # , style={'width': '50%'})


@app.callback(
    [Output(component_id='output_graph', component_property='figure')],
    [Input(component_id='input_path', component_property='value')]
)
def update_graph(input_path):
    print(input_path)

    vis = "/Users/lopez/temp/CASA/casa-distro/regression/ic2233/ic2233_1.ms"
    exclude = None

    # remove trailing / for title basename
    if vis[-1] == '/':
        vis = vis[:-1]
    myms = ms()
    try:
        exclude = myms.msseltoindex(vis, baseline=exclude)['antenna1'].tolist()
    except RuntimeError as rterr:  # MSSelection failed
        errmsg = str(rterr)
        errmsg = errmsg.replace('specificion', 'specification')
        errmsg = errmsg.replace('Antenna Expression: ', '')
        raise RuntimeError("Exclude selection error: " + errmsg)

    telescope, names, ids, xpos, ypos, stations = getPlotantsAntennaInfo(vis, False, exclude, False)
    # fig = px.scatter(x=xpos, y=ypos, width=450, height=450)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=xpos, y=ypos,
        name='antennas',
        mode='markers',
        marker_color='rgba(152, 0, 0, .8)'
    ))

    # Set options common to all traces with fig.update_traces
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=10)
    fig.update_layout(title='VLA',
                      xaxis=dict(title_text="X (m)"),
                      yaxis=dict(title_text="Y (m)"),
                      yaxis_zeroline=False, xaxis_zeroline=False,
                      autosize=False, width=500, height=500)

    return [fig]


if __name__ == '__main__':
    app.run_server(debug=True)
