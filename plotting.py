from motion_detect import df
from bokeh.models import HoverTool,ColumnDataSource
from bokeh.plotting import figure,output_file,show
df["st"] = df["start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["ed"] = df["end"].dt.strftime("%Y-%m-%d %H:%M:%S")


cds = ColumnDataSource(df)

p = figure(x_axis_type='datetime',height=300,width=600,sizing_mode="stretch_width",title='motion graph')
p.yaxis.minor_tick_line_width = 0
p.ygrid.grid_line_color = None

hover = HoverTool(tooltips=[("Start","@st"),("End","@ed")])
p.add_tools(hover)


q= p.quad(left="start",right="end",bottom=0,top=1,color='green',source=cds)

output_file("Graph.html")
show(p)