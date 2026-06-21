"""Testes do chat com a IA local. O Ollama em si e mockado - estes testes
nao dependem de nenhum servico externo nem de rede."""
from __future__ import annotations

from src import chat_manager, job_manager, ollama_client


def test_enviar_mensagem_sem_ollama_disponivel_avisa_o_usuario(workspace, monkeypatch):
    job_id = job_manager.criar_trabalho("analise_juridica", "Cliente", "resumo", [])
    monkeypatch.setattr(ollama_client, "escolher_modelo", lambda tem_imagem: None)

    resposta = chat_manager.enviar_mensagem(job_id, "Ola, pode me ajudar?")

    assert "Nenhum modelo Ollama" in resposta["texto"]
    historico = chat_manager.carregar_chat(job_id)
    assert len(historico) == 2
    assert historico[0]["role"] == "user"
    assert historico[1]["role"] == "assistant"


def test_enviar_mensagem_com_ollama_disponivel_chama_modelo_de_texto(workspace, monkeypatch):
    job_id = job_manager.criar_trabalho("analise_juridica", "Cliente", "resumo", [])
    monkeypatch.setattr(ollama_client, "escolher_modelo", lambda tem_imagem: "llama3.1:8b")
    monkeypatch.setattr(ollama_client, "enviar_chat", lambda modelo, mensagens: "Resposta da IA local.")

    resposta = chat_manager.enviar_mensagem(job_id, "Resuma este texto para mim.")

    assert resposta["texto"] == "Resposta da IA local."


def test_enviar_mensagem_com_anexo_de_imagem_aciona_modelo_de_visao(workspace, monkeypatch):
    job_id = job_manager.criar_trabalho("analise_juridica", "Cliente", "resumo", [])
    chamadas = {}

    def escolher_modelo(tem_imagem):
        chamadas["tem_imagem"] = tem_imagem
        return "llama3.2-vision:11b"

    def enviar_chat(modelo, mensagens):
        chamadas["mensagens"] = mensagens
        return "Antes de analisar, me diga: o que e essa imagem e qual e o caso?"

    monkeypatch.setattr(ollama_client, "escolher_modelo", escolher_modelo)
    monkeypatch.setattr(ollama_client, "enviar_chat", enviar_chat)

    resposta = chat_manager.enviar_mensagem(
        job_id, "O que tem nessa foto?", anexos=[("foto.jpg", b"dados-fake-de-imagem")]
    )

    assert chamadas["tem_imagem"] is True
    assert "images" in chamadas["mensagens"][-1]
    assert "o que e essa imagem" in resposta["texto"]

    historico = chat_manager.carregar_chat(job_id)
    assert historico[0]["anexos"] == ["foto.jpg"]


def test_limpar_chat_arquiva_em_vez_de_apagar(workspace, monkeypatch):
    job_id = job_manager.criar_trabalho("analise_juridica", "Cliente", "resumo", [])
    monkeypatch.setattr(ollama_client, "escolher_modelo", lambda tem_imagem: "llama3.1:8b")
    monkeypatch.setattr(ollama_client, "enviar_chat", lambda modelo, mensagens: "ok")
    chat_manager.enviar_mensagem(job_id, "mensagem antes de limpar")

    chat_manager.limpar_chat(job_id)

    assert chat_manager.carregar_chat(job_id) == []
    pasta = job_manager.caminho_trabalho(job_id)
    arquivados = list(pasta.glob("chat_arquivado_*.json"))
    assert len(arquivados) == 1
