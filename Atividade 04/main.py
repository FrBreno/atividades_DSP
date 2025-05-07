import logging
import yaml
import sys
import json
from typing import Dict, Any, List

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

def validar_registro(reg: Dict[str, Any]) -> bool:
    """
    Valida presença e tipo de 'id', 'name' e 'age'.
    Retorna True se válido, False caso contrário e já emite logs.
    """
    valido = True
    reg_id = reg.get('id', 'N/A')
    id_info = f"[ID: {reg_id}] - Registro nao processado! -"

    logger.info(f"Processando registro de ID {reg_id}...")

    if 'id' not in reg:
        logger.warning(f"{id_info} Campo 'id' ausente.")
        valido = False
    elif not isinstance(reg['id'], int):
        logger.warning(f"{id_info} 'id' deve ser inteiro. Encontrado: {reg['id']!r}.")
        valido = False

    if 'name' not in reg:
        logger.warning(f"{id_info} Campo 'name' ausente.")
        valido = False
    elif not isinstance(reg['name'], str) or not reg['name'].strip():
        logger.warning(f"{id_info} 'name' deve ser string nao-vazia. Encontrado: {reg['name']!r}.")
        valido = False

    if 'age' not in reg:
        logger.warning(f"{id_info} Campo 'age' ausente.")
        valido = False
    else:
        age = reg['age']
        if not isinstance(age, int):
            logger.warning(f"{id_info} 'age' deve ser inteiro, encontrado: {age!r}.")
            valido = False
        else:
            if age < 0 or age > 120:
                logger.warning(f"{id_info} 'age' fora do intervalo aceitavel (0-120). encontrado: {age}.")
                valido = False
    if valido:
        logger.info(f"Registro de ID {reg_id} processado com sucesso!")

    return valido

# 3. Ler e processar os dados JSON
def ler_e_processar_JSON() -> None:
    logger.info('Iniciando leitura dos dados em JSON...')
    try:
        with open('data.json', 'r') as file:
            dados = json.load(file)
            logger.info('Dados lidos com sucesso.')
    except FileNotFoundError:
        logger.error('Arquivo JSON nao encontrado.')
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f'Erro ao decodificar o arquivo JSON: {e}')
        sys.exit(1)
    except Exception as e:
        logger.error(f'Erro ao ler o arquivo JSON: {e}')
        sys.exit(1)

    if not isinstance(dados, list):
        logger.error('Dados JSON invalidos. Esperado uma lista de objetos.')
        sys.exit(1)
    if not dados:
        logger.error('Dados JSON vazios.')
        sys.exit(1)

    registros_validos: List[Dict[str, Any]] = []
    for idx, registro in enumerate(dados):
        if validar_registro(registro):
            registros_validos.append(registro)

    logger.info(f"{len(registros_validos)} de {len(dados)} registros sao validos e foram processados com sucesso.")

    return registros_validos

if __name__ == "__main__":
    configurar_logging()
    ler_e_processar_JSON()
