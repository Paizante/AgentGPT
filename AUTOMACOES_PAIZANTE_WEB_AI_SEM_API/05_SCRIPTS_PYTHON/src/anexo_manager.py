"""
Gerenciamento de anexos (documentos/imagens) enviados no chat com a IA
local. Cada anexo e salvo em
01_PAINEL_LOCAL/data/trabalhos/<job_id>/anexos/ - nunca substitui um
anexo existente (sempre soma um sufixo numerico se o nome ja existir).
"""
from __future__ import annotations

import base64
from pathlib import Path

from . import job_manager
from .logger import get_logger

logger = get_logger("anexo_manager")

EXTENSOES_IMAGEM = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
EXTENSOES_PDF = {".pdf"}
EXTENSOES_DOCX = {".docx"}
EXTENSOES_TEXTO = {".txt", ".md", ".csv"}


def pasta_anexos(job_id: str) -> Path:
    pasta = job_manager.caminho_trabalho(job_id) / "anexos"
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta


def salvar_anexo(job_id: str, nome_arquivo: str, conteudo: bytes) -> Path:
    pasta = pasta_anexos(job_id)
    destino = pasta / Path(nome_arquivo).name
    contador = 1
    while destino.exists():
        destino = pasta / f"{destino.stem}_{contador}{destino.suffix}"
        contador += 1
    destino.write_bytes(conteudo)
    logger.info(f"Anexo salvo: {destino}")
    return destino


def eh_imagem(caminho: Path) -> bool:
    return caminho.suffix.lower() in EXTENSOES_IMAGEM


def imagem_para_base64(caminho: Path) -> str:
    return base64.b64encode(caminho.read_bytes()).decode("ascii")


def extrair_texto(caminho: Path) -> str:
    """Extrai texto de documentos (PDF/DOCX/TXT) para dar contexto a IA
    local. Para imagens, retorna vazio (tratadas via visao, nao texto)."""
    sufixo = caminho.suffix.lower()
    try:
        if sufixo in EXTENSOES_PDF:
            from . import pdf_tools
            return pdf_tools.extrair_texto(caminho)
        if sufixo in EXTENSOES_DOCX:
            from . import docx_tools
            return docx_tools.ler_docx(caminho)
        if sufixo in EXTENSOES_TEXTO:
            return caminho.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        logger.warning(f"Nao foi possivel extrair texto de {caminho}: {exc}")
        return ""
    return ""
