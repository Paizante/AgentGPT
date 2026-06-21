"""Testes de geracao de prompts por IA."""
from __future__ import annotations

from src import config, job_manager, prompt_builder


def test_tarefas_por_tipo_cobre_todos_os_tipos_de_config():
    assert set(prompt_builder.TAREFAS_POR_TIPO.keys()) == set(config.TIPOS_TAREFA.keys())


def test_construir_prompt_contem_secoes_obrigatorias_para_cada_ia():
    for ia in config.IAS:
        texto = prompt_builder.construir_prompt(
            ia=ia,
            tipo_tarefa="analise_juridica",
            cliente="Cliente Teste",
            resumo="Resumo do caso de teste.",
        )
        assert "Papel da IA" in texto
        assert "Limitacoes obrigatorias" in texto
        assert "Nao invente fatos" in texto
        assert "Checklist final" in texto
        assert config.ASSINATURA in texto


def test_gerar_e_salvar_prompt_cria_arquivo_no_trabalho_e_na_fila(workspace):
    job_id = job_manager.criar_trabalho("analise_juridica", "Cliente Teste", "resumo", ["chatgpt"])

    texto = prompt_builder.gerar_e_salvar_prompt(job_id, "chatgpt")

    caminho_trabalho = job_manager.caminho_trabalho(job_id) / "prompt_chatgpt.md"
    assert caminho_trabalho.exists()
    assert caminho_trabalho.read_text(encoding="utf-8") == texto

    fila = config.FILA_PARA["chatgpt"]
    caminho_fila = config.PASTA_FILAS / fila / f"{job_id}.md"
    assert caminho_fila.exists()
