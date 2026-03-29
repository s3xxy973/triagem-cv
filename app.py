import streamlit as st
import PyPDF2

st.set_page_config(page_title="Triagem de Currículos", layout="wide")

# -----------------------
# LER PDF
# -----------------------
def ler_pdf(file):
    reader = PyPDF2.PdfReader(file)
    texto = ""
    for page in reader.pages:
        if page.extract_text():
            texto += page.extract_text()
    return texto.lower()

# -----------------------
# BASE DE ÁREAS E SKILLS
# -----------------------
areas = {
    "recursos humanos": ["rh", "recrutamento", "liderança", "gestão de pessoas", "treinamento"],
    "gestão": ["gestão", "administração", "planejamento", "estratégia", "liderança"],
    "contabilidade": ["contabilidade", "balanço", "impostos", "auditoria", "finanças"],
    "financeiro": ["finanças", "investimento", "orçamento", "análise financeira"],
    "marketing": ["marketing", "seo", "vendas", "branding", "publicidade"],
    "programação": ["python", "java", "javascript", "sql", "desenvolvimento"],
    "agricultura": ["agricultura", "agronomia", "irrigação", "solo", "pecuária"],
    "engenharia civil": ["construção", "obras", "betão", "estruturas"],
    "enfermagem": ["enfermagem", "hospital", "paciente", "cuidados"],
    "medicina": ["medicina", "diagnóstico", "tratamento", "clínica"],
    "direito": ["advogado", "lei", "jurídico", "tribunal", "contrato"],
    "educação": ["professor", "ensino", "educação", "aula"],
    "logística": ["logística", "transporte", "armazenamento", "distribuição"],
    "vendas": ["vendas", "negociação", "cliente", "comercial"],
    "design": ["design", "ui", "ux", "photoshop", "criatividade"],
    "hotelaria": ["hotel", "turismo", "atendimento", "hospitalidade"]
}

# -----------------------
# INTERFACE
# -----------------------
st.title("📄 Triagem Inteligente de Currículos")

cargo_input = st.text_input("🎯 Escreve o cargo desejado")

files = st.file_uploader(
    "📥 Upload de CVs (PDF)",
    type="pdf",
    accept_multiple_files=True
)

st.markdown("---")

# -----------------------
# PROCESSAMENTO
# -----------------------
if cargo_input and files:

    cargo = cargo_input.lower()

    # 🔥 SEM ERRO DE CARGO: procura por correspondência parcial
    cargo_encontrado = None

    for area in areas:
        if area in cargo:
            cargo_encontrado = area
            break

    if cargo_encontrado is None:
        st.error("❌ Área não reconhecida. Tenta: gestão, marketing, contabilidade, recursos humanos...")
        st.stop()

    skills = areas[cargo_encontrado]

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
    encontrou = False

    for r in resultados:
        if r["score"] > 0:
            encontrou = True
            st.write(f"{pos}º - {r['nome']} → {r['score']}%")
            pos += 1

    if not encontrou:
        st.warning("❌ Nenhum candidato compatível encontrado")