from datetime import date, timedelta

import pandas as pd

class Equipa:
    def __init__(self, id_num: int, nome: str):
        self.id_num = id_num
        self.nome = nome

    def to_dict(self):
        return {"id_num": self.id_num, "nome": self.nome}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id_num"], data["nome"])


class Jogo:
    def __init__(self, jornada: int, equipa_casa: int, equipa_fora: int, golo_casa: int = 0, golo_fora: int = 0, realizado: bool = False,
                 adiado: bool = False, data_adiamento: str = None, nao_realizado: bool = False):
        self.jornada = jornada
        self.equipa_casa = equipa_casa
        self.equipa_fora = equipa_fora
        self.golo_casa = golo_casa
        self.golo_fora = golo_fora
        self.realizado = realizado
        self.adiado = adiado                    # jogo adiado com data marcada
        self.data_adiamento = data_adiamento    # data ISO "AAAA-MM-DD" (só quando adiado)
        self.nao_realizado = nao_realizado      # não se realizou na data prevista, ainda sem nova data

    def limpar_adiamento(self):
        """Apaga o estado de adiamento / não realizado (jogo resolvido ou reposto)."""
        self.adiado = False
        self.data_adiamento = None
        self.nao_realizado = False

    def definir_resultado(self, golo_casa: int, golo_fora: int):
        self.golo_casa = golo_casa
        self.golo_fora = golo_fora
        self.realizado = True
        self.limpar_adiamento()

    def repor_por_jogar(self):
        self.realizado = False
        self.golo_casa = 0
        self.golo_fora = 0
        self.limpar_adiamento()

    def adiar(self, data_iso: str):
        self.realizado = False
        self.golo_casa = 0
        self.golo_fora = 0
        self.adiado = True
        self.data_adiamento = data_iso
        self.nao_realizado = False

    def marcar_nao_realizado(self):
        self.realizado = False
        self.golo_casa = 0
        self.golo_fora = 0
        self.adiado = False
        self.data_adiamento = None
        self.nao_realizado = True

    def data_adiamento_date(self):
        try:
            return date.fromisoformat(self.data_adiamento) if self.data_adiamento else None
        except ValueError:
            return None

    def to_dict(self):
        d = {
            "jornada": self.jornada,
            "equipa_casa": self.equipa_casa,
            "equipa_fora": self.equipa_fora,
            "golo_casa": self.golo_casa,
            "golo_fora": self.golo_fora,
            "realizado": self.realizado
        }
        # Só grava o estado de adiamento enquanto existir (jogo resolvido = apagado)
        if self.adiado:
            d["adiado"] = True
            d["data_adiamento"] = self.data_adiamento
        if self.nao_realizado:
            d["nao_realizado"] = True
        return d

    @classmethod
    def from_dict(cls, data):
        return cls(
            jornada=data["jornada"],
            equipa_casa=data["equipa_casa"],
            equipa_fora=data["equipa_fora"],
            golo_casa=data.get("golo_casa", 0),
            golo_fora=data.get("golo_fora", 0),
            realizado=data.get("realizado", False),
            adiado=data.get("adiado", False),
            data_adiamento=data.get("data_adiamento"),
            nao_realizado=data.get("nao_realizado", False)
        )


class Serie:
    def __init__(self, nome: str):
        self.nome = nome
        self.equipas = {}  # {int_id: Equipa}
        self.jogos = []     # list[Jogo]

    def adicionar_equipa(self, id_num: int, nome: str):
        self.equipas[id_num] = Equipa(id_num, nome)

    def adicionar_jogo(self, jornada: int, equipa_casa: int, equipa_fora: int) -> Jogo:
        j = Jogo(jornada, equipa_casa, equipa_fora)
        self.jogos.append(j)
        return j

    def jogos_em_falta(self):
        """Jogos sem resultado de jornadas já em curso/passadas, sem contar os adiados.
        Inclui sempre os marcados como não realizados."""
        realizadas = [j.jornada for j in self.jogos if j.realizado]
        ref = max(realizadas) if realizadas else 0
        em_falta = [
            j for j in self.jogos
            if not j.realizado and not j.adiado and (j.jornada <= ref or j.nao_realizado)
        ]
        return sorted(em_falta, key=lambda j: (j.jornada, j.equipa_casa))

    def obter_classificacao(self) -> pd.DataFrame:
        classif = {}
        for num, eq in self.equipas.items():
            classif[num] = {
                "Equipa": eq.nome,
                "Pts": 0,
                "J": 0,
                "V": 0,
                "E": 0,
                "D": 0
            }

        for j in self.jogos:
            if j.realizado and j.equipa_casa in classif and j.equipa_fora in classif:
                c = classif[j.equipa_casa]
                f = classif[j.equipa_fora]

                c["J"] += 1
                f["J"] += 1

                if j.golo_casa > j.golo_fora:
                    c["Pts"] += 3
                    c["V"] += 1
                    f["D"] += 1
                elif j.golo_casa < j.golo_fora:
                    f["Pts"] += 3
                    f["V"] += 1
                    c["D"] += 1
                else:
                    c["Pts"] += 1
                    f["Pts"] += 1
                    c["E"] += 1
                    f["E"] += 1

        df = pd.DataFrame(list(classif.values()))
        if not df.empty:
            df = df.sort_values(by=["Pts", "V", "J", "Equipa"], ascending=[False, False, True, True])
        return df

    def to_dict(self):
        return {
            "nome": self.nome,
            "equipas": {str(k): v.to_dict() for k, v in self.equipas.items()},
            "jogos": [j.to_dict() for j in self.jogos]
        }

    @classmethod
    def from_dict(cls, data):
        s = cls(data["nome"])
        for k, v in data.get("equipas", {}).items():
            s.equipas[int(k)] = Equipa.from_dict(v)
        for j_data in data.get("jogos", []):
            s.jogos.append(Jogo.from_dict(j_data))
        return s


class GestorCampeonato:
    def __init__(self):
        self.series = {}                      # {str: Serie}
        self.fichas_lousanense = {}           # {str(jornada): dict_ficha}
        self.jogadores_extra_lousanense = []  # list[dict] e.g. [{"nome": "Manuel", "posicao": "Sub10"}]

    def to_dict(self):
        return {
            "series": {k: v.to_dict() for k, v in self.series.items()},
            "fichas_lousanense": self.fichas_lousanense,
            "jogadores_extra_lousanense": getattr(self, "jogadores_extra_lousanense", [])
        }

    @classmethod
    def from_dict(cls, data):
        gc = cls()
        for k, v in data.get("series", {}).items():
            gc.series[k] = Serie.from_dict(v)
        gc.fichas_lousanense = data.get("fichas_lousanense", {})
        gc.jogadores_extra_lousanense = data.get("jogadores_extra_lousanense", [])
        return gc