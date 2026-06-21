"""
Copia de prompts para a area de transferencia. Nunca envia nada
automaticamente - apenas copia, registra o historico e (opcionalmente)
abre a IA correspondente para o usuario colar e enviar manualmente.
"""
from __future__ import annotations

from datetime import datetime

import pyperclip

from . import browser_launcher, config
from .logger import get_logger

logger = get_logger("clipboard_tools")

AVISO_PADRAO = "Cole manualmente no ChatGPT/Claude/Gemini e revise antes de enviar."


def copiar_para_clipboard(texto: str) -> bool:
    try:
        pyperclip.copy(texto)
        logger.info(f"Texto copiado para a area de transferencia ({len(texto)} caracteres).")
        return True
    except Exception as exc:
        logger.warning(f"Nao foi possivel copiar para a area de transferencia: {exc}")
        return False


def registrar_copia(job_id: str, ia: str) -> None:
    pasta = config.PASTA_LOGS / "automacoes"
    pasta.mkdir(parents=True, exist_ok=True)
    linha = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - prompt copiado - job={job_id} ia={ia}\n"
    with open(pasta / "historico_clipboard.log", "a", encoding="utf-8") as f:
        f.write(linha)


def copiar_e_abrir_ia(job_id: str, ia: str, texto: str) -> str:
    copiar_para_clipboard(texto)
    registrar_copia(job_id, ia)
    browser_launcher.abrir_ia(ia)
    print(AVISO_PADRAO)
    return AVISO_PADRAO
