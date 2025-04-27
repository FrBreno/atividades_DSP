import logging
import yaml
import sys

logger = logging.getLogger(__name__)

# 1. Ler as configurações do arquivo YAML
def ler_config_yaml(config_path: str='config.yaml') -> object:
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file) or {}
    except FileNotFoundError:
        print(f'O arquivo de configuração {config_path} não foi encontrado.')
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f'Erro ao fazer o parsing do arquivo YAML: {e}')
        sys.exit(1)
    except Exception as e:
        print(f'Error ao ler o arquivo de configuração {config_path}: {e}')
        sys.exit(1)
    return config

# 2. Configurar sistema de logging
def configurar_logging() -> None:
    loggign_config = ler_config_yaml().get('logging', {})
    
    if not loggign_config:
        print('Nenhuma configuração de logging encontrada. Utilizando configuração padrão.')
        return
    
    log_level = getattr(logging, loggign_config.get('level', 'INFO').upper(), logging.INFO)
    log_format = loggign_config.get('format', '%(asctime)s - %(levelname)s - %(message)s')
    output_file = loggign_config.get('file', None)

    # Determinando o destino dos logs de acordo com o valor de `output_file`
    handlers = []
    if output_file:
        handlers.append(logging.FileHandler(output_file))
    else:
        handlers.append(logging.StreamHandler())

    # Configuração do logging
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=handlers
    )

# 3. Ler e processar os dados JSON
def ler_e_processar_JSON() -> None:
    logger.info('Iniciando leitura dos dados em JSON...')
    # TODO: Implementar leitura e processamento dos dados.
    return

if __name__ == "__main__":
    configurar_logging()
    ler_e_processar_JSON()