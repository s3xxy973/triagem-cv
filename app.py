import streamlit as st
import PyPDF2

st.set_page_config(page_title="Triagem Inteligente de CVs", layout="wide")

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
# PERFIS (mais inteligentes)
# -------------------------
perfis = {
    "recursos humanos": {
        "peso_alto": ["recrutamento", "seleção", "rh", "gestão de pessoas"],
        "peso_medio": ["liderança", "treinamento", "equipa", "contratação"]
    },
    "gestão": {
        "peso_alto": ["gestão", "administração", "planejamento", "estratégia"],
        "peso_medio": ["liderança", "organização", "coordenação"]
    },
    "contabilidade": {
        "peso_alto": ["contabilidade", "balanço", "impostos", "auditoria"],
        "peso_medio": ["finanças", "relatórios", "caixa"]
    },
    "financeiro": {
        "peso_alto": ["finanças", "investimento", "orçamento"],
        "peso_medio": ["análise financeira", "planeamento"]
    },
    "marketing": {
        "peso_alto": ["marketing", "seo", "publicidade", "vendas"],
        "peso_medio": ["branding", "redes sociais"]
    },
    "programação": {
        "peso_alto": ["python", "java", "javascript", "sql"],
        "peso_medio": ["desenvolvimento", "software", "git"]
    }
}

# -------------------------
# INTERFACE
# -------------------------
st.title("📄 IA de Triagem de Currículos")

cargo_input = st.text_input("🎯 Cargo desejado (ex: gestor de recursos humanos, marketing, contabilidade)")
files = st.file_uploader("📥 Upload de CVs (PDF)", type="pdf", accept_multiple_files=True)

st.markdown("---")

# -------------------------
# PROCESSAMENTO
# -------------------------
if cargo_input and files:

    cargo = cargo_input.lower()

    # identificar perfil
    perfil_encontrado = None

    for p in perfis:
        if p in cargo:
            perfil_encontrado = p
            break

    if not perfil_encontrado:
        st.error("❌ Não consegui identificar o cargo. Tenta: recursos humanos, gestão, marketing, contabilidade, financeiro, programação")
        st.stop()

    regras = perfis[perfil_encontrado]

    resultados = []

    for file in files:

        texto = ler_pdf(file)

        score = 0

        # peso alto
        for palavra in regras["peso_alto"]:
            if palavra in texto:
                score += 20

        # peso médio
        for palavra in regras["peso_medio"]:
            if palavra in texto:
                score += 10

        if score > 100:
            score = 100

        resultados.append({
            "nome": file.name,
            "score": score
        })

    resultados.sort(key=lambda x: x["score"], reverse=True)

    st.subheader("📊 Ranking de Candidatos")

    pos = 1

    for r in resultados:
        st.write(f"{pos}º - {r['nome']} → {r['score']}%")
        pos += 1