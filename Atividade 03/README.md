# Lista 3 - CRUD de Livros com FastAPI e Persistência em XML

## Discentes
1. Francisco Breno da Silveira (511429)
2. João Victor Amarante Diniz (510466)

## Setup
1. Criar ambiente virtual, por exemplo:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate  # Windows
    ```  
2. Instalar as dependências:
    ```bash
    pip install fastapi uvicorn
    ```

## Execução
1. Rodar projeto:
    ```bash
    uvicorn main:app --reload
    ```
2. Acesse no navegador:
    - API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
    - Documentação Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)