import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput, Select, LabelSet
from bokeh.plotting import figure

from task_plotants import getPlotantsAntennaInfo

# Set up data
source = ColumnDataSource(data=dict(x=[], y=[], labels=[]))

# Set up plot
plot = figure(plot_height=400, plot_width=400)
plot.scatter('x', 'y', source=source, size=10,
             line_color="red", fill_color="red", fill_alpha=0.5)

# Set up widgets
text = TextInput(title="Path to MS", value='Path to MS')
mss=["/Users/lopez/temp/CASA/casa-distro/regression/ic2233/ic2233_1.ms",
     "/Users/lopez/temp/CASA/casa-distro/regression/unittest/setjy/3c391calonly.ms",
     "/Users/lopez/temp/CASA/casa-distro/regression/unittest/setjy/alma_ephemobj_icrs.ms"]
select = Select(title="Choose MS", value=mss[0], options=mss)

# Set up callbacks
def update_plot(attrname, old, new):
    vis = select.value
    exclude = []
    telescope, names, ids, xpos, ypos, stations = getPlotantsAntennaInfo(vis, False, exclude, False)
    source.data = dict(x=xpos, y=ypos, labels=names)

    plot.title.text = telescope
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

    plot.xaxis[0].axis_label = labelx
    plot.yaxis[0].axis_label = labely

    labels = LabelSet(x='xp', y='yp', text='labels', level='glyph',
                         x_offset=10, y_offset=10, source=source,
                         render_mode='canvas')
    plot.add_layout(labels)


# text.on_change('value', update_plot)
select.on_change('value', update_plot)


# Set up layouts and add to document
inputs = column(text,select)
curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "PLOTANTS"
