import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime


# https://stooq.com/
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 12, 3)

df = web.DataReader(['AMZN','GOOGL','FB','PFE','MRNA','BNTX'],
                    'stooq', start=start, end=end)

# df=df.melt(ignore_index=False, value_name="price").reset_index()

df = df.stack().reset_index()
# print(df[:15])

app = dash.Dash( __name__ , external_stylesheets=[dbc.themes.SOLAR],
                        # para gerar responsividade - mobile
                        meta_tags=[{'name': 'viewport', 
                                    'content': 'width=device-width, initial-scale=1.0'}]  )
                
                   
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Stock Market Dashboard", 
                        className = 'text-center text-primary, mb-4'), 
                        width = 12  )

    ]),

    dbc.Row([


    ]),

    dbc.Row([


    ])

])

if __name__ == '__main__':
    app.run_server(debug = True,port = 3000)