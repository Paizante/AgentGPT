"""
Abertura de URLs no Chrome a partir do Python (equivalente em Python aos
scripts PowerShell de 02_CHROME_WORKSPACE). Nunca preenche login, nunca
envia nada, nunca le cookies/sessao/token - apenas abre a aba.
"""
from __future__ import annotations

import platform
import shutil
import subprocess
import webbrowser
from pathlib import Path

from . import config
from .logger import get_logger

logger = get_logger("browser_launcher")


def _candidatos_chrome() -> list[str]:
    sistema = platform.system()
    if sistema == "Windows":
        return [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
    if sistema == "Darwin":
        return ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
    return ["google-chrome", "google-chrome-stable", "chromium-browser", "chromium"]


def encontrar_chrome() -> str | None:
    for candidato in _candidatos_chrome():
        if Path(candidato).exists():
            return candidato
        encontrado = shutil.which(candidato)
        if encontrado:
            return encontrado
    return None


def abrir_url(url: str) -> bool:
    chrome = encontrar_chrome()
    try:
        if chrome:
            subprocess.Popen([chrome, url])
        else:
            webbrowser.open(url)
        logger.info(f"Aba aberta: {url}")
        return True
    except Exception as exc:
        logger.warning(f"Nao foi possivel abrir {url}: {exc}")
        return False


def abrir_ia(ia: str) -> bool:
    url = config.URLS_IA.get(ia)
    if not url:
        logger.warning(f"IA desconhecida: {ia}")
        return False
    return abrir_url(url)


def abrir_painel() -> bool:
    return abrir_url(config.URL_PAINEL)


def abrir_n8n() -> bool:
    return abrir_url(config.URL_N8N)


def abrir_todas_ias() -> None:
    for ia in config.IAS:
        abrir_ia(ia)
