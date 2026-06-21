"""Testes do comparativo heuristico entre respostas de IAs."""
from __future__ import annotations

from src import job_manager, response_collector, response_comparer


def test_comparar_respostas_sem_nenhuma_resposta(workspace):
    job_id = job_manager.criar_trabalho("analise_juridica", "Cliente", "resumo", ["chatgpt", "claude"])

    conteudo = response_comparer.comparar_respostas(job_id)

    assert "Nenhuma resposta foi salva ainda" in conteudo


def test_comparar_respostas_com_uma_resposta_nao_gera_secao_de_divergencias(workspace):
    job_id = job_manager.criar_trabalho("analise_juridica", "Cliente", "resumo", ["chatgpt"])
    response_collector.salvar_resposta(job_id, "chatgpt", "Resposta unica da IA, com fundamento legal art. 1.")

    conteudo = response_comparer.comparar_respostas(job_id)

    assert "Chatgpt" in conteudo
    assert "Divergencias e recomendacao" not in conteudo


def test_comparar_respostas_com_duas_respostas_gera_recomendacao(workspace):
    job_id = job_manager.criar_trabalho("analise_juridica", "Cliente", "resumo", ["chatgpt", "claude"])
    response_collector.salvar_resposta(job_id, "chatgpt", "Resposta do ChatGPT com fundamento legal art. 5.")
    response_collector.salvar_resposta(job_id, "claude", "Resposta do Claude apontando uma lacuna importante.")

    conteudo = response_comparer.comparar_respostas(job_id)

    assert "Divergencias e recomendacao" in conteudo
    assert "Decisao final e sempre humana" in conteudo
