#%%
# INTRODUÇÃO AO DASH

import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# https://www.kaggle.com/kyanyoga/sample-sales-data
df = pd.read_csv('sales_data_sample.csv',encoding = 'latin-1')
df.head()
# %%
usa_df = df[df['COUNTRY'] == 'USA']


df.columns
# %%
usa_df['Data_Pedido'] = pd.to_datetime(usa_df['ORDERDATE'])
usa_df['Ano'] = usa_df['Data_Pedido'].dt.year
usa_df['Meses'] = usa_df['Data_Pedido'].dt.month_name()

# %%
usa_df.isnull().sum()

# %%
drop_cols  = ['ADDRESSLINE1', 'ADDRESSLINE2', 'POSTALCODE', 'TERRITORY', 'PHONE', 'CONTACTFIRSTNAME', 'CONTACTLASTNAME', 'CUSTOMERNAME', 'ORDERNUMBER']
usa_df = usa_df.drop(drop_cols, axis = 1)
# usa_df = usa_df.groupby('STATE').count()
# usa_df.head()
# %%
usa_df.isnull().sum()

usa_df = usa_df.groupby(['STATE','Ano','STATUS'])[['SALES']].mean()
usa_df.reset_index(inplace=True)    

# %%

app = dash.Dash(__name__)

app.layout = html.Div([

    html.H1(id = 'output_title', children = [], style={'text-align': 'center'}  ),

    dcc.Dropdown(id="ano_selecionado",
                 options=[
                     {"label": "2003", "value": 2003},
                     {"label": "2004", "value": 2004},
                     {"label": "2005", "value": 2005}],
                 multi=False,
                 value=2003,
                 style={'width': "40%"}
                 ),              
                 
    html.Br(),
    html.Div(id='output_container', children=[]),       
    html.Br(),

    dcc.Graph(id='mapa_de_vendas', figure={})

])
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='output_title', component_property='children'),
    Output(component_id='mapa_de_vendas', component_property='figure')],
    [Input(component_id='ano_selecionado', component_property='value')]
)
def update_graph(ano_selecionado):

    container = "O ano selecionado foi: {}".format(ano_selecionado)

    title = "Mapa de Vendas nos EUA no ano : {}".format(ano_selecionado)

    df_ = usa_df.copy()
    df_ = df_[df_["Ano"] == ano_selecionado]
    df_ = df_[df_["STATUS"] == "Shipped"]

    # # Plotly Express
    fig = px.choropleth(
        data_frame=df_,
        locationmode= 'USA-states',
        locations= 'STATE',
        scope="usa",
        color='SALES',
        hover_data = ['STATE', 'SALES'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        template='plotly_dark'
        

    )

    return container, title, fig  

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=df_['STATE'],
    #         z=df_["SALES"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    
    # fig.update_layout(
    #     title_text="VENDAS - USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    # return container, fig
if __name__ == '__main__':
    app.run_server(debug=True)


# %%
