import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np


def busca_cientista_dados_glassdoor():
    headers = {'user-agent': 'Mozilla/5.0'}

    resposta =  requests.get('https://www.glassdoor.com.br/Sal%C3%A1rios/cientista-de-dados-sal%C3%A1rio-SRCH_KO0,18.htm', headers=headers)

    resposta_raw = resposta.text

    resposta_html = BeautifulSoup(resposta_raw, 'html.parser')

    lista_empresas = resposta_html.find_all('h3', {'data-test': re.compile('salaries-list-item-.*-employer-name')})
    lista_salario = resposta_html.find_all('div', {'data-test': re.compile('salaries-list-item-.*-salary-info')})

    lista_todos = []

    for empresa, salario in zip(lista_empresas, lista_salario):
        nome_empresa = empresa.find('a').text

        valor_salario = salario.contents[0].text
        valor_salario = valor_salario.replace('R$', '').replace('\xa0', '').replace('.','')

        lista_todos.append((nome_empresa, valor_salario))

    df_lista_salarios_cientista_dados = pd.DataFrame(lista_todos, columns=['Empresa', 'Remuneracao'])  
    df_lista_salarios_cientista_dados['Remuneracao'] = df_lista_salarios_cientista_dados['Remuneracao'].astype(np.float32)  
    df_lista_salarios_cientista_dados['Cargos'] = 'Cientista De Dados' 
    return df_lista_salarios_cientista_dados

print(busca_cientista_dados_glassdoor())

def busca_analista_dados_glassdoor():

    headers = {'user-agent': 'Mozilla/5.0'}

    resposta =  requests.get('https://www.glassdoor.com.br/Sal%C3%A1rios/analista-de-dados-sal%C3%A1rio-SRCH_KO0,17.htm', headers=headers)

    resposta_raw = resposta.text

    resposta_html = BeautifulSoup(resposta_raw, 'html.parser')

    lista_empresas = resposta_html.find_all('h3', {'data-test': re.compile('salaries-list-item-.*-employer-name')})
    lista_salario = resposta_html.find_all('div', {'data-test': re.compile('salaries-list-item-.*-salary-info')})

    lista_todos = []

    for empresa, salario in zip(lista_empresas, lista_salario):
        nome_empresa = empresa.find('a').text

        valor_salario = salario.contents[0].text
        valor_salario = valor_salario.replace('R$', '').replace('\xa0', '').replace('.','')

        lista_todos.append((nome_empresa, valor_salario))

    df_lista_salarios_analista_dados = pd.DataFrame(lista_todos, columns=['Empresa', 'Remuneracao'])  
    df_lista_salarios_analista_dados['Remuneracao'] = df_lista_salarios_analista_dados['Remuneracao'].astype(np.float32)  
    df_lista_salarios_analista_dados['Cargos'] = 'Analista De Dados' 
    return df_lista_salarios_analista_dados

print(busca_analista_dados_glassdoor())