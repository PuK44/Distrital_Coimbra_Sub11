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

# Inicialização do Gestor de Dados
gestor_dados = GestorDados()
st.session_state["gestor_dados"] = gestor_dados

# --- FUNÇÕES AUXILIARES DE SEGURANÇA (Detetam atributos dinamicamente) ---

def obter_jogos_serie(s):
    """Obtém a lista de jogos de uma Serie de forma segura."""
    # 1. Procura atributos conhecidos
    for attr in ["jogos", "lista_jogos", "jogos_lista", "calendario", "partidas"]:
        if hasattr(s, attr):
            val = getattr(s, attr)
            if isinstance(val, list):
                return val
            elif isinstance(val, dict):
                return list(val.values())
    
    # 2. Se não encontrou, procura qualquer lista no objeto (exceto equipas)
    for k, v in getattr(s, "__dict__", {}).items():
        if k != "equipas":
            if isinstance(v, list):
                return v
            elif isinstance(v, dict):
                return list(v.values())
                
    # 3. Se nada existir, cria o atributo 'jogos'
    s.jogos = []
    return s.jogos

def obter_ids_equipas(jogo):
    """Obtém os IDs das equipas da casa e fora de um jogo."""
    c = getattr(jogo, "equipa_casa", getattr(jogo, "id_casa", getattr(jogo, "casa", None)))
    f = getattr(jogo, "equipa_fora", getattr(jogo, "id_fora", getattr(jogo, "fora", None)))
    return c, f

def obter_jornada(jogo):
    """Obtém a jornada do jogo."""
    return getattr(jogo, "jornada", 1)

def obter_resultado_str(jogo):
    """Retorna o resultado em texto ('1 - 0', '0 - 0', '0 - 1' ou 'Por jogar')."""
    realizado = getattr(jogo, "realizado", getattr(jogo, "concluido", False))
    if realizado:
        gc = getattr(jogo, "golo_casa", getattr(jogo, "golos_casa", 0))
        gf = getattr(jogo, "golo_fora", getattr(jogo, "golos_fora", 0))
        return f"{gc} - {gf}"
    return "Por jogar"

def definir_resultado_jogo(jogo, gc, gf):
    """Define o resultado no objeto Jogo."""
    if hasattr(jogo, "definir_resultado") and callable(getattr(jogo, "definir_resultado")):
        try:
            jogo.definir_resultado(gc, gf)
            return
        except Exception:
            pass
            
    # Se não houver método, atribui diretamente nos atributos
    if hasattr(jogo, "golo_casa"): jogo.golo_casa = gc
    elif hasattr(jogo, "golos_casa"): jogo.golos_casa = gc
    
    if hasattr(jogo, "golo_fora"): jogo.golo_fora = gf
    elif hasattr(jogo, "golos_fora"): jogo.golos_fora = gf
    
    if hasattr(jogo, "realizado"): jogo.realizado = True
    elif hasattr(jogo, "concluido"): jogo.concluido = True

def limpar_resultado_jogo(jogo):
    """Marca o jogo como 'Por jogar'."""
    if hasattr(jogo, "realizado"): jogo.realizado = False
    elif hasattr(jogo, "concluido"): jogo.concluido = False
    
    if hasattr(jogo, "golo_casa"): jogo.golo_casa = 0
    if hasattr(jogo, "golo_fora"): jogo.golo_fora = 0


# --- DADOS PRÉ-CARREGADOS DAS 4 SÉRIES ---

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

def inicializar_campeonato():
    g = GestorCampeonato()
    dict_series = getattr(g, "series", getattr(g, "fase1_series", {}))
    if not dict_series:
        g.series = {}
        dict_series = g.series
        
    for nome_s, info in DADOS_INICIAIS.items():
        s = Serie(nome_s)
        for num, eq in info["equipas"].items():
            s.adicionar_equipa(num, eq)
        
        for c, f, gc, gf in info["jogos_j1"]:
            s.adicionar_jogo(1, c, f)
            lista_j = obter_jogos_serie(s)
            if lista_j:
                definir_resultado_jogo(lista_j[-1], gc, gf)
                
        dict_series[nome_s] = s
    
    gestor_dados.guardar_dados(g)
    return g

