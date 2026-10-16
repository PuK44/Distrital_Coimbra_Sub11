import sys
import os

# Adiciona a diretoria raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from src.modelos import GestorCampeonato, Serie
from src.gestor_dados import GestorDados

# Configuração da página
st.set_page_config(page_title="Troféu Distrital Coimbra Sub11", layout="wide")

# Inicialização segura
gestor_dados = GestorDados()
st.session_state["gestor_dados"] = gestor_dados

# Dados pré-carregados das 4 séries
DADOS_INICIAIS = {
    "SÉRIE A": {
        "equipas": {
            1: "Cd Lousanense", 2: "Fc Oliveira Hospital",
            3: "Red School", 4: "Cdr Penelense",
            5: "Cdr Vasco Gama", 6: "Gd Pampilhosense",
            7: "Red Eagle", 8: "União 1919",
            9: "Co Jardim Alva", 10: "Mocidade Fc",
            11: "Gd Tourizense", 12: "Ca Gândaras"
        },
        "jogos_j1": [(1,2,1,0), (3,4,1,0), (5,6,1,0), (7,8,0,0), (9,10,0,1), (11,12,0,1)]
    },
    "SÉRIE B": {
        "equipas": {
            1: "Sanjoanense Ac", 2: "Adc Adémia",
            3: "Cd Assafarge", 4: "Gr Vigor Mocidade",
            5: "Uc Eirense", 6: "Ad Souselas",
            7: "Académica Coimbra/Oaf", 8: "A. D. Briosa Talent",
            9: "Académica Coimbra/Sf", 10: "Esperança Ac"
        },
        "jogos_j1": [(1,2,0,1), (3,4,0,1), (5,6,0,0), (7,8,1,0), (9,10,0,1)]
    },
    "SÉRIE C": {
        "equipas": {
            1: "Academia \"Os Marialvas\"", 2: "Núcleo Sporting Ançã",
            3: "Cl. Condeixa", 4: "Ar Casaense",
            5: "Cd Carapinheirense", 6: "Ançã Fc",
            7: "Fc São Silvestre", 8: "Gd Sepins",
            9: "Sc Ribeirense", 10: "Gd Sourense \"A\""
        },
        "jogos_j1": [(1,2,1,0), (3,4,0,1), (5,6,0,1), (7,8,0,1), (9,10,0,1)]
    },
    "SÉRIE D": {
        "equipas": {
            1: "Ac Montemorense", 2: "Gd Maiorca",
            3: "Gd Os Águias", 4: "Gc Figueirense",
            5: "A. Naval 1893", 6: "Cr Praia Leirosa",
            7: "Gd Pm - Touring 1970", 8: "Acds Vinha Rainha",
            9: "Gd Sourense \"B\"", 10: "Ud Tocha",
            11: "Cd Porto - Coimbra", 12: "Acr Seixo Mira"
        },
        "jogos_j1": [(1,2,1,0), (3,4,0,1), (5,6,1,0), (7,8,0,0), (9,10,0,1), (11,12,1,0)]
    }
}

def carregar_ou_inicializar():
    g = None
    try:
        g = gestor_dados.carregar_dados()
    except Exception:
        g = None
    
    if g is None or not getattr(g, "series", {}):
        g = GestorCampeonato()
        g.series = {}
        for nome_s, info in DADOS_INICIAIS.items():
            s = Serie(nome_s)
            for num, eq in info["equipas"].items():
                s.adicionar_equipa(num, eq)
            for c, f, gc, gf in info["jogos_j1"]:
                j = s.adicionar_jogo(jornada=1, equipa_casa=c, equipa_fora=f)
                j.definir_resultado(gc, gf)
            g.series[nome_s] = s
        gestor_dados.guardar_dados(g)
    return g

if "campeonato" not in st.session_state or st.session_state["campeonato"] is None:
    st.session_state["campeonato"] = carregar_ou_inicializar()

gestor = st.session_state["campeonato"]

st.title("⚽ Troféu Distrital Coimbra - Sub11")

# Sidebar - Modo Administrador
st.sidebar.header("⚙️ Definições & Acesso")
senha_admin = st.sidebar.text_input("Palavra-passe Admin", type="password")
e_admin = (senha_admin == "lsasub11")

