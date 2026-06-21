"""
Utilitarios de arquivo. Modo "criar, nunca destruir": nenhuma funcao
aqui apaga ou sobrescreve um arquivo original sem antes copia-lo para
10_BACKUPS.
"""
from __future__ import annotations

import platform
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from . import config
from .logger import get_logger

logger = get_logger("file_utils")


def garantir_pasta(caminho: Path) -> Path:
    caminho.mkdir(parents=True, exist_ok=True)
    return caminho


def backup_antes_de_sobrescrever(caminho: Path) -> Path | None:
    """Copia o arquivo/pasta para 10_BACKUPS antes de uma sobrescrita inevitavel."""
    if not caminho.exists():
        return None
    selo = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino_raiz = config.PASTA_BACKUPS / "documentos" / "pre_sobrescrita"
    garantir_pasta(destino_raiz)
    destino = destino_raiz / f"{caminho.name}__{selo}"
    if caminho.is_dir():
        shutil.copytree(caminho, destino)
    else:
        shutil.copy2(caminho, destino)
    logger.info(f"Backup de seguranca criado em {destino} antes de sobrescrever {caminho}.")
    return destino


def copiar_arquivo_seguro(origem: Path, destino: Path) -> Path:
    """Copia origem para destino sem jamais apagar ou mover o original."""
    garantir_pasta(destino.parent)
    if destino.exists():
        backup_antes_de_sobrescrever(destino)
    shutil.copy2(origem, destino)
    logger.info(f"Copiado {origem} -> {destino}")
    return destino


def abrir_pasta(caminho: Path) -> bool:
    """Abre a pasta no explorador de arquivos do sistema operacional."""
    caminho = Path(caminho)
    garantir_pasta(caminho)
    sistema = platform.system()
    try:
        if sistema == "Windows":
            import os
            os.startfile(str(caminho))  # type: ignore[attr-defined]
        elif sistema == "Darwin":
            subprocess.run(["open", str(caminho)], check=False)
        else:
            subprocess.run(["xdg-open", str(caminho)], check=False)
        return True
    except Exception as exc:
        logger.warning(f"Nao foi possivel abrir a pasta {caminho}: {exc}")
        return False


def listar_arquivos(pasta: Path, extensoes: list[str] | None = None) -> list[Path]:
    if not pasta.exists():
        return []
    arquivos = [p for p in pasta.iterdir() if p.is_file()]
    if extensoes:
        extensoes_norm = {e.lower().lstrip(".") for e in extensoes}
        arquivos = [a for a in arquivos if a.suffix.lower().lstrip(".") in extensoes_norm]
    return sorted(arquivos)