# Carregamento seguro
g_existente = None
try:
    g_existente = gestor_dados.carregar_dados()
except Exception:
    g_existente = None

dict_series_exist = getattr(g_existente, "series", getattr(g_existente, "fase1_series", {})) if g_existente else {}

if g_existente is None or not dict_series_exist or len(dict_series_exist) < 4:
    st.session_state["campeonato"] = inicializar_campeonato()
else:
    st.session_state["campeonato"] = g_existente

gestor = st.session_state["campeonato"]
dict_series_ativas = getattr(gestor, "series", getattr(gestor, "fase1_series", {}))

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
    
    series_list = list(dict_series_ativas.keys())
    serie_ativa = st.selectbox("Selecionar Série", series_list)
    s_ativa = dict_series_ativas[serie_ativa]

    # Painel do Admin para consultar números e agendar jogos
    if e_admin:
        with st.expander("🛠️ ÁREA ADMIN: Guia de Números das Equipas & Criar Jogos", expanded=True):
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.write(f"**Equipas Registadas na {serie_ativa}:**")
                for num, eq in sorted(s_ativa.equipas.items()):
                    nome_eq = getattr(eq, "nome", str(eq))
                    st.text(f"Nº {num}: {nome_eq}")
            
            with col_b:
                st.write("**Agendar Novo Jogo:**")
                num_casa = st.number_input("Nº Equipa Casa", min_value=1, max_value=20, value=1, key="ncasa")
                num_fora = st.number_input("Nº Equipa Fora", min_value=1, max_value=20, value=2, key="nfora")
                jornada_in = st.number_input("Jornada", min_value=1, max_value=30, value=2, key="jornada_in")
                
                if st.button("Agendar Jogo"):
                    if num_casa in s_ativa.equipas and num_fora in s_ativa.equipas:
                        s_ativa.adicionar_jogo(int(jornada_in), int(num_casa), int(num_fora))
                        gestor_dados.guardar_dados(gestor)
                        st.success(f"Jogo da Jornada {jornada_in} adicionado!")
                        st.rerun()
                    else:
                        st.error("Número de equipa inválido para esta série.")

    # Exibição de Jogos e Classificação
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🗓️ Jogos & Resultados")
        
        lista_jogos_s = obter_jogos_serie(s_ativa)
        jornadas_existentes = sorted(list(set(obter_jornada(j) for j in lista_jogos_s))) if lista_jogos_s else []
        jornada_sel = st.selectbox("Filtrar por Jornada", jornadas_existentes) if jornadas_existentes else None

        jogos_filtrados = [j for j in lista_jogos_s if obter_jornada(j) == jornada_sel] if jornada_sel else lista_jogos_s

        if not jogos_filtrados:
            st.info("Nenhum jogo registado.")
        else:
            for idx, jogo in enumerate(jogos_filtrados):
                c_id, f_id = obter_ids_equipas(jogo)
                eq_c = s_ativa.equipas.get(c_id)
                eq_f = s_ativa.equipas.get(f_id)
                
                nome_c = getattr(eq_c, "nome", f"Equipa {c_id}") if eq_c else f"Equipa {c_id}"
                nome_f = getattr(eq_f, "nome", f"Equipa {f_id}") if eq_f else f"Equipa {f_id}"
                j_num = obter_jornada(jogo)
                
                st.write(f"**Jornada {j_num}:** {nome_c} vs {nome_f}")
                
                res_atual = obter_resultado_str(jogo)
                opcoes_res = ["Por jogar", "1 - 0", "0 - 0", "0 - 1"]
                idx_default = opcoes_res.index(res_atual) if res_atual in opcoes_res else 0
                
                novo_res = st.selectbox(
                    f"Resultado Jogo {idx+1}",
                    opcoes_res,
                    index=idx_default,
                    key=f"res_{serie_ativa}_{j_num}_{idx}"
                )
                
                if st.button(f"Guardar Resultado (Jogo {idx+1})", key=f"btn_{serie_ativa}_{j_num}_{idx}"):
                    if novo_res == "Por jogar":
                        limpar_resultado_jogo(jogo)
                    else:
                        gc, gf = map(int, novo_res.split(" - "))
                        definir_resultado_jogo(jogo, gc, gf)
                    
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