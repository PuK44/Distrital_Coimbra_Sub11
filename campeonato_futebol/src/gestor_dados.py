import json
import os
from src.modelos import GestorCampeonato

class GestorDados:
    def __init__(self, caminho_ficheiro="dados_campeonato.json"):
        self.caminho_ficheiro = caminho_ficheiro

    def guardar_dados(self, campeonato: GestorCampeonato):
        try:
            with open(self.caminho_ficheiro, "w", encoding="utf-8") as f:
                json.dump(campeonato.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao guardar dados: {e}")

    def carregar_dados() -> GestorCampeonato:
        if not os.path.exists(self.caminho_ficheiro):
            return None
        try:
            with open(self.caminho_ficheiro, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return GestorCampeonato.from_dict(dados)
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return None