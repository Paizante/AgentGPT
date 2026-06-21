"""
Chat estilo ChatGPT com a IA local (Ollama), por trabalho. O historico de
cada trabalho fica em data/trabalhos/<job_id>/chat.json. A IA local nunca
substitui o fluxo manual com ChatGPT/Claude/Gemini nem a revisao humana -
e uma ferramenta extra, gratuita e 100% local, para conversar sobre
anexos (documentos/fotos/imagens) e tarefas simples do dia a dia.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from . import anexo_manager, job_manager, ollama_client
from .logger import get_logger

logger = get_logger("chat_manager")

SYSTEM_PROMPT = (
    "Voce e uma IA local, gratuita e 100% offline, que roda no computador "
    "do usuario (Ollama) dentro de um painel de apoio juridico. Quando o "
    "usuario anexar um documento, foto ou imagem, NUNCA presuma de que "
    "caso ou assunto se trata: pergunte primeiro ao usuario o que e aquele "
    "anexo e para qual finalidade ele quer a analise, antes de dar "
    "qualquer conclusao. Nao invente fatos, numeros, nomes ou "
    "jurisprudencia. Se faltar contexto, diga exatamente o que falta. "
    "Voce nao substitui o ChatGPT/Claude/Gemini para redacao final de "
    "peca nem a revisao humana obrigatoria do advogado."
)


def caminho_chat(job_id: str) -> Path:
    return job_manager.caminho_trabalho(job_id) / "chat.json"


def carregar_chat(job_id: str) -> list[dict]:
    caminho = caminho_chat(job_id)
    if not caminho.exists():
        return []
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def _salvar_chat(job_id: str, mensagens: list[dict]) -> None:
    caminho = caminho_chat(job_id)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(mensagens, ensure_ascii=False, indent=2), encoding="utf-8")


def limpar_chat(job_id: str) -> None:
    """Arquiva o chat atual (nunca apaga) e comeca um historico novo."""
    caminho = caminho_chat(job_id)
    if caminho.exists():
        selo = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho.rename(caminho.parent / f"chat_arquivado_{selo}.json")


def enviar_mensagem(
    job_id: str,
    texto_usuario: str,
    anexos: list[tuple[str, bytes]] | None = None,
) -> dict:
    """Salva a mensagem do usuario (com anexos, se houver), chama a IA
    local e salva/retorna a resposta. anexos: lista de (nome_arquivo, conteudo_bytes)."""
    anexos = anexos or []
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nomes_anexos: list[str] = []
    imagens_base64: list[str] = []
    textos_extraidos: list[str] = []
    tem_imagem = False

    for nome_arquivo, conteudo in anexos:
        if not nome_arquivo:
            continue
        destino = anexo_manager.salvar_anexo(job_id, nome_arquivo, conteudo)
        nomes_anexos.append(destino.name)
        if anexo_manager.eh_imagem(destino):
            tem_imagem = True
            imagens_base64.append(anexo_manager.imagem_para_base64(destino))
        else:
            texto = anexo_manager.extrair_texto(destino)
            if texto:
                textos_extraidos.append(f"--- Conteudo de {destino.name} ---\n{texto}")

    mensagens = carregar_chat(job_id)

    conteudo_usuario = texto_usuario or "(mensagem vazia - apenas anexo enviado)"
    if textos_extraidos:
        conteudo_usuario = f"{conteudo_usuario}\n\n" + "\n\n".join(textos_extraidos)

    mensagem_usuario = {
        "role": "user",
        "texto": texto_usuario,
        "anexos": nomes_anexos,
        "hora": agora,
    }
    mensagens.append(mensagem_usuario)

    modelo = ollama_client.escolher_modelo(tem_imagem)
    if modelo is None:
        resposta_texto = (
            "Nenhum modelo Ollama compativel esta instalado ainda. "
            + ("Para analisar imagens, instale um modelo com visao, ex.: `ollama pull llama3.2-vision:11b`. "
               if tem_imagem else "Instale um modelo de texto, ex.: `ollama pull llama3.1:8b`. ")
            + "Veja 09_OLLAMA_LOCAL/modelos_recomendados.md."
        )
    else:
        historico_ollama = [{"role": "system", "content": SYSTEM_PROMPT}]
        for m in mensagens[:-1]:
            historico_ollama.append({"role": m["role"], "content": m["texto"]})
        ultima = {"role": "user", "content": conteudo_usuario}
        if imagens_base64:
            ultima["images"] = imagens_base64
        historico_ollama.append(ultima)

        try:
            resposta_texto = ollama_client.enviar_chat(modelo, historico_ollama)
        except RuntimeError as exc:
            resposta_texto = str(exc)

    mensagem_assistente = {
        "role": "assistant",
        "texto": resposta_texto,
        "anexos": [],
        "hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    mensagens.append(mensagem_assistente)

    _salvar_chat(job_id, mensagens)
    job_manager.registrar_log(job_id, "Mensagem enviada ao chat com a IA local (Ollama).")
    return mensagem_assistente
