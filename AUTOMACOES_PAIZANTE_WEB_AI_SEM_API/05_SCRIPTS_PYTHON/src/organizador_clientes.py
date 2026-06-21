"""
Organizacao de pastas por cliente, a partir do modelo
04_DOCUMENTOS/clientes/_MODELO_CLIENTE. Documentos originais nunca sao
alterados ou apagados - todo processamento ocorre em copia.
"""
from __future__ import annotations

import re
import shutil
import unicodedata
from pathlib import Path

from . import config, file_utils
from .logger import get_logger

logger = get_logger("organizador_clientes")

MODELO_CLIENTE = config.PASTA_CLIENTES / "_MODELO_CLIENTE"

CATEGORIAS_POR_TIPO_DOCUMENTO = {
    "identificacao": "02_Documentos_Pessoais",
    "cpf": "02_Documentos_Pessoais",
    "comprovante_endereco": "03_Comprovantes",
    "relatorio_medico": "04_Documentos_Medicos",
    "cadunico": "03_Comprovantes",
    "procuracao": "06_Procuracao_e_Contratos",
    "contrato_honorarios": "06_Procuracao_e_Contratos",
    "hipossuficiencia": "07_Hipossuficiencia",
    "requerimento": "08_Requerimentos",
    "trabalhista": "05_Documentos_Trabalhistas",
}

PADRAO_NOME_POR_TIPO = {
    "identificacao": "01_Documento_Identificacao",
    "cpf": "02_CPF",
    "comprovante_endereco": "03_Comprovante_Endereco",
    "relatorio_medico": "04_Relatorio_Medico",
    "cadunico": "05_CadUnico",
    "procuracao": "06_Procuracao",
    "hipossuficiencia": "07_Hipossuficiencia",
    "requerimento": "08_Requerimento",
}


def _slug(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode("ascii")
    texto = re.sub(r"[^a-zA-Z0-9]+", "_", texto).strip("_")
    return texto or "Cliente"


def criar_cliente(nome: str) -> Path:
    nome_pasta = _slug(nome)
    destino = config.PASTA_CLIENTES / nome_pasta

    if not MODELO_CLIENTE.exists():
        file_utils.garantir_pasta(destino)
        logger.warning("Pasta _MODELO_CLIENTE nao encontrada; criando pasta de cliente vazia.")
        return destino

    if destino.exists():
        logger.info(f"Pasta do cliente {nome_pasta} ja existe.")
        return destino

    shutil.copytree(MODELO_CLIENTE, destino)
    logger.info(f"Pasta do cliente criada a partir do modelo: {destino}")
    return destino


def listar_clientes() -> list[str]:
    if not config.PASTA_CLIENTES.exists():
        return []
    return sorted(
        p.name for p in config.PASTA_CLIENTES.iterdir()
        if p.is_dir() and not p.name.startswith("_")
    )


def copiar_documento_para_cliente(origem: Path, cliente: str, tipo_documento: str, nome_pessoa: str = "") -> Path:
    """Copia (nunca move) um documento de entrada para a subpasta correta
    do cliente, com nome padronizado na copia."""
    pasta_cliente = criar_cliente(cliente)
    subpasta = CATEGORIAS_POR_TIPO_DOCUMENTO.get(tipo_documento, "01_Documentos_Originais")
    pasta_destino = pasta_cliente / subpasta
    file_utils.garantir_pasta(pasta_destino)

    prefixo = PADRAO_NOME_POR_TIPO.get(tipo_documento, "09_Nao_Identificado")
    nome_final = f"{prefixo}_{_slug(nome_pessoa or cliente)}{origem.suffix.lower()}"
    destino = pasta_destino / nome_final

    return file_utils.copiar_arquivo_seguro(origem, destino)
