import json
import os
from typing import Dict
from src.modelos import Serie, Jogo, Equipa


class GestorDados:
    def __init__(self, caminho_ficheiro: str = "dados/campeonato.json"):
        self.caminho_ficheiro = caminho_ficheiro

    def guardar_campeonato(self, series: Dict[str, Serie]) -> bool:
        """Guarda todas as séries, equipas e jogos num ficheiro JSON."""
        # Garantir que a pasta 'dados' existe
        pasta = os.path.dirname(self.caminho_ficheiro)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta)

        dados_exportar = {}

        for nome_serie, serie in series.items():
            dados_serie = {
                "equipas": {
                    num: {"numero": eq.numero, "nome": eq.nome}
                    for num, eq in serie.equipas.items()
                },
                "jornadas": {}
            }

            for num_jornada, jogos in serie.jornadas.items():
                dados_serie["jornadas"][str(num_jornada)] = [
                    {
                        "num_casa": jogo.num_casa,
                        "num_fora": jogo.num_fora,
                        "resultado": jogo.resultado
                    }
                    for jogo in jogos
                ]

            dados_exportar[nome_serie] = dados_serie

        try:
            with open(self.caminho_ficheiro, "w", encoding="utf-8") as f:
                json.dump(dados_exportar, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Erro ao guardar ficheiro: {e}")
            return False

    def carregar_campeonato(self) -> Dict[str, Serie]:
        """Carrega todas as séries a partir do ficheiro JSON."""
        if not os.path.exists(self.caminho_ficheiro):
            return {}

        try:
            with open(self.caminho_ficheiro, "r", encoding="utf-8") as f:
                dados_importados = json.load(f)

            series: Dict[str, Serie] = {}

            for nome_serie, dados_serie in dados_importados.items():
                serie = Serie(nome=nome_serie)

                # Restaurar Equipas
                for num_str, eq_data in dados_serie.get("equipas", {}).items():
                    serie.adicionar_equipa(numero=eq_data["numero"], nome=eq_data["nome"])

                # Restaurar Jornadas e Jogos
                for num_jornada_str, lista_jogos in dados_serie.get("jornadas", {}).items():
                    num_jornada = int(num_jornada_str)
                    for jogo_data in lista_jogos:
                        serie.adicionar_jogo(
                            jornada=num_jornada,
                            num_casa=jogo_data["num_casa"],
                            num_fora=jogo_data["num_fora"]
                        )
                        # Definir resultado se já existir
                        if jogo_data.get("resultado"):
                            indice = len(serie.jornadas[num_jornada]) - 1
                            serie.registar_resultado(
                                jornada=num_jornada,
                                indice_jogo=indice,
                                resultado=jogo_data["resultado"]
                            )

                series[nome_serie] = serie

            return series

        except Exception as e:
            print(f"Erro ao carregar ficheiro: {e}")
            return {}