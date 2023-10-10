#Import relevant packages

# provides a means for interacting with the underlying operating system
import os
# includes functions for manipulating data - getting it into the right format for graphs
import pandas as pd
# includes functions for performing mathematical operations
import numpy as np
# plotting library with functions for visualisations
import matplotlib.pylab as plt


# Bokeh - used to create interactive visualisations
from bokeh.io import curdoc, output_notebook
from bokeh.layouts import column, row
from bokeh.models import (
    ColumnDataSource,
    Spacer,
    Select,
    HTMLTemplateFormatter,
    BasicTicker,
    PrintfTickFormatter,
    LinearColorMapper,
    ColorBar,
)
from bokeh.models.widgets import DataTable, TableColumn, Div
from bokeh.plotting import figure

# Set environment variable to inline 
# Tells Python program to package all the things needed to display our Bokeh plots inside the HTML file itself
os.environ['BOKEH_RESOURCES'] = "inline"


#  Read-in the pre-processed data
current_dir = os.getcwd()
data_dir = os.path.join(current_dir, 'Data')
os.chdir(data_dir)

# read-in SO data for first scatterplot
df = pd.read_csv('final_lang_so.csv')


# Read-in GI data for first scatterplot

df_gi = pd.read_csv('final_lang_gi.csv')



# Interactive scatterplots

# STARTING WITH MAIN LANGUAGE SCATTERPLOTS


# Prepare data sources
source = ColumnDataSource(df)
source2 = ColumnDataSource(df_gi)

# Set column type

df['Urb_Rur'] = df['Urb_Rur'].astype(str)
df_gi['Urb_Rur'] = df_gi['Urb_Rur'].astype(str)

# Colourblind palette 

okabe_ito = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7', '#999999']


# Define tooltips
tool = [
    ("index", "$index"),
    ("(x,y)", "(@Percentage{0.2f}, @Non_response_rate{0.2f})"),
    ("name", "@LA_name"),
]

# CREATE PLOTS FOR GI FIRST

# Create first default graph figure, set title and x and y labels
p0 = figure(title = "Relationship between Non-response Rate and Non-English Speakers", x_axis_label = "Percentage of Non-English Speakers",
           y_axis_label = "Non-response rate", tooltips = tool)

# Create scatterplot with x and y values from columns
p0.scatter("Non_Eng_Percentages", "NR_rate", source=source, fill_alpha=0.5, size=10)

# Plot 1 (dps coloured by region)
p1 = figure(title="Relationship between Non-response Rate and Non-English Speakers",
            x_axis_label="Percentage of Non-English Speakers",
            y_axis_label="Non-response Rate",
            tooltips=tool)

# Loop through each unique region in our df, specifying index too
for (idx, region) in enumerate(df.region.unique()):
    # Subset df for unique region
    b = df[df.region == region]
    # Set colour for region by cycling through colours
    color = okabe_ito[idx % len(okabe_ito)]
    # Plot circle on scatterplot for each dp in 'b', our subsetted df
    p1.circle(x='Non_Eng_Percentages', y='NR_rate', size=10, alpha=0.5, color=color,
              legend_label=region, muted_color=color, muted_alpha=0.1, source=ColumnDataSource(b))

# Set legend attributes
p1.legend.location = "bottom_right"
# Specifies click policy, i.e., hides dps when user clicks on specific region in legend
p1.legend.click_policy = "hide"
p1.legend.title = "Regions"


# Plot 2 (dps coloured by urban-rural classification)
p_2 = figure(title="Relationship between Non-response Rate and Non-English Speakers",
            x_axis_label="Percentage of Non-English Speakers",
            y_axis_label="Non-response Rate",
            tooltips=tool)

# Create dictionary to store filtered data
urban_rural_sources = {} 
# Loop through each unique urban-rural classification
for urb_rur in df.Urb_Rur.unique():
    # Store subset dataframe as a CDS in dictionary key
    urban_rural_sources[urb_rur] = ColumnDataSource(df[df.Urb_Rur == urb_rur])

