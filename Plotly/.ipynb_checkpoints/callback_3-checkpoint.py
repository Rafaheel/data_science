#%%
import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
import datetime


# https://stooq.com/
start = datetime.datetime(2019, 1, 1)
end = datetime.datetime(2021, 1, 25)

df = web.DataReader(['SVAC','JNJ','PFE','MRNA','BNTX'],
                    'stooq', start=start, end=end)

df = df.stack().reset_index()
#%%
print(df.head())

cores = ["black", "red", "blue", "orange"]

app = dash.Dash(__name__)

app.layout = html.Div(

    children = [

        html.H1(id = 'output-titulo', children='Valor de Ação - Covid-19',  style={} ),

        # dash component 1
        dcc.Dropdown( id = 'meu-dropdown', multi = True,
                    options = [{ 'label': x , 'value': x   } for x in sorted(df.Symbols.unique())  ],
                    value = [  'AMZN','GOOGL','FB','PFE','MRNA','BNTX']
                    ,style={'text-align': 'center'}  
                    ),

        html.Br(),

        # # dash component 2
        html.Button( id = 'botao', n_clicks = 0, children = 'Filtrar_acoes',  style={'text-align': 'center'} ),

        # dash component 3
        dcc.Graph(id = 'grafico-output', figure ={}),
        
        # dash component 4
        # html.Div(id = 'sentence-output', children = ['Uma String qualquer'], style={}),
        
        dcc.RadioItems(id = 'meu-radioitem', value = 'black', options = [{ 'label': c, 'value': c   } for c in cores]),
        
        dcc.RangeSlider(
            min=0,
            max=100,
            value=[10, 65],
            marks={
                0: {'label': '0°C', 'style': {'color': '#77b0b1'}},
                26: {'label': '26°C'},
                37: {'label': '37°C'},
                100: {'label': '100°C', 'style': {'color': '#f50'}}
            },
            included=False
        )  
        
        ]

)

@app.callback(
    [Output('grafico-output', 'figure'), Output('output-titulo', 'style')],
    [Input(component_id='meu-radioitem', component_property='value'),
    Input(component_id='meu-dropdown', component_property='value')],
    prevent_initial_call=False
)

def muda_grafico(n, acao_escolhida):

    if len(acao_escolhida) > 0:

        print(f"Ação escolhida pelo usuário: {acao_escolhida}")
        print(type(acao_escolhida))
        
        df_copy = df[df["Symbols"].isin(acao_escolhida)]
        fig = px.line(df_copy, x='Date', y='Close', color = 'Symbols')

        # return fig

    elif len(acao_escolhida) == 0:
        raise dash.exceptions.PreventUpdate # Faz com que o component_property do Output não realize update


# @app.callback(
#     [Output('grafico-output', 'figure'), Output('output-titulo', 'style')],
#     [Input(component_id='meu-radioitem', component_property='value'),
#     Input(component_id='meu-dropdown', component_property='value')],
#     prevent_initial_call=False
# )
# def muda_grafico(cor_escolhida, acao_escolhida):

#     if len(acao_escolhida) == 0:
#         return dash.no_update, {"color": cor_escolhida} # faz update em somente um componente quando a página é atualizada - nesse caso a cor e nao o grafico
#     else:
#         df_copy = df[df["Symbols"].isin(acao_escolhida)]
#         fig = px.line(df_copy, x='Date', y='Close', color = 'Symbols')


    return fig, {"color": cor_escolhida, 'text-align': 'center' }


if __name__ == '__main__':
    app.run_server(debug=True)