import sys
import os

# Força o Python a incluir a pasta raiz no caminho de procura de módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from src.modelos import GestorCampeonato, Serie
from src.gestor_dados import GestorDados

# Configuração da página Web
st.set_page_config(page_title="Gestor de Campeonato de Futebol", layout="wide", page_icon="⚽")

# Inicializar o estado da sessão no Streamlit
if "gestor_dados" not in st.session_state:
    st.session_state.gestor_dados = GestorDados()
    st.session_state.gestor_camp = GestorCampeonato()
    
    # Carregar dados gravados se existirem
    series_carregadas = st.session_state.gestor_dados.carregar_campeonato()
    if series_carregadas:
        st.session_state.gestor_camp.series_fase1 = series_carregadas

def guardar_alteracoes():
    st.session_state.gestor_dados.guardar_campeonato(st.session_state.gestor_camp.series_fase1)

# --- CABEÇALHO ---
st.title("⚽ Gestor de Campeonato de Futebol")
st.markdown("---")

# Separadores principais de navegação
aba_fase1, aba_fase2 = st.tabs(["🏆 Primeira Fase", "🥇 Segunda Fase"])

# ==============================================================================
# SEPARADOR: PRIMEIRA FASE
# ==============================================================================
with aba_fase1:
    col_menu, col_conteudo = st.columns([1, 3])

    with col_menu:
        st.subheader("Gestão de Séries")
        
        # Form de criação de série
        nova_serie_nome = st.text_input("Nome da Nova Série (ex: Série A):")
        if st.button("➕ Criar Série"):
            if nova_serie_nome and nova_serie_nome not in st.session_state.gestor_camp.series_fase1:
                st.session_state.gestor_camp.series_fase1[nova_serie_nome] = Serie(nova_serie_nome)
                guardar_alteracoes()
                st.success(f"{nova_serie_nome} criada com sucesso!")
                st.rerun()

        st.markdown("---")
        
        # Seleção de Série Ativa
        series_disponiveis = list(st.session_state.gestor_camp.series_fase1.keys())
        serie_selecionada = st.selectbox("Selecionar Série:", series_disponiveis if series_disponiveis else ["Nenhuma série criada"])

    with col_conteudo:
        if series_disponiveis and serie_selecionada in st.session_state.gestor_camp.series_fase1:
            serie_atual = st.session_state.gestor_camp.series_fase1[serie_selecionada]
            
            st.header(f"Gestão - {serie_atual.nome}")
            
            # Sub-abas para a série ativa
            sub_tab1, sub_tab2, sub_tab3 = st.tabs(["📝 Adicionar Equipas", "⚔️ Registar Jogos", "📊 Classificação"])

            # 1. Adicionar Equipas
            with sub_tab1:
                st.subheader("Inserção Manual de Equipas")
                col_num, col_nome = st.columns([1, 3])
                with col_num:
                    num_eq = st.number_input("Número da Equipa", min_value=1, step=1)
                with col_nome:
                    nome_eq = st.text_input("Nome da Equipa")
                
                if st.button("Adicionar Equipa"):
                    if nome_eq:
                        sucesso = serie_atual.adicionar_equipa(int(num_eq), nome_eq)
                        if sucesso:
                            guardar_alteracoes()
                            st.success(f"Equipa '{nome_eq}' (Nº {num_eq}) adicionada!")
                            st.rerun()
                        else:
                            st.error("O número desta equipa já se encontra registado nesta série!")

                # Lista de Equipas Existentes
                if serie_atual.equipas:
                    st.markdown("##### Equipas Inscritas:")
                    eq_data = [{"Nº Equipa": eq.numero, "Nome da Equipa": eq.nome} for eq in serie_atual.equipas.values()]
                    st.dataframe(pd.DataFrame(eq_data), use_container_width=True, hide_index=True)

            # 2. Registar Jogos por Número
            with sub_tab2:
                st.subheader("Emparelhamento de Jogos por Número")
                
                jornada_num = st.number_input("Número da Jornada", min_value=1, step=1, value=1)
                
                col_c, col_f, col_r = st.columns([2, 2, 2])
                with col_c:
                    num_casa = st.number_input("Nº Equipa Casa", min_value=1, step=1, key="num_c")
                with col_f:
                    num_fora = st.number_input("Nº Equipa Fora", min_value=1, step=1, key="num_f")
                with col_r:
                    resultado = st.selectbox("Resultado", ["Sem Resultado", "1-0 (Vitória Casa)", "0-0 (Empate)", "0-1 (Vitória Fora)"])

                if st.button("Adicionar / Guardar Jogo"):
                    if num_casa in serie_atual.equipas and num_fora in serie_atual.equipas:
                        # Criar jogo se não existir
                        serie_atual.adicionar_jogo(int(jornada_num), int(num_casa), int(num_fora))
                        
                        # Atualizar resultado
                        res_code = None
                        if "1-0" in resultado: res_code = "1-0"
                        elif "0-0" in resultado: res_code = "0-0"
                        elif "0-1" in resultado: res_code = "0-1"

                        if res_code:
                            # Procurar o jogo criado para atribuir o resultado
                            jogos_jornada = serie_atual.jornadas[int(jornada_num)]
                            for idx, j in enumerate(jogos_jornada):
                                if j.num_casa == int(num_casa) and j.num_fora == int(num_fora):
                                    serie_atual.registar_resultado(int(jornada_num), idx, res_code)
                        
                        guardar_alteracoes()
                        st.success(f"Jogo gravado na Jornada {jornada_num}!")
                        st.rerun()
                    else:
                        st.error("Verifica os números inseridos: uma das equipas não existe nesta série.")

                # Tabela de Jogos Inseridos
                st.markdown(f"##### Jogos da Jornada {jornada_num}:")
                if int(jornada_num) in serie_atual.jornadas:
                    jogos_lista = []
                    for j in serie_atual.jornadas[int(jornada_num)]:
                        nome_casa = serie_atual.equipas[j.num_casa].nome
                        nome_fora = serie_atual.equipas[j.num_fora].nome
                        jogos_lista.append({
                            "Casa": f"[{j.num_casa}] {nome_casa}",
                            "Fora": f"[{j.num_fora}] {nome_fora}",
                            "Resultado": j.resultado if j.resultado else "Pendente"
                        })
                    st.dataframe(pd.DataFrame(jogos_lista), use_container_width=True, hide_index=True)

            # 3. Classificação Atual
            with sub_tab3:
                st.subheader(f"Tabela Classificativa - {serie_atual.nome}")
                tabela = serie_atual.calcular_classificacao()
                if tabela:
                    df_tabela = pd.DataFrame([{
                        "Pos": i + 1,
                        "Nº": eq.numero,
                        "Equipa": eq.nome,
                        "J": eq.jogos,
                        "V": eq.vitorias,
                        "E": eq.empates,
                        "D": eq.derrotas,
                        "Pts": eq.pontos
                    } for i, eq in enumerate(tabela)])
                    st.dataframe(df_tabela, use_container_width=True, hide_index=True)

