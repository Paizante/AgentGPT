"""
Cliente do Ollama local (http://localhost:11434). Gratuito, 100% local,
sem API paga e sem enviar nenhum dado para fora da maquina - so fala com
o servico Ollama na propria maquina do usuario.

Usa apenas a biblioteca padrao (urllib) para nao adicionar dependencias
externas a um ambiente que ja teve problemas de instalacao Python.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request

from . import config
from .logger import get_logger

logger = get_logger("ollama_client")

TIMEOUT_STATUS = 3
TIMEOUT_CHAT = 180

MODELO_TEXTO_PADRAO = "llama3.1:8b"
MODELO_VISAO_PADRAO = "llama3.2-vision:11b"


def esta_disponivel() -> bool:
    try:
        urllib.request.urlopen(f"{config.URL_OLLAMA}/api/tags", timeout=TIMEOUT_STATUS)
        return True
    except (urllib.error.URLError, OSError):
        return False


def listar_modelos() -> list[str]:
    try:
        with urllib.request.urlopen(f"{config.URL_OLLAMA}/api/tags", timeout=TIMEOUT_STATUS) as resp:
            dados = json.loads(resp.read().decode("utf-8"))
        return [m.get("name", "") for m in dados.get("models", []) if m.get("name")]
    except (urllib.error.URLError, OSError, json.JSONDecodeError):
        return []


def escolher_modelo(tem_imagem: bool) -> str | None:
    """Escolhe automaticamente um modelo instalado adequado: modelo com
    visao se houver imagem anexada, modelo de texto nos demais casos."""
    instalados = listar_modelos()
    if not instalados:
        return None

    if tem_imagem:
        for candidato in instalados:
            if "vision" in candidato or "llava" in candidato:
                return candidato
        return None  # nenhum modelo com visao instalado

    for candidato in (MODELO_TEXTO_PADRAO, "qwen2.5:7b", "mistral", "phi3"):
        if candidato in instalados:
            return candidato
    return instalados[0]


def enviar_chat(modelo: str, mensagens: list[dict]) -> str:
    """Envia o historico de mensagens (formato {"role", "content", "images"?})
    para o Ollama local e retorna o texto da resposta. Levanta RuntimeError
    com mensagem amigavel em caso de falha de conexao."""
    corpo = json.dumps({"model": modelo, "messages": mensagens, "stream": False}).encode("utf-8")
    requisicao = urllib.request.Request(
        f"{config.URL_OLLAMA}/api/chat",
        data=corpo,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(requisicao, timeout=TIMEOUT_CHAT) as resp:
            dados = json.loads(resp.read().decode("utf-8"))
        return dados.get("message", {}).get("content", "").strip()
    except (urllib.error.URLError, OSError) as exc:
        logger.warning(f"Falha ao falar com Ollama local: {exc}")
        raise RuntimeError(
            "Nao foi possivel falar com o Ollama local (http://localhost:11434). "
            "Verifique se ele esta instalado e rodando (veja 09_OLLAMA_LOCAL)."
        ) from exc
