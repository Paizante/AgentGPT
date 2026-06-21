"""Fixtures compartilhadas: isolam os testes em uma pasta temporaria,
nunca escrevendo na estrutura real do hub (04_DOCUMENTOS, 10_BACKUPS etc.)."""
from __future__ import annotations

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import pytest

from src import config


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    """Redireciona as pastas do config para dentro de tmp_path, isolando
    cada teste e garantindo que nada seja escrito na estrutura real."""
    monkeypatch.setattr(config, "BASE_DIR", tmp_path)
    monkeypatch.setattr(config, "PASTA_TRABALHOS", tmp_path / "01_PAINEL_LOCAL" / "data" / "trabalhos")
    monkeypatch.setattr(config, "PASTA_FILAS", tmp_path / "03_FILAS_DE_TRABALHO")
    monkeypatch.setattr(config, "PASTA_CLIENTES", tmp_path / "04_DOCUMENTOS" / "clientes")
    monkeypatch.setattr(config, "PASTA_SAIDA", tmp_path / "04_DOCUMENTOS" / "saida")
    monkeypatch.setattr(config, "PASTA_BACKUPS", tmp_path / "10_BACKUPS")
    monkeypatch.setattr(config, "PASTA_LOGS", tmp_path / "11_LOGS")
    monkeypatch.setattr(config, "PASTA_RELATORIOS", tmp_path / "12_RELATORIOS")
    return tmp_path
