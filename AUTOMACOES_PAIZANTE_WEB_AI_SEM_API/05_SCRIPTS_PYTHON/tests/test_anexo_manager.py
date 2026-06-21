"""Testes do gerenciador de anexos do chat com a IA local."""
from __future__ import annotations

from src import anexo_manager, job_manager


def test_salvar_anexo_nunca_sobrescreve_arquivo_existente(workspace):
    job_id = job_manager.criar_trabalho("analise_juridica", "Cliente", "resumo", [])

    primeiro = anexo_manager.salvar_anexo(job_id, "documento.txt", b"conteudo 1")
    segundo = anexo_manager.salvar_anexo(job_id, "documento.txt", b"conteudo 2")

    assert primeiro != segundo
    assert primeiro.read_bytes() == b"conteudo 1"
    assert segundo.read_bytes() == b"conteudo 2"


def test_eh_imagem_identifica_extensoes_de_imagem(workspace):
    job_id = job_manager.criar_trabalho("analise_juridica", "Cliente", "resumo", [])
    foto = anexo_manager.salvar_anexo(job_id, "foto.jpg", b"dados-fake-de-imagem")
    texto = anexo_manager.salvar_anexo(job_id, "nota.txt", b"dados de texto")

    assert anexo_manager.eh_imagem(foto) is True
    assert anexo_manager.eh_imagem(texto) is False


def test_extrair_texto_le_arquivo_txt(workspace):
    job_id = job_manager.criar_trabalho("analise_juridica", "Cliente", "resumo", [])
    arquivo = anexo_manager.salvar_anexo(job_id, "nota.txt", "conteudo em texto".encode("utf-8"))

    assert anexo_manager.extrair_texto(arquivo) == "conteudo em texto"


def test_extrair_texto_de_imagem_retorna_vazio(workspace):
    job_id = job_manager.criar_trabalho("analise_juridica", "Cliente", "resumo", [])
    foto = anexo_manager.salvar_anexo(job_id, "foto.png", b"dados-fake-de-imagem")

    assert anexo_manager.extrair_texto(foto) == ""
