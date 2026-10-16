import sys
import os

# Adiciona a diretoria raiz ao sys.path para importações
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from src.modelos import GestorCampeonato, Serie
from src.gestor_dados import GestorDados

# Configuração da página
st.set_page_config(page_title="Troféu Distrital Coimbra Sub11", layout="wide")

# Inicialização segura do gestor e dados
if "gestor_dados" not in st.session_state:
    st.session_state["gestor_dados"] = GestorDados()

gestor_dados = st.session_state["gestor_dados"]

if "campeonato" not in st.session_state or st.session_state["campeonato"] is None:
    dados_carregados = gestor_dados.carregar()
    st.session_state["campeonato"] = dados_carregados if dados_carregados is not None else GestorCampeonato()

gestor = st.session_state["campeonato"]

st.title("⚽ Troféu Distrital Coimbra - Sub11")

# Sidebar - Modo Administrador
st.sidebar.header("⚙️ Definições & Acesso")
senha_admin = st.sidebar.text_input("Palavra-passe Admin", type="password")
e_admin = (senha_admin == "admin123")

if e_admin:
    st.sidebar.success("Modo Admin Ativo")
else:
    st.sidebar.info("Modo Visitante (Apenas registo de resultados)")

# Tabs principais
tab_fase1, tab_fase2 = st.tabs(["Primeira Fase", "Segunda Fase"])

with tab_fase1:
    st.header("Primeira Fase")
    
    # Administrador: Gestão de Séries e Equipas
    if e_admin:
        with st.expander("🛠️ Gestão de Séries e Equipas (Apenas Admin)", expanded=False):
            st.subheader("Criar / Selecionar Série")
            nome_nova_serie = st.text_input("Nome da nova Série (ex: Série A)")
            if st.button("Criar Série"):
                if nome_nova_serie and nome_nova_serie not in gestor.fase1_series:
                    gestor.fase1_series[nome_nova_serie] = Serie(nome_nova_serie)
                    gestor_dados.guardar(gestor)
                    st.success(f"Série {nome_nova_serie} criada!")
                    st.rerun()

            st.divider()
            
            series_existentes = list(gestor.fase1_series.keys())
            if series_existentes:
                serie_sel_admin = st.selectbox("Escolher Série para adicionar equipas", series_existentes, key="admin_serie")
                s_obj = gestor.fase1_series[serie_sel_admin]
                
                num_equipa = st.number_input("Número da Equipa", min_value=1, max_value=20, value=1)
                nome_equipa = st.text_input("Nome da Equipa")
                
                if st.button("Adicionar / Atualizar Equipa"):
                    if nome_equipa:
                        s_obj.adicionar_equipa(int(num_equipa), nome_equipa)
                        gestor_dados.guardar(gestor)
                        st.success(f"Equipa {num_equipa} - {nome_equipa} gravada!")
                        st.rerun()
                        
                st.write("**Equipas inscritas:**")
                for num, eq in sorted(s_obj.equipas.items()):
                    st.text(f"Nº {num}: {eq.nome}")

    # Visualização e Lançamento de Jogos/Classificação (Público & Admin)
    series_list = list(gestor.fase1_series.keys())
    if not series_list:
        st.warning("Ainda não existem séries criadas.")
    else:
        serie_ativa = st.selectbox("Selecionar Série", series_list)
        s_ativa = gestor.fase1_series[serie_ativa]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🗓️ Jogos & Resultados")
            
            if e_admin:
                with st.expander("➕ Adicionar Jogo por Número de Equipa"):
                    num_casa = st.number_input("Nº Equipa Casa", min_value=1, max_value=20, value=1, key="ncasa")
                    num_fora = st.number_input("Nº Equipa Fora", min_value=1, max_value=20, value=2, key="nfora")
                    jornada = st.number_input("Jornada", min_value=1, max_value=30, value=1)
                    
                    if st.button("Agendar Jogo"):
                        if num_casa in s_ativa.equipas and num_fora in s_ativa.equipas:
                            s_ativa.adicionar_jogo(int(jornada), int(num_casa), int(num_fora))
                            gestor_dados.guardar(gestor)
                            st.success("Jogo adicionado!")
                            st.rerun()
                        else:
                            st.error("Certifica-te de que ambas as equipas (números) já estão criadas nesta série.")

            if not s_ativa.jogos:
                st.info("Ainda não há jogos agendados nesta série.")
            else:
                for idx, jogo in enumerate(s_ativa.jogos):
                    eq_c = s_ativa.equipas.get(jogo.equipa_casa)
                    eq_f = s_ativa.equipas.get(jogo.equipa_fora)
                    
                    nome_c = eq_c.nome if eq_c else f"Equipa {jogo.equipa_casa}"
                    nome_f = eq_f.nome if eq_f else f"Equipa {jogo.equipa_fora}"
                    
                    st.write(f"**Jornada {jogo.jornada}:** {nome_c} (Nº {jogo.equipa_casa}) vs {nome_f} (Nº {jogo.equipa_fora})")
                    
                    res_atual = f"{jogo.golo_casa} - {jogo.golo_fora}" if jogo.realizado else "Por jogar"
                    
                    opcoes_res = ["Por jogar", "1 - 0", "0 - 0", "0 - 1"]
                    idx_default = opcoes_res.index(res_atual) if res_atual in opcoes_res else 0
                    
                    novo_res = st.selectbox(
                        f"Resultado (Jogo {idx+1})",
                        opcoes_res,
                        index=idx_default,
                        key=f"res_{serie_ativa}_{idx}"
                    )
                    
                    if st.button(f"Guardar Resultado Jogo {idx+1}", key=f"btn_{serie_ativa}_{idx}"):
                        if novo_res == "Por jogar":
                            jogo.realizado = False
                            jogo.golo_casa = 0
                            jogo.golo_fora = 0
                        else:
                            gc, gf = map(int, novo_res.split(" - "))
                            jogo.definir_resultado(gc, gf)
                        
                        gestor_dados.guardar(gestor)
                        st.success("Resultado guardado com sucesso!")
                        st.rerun()
                    st.divider()

        with col2:
            st.subheader("📊 Tabela de Classificação")
            df_classificacao = s_ativa.obter_classificacao()
            if not df_classificacao.empty:
                st.dataframe(df_classificacao, width=600, hide_index=True)
            else:
                st.info("Sem equipas registadas.")