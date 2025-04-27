import os
import xml.etree.ElementTree as ET
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from http import HTTPStatus

# Setup.
app = FastAPI()
XML_FILE = 'livros.xml'

# Model Livro.
class Livro(BaseModel):
    id: int
    titulo: str
    autor: str
    ano: int
    genero: str

# Métodos para manipulação do .xml.
# Ler dados do XML.
def ler_dados_xml() -> List[Livro]:
    livros = []
    if os.path.exists(XML_FILE) and os.stat(XML_FILE).st_size > 0:
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        for data in root.findall('livro'):
            livro = Livro(
                id=int(data.find('id').text),
                titulo=data.find('titulo').text,
                autor=data.find('autor').text,
                ano=int(data.find('ano').text),
                genero=data.find('genero').text
            )
            livros.append(livro)
    return livros

# Escrever dados no XML.
def escrever_dados_xml(livros: List[Livro]) -> None:
    root = ET.Element('livros')
    for livro in livros:
        livro_elem = ET.SubElement(root, 'livro')
        ET.SubElement(livro_elem, 'id').text = str(livro.id)
        ET.SubElement(livro_elem, 'titulo').text = livro.titulo
        ET.SubElement(livro_elem, 'autor').text = livro.autor
        ET.SubElement(livro_elem, 'ano').text = str(livro.ano)
        ET.SubElement(livro_elem, 'genero').text = livro.genero
    tree = ET.ElementTree(root)
    tree.write(XML_FILE)

# Rotas.
# Obter livros.
@app.get('/livros', response_model=List[Livro], status_code=HTTPStatus.OK)
def ler_livros():
    return ler_dados_xml()

# Obter livro por ID.
@app.get('/livros/{id}', response_model=Livro, status_code=HTTPStatus.OK)
def ler_livro(id: int):
    livros = ler_dados_xml()
    for livro in livros:
        if livro.id == id:
            return livro
    raise HTTPException(HTTPStatus.NOT_FOUND, detail=f'O Livro com ID {id} não existe!')

# Criar livro.
@app.post('/livros', response_model=Livro, status_code=HTTPStatus.CREATED)
def criar_livro(livro: Livro):
    livros = ler_dados_xml()
    if any (l.id == livro.id for l in livros):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='O ID do livro já existe!')
    livros.append(livro)
    escrever_dados_xml(livros)
    return livro

# Atualizar livro.

# Excluir livro.
    