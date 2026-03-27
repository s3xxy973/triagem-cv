import streamlit as st
import PyPDF2

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

st.title("📄 Sistema de Triagem por Cargo (IA simples)")
st.markdown("Escolhe um cargo e o sistema vai analisar os currículos")

st.markdown("---")

# 👉 NOVO: cargo desejado
cargo = st.text_input("🎯 Escreve o cargo desejado (ex: programador, gestor, marketing)")

# Upload de PDFs
files = st.file_uploader(
    "📥 Carrega os currículos (PDF)",
    type="pdf",
    accept_multiple_files=True
)

# Botão
if st.button("🔍 Analisar currículos"):

    if not cargo:
        st.warning("Escreve primeiro o cargo desejado!")
    
    elif not files:
        st.warning("Carrega pelo menos um PDF!")

    else:
        candidatos = []

        # palavras base por cargo
        palavras_base = {
            "programador": ["python", "java", "programação", "software", "developer", "código"],
            "gestor": ["gestão", "liderança", "equipa", "administração", "projetos"],
            "marketing": ["marketing", "vendas", "publicidade", "digital", "redes sociais"]
        }

        # escolher palavras do cargo
        palavras_chave = palavras_base.get(cargo.lower(), cargo.lower().split())

        for file in files:
            texto = ler_pdf(file)

            score = 0

            # pontuação por palavras-chave
            for palavra in palavras_chave:
                if palavra in texto:
                    score += 20

            # bônus por tamanho do CV
            score += len(texto) // 100

            candidatos.append((file.name, score))

        # ranking
        candidatos.sort(key=lambda x: x[1], reverse=True)

        st.subheader(f"🏆 Ranking para o cargo: {cargo}")

        for i, c in enumerate(candidatos):
            st.write(f"{i+1}. {c[0]} — ⭐ Score: {c[1]}")