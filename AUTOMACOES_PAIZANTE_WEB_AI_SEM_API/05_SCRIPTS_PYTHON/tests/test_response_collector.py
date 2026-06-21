"""Testes de coleta de respostas coladas manualmente pelo usuario."""
from __future__ import annotations

from src import config, job_manager, response_collector


def test_salvar_resposta_vazia_e_ignorada(workspace):
    job_id = job_manager.criar_trabalho("analise_juridica", "Cliente", "resumo", ["chatgpt"])

    salvo = response_collector.salvar_resposta(job_id, "chatgpt", "   ")

    assert salvo is False
    assert response_collector.resposta_existe(job_id, "chatgpt") is False


def test_salvar_resposta_grava_arquivo_e_espelha_na_fila(workspace):
    job_id = job_manager.criar_trabalho("analise_juridica", "Cliente", "resumo", ["chatgpt"])

    salvo = response_collector.salvar_resposta(job_id, "chatgpt", "Texto da resposta da IA.")

    assert salvo is True
    conteudo = job_manager.ler_arquivo_trabalho(job_id, "resposta_chatgpt.md")
    assert "Texto da resposta da IA." in conteudo
    assert "origem: chatgpt" in conteudo

    fila = config.FILA_RETORNO["chatgpt"]
    caminho_fila = config.PASTA_FILAS / fila / f"{job_id}.md"
    assert caminho_fila.exists()

    metadata = job_manager.carregar_trabalho(job_id)
    assert "resposta_chatgpt_salva_em" in metadata


def test_respostas_disponiveis_lista_apenas_ias_com_resposta_salva(workspace):
    job_id = job_manager.criar_trabalho("analise_juridica", "Cliente", "resumo", ["chatgpt", "claude"])
    response_collector.salvar_resposta(job_id, "chatgpt", "Resposta do ChatGPT.")

    disponiveis = response_collector.respostas_disponiveis(job_id)

    assert disponiveis == ["chatgpt"]
