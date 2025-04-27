# 1. Scraping de Websites com BeautifulSoup
# Objetivo: Praticar a extração de dados de um site usando scraping.
# Tarefa: Usando a biblioteca BeautifulSoup, escreva um código que extraia e imprima o título e 
# todos os links de uma página web. A URL pode ser qualquer página pública, como https://example.com.

from bs4 import BeautifulSoup
import requests

def realizar_scraping(url: str) -> None:
    # Fazer requisição
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Erro ao acessar a URL: {e}')
        return
    # Criar documento com BeautifulSoup
    doc = BeautifulSoup(response.content, 'html.parser')
    # Extrair título
    title = doc.title.string if doc.title else ""
    # Extrair links
    links = doc.select('a[href]')
    # Imprimir informações extraidas
    print(f'\nInformações extraídas de {url}:\n')
    print(f'Título extraído: {title}\n')
    print('Links extraídos:')
    for link in links:
        print(link.get('href', ''))