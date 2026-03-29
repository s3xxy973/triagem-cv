import streamlit as st
import PyPDF2

st.set_page_config(page_title="Triagem de Currículos", layout="wide")

# ---------------------------
# LER PDF
# ---------------------------
def ler_pdf(file):
    reader = PyPDF2.PdfReader(file)
    texto = ""
    for page in reader.pages:
        if page.extract_text():
            texto += page.extract_text()
    return texto.lower()

# ---------------------------
# 20 ÁREAS PROFISSIONAIS
# ---------------------------
skills_por_cargo = {
    "recursos humanos": ["rh", "recrutamento", "gestão de pessoas", "liderança", "treinamento"],
    "gestão": ["gestão", "liderança", "administração", "planejamento", "estratégia"],
    "contabilidade": ["contabilidade", "balanço", "finanças", "impostos", "auditoria"],
    "financeiro": ["finanças", "investimento", "orçamento", "análise financeira", "contabilidade"],
    "marketing": ["marketing", "seo", "vendas", "branding", "publicidade"],
    "programação": ["python", "java", "javascript", "sql", "desenvolvimento"],
    "agricultura": ["agricultura", "agronomia", "solo", "irrigação", "pecuária"],
    "engenharia civil": ["construção", "betão", "estruturas", "obras", "engenharia"],
    "enfermagem": ["enfermagem", "hospital", "cuidados", "paciente", "saúde"],
    "medicina": ["diagnóstico", "medicina", "clínica", "paciente", "tratamento"],
    "direito": ["advogado", "lei", "jurídico", "tribunal", "contrato"],
    "educação": ["professor", "ensino", "educação", "didática", "aula"],
    "logística": ["transporte", "logística", "armazenamento", "distribuição"],
    "vendas": ["vendas", "negociação", "cliente", "comercial", "fecho"],
    "administração": ["administração", "gestão", "organização", "processos"],
    "ti": ["tecnologia", "rede", "sistemas", "suporte", "informática"],
    "design": ["design", "photoshop", "ui", "ux", "criatividade"],
    "recursos naturais": ["ambiente", "ecologia", "recursos naturais", "sustentabilidade"],
    "hotelaria": ["hotel", "turismo", "atendimento", "hospitalidade"],
    "construção": ["obra", "engenheiro", "canteiro", "construção", "projeto"]
}

# ---------------------------
# INTERFACE
# ---------------------------
st.title("📄 Sistema Inteligente de Triagem de Currículos")

cargo_input = st.text_input("🎯 Escreve o cargo (ex: gestor de recursos humanos, contabilidade, marketing)")

files = st.file_uploader(
    "📥 Upload de CVs (PDF)",
    type="pdf",
    accept_multiple_files=True
)

st.markdown("---")
st.info("O sistema analisa automaticamente e faz ranking dos melhores candidatos")

# ---------------------------
# PROCESSAMENTO
# ---------------------------
if cargo_input and files:

    cargo = cargo_input.lower()

    # reconhecimento inteligente
    cargo_encontrado = None

    for chave in skills_por_cargo.keys():
        if chave in cargo:
            cargo_encontrado = chave
            break

    if not cargo_encontrado:
        st.error("❌ Cargo não reconhecido no sistema")
        st.stop()

    skills_vaga = skills_por_cargo[cargo_encontrado]

    resultados = []

    for file in files:

        texto = ler_pdf(file)

        matches = [skill for skill in skills_vaga if skill in texto]

        score = 0 if len(matches) == 0 else int((len(matches) / len(skills_vaga)) * 100)

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