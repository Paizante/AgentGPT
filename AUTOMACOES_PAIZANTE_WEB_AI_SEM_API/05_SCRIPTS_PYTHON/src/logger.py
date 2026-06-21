"""Logging padronizado, gravando em 11_LOGS/python/<nome>.log."""
from __future__ import annotations

import logging
from pathlib import Path

from . import config

_LOGGERS: dict[str, logging.Logger] = {}


def get_logger(nome: str) -> logging.Logger:
    if nome in _LOGGERS:
        return _LOGGERS[nome]

    logger = logging.getLogger(f"paizante.{nome}")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        pasta = config.PASTA_LOGS / "python"
        pasta.mkdir(parents=True, exist_ok=True)
        arquivo = pasta / f"{nome}.log"

        handler_arquivo = logging.FileHandler(arquivo, encoding="utf-8")
        handler_arquivo.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler_arquivo)

        handler_console = logging.StreamHandler()
        handler_console.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler_console)

    _LOGGERS[nome] = logger
    return logger
