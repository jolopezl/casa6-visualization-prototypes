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

import os.path

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Center([
    # Welcome message
    html.H1("Dash web application demo", style={'text-align': 'center'}),
    html.Div(id='helper_text'),
    html.Br(),
    # Input and draw actions
    html.Div(
        [dbc.Input(id="input_path", placeholder="Path to MS", type="text")],
        style={'width': '100%', 'display': 'inline-block'}
    ),
    # html.Br(),
    # # test upload
    # html.Div([
    #     dcc.Upload(
    #         id='upload-data',
    #         children=html.Div([
    #             'Drag and Drop or ',
    #             html.A('Select Files')
    #         ]),
    #         style={
    #             'width': '100%',
    #             'height': '60px',
    #             'lineHeight': '60px',
    #             'borderWidth': '1px',
    #             'borderStyle': 'dashed',
    #             'borderRadius': '5px',
    #             'textAlign': 'center',
    #             'margin': '10px'
    #         },
    #         # Allow multiple files to be uploaded
    #         multiple=True
    #     ),
    #     html.Div(id='upload-data-info'),
    # ]),
    # Buttons
    html.Div([
        html.Br(),
        # dbc.Button("Draw XY", id="example-button-1", className="mr-1"),
        # dbc.Button("Draw Polar", id="example-button-2", className="mr-1"),
        dcc.RadioItems(
            id='plot-type',
            options=[{'label': i, 'value': i} for i in ['XY', 'Polar']],
            value='XY',
            labelStyle={'display': 'inline-block'}
        )
    ]),
    # Output container
    html.Br(),
    html.Div(id='output_container', children=[
        dcc.Graph(id='output_graph', figure={}),
        dbc.Alert(id='alert-1', children="Choose a MS", color="info")])
])  # , style={'width': '50%'})


# @app.callback(
#     Output(component_id='upload-data-info', component_property='children'),
#     Input(component_id='upload-data', component_property='contents')
# )
# def update_upload_info(contents):
#     print(contents)
#     return 'Upload is {}'.format(contents)


@app.callback(
    Output(component_id='helper_text', component_property='children'),
    Input(component_id='input_path', component_property='value')
)
def update_helper_text(input):
    if input is None or input is '':
        # return "Enter path to a MS"
        return "Enter path to MS, for example: /Users/lopez/temp/CASA/casa-distro/regression/ic2233/ic2233_1.ms or " \
               "/Users/lopez/temp/CASA/casa-distro/regression/unittest/setjy/3c391calonly.ms or " \
               "/Users/lopez/temp/CASA/casa-distro/regression/unittest/setjy/alma_ephemobj_icrs.ms "
    else:
        return None


@app.callback(
    [Output(component_id='output_graph', component_property='figure'),
     Output(component_id='alert-1', component_property='children')],
    [Input(component_id='input_path', component_property='value'),
     Input('plot-type', 'value')]
)
def update_graph(input_path, plot_type):
    if input_path is None:
        return [draw_empty_figure(), "Nothing to draw yet"]

    if os.path.exists(input_path) is False:
        return [draw_empty_figure(), 'MS {} not found'.format(input_path)]

    vis = input_path  # "/Users/lopez/temp/CASA/casa-distro/regression/ic2233/ic2233_1.ms"
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

    fig = None
    if plot_type == "XY":
        fig = draw_xy(vis, exclude)
    elif plot_type == "Polar":
        fig = draw_polar(vis, exclude)
    else:
        fig = draw_empty_figure()
    return [fig, 'Drawn selected MS: {}'.format(input_path)]


def draw_empty_figure():
    fig = go.Figure()
    fig.update_layout(width=500, height=500)
    return fig


def draw_xy(vis, exclude=None):
    telescope, names, ids, xpos, ypos, stations = getPlotantsAntennaInfo(vis, False, exclude, False)
    # fig = px.scatter(x=xpos, y=ypos, width=450, height=450)
    fig = go.Figure()
    xytrace = go.Scatter(x=xpos, y=ypos, name='antennas', mode='markers', marker_color='rgba(152, 0, 0, .8)')
    fig.add_trace(xytrace)
    # Set options common to all traces with fig.update_traces
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=10)

    if telescope == 'VLBA':
        labelx = 'Longitude (deg)'
        labely = 'Latitude (deg)'
    else:
        # use m or km units
        units = ' (m)'
        if np.median(xpos) > 1e6 or np.median(ypos) > 1e6:
            xpos /= 1e3
            ypos /= 1e3
            units = ' (km)'
        labelx = 'X' + units
        labely = 'Y' + units

    fig.update_layout(title=telescope,
                      xaxis=dict(title_text=labelx),
                      yaxis=dict(title_text=labely),
                      yaxis_zeroline=False, xaxis_zeroline=False,
                      autosize=False, width=500, height=500)
    return fig


def draw_polar(vis, exclude=None):
    telescope, names, ids, xpos, ypos, stations = getPlotantsAntennaInfo(vis, False, exclude, False)

    # code from pipeline summary.py
    # PlotAntsChart draw_polarlog_ant_map_in_subplot
    if 'VLA' in telescope:
        # For (E)VLA, set a fixed local center position that has been
        # tuned to work well for its array configurations (CAS-7479).
        xcenter, ycenter = -32, 0
        # rmin_min, rmin_max = 12.5, 350
    else:
        # For non-(E)VLA, take the median of antenna offsets as the
        # center for the plot.
        xcenter = np.median(xpos)
        ycenter = np.median(ypos)
        # rmin_min, rmin_max = 3, 350

    r = ((xpos - xcenter) ** 2 + (ypos - ycenter) ** 2) ** 0.5
    theta = np.arctan2(xpos - xcenter, ypos - ycenter) * 180.0 / 3.14
    data = go.Scatterpolar(r=r, theta=theta)
    fig = go.Figure(data)
    # Set options common to all traces with fig.update_traces
    fig.update_traces(mode='markers', marker_line_width=2, marker_size=10)
    fig.update_layout(title=telescope,
                      xaxis=dict(title_text="X (m)"),
                      yaxis=dict(title_text="Y (m)"),
                      yaxis_zeroline=False, xaxis_zeroline=False,
                      autosize=False, width=500, height=500)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
