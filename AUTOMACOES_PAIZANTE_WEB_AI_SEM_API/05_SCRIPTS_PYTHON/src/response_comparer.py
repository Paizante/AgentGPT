"""
Comparador de respostas entre ChatGPT, Claude e Gemini.

Gera um comparativo heuristico (tamanho, presenca de seções, possiveis
sinais de alucinacao como numeros/datas isolados sem contexto) para
apoiar a revisao humana - nao substitui a leitura do advogado responsavel.
Para uma comparacao de conteudo mais profunda, use o prompt mestre
`07_PROMPTS_MESTRES/07_comparacao_ias/comparar_respostas_chatgpt_claude_gemini.md`
com Claude ou ChatGPT.
"""
from __future__ import annotations

from . import config, job_manager, response_collector
from .logger import get_logger

logger = get_logger("response_comparer")


def _resumo_simples(texto: str, max_linhas: int = 5) -> str:
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    return "\n".join(linhas[:max_linhas]) if linhas else "(sem conteudo)"


def _pontos_fortes_fracos(texto: str) -> tuple[list[str], list[str]]:
    fortes: list[str] = []
    fracos: list[str] = []

    if len(texto) > 1500:
        fortes.append("Resposta extensa e detalhada.")
    else:
        fracos.append("Resposta curta - pode estar incompleta.")

    if "lacuna" in texto.lower() or "falta" in texto.lower():
        fortes.append("A IA indicou lacunas/faltas de informacao explicitamente.")
    else:
        fracos.append("Nao ficou claro se a IA apontou lacunas de informacao.")

    if "fundamento" in texto.lower() or "art." in texto.lower() or "lei" in texto.lower():
        fortes.append("Ha referencia a fundamentacao legal.")
    else:
        fracos.append("Nao foi identificada referencia explicita a fundamentacao legal.")

    return fortes, fracos


def comparar_respostas(job_id: str) -> str:
    disponiveis = response_collector.respostas_disponiveis(job_id)
    linhas = [f"# Comparativo de Respostas - {job_id}", ""]

    if len(disponiveis) < 1:
        linhas.append("Nenhuma resposta foi salva ainda para este trabalho.")
        conteudo = "\n".join(linhas)
        job_manager.escrever_arquivo_trabalho(job_id, "comparativo.md", conteudo)
        return conteudo

    resumos: dict[str, str] = {}
    for ia in disponiveis:
        texto = job_manager.ler_arquivo_trabalho(job_id, f"resposta_{ia}.md")
        resumos[ia] = texto
        fortes, fracos = _pontos_fortes_fracos(texto)
        linhas.append(f"## {ia.capitalize()}")
        linhas.append("")
        linhas.append("**Resumo (primeiras linhas):**")
        linhas.append(_resumo_simples(texto))
        linhas.append("")
        linhas.append("**Pontos fortes:**")
        linhas.extend(f"- {p}" for p in fortes)
        linhas.append("")
        linhas.append("**Pontos fracos / riscos de alucinacao a verificar:**")
        linhas.extend(f"- {p}" for p in fracos)
        linhas.append("")

    if len(disponiveis) >= 2:
        linhas.append("## Divergencias e recomendacao")
        linhas.append("")
        linhas.append(
            "Revise manualmente as respostas acima lado a lado. Use o prompt "
            "mestre `comparar_respostas_chatgpt_claude_gemini.md` em Claude ou "
            "ChatGPT para uma analise de divergencias mais profunda, colando o "
            "conteudo de cada resposta."
        )
        maior_ia = max(resumos, key=lambda k: len(resumos[k]))
        linhas.append(f"Recomendacao automatica preliminar (heuristica de tamanho/conteudo): considerar `{maior_ia}` como base, combinando trechos das demais. **Decisao final e sempre humana.**")

    conteudo = "\n".join(linhas)
    job_manager.escrever_arquivo_trabalho(job_id, "comparativo.md", conteudo)

    destino = config.PASTA_FILAS / config.FILA_COMPARACAO / f"{job_id}.md"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")

    logger.info(f"Comparativo gerado para o trabalho {job_id} ({len(disponiveis)} respostas).")
    return conteudo
