import json
import os
import requests
import streamlit as st
from src.modelos import GestorCampeonato

class GestorDados:
    def __init__(self, ficheiro_local="dados_campeonato.json"):
        self.ficheiro_local = ficheiro_local
        self.token = st.secrets.get("GITHUB_TOKEN", None)
        self.repo = st.secrets.get("GITHUB_REPO", None)
        self.caminho_github = "campeonato_futebol/dados_campeonato.json"

    def carregar_dados(self) -> GestorCampeonato:
        # Tenta carregar primeiro a partir do GitHub via API se configurado
        if self.token and self.repo:
            url = f"https://raw.githubusercontent.com/{self.repo}/main/{self.caminho_github}"
            headers = {"Authorization": f"token {self.token}"}
            try:
                res = requests.get(url, headers=headers)
                if res.status_code == 200:
                    dados = json.loads(res.text)
                    return GestorCampeonato.from_dict(dados)
            except Exception as e:
                st.warning(f"Aviso: Não foi possível carregar do GitHub ({e}). Tentando ficheiro local.")

        # Fallback para ficheiro local
        if os.path.exists(self.ficheiro_local):
            try:
                with open(self.ficheiro_local, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    return GestorCampeonato.from_dict(dados)
            except Exception:
                pass

        return None

    def guardar_dados(self, gestor: GestorCampeonato):
        dados_dict = gestor.to_dict()
        conteudo_json = json.dumps(dados_dict, indent=4, ensure_ascii=False)

        # 1. Guarda localmente
        with open(self.ficheiro_local, "w", encoding="utf-8") as f:
            f.write(conteudo_json)

        # 2. Faz o commit automático no GitHub via API
        if self.token and self.repo:
            url_api = f"https://api.github.com/repos/{self.repo}/contents/{self.caminho_github}"
            headers = {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json"
            }

            try:
                # Obter o SHA do ficheiro atual para poder atualizar
                get_res = requests.get(url_api, headers=headers)
                sha = get_res.json().get("sha") if get_res.status_code == 200 else None

                import base64
                conteudo_b64 = base64.b64encode(conteudo_json.encode("utf-8")).decode("utf-8")

                payload = {
                    "message": "Update dados_campeonato.json via Streamlit App",
                    "content": conteudo_b64,
                    "branch": "main"
                }
                if sha:
                    payload["sha"] = sha

                requests.put(url_api, headers=headers, json=payload)
            except Exception as e:
                st.error(f"Erro ao guardar no GitHub: {e}")