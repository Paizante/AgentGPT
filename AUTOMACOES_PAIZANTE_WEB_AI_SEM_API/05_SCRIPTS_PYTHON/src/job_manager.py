"""
Gerenciador de trabalhos (jobs) da central Automacoes Paizante Web AI.

Cada trabalho recebe um ID no formato YYYYMMDD_HHMMSS_tipo_cliente e uma
pasta canonica em 01_PAINEL_LOCAL/data/trabalhos/<job_id>/ contendo:
metadata.yaml, contexto.md, prompt_<ia>.md, resposta_<ia>.md,
comparativo.md, consolidado.md, final.md, checklist.md e log.md.

Esses arquivos tambem sao espelhados nas filas de
03_FILAS_DE_TRABALHO para visibilidade operacional, mas a pasta do
trabalho e sempre a fonte de verdade.
"""
from __future__ import annotations

import re
import shutil
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml

from . import config

ARQUIVOS_BASE = [
    "contexto.md",
    "prompt_chatgpt.md",
    "prompt_claude.md",
    "prompt_gemini.md",
    "resposta_chatgpt.md",
    "resposta_claude.md",
    "resposta_gemini.md",
    "comparativo.md",
    "consolidado.md",
    "final.md",
    "checklist.md",
    "log.md",
]


def _slug(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode("ascii")
    texto = re.sub(r"[^a-zA-Z0-9]+", "_", texto).strip("_").lower()
    return texto or "sem_nome"


def novo_id(tipo_tarefa: str, cliente: str) -> str:
    agora = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{agora}_{_slug(tipo_tarefa)}_{_slug(cliente)}"


def caminho_trabalho(job_id: str) -> Path:
    return config.PASTA_TRABALHOS / job_id


def criar_trabalho(tipo_tarefa: str, cliente: str, resumo: str, ias: list[str]) -> str:
    job_id = novo_id(tipo_tarefa, cliente)
    pasta = caminho_trabalho(job_id)
    pasta.mkdir(parents=True, exist_ok=True)

    for nome_arquivo in ARQUIVOS_BASE:
        destino = pasta / nome_arquivo
        if not destino.exists():
            destino.write_text("", encoding="utf-8")

    metadata = {
        "job_id": job_id,
        "tipo_tarefa": tipo_tarefa,
        "cliente": cliente,
        "resumo": resumo,
        "ias": ias,
        "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "criado",
    }
    (pasta / "metadata.yaml").write_text(
        yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    (pasta / "contexto.md").write_text(
        f"# Contexto do trabalho {job_id}\n\nCliente: {cliente}\n\nResumo:\n\n{resumo}\n",
        encoding="utf-8",
    )

    registrar_log(job_id, f"Trabalho criado (tipo={tipo_tarefa}, cliente={cliente}, ias={ias}).")
    return job_id


def carregar_trabalho(job_id: str) -> dict:
    pasta = caminho_trabalho(job_id)
    metadata_path = pasta / "metadata.yaml"
    if not metadata_path.exists():
        return {"job_id": job_id, "tipo_tarefa": "?", "cliente": "?", "resumo": "", "ias": [], "criado_em": "?"}
    dados = yaml.safe_load(metadata_path.read_text(encoding="utf-8")) or {}
    dados.setdefault("ias", [])
    return dados


def listar_trabalhos() -> list[dict]:
    if not config.PASTA_TRABALHOS.exists():
        return []
    trabalhos = []
    for pasta in sorted(config.PASTA_TRABALHOS.iterdir(), reverse=True):
        if pasta.is_dir() and (pasta / "metadata.yaml").exists():
            trabalhos.append(carregar_trabalho(pasta.name))
    return trabalhos


def ler_arquivo_trabalho(job_id: str, nome_arquivo: str) -> str:
    caminho = caminho_trabalho(job_id) / nome_arquivo
    if not caminho.exists():
        return ""
    return caminho.read_text(encoding="utf-8")


def escrever_arquivo_trabalho(job_id: str, nome_arquivo: str, conteudo: str) -> None:
    pasta = caminho_trabalho(job_id)
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / nome_arquivo).write_text(conteudo, encoding="utf-8")


def atualizar_metadata(job_id: str, **campos) -> None:
    dados = carregar_trabalho(job_id)
    dados.update(campos)
    (caminho_trabalho(job_id) / "metadata.yaml").write_text(
        yaml.safe_dump(dados, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )


def registrar_log(job_id: str, mensagem: str) -> None:
    pasta = caminho_trabalho(job_id)
    pasta.mkdir(parents=True, exist_ok=True)
    linha = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {mensagem}\n"
    with open(pasta / "log.md", "a", encoding="utf-8") as f:
        f.write(linha)


def fazer_backup_trabalho(job_id: str) -> Optional[Path]:
    origem = caminho_trabalho(job_id)
    if not origem.exists():
        return None
    destino_raiz = config.PASTA_BACKUPS / "documentos" / "trabalhos"
    destino_raiz.mkdir(parents=True, exist_ok=True)
    selo = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = destino_raiz / f"{job_id}__backup_{selo}"
    shutil.copytree(origem, destino)
    return destino
