"""Testes basicos: criacao de pastas, geracao de ID e estrutura minima."""
from __future__ import annotations

import re

from src import config, job_manager


def test_novo_id_segue_padrao_data_hora_tipo_cliente():
    job_id = job_manager.novo_id("Analise Juridica", "Joao da Silva")
    assert re.match(r"^\d{8}_\d{6}_analise_juridica_joao_da_silva$", job_id)


def test_garantir_estrutura_minima_cria_pastas(workspace):
    config.garantir_estrutura_minima()

    assert config.PASTA_TRABALHOS.exists()
    assert config.PASTA_CLIENTES.exists()
    assert config.PASTA_LOGS.exists()
    assert config.PASTA_BACKUPS.exists()
    assert config.PASTA_RELATORIOS.exists()


def test_criar_trabalho_gera_pasta_e_arquivos_base(workspace):
    job_id = job_manager.criar_trabalho(
        tipo_tarefa="analise_juridica",
        cliente="Joao da Silva",
        resumo="Resumo de teste do caso.",
        ias=["chatgpt", "claude"],
    )

    pasta = job_manager.caminho_trabalho(job_id)
    assert pasta.exists()
    for nome_arquivo in job_manager.ARQUIVOS_BASE:
        assert (pasta / nome_arquivo).exists()
    assert (pasta / "metadata.yaml").exists()

    trabalho = job_manager.carregar_trabalho(job_id)
    assert trabalho["cliente"] == "Joao da Silva"
    assert trabalho["tipo_tarefa"] == "analise_juridica"
    assert trabalho["ias"] == ["chatgpt", "claude"]


def test_listar_trabalhos_inclui_trabalho_criado(workspace):
    job_id = job_manager.criar_trabalho("revisao_peca", "Maria", "resumo", ["gemini"])

    trabalhos = job_manager.listar_trabalhos()

    assert any(t["job_id"] == job_id for t in trabalhos)
