"""
Painel local FastAPI - AUTOMACOES_PAIZANTE_WEB_AI_SEM_API.

Roda 100% local (bind 127.0.0.1:8000). Nao envia nada automaticamente para
ChatGPT/Claude/Gemini: apenas gera prompts, copia para a area de
transferencia e abre a IA no Chrome para o usuario colar e enviar
manualmente. As respostas sao coladas pelo usuario nos campos do painel.
"""
from __future__ import annotations

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
PAINEL_DIR = APP_DIR.parent
BASE_DIR = PAINEL_DIR.parent
SRC_DIR = BASE_DIR / "05_SCRIPTS_PYTHON"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src import (  # noqa: E402
    browser_launcher,
    checklist_protocolo,
    clipboard_tools,
    config,
    file_utils,
    job_manager,
    organizador_clientes,
    prompt_builder,
    response_collector,
    response_comparer,
    response_consolidator,
)

app = FastAPI(title="Painel Local - Automacoes Paizante Web AI")

app.mount("/static", StaticFiles(directory=str(PAINEL_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(PAINEL_DIR / "templates"))

IAS = ["chatgpt", "claude", "gemini"]


def _ctx(request: Request, **extra):
    base = {
        "request": request,
        "tipos_tarefa": config.TIPOS_TAREFA,
        "assinatura": config.ASSINATURA,
        "base_dir": str(config.BASE_DIR),
    }
    base.update(extra)
    return base


@app.get("/")
def home(request: Request):
    trabalhos = job_manager.listar_trabalhos()
    clientes = organizador_clientes.listar_clientes()
    return templates.TemplateResponse(
        "index.html", _ctx(request, trabalhos=trabalhos, clientes=clientes)
    )


@app.get("/novo")
def novo_trabalho_form(request: Request):
    clientes = organizador_clientes.listar_clientes()
    return templates.TemplateResponse("novo_trabalho.html", _ctx(request, clientes=clientes, ias=IAS))


@app.post("/novo")
def novo_trabalho_criar(
    tipo_tarefa: str = Form(...),
    cliente: str = Form(...),
    cliente_novo: str = Form(""),
    resumo: str = Form(""),
    ia_chatgpt: bool = Form(False),
    ia_claude: bool = Form(False),
    ia_gemini: bool = Form(False),
):
    cliente_final = cliente_novo.strip() if cliente == "__novo__" and cliente_novo.strip() else cliente
    if cliente_final and cliente_final != "__novo__":
        organizador_clientes.criar_cliente(cliente_final)
    ias_selecionadas = [ia for ia, marcado in [
        ("chatgpt", ia_chatgpt), ("claude", ia_claude), ("gemini", ia_gemini)
    ] if marcado]
    job_id = job_manager.criar_trabalho(tipo_tarefa, cliente_final, resumo, ias_selecionadas)
    return RedirectResponse(url=f"/trabalho/{job_id}", status_code=303)


@app.get("/trabalho/{job_id}")
def ver_trabalho(request: Request, job_id: str):
    trabalho = job_manager.carregar_trabalho(job_id)
    prompts = {ia: job_manager.ler_arquivo_trabalho(job_id, f"prompt_{ia}.md") for ia in IAS}
    respostas = {ia: job_manager.ler_arquivo_trabalho(job_id, f"resposta_{ia}.md") for ia in IAS}
    comparativo = job_manager.ler_arquivo_trabalho(job_id, "comparativo.md")
    consolidado = job_manager.ler_arquivo_trabalho(job_id, "consolidado.md")
    final = job_manager.ler_arquivo_trabalho(job_id, "final.md")
    checklist = job_manager.ler_arquivo_trabalho(job_id, "checklist.md")
    log = job_manager.ler_arquivo_trabalho(job_id, "log.md")
    return templates.TemplateResponse(
        "trabalho.html",
        _ctx(
            request,
            trabalho=trabalho,
            job_id=job_id,
            ias=IAS,
            prompts=prompts,
            respostas=respostas,
            comparativo=comparativo,
            consolidado=consolidado,
            final=final,
            checklist=checklist,
            log=log,
        ),
    )


@app.post("/trabalho/{job_id}/gerar_prompt/{ia}")
def gerar_prompt(job_id: str, ia: str):
    prompt_builder.gerar_e_salvar_prompt(job_id, ia)
    job_manager.registrar_log(job_id, f"Prompt gerado para {ia}.")
    return RedirectResponse(url=f"/trabalho/{job_id}", status_code=303)


@app.post("/trabalho/{job_id}/copiar/{ia}")
def copiar_prompt(job_id: str, ia: str):
    texto = job_manager.ler_arquivo_trabalho(job_id, f"prompt_{ia}.md")
    clipboard_tools.copiar_para_clipboard(texto)
    clipboard_tools.registrar_copia(job_id, ia)
    job_manager.registrar_log(job_id, f"Prompt de {ia} copiado para a area de transferencia.")
    return RedirectResponse(url=f"/trabalho/{job_id}", status_code=303)


@app.post("/trabalho/{job_id}/abrir_ia/{ia}")
def abrir_ia(job_id: str, ia: str):
    browser_launcher.abrir_ia(ia)
    job_manager.registrar_log(job_id, f"Chrome aberto em {ia} (envio continua manual).")
    return RedirectResponse(url=f"/trabalho/{job_id}", status_code=303)


@app.post("/trabalho/{job_id}/registrar_envio/{ia}")
def registrar_envio(job_id: str, ia: str):
    job_manager.registrar_log(job_id, f"Envio manual confirmado pelo usuario para {ia}.")
    return RedirectResponse(url=f"/trabalho/{job_id}", status_code=303)


@app.post("/trabalho/{job_id}/resposta/{ia}")
def salvar_resposta(job_id: str, ia: str, resposta: str = Form("")):
    ok = response_collector.salvar_resposta(job_id, ia, resposta)
    if ok:
        job_manager.registrar_log(job_id, f"Resposta de {ia} salva.")
    else:
        job_manager.registrar_log(job_id, f"Tentativa de salvar resposta vazia de {ia} ignorada.")
    return RedirectResponse(url=f"/trabalho/{job_id}", status_code=303)


@app.post("/trabalho/{job_id}/comparar")
def comparar(job_id: str):
    response_comparer.comparar_respostas(job_id)
    job_manager.registrar_log(job_id, "Comparacao entre respostas gerada.")
    return RedirectResponse(url=f"/trabalho/{job_id}", status_code=303)


@app.post("/trabalho/{job_id}/consolidar")
def consolidar(job_id: str):
    response_consolidator.consolidar(job_id)
    job_manager.registrar_log(job_id, "Consolidacao gerada.")
    return RedirectResponse(url=f"/trabalho/{job_id}", status_code=303)


@app.post("/trabalho/{job_id}/final")
def gerar_final(job_id: str):
    response_consolidator.gerar_final(job_id)
    job_manager.registrar_log(job_id, "Versao final gerada (revisao humana ainda obrigatoria).")
    return RedirectResponse(url=f"/trabalho/{job_id}", status_code=303)


@app.post("/trabalho/{job_id}/checklist")
def gerar_checklist(job_id: str):
    checklist_protocolo.gerar_checklist_protocolo(job_id)
    job_manager.registrar_log(job_id, "Checklist de protocolo gerado.")
    return RedirectResponse(url=f"/trabalho/{job_id}", status_code=303)


@app.post("/trabalho/{job_id}/abrir_pasta")
def abrir_pasta_trabalho(job_id: str):
    pasta = job_manager.caminho_trabalho(job_id)
    file_utils.abrir_pasta(pasta)
    return RedirectResponse(url=f"/trabalho/{job_id}", status_code=303)


@app.post("/trabalho/{job_id}/backup")
def backup_trabalho(job_id: str):
    job_manager.fazer_backup_trabalho(job_id)
    job_manager.registrar_log(job_id, "Backup do trabalho gerado em 10_BACKUPS.")
    return RedirectResponse(url=f"/trabalho/{job_id}", status_code=303)


@app.get("/clientes")
def clientes_listar(request: Request):
    clientes = organizador_clientes.listar_clientes()
    return templates.TemplateResponse("clientes.html", _ctx(request, clientes=clientes))


@app.post("/clientes/novo")
def clientes_criar(nome: str = Form(...)):
    organizador_clientes.criar_cliente(nome)
    return RedirectResponse(url="/clientes", status_code=303)


@app.post("/clientes/{cliente}/abrir_pasta")
def abrir_pasta_cliente(cliente: str):
    pasta = config.PASTA_CLIENTES / cliente
    file_utils.abrir_pasta(pasta)
    return RedirectResponse(url="/clientes", status_code=303)
