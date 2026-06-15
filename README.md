# 🧠 Meu Segundo Cérebro

Um assistente pessoal de IA que roda 100% no seu computador, gratuito e privado, usando Ollama.


## Como instalar


### 1. Instale o Ollama

Baixe em: https://ollama.com/download

Instale normalmente (próximo, próximo, instalar).


### 2. Baixe o modelo de IA

Abra o terminal (Prompt de Comando no Windows) e digite:

ollama pull llama3.2

Aguarde o download (cerca de 2GB).


### 3. Instale o Python

Verifique se já tem com:

python --version

Se não tiver, baixe em: https://www.python.org/downloads/

⚠️ No Windows, marque "Add Python to PATH" durante a instalação.


### 4. Baixe este projeto

Clique no botão verde \*\*"Code"\*\* no GitHub > \*\*"Download ZIP"\*\*, ou se souber usar git:

git clone <link-do-repositorio>

Extraia a pasta em algum lugar do seu computador.


### 5. Instale as dependências

Abra o terminal \*\*dentro da pasta do projeto\*\* e digite:

pip install streamlit ollama


### 6. Rode o assistente

streamlit run assistente.py

Vai abrir automaticamente no navegador em `http://localhost:8501`

## Como usar

- Converse normalmente com o assistente

- Para ele lembrar de algo permanentemente, digite: `lembra que \[o que você quer que ele lembre]`

- Use a barra lateral para ver o que ele já sabe sobre você, ou limpar a memória/conversa


## Problemas comuns



**Erro de certificado no pip (Windows)**: digite `set CURL\_CA\_BUNDLE=` antes do `pip install`.