# Same process as for the region dps, except uses our dictionary with filtered df as its source
for (idx, urb_rur) in enumerate(df.Urb_Rur.unique()):
    color = okabe_ito[idx % len(okabe_ito)]  # cycle through colors
    p_2.circle(x='Non_Eng_Percentages', y='NR_rate', size=10, alpha=0.5, color=color,
               legend_label=urb_rur, muted_color=color, muted_alpha=0.1, source=urban_rural_sources[urb_rur])

# Set legend attributes
p_2.legend.location = "bottom_right"
p_2.legend.click_policy = "hide"
p_2.legend.title = "Urban-Rural"


# Define separate tooltips for Shannon plot
si_tool = [
    ("index", "$index"),
    ("(x,y)", "(@Percentage{0.2f}, @Non_response_rate{0.2f})"),
    ("name", "@LA_name"),
    ("SI", "@Shannon_idx{0.2f}")
]


# Set colour map with palette set colour range using min and max values
colour_map = LinearColorMapper(palette="Viridis256", low=df.Shannon_idx.min(), high=df.Shannon_idx.max())

# Plot 3 (dps coloured by Shannon Index)
p3 = figure(title="Relationship between Non-response Rate and Non-English Speakers",
            x_axis_label="Non-response Rate",
            y_axis_label="Percentage of Non-English Speakers",
            tooltips=si_tool)

# Plot dps and set colour using dictionary
p3.scatter("Non_Eng_Percentages", "NR_rate", source=source, fill_alpha=0.5, size=10,
           color={'field': 'Shannon_idx', 'transform': colour_map})

# Create ColorBar by using color_map from above
colour_bar = ColorBar(color_mapper=colour_map,
                     title='Shannon Index',
                     ticker=BasicTicker(desired_num_ticks=5),
                     formatter=PrintfTickFormatter(format='%.2f'))

# Add color_bar to the right of the p3 scatterplot layout
p3.add_layout(colour_bar, 'right')

# CREATE PLOTS FOR SO SECOND

# Create default plot
p4 = figure(title = "Relationship between Non-response Rate and Non-English Speakers", x_axis_label = "Percentage of Non-English Speakers",
           y_axis_label = "Non_response rate", tooltips = tool)

p4.scatter("Non_Eng_Percentages", "NR_rate", source=source2, fill_alpha=0.5, size=10)


# Plot 1 (dps coloured by region)
p5 = figure(title="Relationship between Non-response Rate and Non-English Speakers",
            x_axis_label="Percentage of Non-English Speakers",
            y_axis_label="Non-response Rate",
            tooltips=tool)

for (idx, region) in enumerate(df_gi.region.unique()):
    c = df_gi[df_gi.region == region]
    color = okabe_ito[idx % len(okabe_ito)]  # cycle through colors
    p5.circle(x='Non_Eng_Percentages', y='NR_rate', size=10, alpha=0.5, color=color,
              legend_label=region, muted_color=color, muted_alpha=0.1, source=ColumnDataSource(c))

p5.legend.location = "bottom_right"
p5.legend.click_policy = "hide"
p5.legend.title = "Regions"

# Plot 2 (dps coloured by urban vs rural)
p6 = figure(title="Relationship between Non-response Rate and Non-English Speakers",
            x_axis_label="Percentage of Non-English Speakers",
            y_axis_label="Non-response Rate",
            tooltips=tool)

urban_rural_sources = {}  
for (idx, urb_rur) in enumerate(df_gi.Urb_Rur.unique()):
    urban_rural_sources[urb_rur] = ColumnDataSource(df_gi[df_gi.Urb_Rur == urb_rur])
    color = okabe_ito[idx % len(okabe_ito)]  # cycle through colors
    p6.circle(x='Non_Eng_Percentages', y='NR_rate', size=10, alpha=0.5, color=color,
              legend_label=urb_rur, source=urban_rural_sources[urb_rur])

p6.legend.location = "bottom_right"
p6.legend.click_policy = "hide"
p6.legend.title = "Urban-Rural"



