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

# Plantel do CD Lousanense Sub11
PLANTEL_LOUSANENSE = [
    {"nome": "Vitória Madeira", "posicao": "GR"},
    {"nome": "Vasco Santos", "posicao": "GR"},
    {"nome": "Valentim", "posicao": "GR"},
    {"nome": "Martim Simões", "posicao": "Defesa"},
    {"nome": "David Matos", "posicao": "Defesa"},
    {"nome": "João Duarte", "posicao": "Defesa"},
    {"nome": "Ricardo Rosa", "posicao": "Médio"},
    {"nome": "Gonçalo Paiva", "posicao": "Médio"},
    {"nome": "Tomás Vaz", "posicao": "Médio"},
    {"nome": "Simão Rodrigues", "posicao": "Médio"},
    {"nome": "Lourenço Santos", "posicao": "Ala"},
    {"nome": "Gonçalo Ferreira", "posicao": "Ala"},
    {"nome": "Gonçalo Barata", "posicao": "Ala"},
    {"nome": "Isaac Fonseca", "posicao": "Avançado"},
    {"nome": "Elias Soares", "posicao": "Avançado"},
    {"nome": "Maria Nunes", "posicao": "Avançado"},
]

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
if not hasattr(campeonato, "fichas_lousanense"):
    campeonato.fichas_lousanense = {}

st.title("⚽ Troféu Distrital Coimbra - Sub11")

# Sidebar - Painel de Acesso Admin
st.sidebar.header("⚙️ Definições & Acesso")
senha_admin = st.sidebar.text_input("Palavra-passe Admin", type="password")
e_admin = (senha_admin == "admin123")

if e_admin:
    st.sidebar.success("Modo Admin Ativo")
else:
    st.sidebar.info("Modo Visitante (Consulta de resultados)")

# Separadores Principais
tab_fase1, tab_fase2, tab_lousanense = st.tabs(["Primeira Fase", "Segunda Fase", "CD Lousanense"])