if e_admin:
    st.sidebar.success("Modo Admin Ativo")
else:
    st.sidebar.info("Modo Visitante (Apenas registo de resultados)")

# Tabs principais
tab_fase1, tab_fase2 = st.tabs(["Primeira Fase", "Segunda Fase"])

with tab_fase1:
    st.header("Primeira Fase")
    
    series_list = list(gestor.series.keys())
    serie_ativa = st.selectbox("Selecionar Série", series_list)
    s_ativa = gestor.series[serie_ativa]

    # Painel do Admin para agendar jogos por número de equipa
    if e_admin:
        with st.expander("🛠️ ÁREA ADMIN: Guia de Números das Equipas & Criar Jogos", expanded=True):
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.write(f"**Equipas Registadas na {serie_ativa}:**")
                for num, eq in sorted(s_ativa.equipas.items()):
                    st.text(f"Nº {num}: {eq.nome}")
            
            with col_b:
                st.write("**Agendar Novo Jogo:**")
                num_casa = st.number_input("Nº Equipa Casa", min_value=1, max_value=20, value=1, key="ncasa")
                num_fora = st.number_input("Nº Equipa Fora", min_value=1, max_value=20, value=2, key="nfora")
                jornada = st.number_input("Jornada", min_value=1, max_value=30, value=2, key="jornada_in")
                
                if st.button("Agendar Jogo"):
                    if num_casa in s_ativa.equipas and num_fora in s_ativa.equipas:
                        s_ativa.adicionar_jogo(int(jornada), int(num_casa), int(num_fora))
                        gestor_dados.guardar_dados(gestor)
                        st.success(f"Jogo da Jornada {jornada} adicionado!")
                        st.rerun()
                    else:
                        st.error("Número de equipa inválido para esta série.")

    # Exibição de Jogos e Classificação
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🗓️ Jogos & Resultados")
        
        jornadas_existentes = sorted(list(set(j.jornada for j in s_ativa.jogos))) if s_ativa.jogos else []
        jornada_sel = st.selectbox("Filtrar por Jornada", jornadas_existentes) if jornadas_existentes else None

        jogos_filtrados = [j for j in s_ativa.jogos if j.jornada == jornada_sel] if jornada_sel else s_ativa.jogos

        if not jogos_filtrados:
            st.info("Nenhum jogo registado.")
        else:
            for idx, jogo in enumerate(jogos_filtrados):
                eq_c = s_ativa.equipas.get(jogo.equipa_casa)
                eq_f = s_ativa.equipas.get(jogo.equipa_fora)
                
                nome_c = eq_c.nome if eq_c else f"Equipa {jogo.equipa_casa}"
                nome_f = eq_f.nome if eq_f else f"Equipa {jogo.equipa_fora}"
                
                st.write(f"**Jornada {jogo.jornada}:** {nome_c} vs {nome_f}")
                
                res_atual = f"{jogo.golo_casa} - {jogo.golo_fora}" if jogo.realizado else "Por jogar"
                opcoes_res = ["Por jogar", "1 - 0", "0 - 0", "0 - 1"]
                idx_default = opcoes_res.index(res_atual) if res_atual in opcoes_res else 0
                
                novo_res = st.selectbox(
                    f"Resultado Jogo {idx+1}",
                    opcoes_res,
                    index=idx_default,
                    key=f"res_{serie_ativa}_{jogo.jornada}_{idx}"
                )
                
                if st.button(f"Guardar Resultado (Jogo {idx+1})", key=f"btn_{serie_ativa}_{jogo.jornada}_{idx}"):
                    if novo_res == "Por jogar":
                        jogo.realizado = False
                        jogo.golo_casa = 0
                        jogo.golo_fora = 0
                    else:
                        gc, gf = map(int, novo_res.split(" - "))
                        jogo.definir_resultado(gc, gf)
                    
                    gestor_dados.guardar_dados(gestor)
                    st.success("Resultado atualizado!")
                    st.rerun()
                st.divider()

    with col2:
        st.subheader("📊 Tabela de Classificação")
        df_classificacao = s_ativa.obter_classificacao()
        if not df_classificacao.empty:
            st.dataframe(df_classificacao, width=600, hide_index=True)
        else:
            st.info("Sem equipas registadas.")
