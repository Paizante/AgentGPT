"""Geracao de indice/relatorio documental de um cliente."""
from __future__ import annotations

from datetime import datetime

from . import config
from .logger import get_logger
from .organizador_clientes import listar_clientes

logger = get_logger("relatorio_documental")


def gerar_indice(cliente: str) -> str:
    pasta_cliente = config.PASTA_CLIENTES / cliente
    linhas = [f"# Indice Documental - {cliente}", "", f"Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ""]

    if not pasta_cliente.exists():
        linhas.append("Pasta do cliente nao encontrada.")
        return "\n".join(linhas)

    for subpasta in sorted(p for p in pasta_cliente.iterdir() if p.is_dir()):
        arquivos = sorted(a for a in subpasta.iterdir() if a.is_file())
        linhas.append(f"## {subpasta.name}")
        if arquivos:
            linhas.extend(f"- {a.name}" for a in arquivos)
        else:
            linhas.append("(vazio)")
        linhas.append("")

    conteudo = "\n".join(linhas)

    destino = config.PASTA_SAIDA / "relatorios" / f"indice_{cliente}.md"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")

    logger.info(f"Indice documental gerado para o cliente {cliente} em {destino}.")
    return conteudo


def gerar_indice_todos_clientes() -> list[str]:
    return [gerar_indice(cliente) for cliente in listar_clientes()]
