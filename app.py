import streamlit as st
import PyPDF2

st.set_page_config(page_title="IA de Recrutamento", layout="wide")

# -------------------------
# LER PDF
# -------------------------
def ler_pdf(file):
    reader = PyPDF2.PdfReader(file)
    texto = ""
    for page in reader.pages:
        if page.extract_text():
            texto += page.extract_text()
    return texto.lower()

# -------------------------
# PERFIS
# -------------------------
perfis = {
    "recursos humanos": {
        "alto": ["recrutamento", "seleção", "rh", "gestão de pessoas"],
        "medio": ["liderança", "treinamento", "equipa", "contratação"]
    },
    "gestão": {
        "alto": ["gestão", "administração", "estratégia", "planejamento"],
        "medio": ["liderança", "organização", "coordenação"]
    },
    "contabilidade": {
        "alto": ["contabilidade", "balanço", "impostos", "auditoria"],
        "medio": ["finanças", "relatórios", "caixa"]
    },
    "marketing": {
        "alto": ["marketing", "seo", "publicidade", "vendas"],
        "medio": ["branding", "redes sociais"]
    },
    "programação": {
        "alto": ["python", "java", "javascript", "sql"],
        "medio": ["desenvolvimento", "software", "git"]
    }
}

# -------------------------
# INTERFACE
# -------------------------
st.title("📄 IA de Recrutamento Inteligente (HR System)")

cargo_input = st.text_input("🎯 Cargo desejado")
files = st.file_uploader("📥 Upload de CVs (PDF)", type="pdf", accept_multiple_files=True)

st.markdown("---")

# -------------------------
# PROCESSAMENTO
# -------------------------
if cargo_input and files:

    cargo = cargo_input.lower()

    perfil = None

    for p in perfis:
        if p in cargo:
            perfil = p
            break

    if not perfil:
        st.error("❌ Cargo não reconhecido (ex: recursos humanos, gestão, marketing, contabilidade)")
        st.stop()

    regras = perfis[perfil]

    resultados = []

    for file in files:

        texto = ler_pdf(file)

        encontrados_alto = []
        encontrados_medio = []

        score = 0

        for w in regras["alto"]:
            if w in texto:
                encontrados_alto.append(w)
                score += 20

        for w in regras["medio"]:
            if w in texto:
                encontrados_medio.append(w)
                score += 10

        if score > 100:
            score = 100

        resultados.append({
            "nome": file.name,
            "score": score,
            "alto": encontrados_alto,
            "medio": encontrados_medio
        })

    resultados.sort(key=lambda x: x["score"], reverse=True)

    st.subheader("📊 Ranking de Candidatos")

    pos = 1

    for r in resultados:

        st.markdown(f"### {pos}º - {r['nome']}")

        st.progress(r["score"] / 100)
        st.write(f"🎯 Score: {r['score']}%")

        if r["alto"]:
            st.success("🔥 Competências fortes: " + ", ".join(r["alto"]))

        if r["medio"]:
            st.info("📌 Competências médias: " + ", ".join(r["medio"]))

        if not r["alto"] and not r["medio"]:
            st.error("❌ Sem competências relevantes")

        st.markdown("---")

        pos += 1