# Plot 3 (dps coloured by Shannon Index)
color_map = LinearColorMapper(palette="Viridis256", low=df_gi.Shannon_idx.min(), high=df_gi.Shannon_idx.max())

p7 = figure(title="Relationship between Non-response Rate and Non-English Speakers",
            x_axis_label="Non-response Rate",
            y_axis_label="Percentage of Non-English Speakers",
            tooltips=si_tool)

p7.scatter("Non_Eng_Percentages", "NR_rate", source=source2, fill_alpha=0.5, size=10,
           color={'field': 'Shannon_idx', 'transform': color_map})

color_bar = ColorBar(color_mapper=color_map,
                     title='Shannon Index',
                     ticker=BasicTicker(desired_num_ticks=5),
                     formatter=PrintfTickFormatter(format='%.2f'))

p7.add_layout(color_bar, 'right')

# Create dropdown menu for GI and SO scatterplots

dropdown = Select(title="Color By:", value="None", options=["Default", "Region", "Urban", "Shannon Index"])
dropdown2 = Select(title="Color By:", value="None", options=["Default", "Region", "Urban", "Shannon Index"])

# Create default descriptions using HTML

default_description = Div(text="""
<h2>Scatterplot Interaction Tips:</h2>
<ul>
    <li><b>Pan:</b> Click and drag the plot area to pan the view.</li>
    <li><b>Zoom in/out:</b> Scroll up/down with the mouse wheel to zoom in/out.</li>
    <li><b>Box zoom:</b> Click the "Box Zoom" tool in the toolbar, then click and drag a rectangle on the plot area to zoom into a specific region. Press the "Reset" tool to reset the view.</li>
    <li><b>Toggle legend items:</b> Click on the legend items to toggle the visibility of the corresponding data points. Clicking them again will make the data points visible.</li>
    <li><b>Hover:</b> Hover the mouse cursor over data points to see tooltips with additional information.</li>
    <li><b>Reset:</b> Click the "Reset" button in the toolbar to restore plot ranges to their original values.</li>
</ul>
""", width=500)

shannon_description = Div(text="""<h3>Shannon Index</h3>
<p>The Shannon Index is a measure of diversity within a community. In this context, it is used to measure religious diversity. The index quantifies the uncertainty in predicting the religious affiliation of a randomly chosen individual from the community. A higher Shannon Index indicates greater diversity.</p>
<p>Try hovering over a data point with your mouse to see its specific SI (Shannon index)</p>""",
width=300, height=200, css_classes=["shannon-description"])

urban_description = Div(text="""<h3>Urban-Rural Classification</h3>
<p>The Office for National Statistics (ONS) classifies Local Authorities into urban and rural categories. The classification is based on population density, settlement patterns, and the extent of the built-up area.</p>
<p>For more details on the classification system, visit the <a href="https://www.ons.gov.uk/methodology/geography/geographicalproducts/ruralurbanclassifications" target="_blank">ONS website</a>.</p>""",
width=300, height=200, css_classes=["urban-description"])


# Define the update functions for our first set of scatterplots
# Toggle visibility when different plot is selected from drop-down
def update_scatterplots(attr, old, new):
    if dropdown.value == "Default":
        p0.visible = True
        p1.visible = False
        p_2.visible = False
        p3.visible = False
        default_description.visible = True
        shannon_description.visible = False
        urban_description.visible = False
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
        default_description.visible = False
        shannon_description.visible = False
        urban_description.visible = True
    elif dropdown.value == "Shannon Index":
        p0.visible = False
        p1.visible = False
        p_2.visible = False
        p3.visible = True
        default_description.visible = False
        shannon_description.visible = True
        urban_description.visible = False

def update_scatterplots2(attr, old, new):
    if dropdown2.value == "Default":
        p4.visible = True
        p5.visible = False
        p6.visible = False
        p7.visible = False
        default_description.visible = True
        shannon_description.visible = False
        urban_description.visible = False
    elif dropdown2.value == "Region":
        p4.visible = False
        p5.visible = True
        p6.visible = False
        p7.visible = False
    elif dropdown2.value == "Urban":
        p4.visible = False
        p5.visible = False
        p6.visible = True
        p7.visible = False
        default_description.visible = False
        shannon_description.visible = False
        urban_description.visible = True
    elif dropdown2.value == "Shannon Index":
        p4.visible = False
        p5.visible = False
        p6.visible = False
        p7.visible = True
        default_description.visible = False
        shannon_description.visible = True
        urban_description.visible = False

