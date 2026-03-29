import streamlit as st
import PyPDF2

st.set_page_config(page_title="Triagem de Currículos", layout="wide")

# PDF reader
def ler_pdf(file):
    reader = PyPDF2.PdfReader(file)
    texto = ""

    for page in reader.pages:
        if page.extract_text():
            texto += page.extract_text()

    return texto.lower()

# cargos e skills
skills_por_cargo = {
    "gestor": ["gestão", "liderança", "administração", "finanças"],
    "programador": ["python", "java", "javascript", "sql"],
    "marketing": ["marketing", "seo", "vendas"],
    "agricultura": ["agricultura", "irrigação", "campo"]
}

# interface
st.title("📄 Sistema de Triagem de Currículos")

cargo = st.text_input("🎯 Cargo desejado")
files = st.file_uploader("📥 Upload de CVs (PDF)", type="pdf", accept_multiple_files=True)

st.markdown("---")

# SEMPRE MOSTRA ISSO (evita ecrã branco)
st.info("⬆️ Preenche o cargo e faz upload dos CVs para começar")

# só roda se tiver dados
if cargo and files:

    cargo = cargo.lower().strip()

    if cargo not in skills_por_cargo:
        st.error("❌ Cargo não existe no sistema")

    else:

        skills_vaga = skills_por_cargo[cargo]
        resultados = []

        for file in files:

            texto = ler_pdf(file)

            matches = [skill for skill in skills_vaga if skill in texto]

            if len(matches) == 0:
                score = 0
            else:
                score = int((len(matches) / len(skills_vaga)) * 100)

            resultados.append({
                "nome": file.name,
                "score": score,
                "matches": matches
            })

        resultados.sort(key=lambda x: x["score"], reverse=True)

        st.subheader("📊 Ranking de Candidatos")

        pos = 1

        encontrou = False

        for r in resultados:
            if r["score"] > 0:
                encontrou = True
                st.write(f"{pos}º - {r['nome']} → {r['score']}%")
                pos += 1

        if not encontrou:
            st.warning("❌ Nenhum candidato compatível encontrado")