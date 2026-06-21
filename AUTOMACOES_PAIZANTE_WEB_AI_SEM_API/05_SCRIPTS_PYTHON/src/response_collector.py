"""
Coleta de respostas de IA coladas manualmente pelo usuario. Nunca busca a
resposta automaticamente em nenhum site - o texto sempre chega colado
pelo usuario (painel local ou menu de linha de comando).
"""
from __future__ import annotations

from datetime import datetime

from . import config, job_manager
from .logger import get_logger

logger = get_logger("response_collector")


def salvar_resposta(job_id: str, ia: str, texto: str) -> bool:
    texto = (texto or "").strip()
    if not texto:
        logger.warning(f"Resposta vazia ignorada para job={job_id} ia={ia}.")
        return False

    nome_arquivo = f"resposta_{ia}.md"
    cabecalho = (
        f"<!-- origem: {ia} | salvo em: "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->\n\n"
    )
    job_manager.escrever_arquivo_trabalho(job_id, nome_arquivo, cabecalho + texto)

    fila = config.FILA_RETORNO.get(ia)
    if fila:
        destino = config.PASTA_FILAS / fila / f"{job_id}.md"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(cabecalho + texto, encoding="utf-8")

    job_manager.atualizar_metadata(job_id, **{f"resposta_{ia}_salva_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    logger.info(f"Resposta de {ia} salva para o trabalho {job_id}.")
    return True


def resposta_existe(job_id: str, ia: str) -> bool:
    texto = job_manager.ler_arquivo_trabalho(job_id, f"resposta_{ia}.md")
    return bool(texto.strip())


def respostas_disponiveis(job_id: str) -> list[str]:
    return [ia for ia in config.IAS if resposta_existe(job_id, ia)]
