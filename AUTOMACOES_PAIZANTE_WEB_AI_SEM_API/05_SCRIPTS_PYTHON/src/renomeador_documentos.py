"""
Renomeacao padronizada de documentos - sempre na copia, nunca no
original. Padrao: 01_Documento_Identificacao_Nome, 02_CPF_Nome,
03_Comprovante_Endereco_Nome, 04_Relatorio_Medico_Nome, 05_CadUnico_Nome,
06_Procuracao_Nome, 07_Hipossuficiencia_Nome, 08_Requerimento_Nome.
"""
from __future__ import annotations

from pathlib import Path

from . import file_utils
from .logger import get_logger
from .organizador_clientes import PADRAO_NOME_POR_TIPO, _slug

logger = get_logger("renomeador_documentos")


def gerar_nome_padronizado(tipo_documento: str, nome_pessoa: str, extensao: str) -> str:
    prefixo = PADRAO_NOME_POR_TIPO.get(tipo_documento, "09_Nao_Identificado")
    extensao = extensao if extensao.startswith(".") else f".{extensao}"
    return f"{prefixo}_{_slug(nome_pessoa)}{extensao.lower()}"


def renomear_copia(origem: Path, pasta_destino: Path, tipo_documento: str, nome_pessoa: str) -> Path:
    """Cria uma copia de `origem` em `pasta_destino` com o nome
    padronizado. O arquivo original em `origem` nunca e tocado."""
    nome_novo = gerar_nome_padronizado(tipo_documento, nome_pessoa, origem.suffix)
    destino = pasta_destino / nome_novo

    contador = 1
    base_destino = destino
    while destino.exists():
        destino = base_destino.with_name(f"{base_destino.stem}_{contador}{base_destino.suffix}")
        contador += 1

    resultado = file_utils.copiar_arquivo_seguro(origem, destino)
    logger.info(f"Copia renomeada: {origem.name} -> {resultado.name}")
    return resultado
