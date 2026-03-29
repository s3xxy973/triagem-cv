import streamlit as st

    cargo = cargo.lower().strip()

    if cargo not in skills_por_cargo:
        st.error("❌ Cargo não encontrado no sistema")

    else:

        skills_vaga = skills_por_cargo[cargo]

        resultados = []

        for file in files:

            texto = ler_pdf(file)

            matches = []

            for skill in skills_vaga:
                if skill.lower() in texto:
                    matches.append(skill)

            total_matches = len(matches)

            # REGRA IMPORTANTE
            # sem habilidades da vaga = 0%
            if total_matches == 0:
                score = 0

            else:
                score = int((total_matches / len(skills_vaga)) * 100)

            resultados.append({
                "nome": file.name,
                "score": score,
                "matches": matches
            })

        # ordenar ranking
        resultados = sorted(
            resultados,
            key=lambda x: x["score"],
            reverse=True
        )

        st.markdown("---")
        st.subheader("📊 Ranking de Compatibilidade")

        for resultado in resultados:

            st.markdown(f"### 📄 {resultado['nome']}")

            st.progress(resultado["score"] / 100)

            st.write(f"✅ Compatibilidade: {resultado['score']}%")

            if resultado["matches"]:
                st.write(
                    "🧠 Habilidades encontradas:",
                    ", ".join(resultado["matches"])
                )
            else:
                st.write("❌ Nenhuma habilidade compatível encontrada")

            st.markdown("---")