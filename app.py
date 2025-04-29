import streamlit as st
import json
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Conectar com Google Sheets via secrets
def conectar_planilha():
    escopo = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credenciais_dict = st.secrets["gcp_service_account"]
    credenciais_json = json.loads(json.dumps(credenciais_dict))
    credenciais = ServiceAccountCredentials.from_json_keyfile_dict(credenciais_json, escopo)
    cliente = gspread.authorize(credenciais)
    planilha = cliente.open_by_key("1Lotjwh6m-6xTUgRew7pEEzOqNHzrY2R1744Eqix_vmk")  # ID da sua planilha
    return planilha.sheet1

# LER TODOS OS USUÁRIOS
def obter_usuarios():
    aba = conectar_planilha()
    dados = aba.get_all_records()
    return dados

# INSERIR NOVO USUÁRIO
def cadastrar_usuario(usuario, senha, email):
    aba = conectar_planilha()
    aba.append_row([usuario, senha, email])

# INTERFACE STREAMLIT
st.set_page_config(page_title="Sistema de Acesso", layout="centered")
st.title("🔐 Sistema de Acesso")

menu = st.sidebar.radio("Menu", ["Login", "Cadastro", "Recuperar Senha"])

if menu == "Login":
    st.subheader("Fazer Login")
    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        usuarios = obter_usuarios()
        encontrado = False
        for linha in usuarios:
            if linha['usuario'] == user and linha['senha'] == senha:
                st.success(f"Bem-vindo, {user}!")
                st.markdown("[👉 Acessar Dashboard Power BI](https://app.powerbi.com/YOUR-LINK-AQUI)", unsafe_allow_html=True)
                encontrado = True
                break
        if not encontrado:
            st.error("Usuário ou senha incorretos.")

elif menu == "Cadastro":
    st.subheader("Cadastrar novo usuário")
    novo_user = st.text_input("Novo usuário")
    nova_senha = st.text_input("Nova senha", type="password")
    novo_email = st.text_input("E-mail")

    if st.button("Cadastrar"):
        usuarios = obter_usuarios()
        ja_existe = any(u['usuario'] == novo_user for u in usuarios)
        if ja_existe:
            st.warning("⚠️ Esse usuário já está cadastrado.")
        else:
            cadastrar_usuario(novo_user, nova_senha, novo_email)
            st.success("✅ Cadastro realizado com sucesso!")

elif menu == "Recuperar Senha":
    st.subheader("Recuperar senha por e-mail")
    email_digitado = st.text_input("Digite seu e-mail cadastrado")

    if st.button("Recuperar"):
        usuarios = obter_usuarios()
        encontrado = False
        for u in usuarios:
            if u['email'] == email_digitado:
                st.info(f"Usuário: **{u['usuario']}**\n\nSenha: **{u['senha']}**")
                encontrado = True
                break
        if not encontrado:
            st.error("❌ E-mail não encontrado.")
