import streamlit as st
import ollama
import json
import os
from datetime import datetime

# --- Configurações ---
MODELO = "llama3.2"
ARQUIVO_MEMORIA = "memoria/memoria.json"
ARQUIVO_HISTORICO = "memoria/historico.json"

# --- Funções de memória ---
def carregar_memoria():
    if os.path.exists(ARQUIVO_MEMORIA):
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_memoria(memorias):
    os.makedirs("memoria", exist_ok=True)
    with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(memorias, f, ensure_ascii=False, indent=2)

def carregar_historico():
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_historico(historico):
    os.makedirs("memoria", exist_ok=True)
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

# --- Configuração da página ---
st.set_page_config(page_title="Meu Segundo Cérebro", page_icon="🧠")
st.title("🧠 Meu Segundo Cérebro")
st.caption("Seu assistente pessoal rodando localmente com Ollama")

# --- Inicializar estado ---
if "memorias" not in st.session_state:
    st.session_state.memorias = carregar_memoria()

if "mensagens" not in st.session_state:
    st.session_state.mensagens = carregar_historico()

# --- Barra lateral: memórias salvas ---
with st.sidebar:
    st.header("📌 Coisas que eu lembro")
    if st.session_state.memorias:
        for i, mem in enumerate(st.session_state.memorias):
            st.write(f"- {mem}")
    else:
        st.write("Nada salvo ainda.")

    if st.button("🗑️ Limpar memórias"):
        st.session_state.memorias = []
        salvar_memoria([])
        st.rerun()

    st.divider()
    if st.button("🧹 Limpar conversa"):
        st.session_state.mensagens = []
        salvar_historico([])
        st.rerun()

# --- Mostrar histórico de mensagens ---
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Campo de entrada ---
pergunta = st.chat_input("Digite sua mensagem... (use 'lembra que ...' para salvar algo)")

if pergunta:
    # Mostrar mensagem do usuário
    with st.chat_message("user"):
        st.markdown(pergunta)
    st.session_state.mensagens.append({"role": "user", "content": pergunta})

    # Verificar se é um comando de memória
    if pergunta.lower().startswith("lembra que"):
        conteudo = pergunta[10:].strip()
        st.session_state.memorias.append(conteudo)
        salvar_memoria(st.session_state.memorias)
        resposta = f"Anotado! Vou lembrar que: {conteudo}"
    else:
        # Montar contexto com memórias salvas
        contexto_memoria = ""
        if st.session_state.memorias:
            contexto_memoria = "Coisas importantes que você sabe sobre o usuário:\n"
            contexto_memoria += "\n".join(f"- {m}" for m in st.session_state.memorias)
            contexto_memoria += "\n\n"

        prompt_sistema = (
            "Você é um assistente pessoal amigável, paciente e direto. "
            "Ajude o usuário a organizar pensamentos, lembrar de coisas e "
            "executar tarefas de raciocínio. Seja claro e objetivo.\n\n"
            + contexto_memoria
        )

        mensagens_para_ia = [{"role": "system", "content": prompt_sistema}]
        mensagens_para_ia += st.session_state.mensagens[-10:]  # últimas 10 mensagens

        with st.spinner("Pensando..."):
            resposta_ia = ollama.chat(model=MODELO, messages=mensagens_para_ia)
            resposta = resposta_ia["message"]["content"]

    # Mostrar resposta
    with st.chat_message("assistant"):
        st.markdown(resposta)
    st.session_state.mensagens.append({"role": "assistant", "content": resposta})

    # Salvar histórico
    salvar_historico(st.session_state.mensagens)