"""
Consolidacao das respostas das IAs em uma versao unica, e geracao da
versao final + checklist de revisao humana. A IA ajuda a organizar; a
aprovacao final e sempre humana.
"""
from __future__ import annotations

import re

from . import config, job_manager, response_collector
from .logger import get_logger

logger = get_logger("response_consolidator")


def _extrair_documentos_citados(texto: str) -> list[str]:
    candidatos = re.findall(r"(?i)\b(?:documento|certid[aã]o|laudo|comprovante|procura[cç][aã]o|contrato)[^\n,.;]{0,60}", texto)
    vistos: list[str] = []
    for c in candidatos:
        c = c.strip()
        if c and c not in vistos:
            vistos.append(c)
    return vistos[:20]


def _extrair_lacunas(texto: str) -> list[str]:
    linhas = texto.splitlines()
    lacunas = [l.strip("- ").strip() for l in linhas if re.search(r"(?i)lacuna|falta|nao encontrado|ausente", l)]
    return [l for l in lacunas if l][:20]


def consolidar(job_id: str) -> str:
    disponiveis = response_collector.respostas_disponiveis(job_id)
    trabalho = job_manager.carregar_trabalho(job_id)

    linhas = [f"# Consolidado - {job_id}", "", f"Cliente: {trabalho.get('cliente', '')}", ""]

    documentos_citados: list[str] = []
    lacunas: list[str] = []

    if not disponiveis:
        linhas.append("Nenhuma resposta disponivel para consolidar ainda.")
    else:
        for ia in disponiveis:
            texto = job_manager.ler_arquivo_trabalho(job_id, f"resposta_{ia}.md")
            linhas.append(f"## Contribuicao de {ia.capitalize()}")
            linhas.append(texto.strip())
            linhas.append("")
            documentos_citados.extend(_extrair_documentos_citados(texto))
            lacunas.extend(_extrair_lacunas(texto))

    linhas.append("## Documentos citados (consolidado)")
    if documentos_citados:
        linhas.extend(f"- {d}" for d in sorted(set(documentos_citados)))
    else:
        linhas.append("(nenhuma mencao explicita a documentos identificada automaticamente)")

    linhas.append("")
    linhas.append("## Lacunas identificadas (consolidado)")
    if lacunas:
        linhas.extend(f"- {l}" for l in sorted(set(lacunas)))
    else:
        linhas.append("(nenhuma lacuna explicita identificada automaticamente - revise manualmente)")

    linhas.append("")
    linhas.append("## Proximos passos sugeridos")
    linhas.append("1. Revisar manualmente cada contribuicao acima.")
    linhas.append("2. Resolver divergencias entre as IAs (ver comparativo.md).")
    linhas.append("3. Gerar a versao final apos a revisao.")

    conteudo = "\n".join(linhas)
    job_manager.escrever_arquivo_trabalho(job_id, "consolidado.md", conteudo)

    destino = config.PASTA_FILAS / config.FILA_CONSOLIDADO / f"{job_id}.md"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")

    logger.info(f"Consolidado gerado para o trabalho {job_id}.")
    return conteudo


def gerar_final(job_id: str) -> str:
    consolidado = job_manager.ler_arquivo_trabalho(job_id, "consolidado.md")
    trabalho = job_manager.carregar_trabalho(job_id)

    linhas = [
        f"# Versao Final (pre-revisao humana) - {job_id}",
        "",
        "**ATENCAO: esta versao exige revisao e aprovacao humana do advogado",
        "responsavel antes de qualquer uso processual ou envio ao cliente.**",
        "",
        f"Tipo de tarefa: {trabalho.get('tipo_tarefa', '')}",
        f"Cliente: {trabalho.get('cliente', '')}",
        "",
        "## Conteudo consolidado",
        consolidado.strip() or "(consolidado vazio - gere a consolidacao primeiro)",
        "",
        "## Assinatura",
        config.ASSINATURA,
    ]

    conteudo = "\n".join(linhas)
    job_manager.escrever_arquivo_trabalho(job_id, "final.md", conteudo)

    destino = config.PASTA_FILAS / config.FILA_FINAL / f"{job_id}.md"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")

    logger.info(f"Versao final gerada para o trabalho {job_id} (revisao humana pendente).")
    return conteudo


def gerar_checklist_revisao(job_id: str) -> str:
    itens = [
        "Fatos confirmados com os documentos originais do cliente?",
        "Nenhuma jurisprudencia/fundamento foi inventado pela IA?",
        "Fato, inferencia e opiniao estao claramente separados?",
        "Lacunas de prova foram identificadas e resolvidas (ou assumidas conscientemente)?",
        "A peca/texto termina com a assinatura: " + config.ASSINATURA + "?",
        "O cliente foi informado/autorizado quanto ao uso de IA no caso, quando aplicavel?",
        "Revisao humana final concluida e aprovada?",
    ]
    linhas = [f"# Checklist de Revisao Humana - {job_id}", ""]
    linhas.extend(f"- [ ] {item}" for item in itens)
    conteudo = "\n".join(linhas)
    job_manager.escrever_arquivo_trabalho(job_id, "checklist.md", conteudo)
    return conteudo