# Set initial visibility, i.e., what we first see when we open the app
p0.visible = True
p1.visible = False
p_2.visible = False
p3.visible = False

# Set initial visibility
p4.visible = True
p5.visible = False
p6.visible = False
p7.visible = False

# Set initial visibility for HTML descriptions
default_description.visible = True
shannon_description.visible = False
urban_description.visible = False

# Add the callback to the dropdown menu, triggers action when user interacts with graphs
dropdown.on_change('value', update_scatterplots)
dropdown2.on_change('value', update_scatterplots2)


# Create main HTML headings to appear at top of web application

heading_sexual_orientation = Div(text="<h1>Sexual orientation</h1>", width=400)
heading_gender_identity = Div(text="<h1>Gender identity</h1>", width=400)

# Create layouts with headings, dropdowns and scatterplots in specific arrangement
layout1 = column(heading_sexual_orientation, dropdown, p0, p1, p_2, p3)
layout2 = column(heading_gender_identity, dropdown2, p4, p5, p6, p7)

layout = row(layout1, layout2, default_description, shannon_description, urban_description)

# MOVING ONTO RELIGION SCATTERPLOTS

# Read-in SO data

rel = pd.read_csv('religion_so_cleaned.csv')

# Read-in totals and non-response by religion
totals = pd.read_csv('rel_totals_so.csv')
nr_totals = pd.read_csv('rel_nr_totals_so.csv')


# Read-in GI data

rel_2 = pd.read_csv('religion_gi_cleaned.csv')

# Read-in totals and non-response
totals_2 = pd.read_csv('rel_totals_gi.csv')
nr_totals_2 = pd.read_csv('rel_nr_totals_gi.csv')

# Interactive DataTables

# STARTING WITH SO FIRST

# Create template for custom cell formatter
template = """
<% if (Religion_categories == selected_religion) { %>
    <span style="color: red; font-weight: bold"><%= value %></span>
<% } else { %>
    <span style="color: black;"><%= value %></span>
<% } %>
"""

# Create custom cell formatter which inserts the specific religion chosen by user from drop-down
def create_formatter(selected_religion):
    formatter = HTMLTemplateFormatter(template=template.replace("selected_religion", f"'{selected_religion}'"))
    return formatter

# Create custom functions to create DataTables using our total and non-response dataframes
def create_datatable(source, columns):
    heading = Div(text=f"<h1>{columns[0].title}</h1>", width=300)
    data_table = DataTable(source=source, columns=columns, editable=False, width=500, index_position=None)
    return column(heading, data_table), data_table

def create_datatable2(source, columns):
    heading = Div(text=f"<h2>{columns[0].title}</h2>", width=300)
    data_table = DataTable(source=source, columns=columns, editable=False, width=500, height = 80, index_position=None)
    return column(heading, data_table), data_table


# Set HTML description explaining how to interact with DataTables
default_description_2 = Div(text="""
<h2>DataTable Interaction Tips:</h2>
<ul>
    <li><b>Sort data:</b> Click on a column header to sort the data in ascending order, click again to sort in descending order.</li>
    <li><b>Resize columns:</b> Click and drag the border between two column headers to adjust their width.</li>
    <li><b>Dropdown selection:</b> Choose a religious group from the dropdown menu to change the data displayed in the scatterplot and highlight the corresponding rows in the DataTable.</li>
</ul>
""", width=500)


# Set source for DataTable - using totals df
source1 = ColumnDataSource(totals)

# Set column information and set default formatter to make 'Christian' bold
columns1 = [
    TableColumn(field="Religion_categories", title="Totals", formatter=create_formatter('Christian')),
    TableColumn(field="Observation", title="Observation", formatter=create_formatter('Christian')),
    TableColumn(field="Percentages", title="% of respondents", formatter=create_formatter('Christian')),
]

