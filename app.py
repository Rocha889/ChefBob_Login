import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ----------------------------
# Conexão com o Google Sheets
# ----------------------------
def conectar_planilha(nome_aba):
    escopos = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credenciais_dict = st.secrets["gcp_service_account"]
    credenciais = ServiceAccountCredentials.from_json_keyfile_dict(credenciais_dict, escopos)
    cliente = gspread.authorize(credenciais)
    planilha = cliente.open("NOME_DA_SUA_PLANILHA")  # Substitua pelo nome real
    return planilha.worksheet(nome_aba)

# ----------------------------
# Obter usuários da aba
# ----------------------------
def obter_usuarios():
    aba = conectar_planilha("usuarios")
    return aba.get_all_records()

# ----------------------------
# Verificar login
# ----------------------------
def autenticar(usuario, senha):
    usuarios = obter_usuarios()
    for u in usuarios:
        if u["usuario"] == usuario and u["senha"] == senha:
            return True
    return False

# ----------------------------
# Verificar se usuário já existe
# ----------------------------
def usuario_existe(novo_usuario):
    usuarios = obter_usuarios()
    return any(u["usuario"] == novo_usuario for u in usuarios)

# ----------------------------
# Cadastrar novo usuário
# ----------------------------
def cadastrar_usuario(usuario, senha, email):
    aba = conectar_planilha("usuarios")
    aba.append_row([usuario, senha, email])

# ----------------------------
# Recuperar senha por e-mail
# ----------------------------
def recuperar_senha_por_email(email):
    usuarios = obter_usuarios()
    for u in usuarios:
        if u["email"] == email:
            return u["senha"]
    return None

# ----------------------------
# Interface do Streamlit
# ----------------------------
def main():
    st.set_page_config(page_title="ChefBob Login", page_icon="🍽️", layout="centered")

    st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>ChefBob Dashboards</h1>", unsafe_allow_html=True)

    menu = st.radio("Escolha uma opção:", ["Login", "Cadastrar novo usuário", "Recuperar senha"])

    if menu == "Login":
        st.subheader("Login de Usuário")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if autenticar(usuario, senha):
                st.success(f"Bem-vindo(a), {usuario}!")
                st.balloons()
                # Aqui você pode redirecionar para a página dos dashboards
            else:
                st.error("Usuário ou senha inválidos.")

    elif menu == "Cadastrar novo usuário":
        st.subheader("Cadastro")
        novo_usuario = st.text_input("Novo usuário")
        nova_senha = st.text_input("Nova senha", type="password")
        email = st.text_input("E-mail")

        if st.button("Cadastrar"):
            if usuario_existe(novo_usuario):
                st.warning("Esse usuário já existe. Tente outro nome.")
            else:
                cadastrar_usuario(novo_usuario, nova_senha, email)
                st.success("Usuário cadastrado com sucesso!")

    elif menu == "Recuperar senha":
        st.subheader("Recuperação de Senha")
        email = st.text_input("Digite seu e-mail cadastrado")

        if st.button("Recuperar"):
            senha = recuperar_senha_por_email(email)
            if senha:
                st.success(f"A sua senha é: {senha}")
            else:
                st.error("E-mail não encontrado.")

if __name__ == "__main__":
    main()
