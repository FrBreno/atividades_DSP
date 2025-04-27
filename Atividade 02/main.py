from web_scraping.web_scraping import realizar_scraping
from ocr_extraction.ocr_extraction import extrair_texto_imagem
from complete_extraction.complete_extraction import extracao_completa
def voltar() -> None:
    input('\nDigite "v" para voltar ao menu principal: ')
    print('\033[H\033[J', end='')

def main() -> None:
    print(f'Menu - Atividade 02')
    print('Escolha uma das opções abaixo:')
    print(f'1. Scraping de Websites com BeautifulSoup (questão 01)')
    print(f'2. Extração de Texto de Imagens com OCR (questão 02)')
    print(f'3. Extração Completa de Dados (questão 03)')
    print(f'4. Sair')
    while True:
        opcao = input('Digite o número da opção desejada: ')
        print('\033[H\033[J', end='')
        if opcao == '1':
            print('A url do site deve ser pública e acessível.')
            print('Caso contrário, o scraping não funcionará.')
            url = input('Digite a URL do site: ')
            realizar_scraping(url)
            voltar()
        elif opcao == '2':
            print('Antes, faça o upload do arquivo na pasta "data" presente no diretório "./ocr_extraction".')
            imagem_path = input('Digite o nome da imagem (ex: image.png): ')
            extrair_texto_imagem(f'./ocr_extraction/data/{imagem_path}')
            voltar()
            print('\033[H\033[J', end='')
        elif opcao == '3':
            extracao_completa()
            voltar()
        elif opcao == '4':
            break
        else:
            print('Opção inválida. Tente novamente.')
    return

main()