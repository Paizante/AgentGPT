"""Ferramentas de PDF: unir, separar e extrair texto. Sempre em copia."""
from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter

from .logger import get_logger

logger = get_logger("pdf_tools")


def unir_pdfs(caminhos: list[Path], destino: Path) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()
    for caminho in caminhos:
        reader = PdfReader(str(caminho))
        for pagina in reader.pages:
            writer.add_page(pagina)
    with open(destino, "wb") as f:
        writer.write(f)
    logger.info(f"PDFs unidos em {destino} (fontes: {[str(c) for c in caminhos]})")
    return destino


def separar_pdf(origem: Path, destino_dir: Path, paginas_por_arquivo: int = 1) -> list[Path]:
    destino_dir.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(str(origem))
    total_paginas = len(reader.pages)
    gerados: list[Path] = []

    for inicio in range(0, total_paginas, paginas_por_arquivo):
        writer = PdfWriter()
        fim = min(inicio + paginas_por_arquivo, total_paginas)
        for indice in range(inicio, fim):
            writer.add_page(reader.pages[indice])
        nome_saida = destino_dir / f"{origem.stem}_paginas_{inicio + 1}-{fim}.pdf"
        with open(nome_saida, "wb") as f:
            writer.write(f)
        gerados.append(nome_saida)

    logger.info(f"PDF {origem} separado em {len(gerados)} arquivo(s) em {destino_dir}")
    return gerados


def extrair_texto(origem: Path) -> str:
    reader = PdfReader(str(origem))
    partes = [pagina.extract_text() or "" for pagina in reader.pages]
    texto = "\n".join(partes)
    logger.info(f"Texto extraido de {origem} ({len(texto)} caracteres).")
    return texto
