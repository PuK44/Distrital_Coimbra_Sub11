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

# Estrutura Completa da Primeira Fase (Jornadas 1 a 11 para as 4 Séries)
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
        "jogos_j1": [(1,2,1,0), (3,4,1,0), (5,6,1,0), (7,8,0,0), (9,10,0,1), (11,12,0,1)],
        "jogos_sem_resultado": [
            (2, 4, 9), (2, 12, 3), (2, 6, 1), (2, 8, 11), (2, 10, 5), (2, 2, 7),
            (3, 1, 10), (3, 7, 11), (3, 9, 12), (3, 2, 6), (3, 3, 8), (3, 5, 4),
            (4, 8, 9), (4, 11, 3), (4, 4, 1), (4, 10, 2), (4, 6, 7), (4, 12, 5),
            (5, 7, 3), (5, 6, 10), (5, 9, 11), (5, 1, 12), (5, 5, 8), (5, 2, 4),
            (6, 3, 9), (6, 8, 1), (6, 12, 2), (6, 10, 7), (6, 4, 6), (6, 11, 5),
            (7, 7, 9), (7, 5, 3), (7, 1, 11), (7, 6, 12), (7, 2, 8), (7, 10, 4),
            (8, 12, 10), (8, 3, 1), (8, 11, 2), (8, 4, 7), (8, 8, 6), (8, 9, 5),
            (9, 1, 9), (9, 2, 3), (9, 6, 11), (9, 4, 12), (9, 10, 8), (9, 7, 5),
            (10, 11, 10), (10, 5, 1), (10, 7, 12), (10, 9, 2), (10, 3, 6), (10, 8, 4),
            (11, 6, 9), (11, 10, 3), (11, 4, 11), (11, 1, 7), (11, 12, 8), (11, 2, 5)
        ]
    },
    "SÉRIE B": {
        "equipas": {
            1: "Sanjoanense Ac", 2: "Adc Adémia",
            3: "Cd Assafarge", 4: "Gr Vigor Mocidade",
            5: "Uc Eirense", 6: "Ad Souselas",
            7: "Académica Coimbra/Oaf", 8: "A. D. Briosa Talent",
            9: "Académica Coimbra/Sf", 10: "Esperança Ac",
            11: "Af N10"
        },
        "jogos_j1": [(1,2,0,1), (3,4,0,1), (5,6,0,0), (7,8,1,0), (9,10,0,1)],
        "jogos_sem_resultado": [
            (2, 11, 5), (2, 10, 3), (2, 2, 7), (2, 8, 9), (2, 6, 1),
            (3, 9, 2), (3, 1, 11), (3, 7, 6), (3, 3, 8), (3, 4, 10),
            (4, 5, 1), (4, 8, 4), (4, 2, 3), (4, 11, 7), (4, 6, 9),
            (5, 4, 2), (5, 9, 11), (5, 7, 5), (5, 3, 6), (5, 10, 8),
            (6, 6, 4), (6, 11, 3), (6, 1, 7), (6, 5, 9), (6, 2, 10),
            (7, 8, 2), (7, 9, 1), (7, 4, 11), (7, 3, 5), (7, 10, 6),
            (8, 5, 4), (8, 6, 8), (8, 1, 3), (8, 7, 9), (8, 11, 10),
            (9, 4, 1), (9, 8, 11), (9, 10, 5), (9, 2, 6), (9, 3, 7),
            (10, 11, 2), (10, 7, 4), (10, 5, 8), (10, 9, 3), (10, 1, 10),
            (11, 8, 1), (11, 6, 11), (11, 2, 5), (11, 10, 7), (11, 4, 9)
        ]
    },
    "SÉRIE C": {
        "equipas": {
            1: "Academia \"Os Marialvas\"", 2: "Núcleo Sporting Ançã",
            3: "Cl. Condeixa", 4: "Ar Casaense",
            5: "Cd Carapinheirense", 6: "Ançã Fc",
            7: "Fc São Silvestre", 8: "Gd Sepins",
            9: "Sc Ribeirense", 10: "Gd Sourense \"A\"",
            11: "Sc Povoense"
        },
        "jogos_j1": [(1,2,1,0), (3,4,0,1), (5,6,0,1), (7,8,0,1), (9,10,0,1)],
        "jogos_sem_resultado": [
            (2, 6, 3), (2, 11, 9), (2, 8, 5), (2, 10, 1), (2, 2, 7),
            (3, 1, 11), (3, 5, 2), (3, 7, 10), (3, 4, 6), (3, 3, 8),
            (4, 10, 5), (4, 11, 7), (4, 9, 1), (4, 8, 4), (4, 2, 3),
            (5, 5, 11), (5, 4, 2), (5, 3, 10), (5, 7, 9), (5, 6, 8),
            (6, 9, 5), (6, 1, 7), (6, 10, 4), (6, 2, 6), (6, 11, 3),
            (7, 4, 11), (7, 8, 2), (7, 6, 10), (7, 3, 9), (7, 5, 1),
            (8, 7, 5), (8, 9, 4), (8, 11, 6), (8, 10, 8), (8, 1, 3),
            (9, 8, 11), (9, 2, 10), (9, 6, 9), (9, 3, 7), (9, 4, 1),
            (10, 11, 2), (10, 7, 4), (10, 1, 6), (10, 9, 8), (10, 5, 3),
            (11, 4, 5), (11, 10, 11), (11, 2, 9), (11, 6, 7), (11, 8, 1)
        ]
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
        "jogos_j1": [(1,2,1,0), (3,4,0,1), (5,6,1,0), (7,8,0,0), (9,10,0,1), (11,12,1,0)],
        "jogos_sem_resultado": [
            (2, 2, 5), (2, 8, 3), (2, 6, 9), (2, 10, 11), (2, 12, 7), (2, 4, 1),
            (3, 3, 12), (3, 9, 2), (3, 1, 5), (3, 7, 10), (3, 11, 6), (3, 4, 8),
            (4, 10, 3), (4, 5, 9), (4, 12, 4), (4, 8, 1), (4, 2, 11), (4, 6, 7),
            (5, 8, 12), (5, 1, 9), (5, 7, 2), (5, 11, 5), (5, 4, 10), (5, 3, 6),
            (6, 2, 3), (6, 6, 4), (6, 12, 1), (6, 9, 11), (6, 5, 7), (6, 10, 8),
            (7, 7, 9), (7, 4, 2), (7, 3, 5), (7, 12, 10), (7, 1, 11), (7, 8, 6),
            (8, 9, 3), (8, 6, 12), (8, 5, 4), (8, 10, 1), (8, 11, 7), (8, 2, 8),
            (9, 4, 9), (9, 12, 2), (9, 8, 5), (9, 3, 11), (9, 10, 6), (9, 1, 7),
            (10, 7, 3), (10, 5, 12), (10, 11, 4), (10, 2, 10), (10, 1, 6), (10, 9, 8),
            (11, 12, 9), (11, 6, 2), (11, 10, 5), (11, 3, 1), (11, 8, 11), (11, 4, 7)
        ]
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
            
        for j_num, c, f in info["jogos_sem_resultado"]:
            s.adicionar_jogo(j_num, c, f)
            
        g.series[nome_s] = s
    gestor_dados.guardar_dados(g)
    return g

def precisa_reinstalar(dados):
    if dados is None or not dados.series or len(dados.series) < 4:
        return True
    for s in dados.series.values():
        jornadas = set(j.jornada for j in s.jogos)
        if max(jornadas, default=0) < 11:
            return True
    return False

# Carregamento seguro na memória de sessão
if "campeonato" not in st.session_state or precisa_reinstalar(st.session_state.get("campeonato")):
    dados = gestor_dados.carregar_dados()
    if precisa_reinstalar(dados):
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
        with st.expander("🛠️ ÁREA ADMIN: Gestão de Jogos & Guia de Equipas", expanded=False):
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.write(f"**Equipas da {serie_sel}:**")
                for num, eq in sorted(s_obj.equipas.items()):
                    st.text(f"Nº {num}: {eq.nome}")
            
            with col_b:
                tab_add, tab_edit = st.tabs(["➕ Adicionar Jogo", "✏️ Alterar / Eliminar Jogo"])
                
                with tab_add:
                    num_casa = st.number_input("Nº Equipa Casa", min_value=1, max_value=20, value=1, key="ncasa")
                    num_fora = st.number_input("Nº Equipa Fora", min_value=1, max_value=20, value=2, key="nfora")
                    jornada_in = st.number_input("Jornada", min_value=1, max_value=30, value=12, key="jornada_in")
                    
                    if st.button("Agendar Jogo"):
                        if num_casa in s_obj.equipas and num_fora in s_obj.equipas:
                            s_obj.adicionar_jogo(int(jornada_in), int(num_casa), int(num_fora))
                            gestor_dados.guardar_dados(campeonato)
                            st.success(f"Jogo da Jornada {jornada_in} agendado!")
                            st.rerun()
                        else:
                            st.error("Número de equipa inválido para esta série.")
                            
                with tab_edit:
                    if not s_obj.jogos:
                        st.info("Não existem jogos para editar nesta série.")
                    else:
                        opcoes_jogos = {
                            f"J{j.jornada}: {s_obj.equipas.get(j.equipa_casa, Jogo(0,0,0)).nome} vs {s_obj.equipas.get(j.equipa_fora, Jogo(0,0,0)).nome}": idx
                            for idx, j in enumerate(s_obj.jogos)
                        }
                        jogo_sel_label = st.selectbox("Escolher Jogo a Alterar", list(opcoes_jogos.keys()))
                        jogo_idx = opcoes_jogos[jogo_sel_label]
                        jogo_alvo = s_obj.jogos[jogo_idx]
                        
                        nova_jornada = st.number_input("Nova Jornada", min_value=1, max_value=30, value=int(jogo_alvo.jornada), key="edit_jornada")
                        
                        equipas_dict = {f"Nº {num}: {eq.nome}": num for num, eq in sorted(s_obj.equipas.items())}
                        labels_equipas = list(equipas_dict.keys())
                        
                        idx_c_default = list(s_obj.equipas.keys()).index(jogo_alvo.equipa_casa) if jogo_alvo.equipa_casa in s_obj.equipas else 0
                        idx_f_default = list(s_obj.equipas.keys()).index(jogo_alvo.equipa_fora) if jogo_alvo.equipa_fora in s_obj.equipas else 0
                        
                        nova_casa_label = st.selectbox("Nova Equipa Casa", labels_equipas, index=idx_c_default, key="edit_casa")
                        nova_fora_label = st.selectbox("Nova Equipa Fora", labels_equipas, index=idx_f_default, key="edit_fora")
                        
                        col_bt1, col_bt2 = st.columns([1, 1])
                        with col_bt1:
                            if st.button("Guardar Alterações do Jogo"):
                                jogo_alvo.jornada = int(nova_jornada)
                                jogo_alvo.equipa_casa = equipas_dict[nova_casa_label]
                                jogo_alvo.equipa_fora = equipas_dict[nova_fora_label]
                                gestor_dados.guardar_dados(campeonato)
                                st.success("Jogo alterado com sucesso!")
                                st.rerun()
                        with col_bt2:
                            if st.button("🗑️ Eliminar Jogo"):
                                s_obj.jogos.pop(jogo_idx)
                                gestor_dados.guardar_dados(campeonato)
                                st.success("Jogo eliminado!")
                                st.rerun()

    # Visualização e Lançamento de Resultados com nova largura de colunas (1 vs 1.45)
    col1, col2 = st.columns([1, 1.45])
    
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
                
                # Cartão Visual de Destaque da Jornada
                st.markdown(
                    f"""
                    <div style="
                        background-color: #1e293b;
                        color: #ffffff;
                        padding: 10px 14px;
                        border-radius: 8px;
                        border-left: 5px solid #00d47e;
                        margin-bottom: 8px;
                        font-size: 15px;
                        font-weight: 600;
                    ">
                        ⚽ Jornada {jogo.jornada}: {nome_c} <span style="color: #94a3b8; font-weight: 400;">vs</span> {nome_f}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
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
            st.dataframe(
                df_classif,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Equipa": st.column_config.TextColumn("Equipa", width="large"),
                    "Pts": st.column_config.NumberColumn("Pts", width="small"),
                    "J": st.column_config.NumberColumn("J", width="small"),
                    "V": st.column_config.NumberColumn("V", width="small"),
                    "E": st.column_config.NumberColumn("E", width="small"),
                    "D": st.column_config.NumberColumn("D", width="small"),
                }
            )
        else:
            st.info("Sem equipas registadas.")