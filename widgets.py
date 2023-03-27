#Imports
from bokeh.plotting import figure, show
from bokeh.layouts import layout
from bokeh.models import Div, RangeSlider, Spinner, HoverTool, ColumnDataSource, CategoricalColorMapper
import pandas as pd
from bokeh.palettes import Category20c, plasma # select a palette
from bokeh.transform import transform

df = pd.read_excel('factbook_fixed.xlsx')
numLines = len(df. index)
# print(numLines) #149

list_colors = []
for i in Category20c:
    for j in Category20c[i]:
        list_colors.append(j)

colormap = dict(zip(df['Country'], list_colors))

colors = [colormap[x] for x in df['Country']]

cols = df.columns
cols = cols.map(lambda x: x.strip().replace(' ', '_'))
df.columns = cols

#Create Data
x = df['Industrial_production_growth_rate']
y = df["GDP_real_growth_rate"]

list_x = x.tolist()
list_y = y.tolist()
list_country = df["Country"].tolist()

desc = [str(i) for i in df["Country"]]
# desc = dict(zip(df['Country'], desc))
# desc = df["Country"].tolist()

hover = HoverTool(tooltips=[
    ("index", "$index"),
    ("(x,y)", "(@x, @y)"),
    ('country', "@desc"),
])
source = ColumnDataSource(data=dict(x=list_x, y=list_y, desc=desc, label=list_country))
# mapper = LinearColorMapper(palette=plasma(256), low=min(list_y), high=max(list_y))
color_mapper = CategoricalColorMapper(factors=list_country, palette=colors)

#create plot/figure
p = figure(x_range=(1,9), width=800, height=400, tools=[hover], title="Widgets for Factbook Data")
p.xaxis.axis_label = 'Industrial Production Growth Rate'
p.yaxis.axis_label = 'GDP Real Growth Rate'

# points = p.scatter(x, y, size=20, color=colors)
# points = p.circle('x', 'y', size=20, source=source)
# points = p.circle('x', 'y', size=20, source=source, fill_color=transform('y', mapper))
points = p.circle(
    x='x', y='y', source=source,
    size=20,
    color={'field': 'label', 'transform': color_mapper},
    legend_group='label'
)

# points = p.circle(x=x, y=y, size=40, fill_color="#FFE1FF")

#Div
div = Div(
    text="""<p>Select the circle's size using this controller:</p>""",
    width=200,
    height=300
)

label_list_country = map(str, list_country)
label = Div(
    text="""<p>Select the circle's size using this controller:</p>""",
    width=200,
    height=300
)

#Spinner
spinner = Spinner(
    title="Circle Size",
    low=0,
    high=60,
    step=5,
    value = points.glyph.size,
    width=200,
)

spinner.js_link("value", points.glyph, "size")

#Range Slider
range_slider = RangeSlider(
    title="Adjust X-Axis Range",
    start=0,
    end= 10,
    step=1,
    value=(p.x_range.start, p.x_range.end),
)

range_slider.js_link("value", p.x_range, "start", attr_selector=0)

range_slider.js_link("value", p.x_range, "end", attr_selector=1)

# Create layout
layout = layout(
    [
        [div, spinner],
        [range_slider],
        [p],
    ],

)

show(layout)