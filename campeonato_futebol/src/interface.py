import sys
import os

# Adiciona a diretoria raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from src.modelos import GestorCampeonato, Serie, Jogo
from src.gestor_dados import GestorDados

# Configuração da página
st.set_page_config(page_title="Troféu Distrital Coimbra Sub11", layout="wide")

# Inicialização do gestor de dados
gestor_dados = GestorDados()

# Estrutura com as 4 Séries, 44 Equipas e Resultados da Jornada 1
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

def criar_campeonato_inicial():
    g = GestorCampeonato()
    for nome_s, info in DADOS_INICIAIS.items():
        s = Serie(nome_s)
        for num, eq in info["equipas"].items():
            s.adicionar_equipa(num, eq)
        for c, f, gc, gf in info["jogos_j1"]:
            j = s.adicionar_jogo(1, c, f)
            j.definir_resultado(gc, gf)
        g.series[nome_s] = s
    gestor_dados.guardar_dados(g)
    return g

# Carregamento seguro na memória de sessão
if "campeonato" not in st.session_state:
    dados = gestor_dados.carregar_dados()
    if dados is None or not dados.series or len(dados.series) < 4:
        st.session_state["campeonato"] = criar_campeonato_inicial()
    else:
        st.session_state["campeonato"] = dados

campeonato = st.session_state["campeonato"]

st.title("⚽ Troféu Distrital Coimbra - Sub11")

# Sidebar - Painel de Acesso Admin
st.sidebar.header("⚙️ Definições & Acesso")
senha_admin = st.sidebar.text_input("Palavra-passe Admin", type="password")
e_admin = (senha_admin == "admin123")

if e_admin:
    st.sidebar.success("Modo Admin Ativo")
else:
    st.sidebar.info("Modo Visitante (Registo de resultados)")

# Separadores das Fases
tab_fase1, tab_fase2 = st.tabs(["Primeira Fase", "Segunda Fase"])

with tab_fase1:
    st.header("Primeira Fase")
    
    series_nomes = list(campeonato.series.keys())
    serie_sel = st.selectbox("Selecionar Série", series_nomes)
    s_obj = campeonato.series[serie_sel]

    # Painel exclusivo de Administrador
    if e_admin:
        with st.expander("🛠️ ÁREA ADMIN: Guia de Números & Criar Jogos", expanded=True):
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.write(f"**Equipas da {serie_sel}:**")
                for num, eq in sorted(s_obj.equipas.items()):
                    st.text(f"Nº {num}: {eq.nome}")
            
            with col_b:
                st.write("**Agendar Novo Jogo:**")
                num_casa = st.number_input("Nº Equipa Casa", min_value=1, max_value=20, value=1, key="ncasa")
                num_fora = st.number_input("Nº Equipa Fora", min_value=1, max_value=20, value=2, key="nfora")
                jornada_in = st.number_input("Jornada", min_value=1, max_value=30, value=2, key="jornada_in")
                
                if st.button("Agendar Jogo"):
                    if num_casa in s_obj.equipas and num_fora in s_obj.equipas:
                        s_obj.adicionar_jogo(int(jornada_in), int(num_casa), int(num_fora))
                        gestor_dados.guardar_dados(campeonato)
                        st.success(f"Jogo da Jornada {jornada_in} agendado!")
                        st.rerun()
                    else:
                        st.error("Número de equipa inválido para esta série.")

    # Visualização e Lançamento de Resultados
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🗓️ Jogos & Resultados")
        
        jornadas_existentes = sorted(list(set(j.jornada for j in s_obj.jogos))) if s_obj.jogos else []
        jornada_filtro = st.selectbox("Filtrar por Jornada", jornadas_existentes) if jornadas_existentes else None

        jogos_exibir = [j for j in s_obj.jogos if j.jornada == jornada_filtro] if jornada_filtro else s_obj.jogos

        if not jogos_exibir:
            st.info("Nenhum jogo agendado.")
        else:
            for idx, jogo in enumerate(jogos_exibir):
                eq_c = s_obj.equipas.get(jogo.equipa_casa)
                eq_f = s_obj.equipas.get(jogo.equipa_fora)
                
                nome_c = eq_c.nome if eq_c else f"Equipa {jogo.equipa_casa}"
                nome_f = eq_f.nome if eq_f else f"Equipa {jogo.equipa_fora}"
                
                st.write(f"**Jornada {jogo.jornada}:** {nome_c} vs {nome_f}")
                
                res_atual = f"{jogo.golo_casa} - {jogo.golo_fora}" if jogo.realizado else "Por jogar"
                opcoes_res = ["Por jogar", "1 - 0", "0 - 0", "0 - 1"]
                idx_default = opcoes_res.index(res_atual) if res_atual in opcoes_res else 0
                
                novo_res = st.selectbox(
                    f"Resultado (Jogo {idx+1})",
                    opcoes_res,
                    index=idx_default,
                    key=f"res_{serie_sel}_{jogo.jornada}_{idx}"
                )
                
                if st.button(f"Guardar Resultado (Jogo {idx+1})", key=f"btn_{serie_sel}_{jogo.jornada}_{idx}"):
                    if novo_res == "Por jogar":
                        jogo.realizado = False
                        jogo.golo_casa = 0
                        jogo.golo_fora = 0
                    else:
                        gc, gf = map(int, novo_res.split(" - "))
                        jogo.definir_resultado(gc, gf)
                    
                    gestor_dados.guardar_dados(campeonato)
                    st.success("Resultado guardado com sucesso!")
                    st.rerun()
                st.divider()

    with col2:
        st.subheader("📊 Tabela de Classificação")
        df_classif = s_obj.obter_classificacao()
        if not df_classif.empty:
            st.dataframe(df_classif, width=600, hide_index=True)
        else:
            st.info("Sem equipas registadas.")