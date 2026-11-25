"""Leitura dos resultados do Centro de Resultados da FPF.

Época 2026-2027 · Troféu Distrital Benjamins SUB-11 - Fut.7 · 1.ª fase.
Cada jornada tem o seu identificador (fixtureId) na página da competição.
"""
import html as html_lib
import re

URL_JORNADA = (
    "https://resultados.fpf.pt/Competition/GetClassificationAndMatchesByFixture"
    "?fixtureId={}"
)

# Identificadores por série e jornada (recolhidos em 2026-11-25)
FIXTURE_IDS = {
    "SÉRIE A": {j: fid for j, fid in enumerate(range(680817, 680828), start=1)},
    "SÉRIE B": {j: fid for j, fid in enumerate(range(680850, 680861), start=1)},
    "SÉRIE C": {j: fid for j, fid in enumerate(range(683066, 683077), start=1)},
    "SÉRIE D": {j: fid for j, fid in enumerate(range(680839, 680850), start=1)},
}

_BLOCOS = re.compile(r"(?i)<br\s*/?>|</(div|p|li|tr|td|th|h[1-6]|table|ul|ol)>")
_TAGS = re.compile(r"<[^>]+>")
_SCRIPTS = re.compile(r"(?is)<(script|style)\b.*?</\1>")
_RESULTADO = re.compile(r"^(\d+)\s*-\s*(\d+)\b")
_DATA = re.compile(r"^\d{1,2}\s+\w+\.?$")
_HORA = re.compile(r"^\d{1,2}:\d{2}$")
_NAO_INICIADO = re.compile(r"(?i)^\(n[ãa]o iniciado\)$")


def url_jornada(serie: str, jornada: int) -> str:
    return URL_JORNADA.format(FIXTURE_IDS[serie][jornada])


def normalizar_nome(nome: str) -> str:
    """Compara nomes de equipas ignorando maiúsculas, espaços e tipo de traço."""
    n = nome.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", n).strip().lower()


def html_para_linhas(html: str) -> list[str]:
    texto = _SCRIPTS.sub("", html)
    texto = _BLOCOS.sub("\n", texto)
    texto = _TAGS.sub("", texto)
    texto = html_lib.unescape(texto)
    return [linha.strip() for linha in texto.split("\n") if linha.strip()]


def extrair_resultados(linhas: list[str]) -> list[dict]:
    """Devolve os jogos já realizados, como {casa, golo_casa, golo_fora, fora}.

    Assume o formato da FPF: nome da equipa da casa, linha com o resultado
    (e a data), nome da equipa visitante. Jogos por iniciar são ignorados.
    """
    resultados = []
    for i, linha in enumerate(linhas):
        m = _RESULTADO.match(linha)
        if not m or i == 0:
            continue
        casa = linhas[i - 1]
        if _RESULTADO.match(casa) or _DATA.match(casa) or _HORA.match(casa):
            continue
        k = i + 1
        while k < len(linhas) and (_DATA.match(linhas[k]) or _HORA.match(linhas[k])):
            k += 1
        if k >= len(linhas) or _NAO_INICIADO.match(linhas[k]):
            continue
        resultados.append({
            "casa": casa,
            "golo_casa": int(m.group(1)),
            "golo_fora": int(m.group(2)),
            "fora": linhas[k],
        })
    return resultados


def buscar_resultados_fpf(serie: str, jornada: int) -> list[dict]:
    """Vai buscar à FPF os jogos realizados de uma jornada."""
    import requests  # importado aqui para o módulo poder ser testado sem rede

    resposta = requests.get(
        url_jornada(serie, jornada),
        timeout=20,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    resposta.raise_for_status()
    return extrair_resultados(html_para_linhas(resposta.text))


def encontrar_id_equipa(nome_fpf: str, equipas: dict) -> int | None:
    alvo = normalizar_nome(nome_fpf)
    for id_num, equipa in equipas.items():
        if normalizar_nome(equipa.nome) == alvo:
            return id_num
    return None
