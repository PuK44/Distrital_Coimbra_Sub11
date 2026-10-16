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
    def __init__(self, jornada: int, equipa_casa: int, equipa_fora: int, golo_casa: int = 0, golo_fora: int = 0, realizado: bool = False):
        self.jornada = jornada
        self.equipa_casa = equipa_casa
        self.equipa_fora = equipa_fora
        self.golo_casa = golo_casa
        self.golo_fora = golo_fora
        self.realizado = realizado

    def definir_resultado(self, golo_casa: int, golo_fora: int):
        self.golo_casa = golo_casa
        self.golo_fora = golo_fora
        self.realizado = True

    def to_dict(self):
        return {
            "jornada": self.jornada,
            "equipa_casa": self.equipa_casa,
            "equipa_fora": self.equipa_fora,
            "golo_casa": self.golo_casa,
            "golo_fora": self.golo_fora,
            "realizado": self.realizado
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            jornada=data["jornada"],
            equipa_casa=data["equipa_casa"],
            equipa_fora=data["equipa_fora"],
            golo_casa=data.get("golo_casa", 0),
            golo_fora=data.get("golo_fora", 0),
            realizado=data.get("realizado", False)
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
        self.series = {}  # {str: Serie}

    def to_dict(self):
        return {
            "series": {k: v.to_dict() for k, v in self.series.items()}
        }

    @classmethod
    def from_dict(cls, data):
        gc = cls()
        for k, v in data.get("series", {}).items():
            gc.series[k] = Serie.from_dict(v)
        return gc