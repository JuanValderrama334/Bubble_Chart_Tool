#------------ Importing the libraries ------------#

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

import dash
import dash_bootstrap_components as dbc
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#------------ Reading and loading the dummy dataset ------------#

data = pd.read_excel('CCEP-BubbleChart-Test.xlsx')
data.sort_values(by = ['Total PE ', 'To competition', 'SALES'], ignore_index=True, inplace=True)
#data.head()

#------------ Making a preliminary bubble plot ------------#

plt.figure(figsize=(10, 10))
sns.scatterplot(data = data, x = data['Total PE '], y = data['To competition'], size = data['SALES'], hue = data['Brand'] ,alpha = 0.5, legend = True, sizes=(20, 800))
plt.xlabel('Total RPE')
plt.ylabel('% Share RPE To Competition')
#plt.show()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#------------ Dash App ------------#

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP], meta_tags=[{'content': 'width=device-width'}])

#------------ Layout section: Boostrap ------------#

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H2('Bubble Chart Tool - Preliminary Version', className='text-center'), width={'size': 6, 'offset': 5})),

    dbc.Row([
        
        dbc.Col(dcc.Dropdown(
            data['Brand'].unique(),
            id='brand-dropdown', multi=True, value = data['Brand'].unique(), placeholder = 'Select the brands you want to see',
            optionHeight = 35, searchable = True, style = {'width': '80%'}), width = 7, lg= {'size': 5, 'offset': 0, 'order': 'first'}),

            dbc.Col(dcc.Dropdown(
            data['Manufacturer'].unique(),
            id='manufacturer-dropdown', multi=True, value = data['Manufacturer'].unique(), placeholder = 'Select the brands you want to see',
            optionHeight = 35, searchable = True, style = {'width': '80%'}), width = 7, lg= {'size': 5, 'offset': 0, 'order': 'last'})

    ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id = 'bubble_chart', figure = {}), width = 8, lg = {'size': 6, 'offset': 0, 'order': 'first'})
    ])

])
 
@app.callback(
    Output(component_id = 'bubble_chart', component_property = 'figure'),
    [Input(component_id = 'brand-dropdown', component_property = 'value'),
    Input(component_id = 'manufacturer-dropdown', component_property = 'value')],
    prevent_initial_call = False
)

def update_my_graph(brand_value, manufacturer_value):
    if len(brand_value) > 0 | len(manufacturer_value) > 0:
        print(f"Brand: {brand_value}")
        print(f"Manufacturer: {brand_value}")
        dff_1 = data[data["Brand"].isin(brand_value)]
        dff_2 = dff_1[dff_1["Manufacturer"].isin(manufacturer_value)]
        fig = px.scatter(dff_2, x = 'Total PE ', y = 'To competition', size = 'SALES', color = 'Brand', hover_name = 'PPG name' , size_max = 40, labels = 'Brand',
                         width = 1300, height = 800)
        return fig
    elif len(brand_value) == 0 | len(manufacturer_value) == 0:
        raise dash.exceptions.PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)