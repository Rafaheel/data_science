import pandas as pd 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

df = pd.read_csv('sales_data_sample.csv',encoding = 'latin-1')

df['Data_Pedido'] = pd.to_datetime(df['ORDERDATE'])
df['Ano'] = df['Data_Pedido'].dt.year
df['Mes'] = df['Data_Pedido'].dt.month_name()

drop_cols  = ['ADDRESSLINE1', 'ADDRESSLINE2', 'POSTALCODE', 'CITY', 'TERRITORY', 'PHONE', 'STATE', 'CONTACTFIRSTNAME', 'CONTACTLASTNAME', 'CUSTOMERNAME', 'ORDERNUMBER']
df = df.drop(drop_cols, axis = 1)


sales_by_country_series = df.groupby('COUNTRY').sum()['SALES']

app = dash.Dash()

app.title = 'Dashboard Part 1'

app.layout = html.Div(
    html.Div([
        html.H1(children='Primeira Vizualização'),

        html.Div(children='''
            Dashboard de Vendas - Minerando Dados
        '''),

        dcc.Graph(
            id='vendas-por-pais',
            figure={
                'data': [
                    {'x': sales_by_country_series.index, 'y':sales_by_country_series.values , 'type': 'bar', 'name': 'VbyC'}
                ],
                'layout': {
                    'title': 'Vendas Por País [$]'
                }
            }
        ),

    ])
)

if __name__ == '__main__':
    app.run_server(debug=True)
