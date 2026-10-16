from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple


@dataclass
class Equipa:
    numero: int
    nome: str
    jogos: int = 0
    vitorias: int = 0
    empates: int = 0
    derrotas: int = 0
    pontos: int = 0

    def reset_estatisticas(self):
        """Reinicia os pontos e estatísticas da equipa."""
        self.jogos = 0
        self.vitorias = 0
        self.empates = 0
        self.derrotas = 0
        self.pontos = 0


@dataclass
class Jogo:
    num_casa: int
    num_fora: int
    # Resultado pode ser '1-0' (Vitória Casa), '0-0' (Empate), '0-1' (Vitória Fora) ou None (não jogado)
    resultado: Optional[str] = None

    def obter_pontos(self) -> Tuple[int, int]:
        """
        Retorna os pontos atribuídos (pontos_casa, pontos_fora) com base no resultado.
        Vitória = 3 pts, Empate = 1 pt, Derrota = 0 pt.
        """
        if self.resultado == "1-0":
            return 3, 0
        elif self.resultado == "0-0":
            return 1, 1
        elif self.resultado == "0-1":
            return 0, 3
        return 0, 0


class Serie:
    def __init__(self, nome: str):
        self.nome = nome
        self.equipas: Dict[int, Equipa] = {}  # Mapeia numero_equipa -> Objeto Equipa
        self.jornadas: Dict[int, List[Jogo]] = {}  # Mapeia numero_jornada -> Lista de Jogos

    def adicionar_equipa(self, numero: int, nome: str) -> bool:
        """Adiciona uma equipa à série registando o seu número."""
        if numero in self.equipas:
            return False  # Número já atribuído nesta série
        self.equipas[numero] = Equipa(numero=numero, nome=nome)
        return True

    def adicionar_jogo(self, jornada: int, num_casa: int, num_fora: int) -> bool:
        """Adiciona um jogo manual a uma jornada através do número das equipas."""
        if num_casa not in self.equipas or num_fora not in self.equipas:
            return False  # Alguma das equipas não existe na série
        
        if jornada not in self.jornadas:
            self.jornadas[jornada] = []
            
        self.jornadas[jornada].append(Jogo(num_casa=num_casa, num_fora=num_fora))
        return True

    def registar_resultado(self, jornada: int, indice_jogo: int, resultado: str) -> bool:
        """Atualiza o resultado de um jogo específico de uma jornada ('1-0', '0-0' ou '0-1')."""
        if resultado not in ["1-0", "0-0", "0-1"]:
            return False
            
        if jornada in self.jornadas and 0 <= indice_jogo < len(self.jornadas[jornada]):
            self.jornadas[jornada][indice_jogo].resultado = resultado
            return True
        return False

    def calcular_classificacao(self) -> List[Equipa]:
        """Recalcula a tabela de classificação de toda a série."""
        # 1. Reset às estatísticas de todas as equipas
        for equipa in self.equipas.values():
            equipa.reset_estatisticas()

        # 2. Processar todos os jogos com resultado definido
        for jogos in self.jornadas.values():
            for jogo in jogos:
                if jogo.resultado:
                    eq_casa = self.equipas[jogo.num_casa]
                    eq_fora = self.equipas[jogo.num_fora]
                    pts_casa, pts_fora = jogo.obter_pontos()

                    # Atualizar jogos efetuados
                    eq_casa.jogos += 1
                    eq_fora.jogos += 1

                    # Atribuir pontos e registar V/E/D
                    eq_casa.pontos += pts_casa
                    eq_fora.pontos += pts_fora

                    if pts_casa == 3:
                        eq_casa.vitorias += 1
                        eq_fora.derrotas += 1
                    elif pts_fora == 3:
                        eq_fora.vitorias += 1
                        eq_casa.derrotas += 1
                    else:
                        eq_casa.empates += 1
                        eq_fora.empates += 1

        # 3. Ordenar tabela por Pontos (descendente) e Número da Equipa (ascendente como desempate)
        tabela = list(self.equipas.values())
        tabela.sort(key=lambda eq: (-eq.pontos, eq.numero))
        return tabela


class GestorCampeonato:
    def __init__(self):
        self.series_fase1: Dict[str, Serie] = {}
        self.series_fase2: Dict[str, Serie] = {}

    def gerar_fase2(self, vagas_por_grupo: int) -> bool:
        """
        Gera as séries da Fase 2 com base nas posições finais da Fase 1.
        """
        if not self.series_fase1:
            return False

        classificacoes = {}
        for nome_s, serie in self.series_fase1.items():
            classificacoes[nome_s] = serie.calcular_classificacao()

        self.series_fase2.clear()

        max_equipas = max(len(eqs) for eqs in classificacoes.values()) if classificacoes else 0
        if max_equipas == 0:
            return False

        grupo_idx = 1
        for inicio in range(0, max_equipas, vagas_por_grupo):
            nome_serie_f2 = f"Fase 2 - Grupo {grupo_idx}"
            nova_serie = Serie(nome=nome_serie_f2)

            num_equipa_f2 = 1
            for nome_s1, tabela in classificacoes.items():
                fatia = tabela[inicio:inicio + vagas_por_grupo]
                for eq in fatia:
                    nova_serie.adicionar_equipa(numero=num_equipa_f2, nome=eq.nome)
                    num_equipa_f2 += 1

            if nova_serie.equipas:
                self.series_fase2[nome_serie_f2] = nova_serie
                grupo_idx += 1

        return True