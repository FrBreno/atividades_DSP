# 2. Extração de Texto de Imagens com OCR
# Objetivo: Extrair texto de imagens usando OCR.
# Tarefa: Usando pytesseract e PIL, escreva um código para carregar uma imagem, extrair o 
# texto nela contido e salvar o resultado num arquivo txt.

import pytesseract
from PIL import Image

def extrair_texto_imagem(imagem_path: str) -> None:
    result_path = './ocr_extraction/resultado.txt'
    try:
        # Carregar imagem
        image = Image.open(imagem_path)
        # Extrair texto da imagem
        text = pytesseract.image_to_string(image)
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
        with open(result_path, 'w', encoding='utf-8') as file:
            file.write(text)
    except FileNotFoundError:
        print(f'Erro: O arquivo {result_path} não foi encontrado.')
        return
    except IOError:
        print(f'Erro: Não foi possível escrever no arquivo {result_path}.')
        return
    except Exception as e:
        print(f'Erro inesperado: {e}')
        return
    print(f'Texto extraído e salvo em {result_path}')