# 3. Implementação Completa de um Extrator de Dados Estruturados e Não Estruturados
# Objetivo: Integrar conhecimentos e simular um fluxo completo de extração de dados.
# Tarefa: Escreva um código que possa extrair dados de um site (HTML), de um PDF e de 
# uma imagem. O código deve identificar o tipo de cada arquivo, extrair as informações relevantes e exibi-las em um formato organizado.

import requests
import pdfplumber
import pytesseract
from bs4 import BeautifulSoup
from PIL import Image

resultado_extracao = './complete_extraction/resultado.txt'

def ler_resultado_extracao() -> None:
    try:
        with open(resultado_extracao, 'r', encoding='utf-8') as file:
            conteudo = file.read()
            print(f'Conteúdo da extração:\n{conteudo}')
    except FileNotFoundError:
        print(f'Erro: Erro ao obter conteúdo da extração, o arquivo {resultado_extracao} não foi encontrado.')
    except IOError:
        print(f'Erro: Não foi possível ler o arquivo {resultado_extracao} com o resultado da extração .')
    except Exception as e:
        print(f'Erro inesperado: {e}')

def extrair_dados_html(html_path: str) -> None:
    # Fazer requisição
    try:
        response = requests.get(html_path)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Erro ao acessar a URL: {e}')
        return
    # Criar documento com BeautifulSoup
    doc = BeautifulSoup(response.content, 'html.parser')
    # Extrair informações
    title = doc.title.string if doc.title else ''
    links = doc.select('a[href]')
    headers = doc.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    paragrafos = doc.find_all('p')
    imagens = [{ 'alt': imagem.get('alt', ''), 'src': imagem.get('src') } for imagem in doc.find_all('img') if imagem.get('src')]
    # Salvar resultado em .txt
    try:
        with open(resultado_extracao, 'w', encoding='utf-8') as file:
            file.write(f'Informações extraídas de {html_path}:\n\n')
            file.write(f'Título extraído: {title}\n\n')
            file.write('========== Links extraídos ==========\n')
            for link in links:
                file.write(f"{link.get('href', '')}\n")
            file.write('\n========== Cabeçalhos extraídos ==========\n')
            for header in headers:
                file.write(f"{header.get_text(strip=True)}\n")
            file.write('\n========== Parágrafos extraídos ==========\n')
            for paragrafo in paragrafos:
                file.write(f"{paragrafo.get_text(strip=True)}\n\n")
            file.write('\n========== Imagens extraídas ==========\n')
            for imagem in imagens:
                file.write(f"Imagem: {imagem['alt']}, \nURL: {imagem['src']}\n\n")
    except FileNotFoundError:
        print(f'Erro: Erro ao salvar as informações da extração, o arquivo {resultado_extracao} não foi encontrado.')
        return
    except IOError:
        print(f'Não foi possível escrever no arquivo {resultado_extracao}.')
        return
    except Exception as e:
        print(f'Erro inesperado: {e}')
        return
    # Ler informações extraídas e imprimir
    ler_resultado_extracao()
    return

def extrair_dados_pdf(pdf_path: str) -> None:
    try:
        # Carregar PDF
        with pdfplumber.open(pdf_path) as pdf:
            texto = ''
            for pagina in pdf.pages:
                texto += f'=========== Página {pagina.page_number} =========== \n\n'
                texto += pagina.extract_text() + '\n\n'
                texto += f'====================== \n\n'
    except FileNotFoundError as e:
        print(f'Erro ao extrair dados do PDF, o arquivo {pdf_path} não foi encontrado.')
        return
    except IOError as e:
        print(f'Erro ao extrair dados do PDF, não foi possível abrir o arquivo {pdf_path}.')
        return
    except Exception as e:
        print(f'Erro inesperado: {e}')
        return
    try:
        # Salvar resultado em .txt
        with open(resultado_extracao, 'w', encoding='utf-8') as file:
            file.write(texto)
    except FileNotFoundError:
        print(f'Erro ao salvar a extração, o arquivo {resultado_extracao} não foi encontrado.')
        return
    except IOError:
        print(f'Erro ao salvar a extração, não foi possível escrever no arquivo {resultado_extracao}.')
        return
    except Exception as e:
        print(f'Erro inesperado: {e}')
        return
    # Ler informações extraídas e imprimir
    ler_resultado_extracao()
    return

def extrair_dados_imagem(imagem_path: str) -> None:
    try:
        # Carregar imagem
        imagem = Image.open(imagem_path)
        # Extrair texto da imagem
        texto = pytesseract.image_to_string(imagem)
    except FileNotFoundError as e:
        print(f'Erro: O arquivo {imagem_path} não foi encontrado.')
        return
    except IOError as e:
        print(f'Erro: Não foi possível abrir o arquivo {imagem_path}.')
        return
    except Exception as e:
        print(f'Erro inesperado: {e}')
        return
    try:
    # Salvar resultado em .txt
        with open(resultado_extracao, 'w', encoding='utf-8') as file:
            file.write(texto)
    except FileNotFoundError:
        print(f'Erro ao salvar a extração, o arquivo {resultado_extracao} não foi encontrado.')
        return
    except IOError:
        print(f'Erro ao salvar a extração, não foi possível escrever no arquivo {resultado_extracao}.')
        return
    except Exception as e:
        print(f'Erro inesperado: {e}')
        return
    # Ler informações extraídas e imprimir
    ler_resultado_extracao()
    return

def voltar() -> None:
    input('\nDigite "v" para voltar ao menu principal: ')
    print('\033[H\033[J', end='')

def extracao_completa() -> None:
    print('Extração Completa de Dados.')
    print('Instruções:')
    print('1. Para extrair dados de um site, forneça a URL.')
    print('2. Para extrair dados de um PDF, forneça o nome de um arquivo com a extensão .pdf.')
    print('3. Para extrair dados de uma imagem, forneça o nome de um arquivo com a extensão .png ou .jpg.')
    print('4. Para as opções 2 e 3, certifique-se de antes fazer o upload do arquivo na pasta "data" presente neste mesmo diretório.')
    print('5. Para sair, digite "sair".\n')
    while True:
        data = input('Digite a URL, o nome do arquivo PDF ou o nome do arquivo de imagem: ')
        print('\033[H\033[J', end='')
        if data.lower() == 'sair':
            print('\033[H\033[J', end='')
            break
        elif data.endswith('.pdf'):
            extrair_dados_pdf(f'./complete_extraction/data/{data}')
            voltar()
        elif data.endswith('.png') or data.endswith('.jpg'):
            extrair_dados_imagem(f'./complete_extraction/data/{data}')
            voltar()
        elif data.startswith('http://') or data.startswith('https://'):
            extrair_dados_html(data)
            voltar()
        else:
            print('Formato inválido. Por favor, forneça uma URL, o nome de um arquivo PDF ou de uma imagem.')
            print('Lembre-se de, no caso de arquivos PDF ou de imagem, fazer o upload no diretório "./complete_extraction/data".')
            print('Lembre-se também de que o arquivo deve ter a extensão .pdf, .png ou .jpg.')
            print('Links devem começar com http:// ou https://, e devem ser acessíveis publicamente.\n')