layout_1, data_table1 = create_datatable(source1, columns1)

# Create DataTable for layout2
source_2 = ColumnDataSource(nr_totals)

columns2 = [
    TableColumn(field="Religion_categories", title="Non-response rates", formatter=create_formatter('Christian')),
    TableColumn(field="Observation", title="Observation", formatter=create_formatter('Christian')),
    TableColumn(field="NR_rate", title="Non-response rate", formatter=create_formatter('Christian')),
    TableColumn(field="Per_Total", title="% of total Non-response", formatter=create_formatter('Christian')),
]

layout_2, data_table2 = create_datatable(source_2, columns2)

source_3 = ColumnDataSource(totals_2)

columns3 = [
    TableColumn(field="Religion_categories", title="Totals", formatter=create_formatter('Christian')),
    TableColumn(field="Observation", title="Observation", formatter=create_formatter('Christian')),
    TableColumn(field="Percentages", title="% of respondents", formatter=create_formatter('Christian')),
]

layout_3, data_table3 = create_datatable(source_3, columns3)

source_4 = ColumnDataSource(nr_totals_2)

columns4 = [
    TableColumn(field="Religion_categories", title="Non-response rates", formatter=create_formatter('Christian')),
    TableColumn(field="Observation", title="Observation", formatter=create_formatter('Christian')),
    TableColumn(field="NR_rate", title="Non-response rate", formatter=create_formatter('Christian')),
    TableColumn(field="Per_Total", title="% of total Non-response", formatter=create_formatter('Christian')),
]

layout_4, data_table4 = create_datatable(source_4, columns4)


# Scatter plot
output_notebook()

# Prepare data
rel['selected_religion'] = rel['Christian_Percentage']  # Default religion
rel['selected_percentages'] = rel['Christian_NR']

source = ColumnDataSource(rel)

# Define tooltips
tool = [
    ("index", "$index"),
    ("(x,y)", "(@selected_religion{0.2f}, @selected_percentages{0.2f})"),
    ("name", "@LA_name"),
]

# Create figure
p8 = figure(title="Relationship between % of religious group in given LA, and their non-response rate",
            y_axis_label="Non-response Rate", x_axis_label="Percentage of religious group in given LA", tooltips=tool)

# Scatter plot
p8.scatter("selected_religion", "selected_percentages", source=source, fill_alpha=0.5, size=10)

# Prepare data
rel_2['selected_religion'] = rel_2['Christian_Percentage']  # Default religion
rel_2['selected_percentages'] = rel_2['Christian_NR']

source_new = ColumnDataSource(rel_2)

# Create figure for the new dataset
p9 = figure(title="Relationship between % of religious group in given LA, and their non-response rate",
            y_axis_label="Non-response Rate", x_axis_label="Percentage of religious group in given LA", tooltips=tool)

# Scatter plot for the new dataset
p9.scatter("selected_religion", "selected_percentages", source=source_new, fill_alpha=0.5, size=10)

def update_highlighted_rows(selected_religion):
    formatter = create_formatter(selected_religion)
    for col in columns1:
        col.formatter = formatter
    for col in columns2:
        col.formatter = formatter
    data_table1.columns = columns1
    data_table2.columns = columns2
    layout_1.children[1].columns = columns1
    layout_2.children[1].columns = columns2

def update_highlighted_rows_2(selected_religion):
    formatter = create_formatter(selected_religion)
    for col in columns3:
        col.formatter = formatter
    for col in columns4:
        col.formatter = formatter
    data_table3.columns = columns3
    data_table4.columns = columns4
    layout_3.children[1].columns = columns3
    layout_4.children[1].columns = columns4


# Define callback for updating data source

def update_plot(attr, old, new):
    selected_religion = select_religion.value
    rel['selected_religion'] = rel[f'{selected_religion}_Percentage']
    rel['selected_percentages'] = rel[f'{selected_religion}_NR']
    source.data = source.from_df(rel)
    update_highlighted_rows(selected_religion)

