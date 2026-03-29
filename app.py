import streamlit as st
import PyPDF2

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(page_title="AI Recruitment System", layout="wide")

# =========================
# DESIGN MODERNO
# =========================
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: white;
    }

    h1 {
        color: #00ffcc;
        text-align: center;
    }

    .stTextInput > div > div > input {
        background-color: #1c1f26;
        color: white;
    }

    .stFileUploader {
        background-color: #1c1f26;
        border-radius: 10px;
        padding: 10px;
    }

    .stProgress > div > div > div > div {
        background-color: #00ffcc;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# PDF READER
# =========================
def ler_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# =========================
# BASE DE CARGOS (20 ÁREAS)
# =========================
areas = {
    "recursos humanos": ["recrutamento", "seleção", "rh", "gestão de pessoas", "treinamento"],
    "gestão": ["gestão", "administração", "planejamento", "estratégia", "liderança"],
    "contabilidade": ["contabilidade", "balanço", "impostos", "auditoria"],
    "financeiro": ["finanças", "investimento", "orçamento", "análise financeira"],
    "marketing": ["marketing", "seo", "publicidade", "vendas", "branding"],
    "programação": ["python", "java", "javascript", "sql", "desenvolvimento"],
    "agricultura": ["agricultura", "irrigação", "solo", "pecuária"],
    "engenharia civil": ["construção", "obras", "betão", "engenharia"],
    "enfermagem": ["enfermagem", "hospital", "paciente", "cuidados"],
    "medicina": ["medicina", "diagnóstico", "tratamento", "clínica"],
    "direito": ["advogado", "lei", "jurídico", "tribunal"],
    "educação": ["professor", "ensino", "educação", "aula"],
    "logística": ["logística", "transporte", "armazenamento", "distribuição"],
    "vendas": ["vendas", "negociação", "cliente", "comercial"],
    "design": ["design", "ui", "ux", "photoshop", "criatividade"],
    "hotelaria": ["hotel", "turismo", "hospitalidade", "atendimento"],
    "recursos naturais": ["ambiente", "ecologia", "sustentabilidade"],
    "ti": ["tecnologia", "rede", "sistemas", "suporte"],
    "administração": ["administração", "organização", "processos"],
    "engenharia": ["engenharia", "projeto", "cálculo", "estrutura"]
}

# =========================
# INTERFACE
# =========================
st.title("🚀 AI Recruitment System")
st.caption("Triagem inteligente de currículos com análise automática")

cargo_input = st.text_input("🎯 Escreve o cargo desejado (ex: gestor de recursos humanos, marketing, contabilidade)")

files = st.file_uploader("📥 Upload de CVs (PDF)", type="pdf", accept_multiple_files=True)

st.markdown("---")

st.info("ℹ️ O sistema analisa os CVs e cria ranking automático baseado em competências")

# =========================
# PROCESSAMENTO
# =========================
if cargo_input and files:

    cargo = cargo_input.lower()

    # detectar área automaticamente
    area_detectada = None

    for a in areas:
        if a in cargo:
            area_detectada = a
            break

    if not area_detectada:
        st.error("❌ Cargo não reconhecido. Tenta algo como: gestão, marketing, contabilidade, recursos humanos, programação")
        st.stop()

    skills = areas[area_detectada]

    resultados = []

    for file in files:

        texto = ler_pdf(file)

        matches = [s for s in skills if s in texto]

        score = int((len(matches) / len(skills)) * 100) if matches else 0

        resultados.append({
            "nome": file.name,
            "score": score,
            "matches": matches
        })

    resultados.sort(key=lambda x: x["score"], reverse=True)

    st.subheader("📊 Ranking de Candidatos")

    pos = 1

    for r in resultados:

        st.markdown(f"### {pos}º - {r['nome']}")

        st.progress(r["score"] / 100)
        st.write(f"🎯 Score: {r['score']}%")

        if r["matches"]:
            st.success("✔ Competências encontradas: " + ", ".join(r["matches"]))
        else:
            st.error("❌ Sem competências relevantes")

        st.markdown("---")

        pos += 1