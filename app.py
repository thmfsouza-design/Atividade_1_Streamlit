from pathlib import Path

import pandas as pd
import streamlit as st


CSV_PATH = Path(__file__).with_name("pacientes.csv")
COLUNAS = [
    "Nome do paciente",
    "Idade",
    "Convênio",
    "Prioridade do atendimento",
    "Motivo da consulta / observações",
]


def carregar_cadastros():
    if CSV_PATH.exists():
        return pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    return pd.DataFrame(columns=COLUNAS)


st.set_page_config(page_title="Cadastro de pacientes", page_icon="🏥", layout="centered")
st.title("Cadastro de pacientes")
st.caption("Registre os dados do atendimento e baixe os cadastros em CSV.")

if "pacientes" not in st.session_state:
    st.session_state.pacientes = carregar_cadastros()

with st.form("formulario_paciente", clear_on_submit=True):
    nome = st.text_input("Nome do paciente")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1, value=0)
    convenio = st.selectbox(
        "Convênio",
        ["Particular", "Unimed", "Bradesco Saúde", "Amil", "SulAmérica", "Outro"],
    )
    prioridade = st.slider("Prioridade do atendimento (1 a 5)", 1, 5, 3)
    motivo = st.text_area("Motivo da consulta / observações")
    enviar = st.form_submit_button("Cadastrar", type="primary", use_container_width=True)

if enviar:
    nome = nome.strip()
    if not nome:
        st.error("Informe o nome do paciente.")
    else:
        novo_cadastro = pd.DataFrame(
            [[nome, int(idade), convenio, int(prioridade), motivo.strip()]],
            columns=COLUNAS,
        )
        st.session_state.pacientes = pd.concat(
            [st.session_state.pacientes, novo_cadastro], ignore_index=True
        )
        st.session_state.pacientes.to_csv(CSV_PATH, index=False, encoding="utf-8-sig")
        st.success("Cadastro realizado com sucesso.")

st.subheader("Últimos cadastros")
st.dataframe(
    st.session_state.pacientes.tail(10).iloc[::-1],
    use_container_width=True,
    hide_index=True,
)
st.download_button(
    label="Baixar CSV",
    data=st.session_state.pacientes.to_csv(index=False).encode("utf-8-sig"),
    file_name="pacientes.csv",
    mime="text/csv",
    use_container_width=True,
)