"""
Configuracao central da Automacoes Paizante Web AI Sem API.

Detecta a pasta base do projeto de forma robusta: primeiro tenta inferir
a partir da localizacao deste arquivo (funciona tanto no checkout do
repositorio quanto depois de copiado para o Windows); se nao conseguir,
cai para `$env:USERPROFILE\\Documents\\AUTOMACOES_PAIZANTE_WEB_AI_SEM_API`
(ou `$HOME` em sistemas Unix), sem nunca assumir um nome fixo de usuario.
"""
from __future__ import annotations

import os
from pathlib import Path


def _detectar_base_dir() -> Path:
    aqui = Path(__file__).resolve()
    candidata = aqui.parent.parent.parent  # src -> 05_SCRIPTS_PYTHON -> BASE
    if (candidata / "04_DOCUMENTOS").exists() and (candidata / "07_PROMPTS_MESTRES").exists():
        return candidata

    perfil_usuario = os.environ.get("USERPROFILE") or os.environ.get("HOME") or str(Path.home())
    return Path(perfil_usuario) / "Documents" / "AUTOMACOES_PAIZANTE_WEB_AI_SEM_API"


BASE_DIR = _detectar_base_dir()

PASTA_PAINEL = BASE_DIR / "01_PAINEL_LOCAL"
PASTA_TRABALHOS = PASTA_PAINEL / "data" / "trabalhos"
PASTA_CHROME_WORKSPACE = BASE_DIR / "02_CHROME_WORKSPACE"
PASTA_FILAS = BASE_DIR / "03_FILAS_DE_TRABALHO"
PASTA_DOCUMENTOS = BASE_DIR / "04_DOCUMENTOS"
PASTA_ENTRADA = PASTA_DOCUMENTOS / "entrada"
PASTA_CLIENTES = PASTA_DOCUMENTOS / "clientes"
PASTA_SAIDA = PASTA_DOCUMENTOS / "saida"
PASTA_SCRIPTS_PYTHON = BASE_DIR / "05_SCRIPTS_PYTHON"
PASTA_N8N = BASE_DIR / "06_N8N_LOCAL"
PASTA_PROMPTS_MESTRES = BASE_DIR / "07_PROMPTS_MESTRES"
PASTA_MODELOS_JURIDICOS = BASE_DIR / "08_MODELOS_JURIDICOS"
PASTA_OLLAMA = BASE_DIR / "09_OLLAMA_LOCAL"
PASTA_BACKUPS = BASE_DIR / "10_BACKUPS"
PASTA_LOGS = BASE_DIR / "11_LOGS"
PASTA_RELATORIOS = BASE_DIR / "12_RELATORIOS"

ASSINATURA = "Dr. Gustavo Paizante - OAB/MG 180.822"

IAS = ["chatgpt", "claude", "gemini"]

URLS_IA = {
    "chatgpt": "https://chatgpt.com",
    "claude": "https://claude.ai",
    "gemini": "https://gemini.google.com",
}
URL_PAINEL = "http://localhost:8000"
URL_N8N = "http://localhost:5678"
URL_OLLAMA = "http://localhost:11434"

FILA_PARA = {
    "chatgpt": "01_para_chatgpt",
    "claude": "03_para_claude",
    "gemini": "05_para_gemini",
}
FILA_RETORNO = {
    "chatgpt": "02_retorno_chatgpt",
    "claude": "04_retorno_claude",
    "gemini": "06_retorno_gemini",
}
FILA_COMPARACAO = "07_comparacao"
FILA_CONSOLIDADO = "08_consolidado"
FILA_FINAL = "09_final"

TIPOS_TAREFA = {
    "analise_juridica": "Analise juridica",
    "revisao_peca": "Revisao de peca",
    "criacao_peticao": "Criacao de peticao",
    "requerimento_administrativo": "Requerimento administrativo",
    "loas_bpc": "LOAS / BPC",
    "auxilio_doenca": "Auxilio-doenca",
    "reclamacao_trabalhista": "Reclamacao trabalhista",
    "mandado_seguranca": "Mandado de seguranca",
    "procuracao": "Procuracao",
    "contrato_honorarios": "Contrato de honorarios",
    "declaracao": "Declaracao",
    "organizacao_documental": "Organizacao documental",
    "analise_documentos": "Analise de documentos",
    "prompt_claude_code": "Prompt para Claude Code",
    "automacao_n8n": "Automacao n8n",
    "edicao_video": "Edicao de video",
    "relatorio_reuniao": "Relatorio de reuniao",
    "resumo_emails": "Resumo de e-mails",
    "plano_de_acao": "Plano de acao",
    "comparacao_ias": "Comparacao entre IAs",
}

PADRAO_NOMES_DOCUMENTOS = [
    "01_Documento_Identificacao",
    "02_CPF",
    "03_Comprovante_Endereco",
    "04_Relatorio_Medico",
    "05_CadUnico",
    "06_Procuracao",
    "07_Hipossuficiencia",
    "08_Requerimento",
]


def garantir_estrutura_minima() -> None:
    for pasta in [
        PASTA_TRABALHOS, PASTA_CLIENTES, PASTA_LOGS, PASTA_BACKUPS, PASTA_RELATORIOS,
    ]:
        pasta.mkdir(parents=True, exist_ok=True)