def update_plot_2(attr, old, new):
    selected_religion = select_religion_2.value
    rel_2['selected_religion'] = rel_2[f'{selected_religion}_Percentage']
    rel_2['selected_percentages'] = rel_2[f'{selected_religion}_NR']
    source_new.data = source_new.from_df(rel_2)
    update_highlighted_rows_2(selected_religion)    
    
    
# Create select widget
options = ['Christian', 'No religion', 'Muslim', 'Jewish', 'Buddhist', 'Hindu', 'Sikh', 'Other religion']
select_religion = Select(title="Religious Group:", value='Christian', options=options)
select_religion.on_change('value', update_plot)

select_religion_2 = Select(title="Religious Group:", value='Christian', options=options)
select_religion_2.on_change('value', update_plot_2)

# Initial update of the highlighted rows
update_highlighted_rows(select_religion.value)
update_highlighted_rows_2(select_religion_2.value)

# Add sex dataset in

so_tot = pd.read_csv('sex_tot_SO.csv')
so_nr = pd.read_csv('sex_nr_SO.csv')
gi_tot = pd.read_csv('sex_tot_GI.csv')
gi_nr = pd.read_csv('sex_nr_GI.csv')


bold_formatter = HTMLTemplateFormatter(template="""
    <div style="color: red; font-weight: bold;"><%= value %></div>
""")


sourc1 = ColumnDataSource(so_tot)

columnz1 = [
    TableColumn(field="Sex (2 categories)", title="Sex"),
    TableColumn(field="Total_Observations", title="Total Observations")]

ly1, table1 = create_datatable2(sourc1, columnz1)

sourc2 = ColumnDataSource(so_nr)

columnz2 = [
    TableColumn(field="Sex (2 categories)", title="Sex"),
    TableColumn(field="NR_Total", title="NR Total"),
    TableColumn(field="NR_rate", title="Non-response rate", formatter = bold_formatter)]

ly2, table2 = create_datatable2(sourc2, columnz2)

sourc3 = ColumnDataSource(gi_tot)

columnz3 = [
    TableColumn(field="Sex (2 categories)", title="Sex"),
    TableColumn(field="Total_Observations", title="Total Observations")]

ly3, table3 = create_datatable2(sourc3, columnz3)



sourc4 = ColumnDataSource(gi_nr)

columnz4 = [
    TableColumn(field="Sex (2 categories)", title="Sex"),
    TableColumn(field="NR_Total", title="NR Total"),
    TableColumn(field="NR_rate", title="Non-response rate", formatter = bold_formatter)]

ly4, table4 = create_datatable2(sourc4, columnz4)

heading_sex = Div(text="<h1>Sex: sexual orientation</h1>", width=400)
heading_gen = Div(text="<h1>Sex: gender identity</h1>", width=400)

sex_description = Div(text="""<h3>Sex</h3>
<p>Because we're only dealing with two variables i.e. sex and non-response rate, this does not make for a particularly interesting visualisation. Therefore, I've only included a table here which displays:</p>
<li><b>Total:</b> Total number of male and females sampled.</li>
<li><b>Total non-response:</b> Total number of male and females that didn't respond to either question.</li>
<li><b>Non response rate:</b> The non-response as a percentage for each sex.</li>
""",
width=500, height=200, css_classes=["shannon-description"])

footer = Div(text="""
<hr style='border-top: 1px solid;'>
<h2>Created by Louise Capener</h2>
<p>Organisation: UK Data Service</p>
""", width=800, height=100)

# Layout

col1 = column(select_religion, p8, layout_1, layout_2, heading_sex, ly1, Spacer(height = 1),ly2)
col2 = column(select_religion_2, p9, layout_3, layout_4, heading_gen, ly3,Spacer(height = 1), ly4)
final_layout = row(col1, col2)
final_layout_with_description = row(final_layout, default_description_2)
final_layout.margin = (30, 30, 30, 30)


r = column(layout, final_layout_with_description, footer)
r.margin = (30, 30, 30, 30)  # Add margin to the final layout
curdoc().add_root(r)



