from cgitb import text
import requests
from bs4 import BeautifulSoup

url_base = 'https://lista.mercadolivre.com.br/'

produto_nome = 'mi band 5'

response = requests.get(url_base + produto_nome)

print(url_base + produto_nome)

site = BeautifulSoup(response.text, 'html.parser')

produtos = site.findAll('div', attrs={'class': 'andes-card andes-card--flat andes-card--default ui-search-result ui-search-result--core andes-card--padding-default'})

contagem = 0

for produto in produtos:
    contagem += 1

    titulo  = produto.find('h2', attrs={'class': 'ui-search-item__title'})

    link = produto.find('a', attrs={'class': 'ui-search-link'})

    real = produto.find('span', attrs={'class': 'price-tag-fraction'})
    centavos = produto.find('span', attrs={'class': 'price-tag-cents'})
    separador = produto.find('span', attrs={'class': 'price-tag-decimal-separator'})

    
    print(f'O titulo do produto é: {titulo.text}')
    print('O link do produto é: ', link['href'])
    if (centavos):
        print('O preço do produto é: R$', real.text + ',' + centavos.text)
    else:
        print('O preço do produto é: R$', real.text)

    print('\n'* 2)
    print(contagem)



