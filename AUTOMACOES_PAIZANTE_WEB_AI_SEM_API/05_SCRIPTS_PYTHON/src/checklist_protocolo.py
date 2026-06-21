"""Checklist de protocolo: combina a revisao humana com a conferencia
documental antes de protocolar uma peca."""
from __future__ import annotations

from . import config, job_manager
from .logger import get_logger
from .response_consolidator import gerar_checklist_revisao

logger = get_logger("checklist_protocolo")

ITENS_PROTOCOLO = [
    "Todos os documentos do pacote de protocolo estao presentes e legiveis?",
    "Os nomes dos arquivos seguem o padrao definido (01_Documento_Identificacao_Nome etc.)?",
    "Prazos (decadencial/prescricional/recursal) foram verificados?",
    "O valor da causa (quando exigivel) foi informado corretamente?",
    "A peca foi revisada e aprovada pelo advogado responsavel?",
]


def gerar_checklist_protocolo(job_id: str) -> str:
    checklist_revisao = gerar_checklist_revisao(job_id)
    trabalho = job_manager.carregar_trabalho(job_id)

    linhas = [checklist_revisao, "", "## Checklist Especifico de Protocolo", ""]
    linhas.extend(f"- [ ] {item}" for item in ITENS_PROTOCOLO)
    linhas.append("")
    linhas.append(f"Cliente: {trabalho.get('cliente', '')}")
    linhas.append(f"Tipo de tarefa: {trabalho.get('tipo_tarefa', '')}")
    linhas.append("")
    linhas.append(f"Assinatura responsavel: {config.ASSINATURA}")

    conteudo = "\n".join(linhas)
    job_manager.escrever_arquivo_trabalho(job_id, "checklist.md", conteudo)

    logger.info(f"Checklist de protocolo gerado para o trabalho {job_id}.")
    return conteudo
