#Import relevant packages

import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt
import os

from bokeh.io import show, curdoc, output_notebook
from bokeh.layouts import column
from bokeh.models import (
    ColumnDataSource,
    Label,
    LabelSet,
    CheckboxGroup,
    CustomJS,
    Button,
)
from bokeh.models.annotations import LabelSet
from bokeh.palettes import Category10
from bokeh.plotting import figure

import numpy as np

os.environ['BOKEH_RESOURCES'] = "inline"

#  Read-in the pre-processed data
current_dir = os.getcwd()
data_dir = os.path.join(current_dir, 'Data')
os.chdir(data_dir)

# df without urban-rural classification
df = pd.read_csv('cleaned_lang_SO.csv')

# Let's take a quick glance

df.head()

# df with urban-rural classification
df2 = pd.read_csv('urban_rural_SO.csv')

# Let's take a quick glance
# IMPORTANT: we only have urb_rural classification for ENGLISH LA's
df2.head()

df['Urb_Rur'] = df2['Urb_Rur']

import pandas as pd
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure, curdoc
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap
from bokeh.models import ColorBar, BasicTicker, PrintfTickFormatter, LogColorMapper


output_notebook()

# Prepare data sources
df['Urb_Rur'] = df['Urb_Rur'].astype(str)
source = ColumnDataSource(df)


# Define tooltips
tool = [
    ("index", "$index"),
    ("(x,y)", "($x, $y)"),
    ("name", "@LA_name"),
]

p0 = figure(title = "Relationship between Non-response Rate and Non-English Speakers", x_axis_label = "Percentage of Non-English Speakers",
           y_axis_label = "Non-response rate", tooltips = tool)

p0.scatter("Percentage", "Non-response_rate", source=source, fill_alpha=0.5, size=10)

# Plot 1 (By Region)
p1 = figure(title="Relationship between Non-response Rate and Non-English Speakers",
            x_axis_label="Percentage of Non-English Speakers",
            y_axis_label="Non-response Rate",
            tooltips=tool)

for region, color in zip(df.region_x.unique(), Category10[10]):
    b = df[df.region_x == region]
    p1.circle(x='Percentage', y='Non-response_rate', size=10, alpha=0.5, color=color,
              legend_label=region, muted_color=color, muted_alpha=0.1, source=ColumnDataSource(b))

p1.legend.location = "bottom_right"
p1.legend.click_policy = "hide"
p1.legend.title = "Regions"

# Plot 2 (Urban vs Rural)
p_2 = figure(title="Relationship between Non-response Rate and Non-English Speakers",
            x_axis_label="Percentage of Non-English Speakers",
            y_axis_label="Non-response Rate",
            tooltips=tool)

urban_rural_sources = {}  # Create a dictionary to store the ColumnDataSource objects
for urb_rur in df.Urb_Rur.unique():
    urban_rural_sources[urb_rur] = ColumnDataSource(df[df.Urb_Rur == urb_rur])

for urb_rur, color in zip(df.Urb_Rur.unique(), Category10[10]):
    p_2.circle(x='Percentage', y='Non-response_rate', size=10, alpha=0.5, color=color,
              legend_label=urb_rur, muted_color=color, muted_alpha=0.1, source=urban_rural_sources[urb_rur])

p_2.legend.location = "bottom_right"
p_2.legend.click_policy = "hide"
p_2.legend.title = "Urban-Rural"



# Plot 3 (Shannon Index)
color_map = LogColorMapper(palette="Viridis256", low=df.Shannon_idx.min(), high=df.Shannon_idx.max())

p3 = figure(title="Relationship between Non-response Rate and Non-English Speakers",
            x_axis_label="Non-response Rate",
            y_axis_label="Percentage of Non-English Speakers",
            tooltips=tool)

p3.scatter("Percentage", "Non-response_rate", source=source, fill_alpha=0.5, size=10,
           color={'field': 'Shannon_idx', 'transform': color_map})

color_bar = ColorBar(color_mapper=color_map,
                     title='Shannon Index',
                     ticker=BasicTicker(desired_num_ticks=5),
                     formatter=PrintfTickFormatter(format='%.2f'))

p3.add_layout(color_bar, 'right')

# Dropdown menu
dropdown = Select(title="Color By:", value="None", options=["Default", "Region", "Urban", "Shannon Index"])

# Define the update function
def update_scatterplots(attr, old, new):
    if dropdown.value == "Default":
        p0.visible = True
        p1.visible = False
        p_2.visible = False
        p3.visible = False
    elif dropdown.value == "Region":
        p0.visible = False
        p1.visible = True
        p_2.visible = False
        p3.visible = False
    elif dropdown.value == "Urban":
        p0.visible = False
        p1.visible = False
        p_2.visible = True
        p3.visible = False
    elif dropdown.value == "Shannon Index":
        p0.visible = False
        p1.visible = False
        p_2.visible = False
        p3.visible = True

