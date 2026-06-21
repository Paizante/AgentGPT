"""
Divide um texto/tarefa longa em partes menores, para respeitar limites
de contexto/colagem das IAs web (ChatGPT/Claude/Gemini).
"""
from __future__ import annotations


def dividir_texto(texto: str, tamanho_maximo: int = 12000) -> list[str]:
    """Divide o texto em blocos de no maximo `tamanho_maximo` caracteres,
    tentando quebrar em fim de paragrafo para preservar contexto."""
    if len(texto) <= tamanho_maximo:
        return [texto]

    paragrafos = texto.split("\n\n")
    blocos: list[str] = []
    atual = ""

    for paragrafo in paragrafos:
        candidato = f"{atual}\n\n{paragrafo}" if atual else paragrafo
        if len(candidato) > tamanho_maximo and atual:
            blocos.append(atual)
            atual = paragrafo
        else:
            atual = candidato

    if atual:
        blocos.append(atual)

    return blocos


def dividir_tarefa_em_partes(texto: str, n_partes: int) -> list[str]:
    """Divide o texto em aproximadamente `n_partes` partes de tamanho
    semelhante, preservando quebras de linha."""
    if n_partes <= 1:
        return [texto]
    tamanho_aproximado = max(1, len(texto) // n_partes)
    return dividir_texto(texto, tamanho_maximo=tamanho_aproximado)


def montar_cabecalho_parte(indice: int, total: int) -> str:
    return f"[Parte {indice} de {total} - cole esta parte primeiro, na ordem indicada]\n\n"