# ==================== ABA 1: PRIMEIRA FASE ====================
with tab_fase1:
    st.header("Primeira Fase")
    
    series_nomes = list(campeonato.series.keys())
    serie_sel = st.selectbox("Selecionar Série", series_nomes)
    s_obj = campeonato.series[serie_sel]

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

    col1, col_espaco, col2 = st.columns([1.1, 0.15, 0.95])
    
    with col1:
        st.subheader("🗓️ Jogos & Resultados")
        
        jornadas_existentes = sorted(list(set(j.jornada for j in s_obj.jogos))) if s_obj.jogos else []
        
        if jornadas_existentes:
            col_f1, col_f2 = st.columns([1, 1])
            with col_f1:
                jornada_filtro = st.selectbox("Filtrar por Jornada", jornadas_existentes)
        else:
            jornada_filtro = None

        jogos_exibir = [j for j in s_obj.jogos if j.jornada == jornada_filtro] if jornada_filtro else s_obj.jogos

        if not jogos_exibir:
            st.info("Nenhum jogo agendado.")
        else:
            for idx, jogo in enumerate(jogos_exibir):
                eq_c = s_obj.equipas.get(jogo.equipa_casa)
                eq_f = s_obj.equipas.get(jogo.equipa_fora)
                
                nome_c = eq_c.nome if eq_c else f"Equipa {jogo.equipa_casa}"
                nome_f = eq_f.nome if eq_f else f"Equipa {jogo.equipa_fora}"
                
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
                
                res_texto = f"{jogo.golo_casa} - {jogo.golo_fora}" if jogo.realizado else "Por jogar"
                
                if e_admin:
                    col_r1, col_r2 = st.columns([1, 1])
                    with col_r1:
                        opcoes_res = ["Por jogar", "1 - 0", "0 - 0", "0 - 1"]
                        idx_default = opcoes_res.index(res_texto) if res_texto in opcoes_res else 0
                        
                        novo_res = st.selectbox(
                            f"Resultado (Jogo {idx+1})",
                            opcoes_res,
                            index=idx_default,
                            key=f"res_{serie_sel}_{jogo.jornada}_{idx}"
                        )
                        
                        if st.button(f"Guardar Resultado", key=f"btn_{serie_sel}_{jogo.jornada}_{idx}"):
                            if novo_res == "Por jogar":
                                jogo.realizado = False
                                jogo.golo_casa = 0
                                jogo.golo_fora = 0
                            else:
                                gc, gf = map(int, novo_res.split(" - "))
                                jogo.definir_resultado(gc, gf)
                            
                            gestor_dados.guardar_dados(campeonato)
                            st.success("Resultado guardado!")
                            st.rerun()
                else:
                    cor_status = "#00d47e" if jogo.realizado else "#94a3b8"
                    st.markdown(
                        f"""
                        <div style="margin-top: -2px; margin-bottom: 12px; padding-left: 4px; font-size: 14px;">
                            <span style="color: #94a3b8;">Resultado:</span> 
                            <strong style="color: {cor_status}; font-size: 15px;">{res_texto}</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
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
                    "Equipa": st.column_config.TextColumn("Equipa", width="medium"),
                    "Pts": st.column_config.NumberColumn("Pts", width="small"),
                    "J": st.column_config.NumberColumn("J", width="small"),
                    "V": st.column_config.NumberColumn("V", width="small"),
                    "E": st.column_config.NumberColumn("E", width="small"),
                    "D": st.column_config.NumberColumn("D", width="small"),
                }
            )
        else:
            st.info("Sem equipas registadas.")


# ==================== ABA 3: CD LOUSANENSE ====================
with tab_lousanense:
    st.header("🔴⚪ CD Lousanense - Estatísticas de Jogadores & Resultados Reais")

    # Obter os jogos do Cd Lousanense na Série A (Lousanense é ID 1)
    serie_a = campeonato.series.get("SÉRIE A")
    jogos_lousanense = []
    if serie_a:
        for j in sorted(serie_a.jogos, key=lambda x: x.jornada):
            if j.equipa_casa == 1 or j.equipa_fora == 1:
                eq_casa = serie_a.equipas.get(j.equipa_casa)
                eq_fora = serie_a.equipas.get(j.equipa_fora)
                nome_c = eq_casa.nome if eq_casa else f"Equipa {j.equipa_casa}"
                nome_f = eq_fora.nome if eq_fora else f"Equipa {j.equipa_fora}"
                jogos_lousanense.append((j.jornada, nome_c, nome_f, j.equipa_casa == 1))

    col_stats, col_espaco_l, col_ficha = st.columns([1.1, 0.15, 0.95])

    # --- COLUNA DA ESQUERDA: TABELA DE JOGADORES (JOGOS, GOLOS & ASSISTÊNCIAS) ---
    with col_stats:
        st.subheader("📊 Tabela de Jogadores")

        # Inicializa a contagem dos atletas
        stats_jogadores = {p["nome"]: {"Posição": p["posicao"], "Jogos": 0, "Golos": 0, "Assistências": 0} for p in PLANTEL_LOUSANENSE}

        # Agrega presenças, golos e assistências de todas as fichas guardadas
        for j_str, ficha in campeonato.fichas_lousanense.items():
            # Contagem de Jogos
            for jog in ficha.get("convocados", []):
                if jog in stats_jogadores:
                    stats_jogadores[jog]["Jogos"] += 1

            # Contagem de Golos e Assistências
            for golo in ficha.get("detalhes", []):
                autor = golo.get("autor")
                assist = golo.get("assistencia")

                if autor in stats_jogadores:
                    stats_jogadores[autor]["Golos"] += 1
                if assist in stats_jogadores:
                    stats_jogadores[assist]["Assistências"] += 1

        lista_stats = []
        for nome_p, datos in stats_jogadores.items():
            lista_stats.append({
                "Jogador": nome_p,
                "Posição": datos["Posição"],
                "Jogos": datos["Jogos"],
                "Golos": datos["Golos"],
                "Assistências": datos["Assistências"]
            })

        df_jogadores = pd.DataFrame(lista_stats)
        df_jogadores = df_jogadores.sort_values(by=["Golos", "Assistências", "Jogos", "Jogador"], ascending=[False, False, False, True])

        st.dataframe(
            df_jogadores,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Jogador": st.column_config.TextColumn("Jogador", width="medium"),
                "Posição": st.column_config.TextColumn("Posição", width="small"),
                "Jogos": st.column_config.NumberColumn("👕 Jogos", width="small"),
                "Golos": st.column_config.NumberColumn("⚽ Golos", width="small"),
                "Assistências": st.column_config.NumberColumn("👟 Assistências", width="small"),
            }
        )

    # --- COLUNA DA DIREITA: FICHA DE JOGO / RESULTADO REAL ---
    with col_ficha:
        st.subheader("📝 Ficha de Jogo (Resultados Reais)")

        if not jogos_lousanense:
            st.info("Nenhum jogo do CD Lousanense encontrado na Série A.")
        else:
            opcoes_j_lous = {
                f"Jornada {j_num}: {c_nome} vs {f_nome}": (j_num, c_nome, f_nome, e_casa)
                for j_num, c_nome, f_nome, e_casa in jogos_lousanense
            }

            col_sel1, _ = st.columns([1, 1])
            with col_sel1:
                sel_jogo_label = st.selectbox("Selecionar Jogo", list(opcoes_j_lous.keys()))

            j_num_sel, c_nome_sel, f_nome_sel, e_casa_sel = opcoes_j_lous[sel_jogo_label]
            j_str_key = str(j_num_sel)

            ficha_atual = campeonato.fichas_lousanense.get(j_str_key, {})

            # PAINEL DO ADMINISTRADOR (Lançamento da ficha, convocados e marcadores)
            if e_admin:
                st.markdown("##### 🛠️ Lançar / Alterar Ficha de Jogo")
                
                col_g1, col_g2 = st.columns([1, 1])
                with col_g1:
                    g_marcados = st.number_input(
                        f"Golos do CD Lousanense",
                        min_value=0, max_value=20,
                        value=int(ficha_atual.get("golos_marcados", 0)),
                        key=f"gm_{j_str_key}"
                    )
                with col_g2:
                    g_sofridos = st.number_input(
                        f"Golos Sofridos",
                        min_value=0, max_value=20,
                        value=int(ficha_atual.get("golos_sofridos", 0)),
                        key=f"gs_{j_str_key}"
                    )

                # Seleção dos Jogadores que Jogaram
                st.write("**Jogadores Utilizados neste Jogo:**")
                nomes_jogadores_lista = [p["nome"] for p in PLANTEL_LOUSANENSE]
                convocados_antigos = ficha_atual.get("convocados", [])
                
                jogadores_utilizados = st.multiselect(
                    "Seleciona os atletas que jogaram:",
                    options=nomes_jogadores_lista,
                    default=[j for j in convocados_antigos if j in nomes_jogadores_lista],
                    key=f"conv_{j_str_key}"
                )

                detalhes_input = []
                if g_marcados > 0:
                    st.write("**Marcadores e Assistências dos Golos:**")
                    detalhes_antigos = ficha_atual.get("detalhes", [])

                    for i in range(int(g_marcados)):
                        st.caption(f"⚽ Golo {i+1} do CD Lousanense:")
                        col_m1, col_m2 = st.columns([1, 1])

                        def_autor = detalhes_antigos[i]["autor"] if i < len(detalhes_antigos) else nomes_jogadores_lista[0]
                        def_assist = detalhes_antigos[i]["assistencia"] if i < len(detalhes_antigos) else "Sem assistência"

                        opcoes_autor = nomes_jogadores_lista + ["Auto-golo"]
                        opcoes_assist = ["Sem assistência"] + nomes_jogadores_lista

                        idx_aut = opcoes_autor.index(def_autor) if def_autor in opcoes_autor else 0
                        idx_ass = opcoes_assist.index(def_assist) if def_assist in opcoes_assist else 0

                        with col_m1:
                            autor_sel = st.selectbox(f"Marcador #{i+1}", opcoes_autor, index=idx_aut, key=f"aut_{j_str_key}_{i}")
                        with col_m2:
                            assist_sel = st.selectbox(f"Assistência #{i+1}", opcoes_assist, index=idx_ass, key=f"ass_{j_str_key}_{i}")

                        detalhes_input.append({"autor": autor_sel, "assistencia": assist_sel})

                if st.button("Guardar Ficha de Jogo", key=f"btn_ficha_{j_str_key}"):
                    campeonato.fichas_lousanense[j_str_key] = {
                        "jornada": j_num_sel,
                        "golos_marcados": int(g_marcados),
                        "golos_sofridos": int(g_sofridos),
                        "convocados": jogadores_utilizados,
                        "detalhes": detalhes_input
                    }
                    gestor_dados.guardar_dados(campeonato)
                    st.success("Ficha de jogo guardada e estatísticas atualizadas!")
                    st.rerun()

            # VISUALIZAÇÃO PARA VISITANTES (E resumo para o Admin)
            if ficha_atual:
                st.markdown("---")
                st.markdown(
                    f"""
                    <div style="
                        background-color: #1e293b;
                        color: #ffffff;
                        padding: 12px 16px;
                        border-radius: 8px;
                        border-left: 5px solid #00d47e;
                        margin-bottom: 12px;
                        font-size: 16px;
                        font-weight: 600;
                    ">
                        🔴⚪ Resultado Real (Jornada {j_num_sel}):<br>
                        <span style="color: #00d47e; font-size: 20px;">
                            {c_nome_sel} {ficha_atual['golos_marcados'] if e_casa_sel else ficha_atual['golos_sofridos']} - {ficha_atual['golos_sofridos'] if e_casa_sel else ficha_atual['golos_marcados']} {f_nome_sel}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                conv_gravados = ficha_atual.get("convocados", [])
                if conv_gravados:
                    st.write(f"**👕 Jogadores Utilizados ({len(conv_gravados)}):**")
                    st.text(", ".join(conv_gravados))

                detalhes_gravados = ficha_atual.get("detalhes", [])
                if detalhes_gravados:
                    st.write("**Resumo dos Golos do CD Lousanense:**")
                    for idx_g, g_info in enumerate(detalhes_gravados):
                        aut = g_info.get("autor")
                        ass = g_info.get("assistencia")
                        txt_ass = f" *(Assistência: {ass})*" if ass != "Sem assistência" else " *(Sem assistência)*"
                        st.markdown(f"- ⚽ **Golo {idx_g+1}:** {aut}{txt_ass}")
            else:
                st.info("Ficha de jogo ainda não preenchida para esta jornada.")