# Set initial visibility
p0.visible = True
p1.visible = False
p_2.visible = False
p3.visible = False

# Add the callback to the dropdown menu
dropdown.on_change('value', update_scatterplots)

# Create a layout with the dropdown menu and the scatterplots
layout = column(dropdown, p0, p1, p_2, p3)

# Add the layout to the document
curdoc().add_root(layout)

# show(p2)

# Read-in pre-processed data for religion

rel = pd.read_csv('cleaned_religion_SO.csv')

totals = pd.read_csv('gen_totals_SO.csv')

totals = totals.sort_values(by = "Percent_of_survey_respondents", ascending = False)

# Read-in Non-response table

nr_totals = pd.read_csv('nr_totals_SO.csv')

nr_totals.head()

nr_totals = nr_totals.sort_values(by = "Contribution_to_overall_non_response_rate", ascending = False)

import pandas as pd
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Select, HTMLTemplateFormatter
from bokeh.models.widgets import DataTable, TableColumn, Div
from bokeh.plotting import figure, show, curdoc
from bokeh.io import output_notebook

# Custom cell formatter
template = """
<% if (Religion_categories == selected_religion) { %>
    <span style="color: red; font-weight: bold"><%= value %></span>
<% } else { %>
    <span style="font-weight: bold"><%= value %></span>
<% } %>
"""

def create_formatter(selected_religion):
    formatter = HTMLTemplateFormatter(template=template.replace("selected_religion", f"'{selected_religion}'"))
    return formatter

# Create DataTable for layout1
source1 = ColumnDataSource(totals)

columns1 = [
    TableColumn(field="Religion_categories", title="Religion", formatter=create_formatter('Christian')),
    TableColumn(field="Observation", title="Observation", formatter=create_formatter('Christian')),
    TableColumn(field="Percent_of_survey_respondents", title="% of respondents", formatter=create_formatter('Christian')),
]

heading1 = Div(text="<h1>Totals</h1>", width=300)

data_table1 = DataTable(source=source1, columns=columns1, editable=False, width=500, index_position=None)

layout1 = column(heading1, data_table1)

# Create DataTable for layout2
source2 = ColumnDataSource(nr_totals)

columns2 = [
    TableColumn(field="Religion_categories", title="Religion", formatter=create_formatter('Christian')),
    TableColumn(field="Observation", title="Observation", formatter=create_formatter('Christian')),
    TableColumn(field="Non_response_rate", title="Non response rate", formatter=create_formatter('Christian')),
    TableColumn(field="Contribution_to_overall_non_response_rate", title="% of total Non-response rate", formatter=create_formatter('Christian')),
]

heading2 = Div(text="<h1>Non-response rates</h1>", width=300)

data_table2 = DataTable(source=source2, columns=columns2, editable=False, width=700, index_position=None)

layout2 = column(heading2, data_table2)

# Scatter plot
output_notebook()

# Prepare data
rel['selected_religion'] = rel['Christian_%']  # Default religion
rel['selected_percentages'] = rel['Group_Percentages_Christian']

source = ColumnDataSource(rel)

# Define tooltips
tool = [
    ("index", "$index"),
    ("(x,y)", "($x, $y)"),
    ("name", "@LA_name"),
]

# Create figure
p4 = figure(title="Relationship between % of religious group in given LA, and their non-response rate",
            y_axis_label="Non-response Rate", x_axis_label="Percentage of religious group in given LA", tooltips=tool)

# Scatter plot
p4.scatter("selected_religion", "selected_percentages", source=source, fill_alpha=0.5, size=10)

def update_highlighted_rows(selected_religion):
    formatter = create_formatter(selected_religion)
    for col in columns1:
        col.formatter = formatter
    for col in columns2:
        col.formatter = formatter
    data_table1.columns = columns1
    data_table2.columns = columns2

# Define callback for updating data source

def update_plot(attr, old, new):
    selected_religion = select_religion.value
    rel['selected_religion'] = rel[f'{selected_religion}_%']
    rel['selected_percentages'] = rel[f'Group_Percentages_{selected_religion}']
    source.data = source.from_df(rel)
    update_highlighted_rows(selected_religion)

# Create select widget
options = ['Christian', 'No religion', 'Muslim', 'Jewish', 'Buddhist', 'Hindu', 'Sikh', 'Other']
select_religion = Select(title="Religious Group:", value='Christian', options=options)
select_religion.on_change('value', update_plot)

# Initial update of the highlighted rows
update_highlighted_rows(select_religion.value)

# Layout
layout = column(select_religion, p4)
l = row(layout1, layout2)

# Show plot
curdoc().add_root(column(layout, l))
