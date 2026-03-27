import streamlit as st
import PyPDF2

# Configuração da página
st.set_page_config(
    page_title="Triagem de Currículos",
    layout="wide",
    page_icon="📄"
)

# Função para ler PDF
def ler_pdf(file):
    reader = PyPDF2.PdfReader(file)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text() or ""
    return texto.lower()

st.title("📄 Sistema de Triagem de Currículos")
st.markdown("Escolhe um cargo e envia os currículos para análise")

st.markdown("---")

# Cargo desejado
cargo = st.text_input("🎯 Escreve o cargo desejado (ex: programador, marketing, gestor)")

# Upload de PDFs
files = st.file_uploader(
    "📥 Carrega os currículos (PDF)",
    type="pdf",
    accept_multiple_files=True
)

# PROCESSAMENTO
if files and cargo:

    st.markdown("---")
    st.subheader("📊 Ranking de Currículos")

    resultados = []

    # palavras-chave do cargo
    palavras_chave = cargo.lower().split()

    for file in files:
        texto = ler_pdf(file)

        # contar matches
        matches = 0
        for palavra in palavras_chave:
            if palavra in texto:
                matches += 1

        # REGRA PRINCIPAL: sem match = 0%
        if matches == 0:
            score = 0
        else:
            score = (matches / len(palavras_chave)) * 100

        resultados.append((file.name, score))

    # ordenar do melhor para o pior
    resultados.sort(key=lambda x: x[1], reverse=True)

    # mostrar resultados
    for nome, score in resultados:
        st.write(f"📄 {nome} → {score:.0f}%")