# ==============================================================================
# SEPARADOR: SEGUNDA FASE
# ==============================================================================
with aba_fase2:
    st.header("Gerar Segunda Fase (Apuramentos)")
    
    col_vagas, col_btn = st.columns([2, 2])
    with col_vagas:
        vagas = st.number_input("Quantas equipas de cada série passam por grupo? (ex: 2 a 2, 3 a 3)", min_value=1, value=2)
    with col_btn:
        st.write("") # Espaçamento
        st.write("")
        if st.button("🔄 Gerar Séries da 2ª Fase"):
            sucesso = st.session_state.gestor_camp.gerar_fase2(int(vagas))
            if sucesso:
                st.success("Segunda Fase gerada com sucesso com base nas classificações da Fase 1!")
            else:
                st.error("Não foi possível gerar a Segunda Fase. Garante que existem séries com equipas na Fase 1.")

    st.markdown("---")
    
    # Exibir séries geradas para a Fase 2
    if st.session_state.gestor_camp.series_fase2:
        for nome_f2, serie_f2 in st.session_state.gestor_camp.series_fase2.items():
            st.subheader(nome_f2)
            eq_f2 = [{"Nº F2": eq.numero, "Equipa Apurada": eq.nome} for eq in serie_f2.equipas.values()]
            st.dataframe(pd.DataFrame(eq_f2), use_container_width=True, hide_index=True)