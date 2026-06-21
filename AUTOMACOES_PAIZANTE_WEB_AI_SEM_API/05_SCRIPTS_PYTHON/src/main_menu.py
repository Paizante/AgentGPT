"""Menu interativo de linha de comando (usado por run.py)."""
from __future__ import annotations

from pathlib import Path

from rich.console import Console

from . import (
    browser_launcher,
    checklist_protocolo,
    clipboard_tools,
    config,
    job_manager,
    organizador_clientes,
    pdf_tools,
    prompt_builder,
    response_collector,
    response_comparer,
    response_consolidator,
)

console = Console()

OPCOES = """
 1 - Abrir painel local (instrucoes)
 2 - Abrir ChatGPT no Chrome
 3 - Abrir Claude no Chrome
 4 - Abrir Gemini no Chrome
 5 - Abrir todas as IAs no Chrome
 6 - Criar novo trabalho
 7 - Gerar prompts do trabalho
 8 - Copiar prompt para clipboard
 9 - Registrar resposta de uma IA
10 - Comparar respostas
11 - Consolidar respostas
12 - Organizar documentos de um cliente
13 - Unir PDFs
14 - Separar PDF
15 - Extrair texto de PDF
16 - Gerar checklist de protocolo
17 - Iniciar n8n (instrucoes)
18 - Gerar backup de um trabalho
19 - Rodar diagnostico do ambiente
20 - Sair
"""


def _pedir_job_id() -> str:
    return console.input("ID do trabalho: ").strip()


def executar_opcao(opcao: str) -> bool:
    """Retorna False quando o usuario escolhe sair."""
    if opcao == "1":
        console.print(f"Abra {config.URL_PAINEL} no navegador, ou rode 01_PAINEL_LOCAL/run_painel.ps1.")
    elif opcao == "2":
        browser_launcher.abrir_ia("chatgpt")
    elif opcao == "3":
        browser_launcher.abrir_ia("claude")
    elif opcao == "4":
        browser_launcher.abrir_ia("gemini")
    elif opcao == "5":
        browser_launcher.abrir_todas_ias()
    elif opcao == "6":
        tipo = console.input(f"Tipo de tarefa ({', '.join(config.TIPOS_TAREFA)}): ").strip()
        cliente = console.input("Cliente: ").strip()
        resumo = console.input("Resumo do caso: ").strip()
        ias_texto = console.input("IAs (separadas por virgula, ex: chatgpt,claude): ").strip()
        ias = [i.strip() for i in ias_texto.split(",") if i.strip()]
        job_id = job_manager.criar_trabalho(tipo, cliente, resumo, ias)
        console.print(f"Trabalho criado: {job_id}")
    elif opcao == "7":
        job_id = _pedir_job_id()
        for ia in config.IAS:
            prompt_builder.gerar_e_salvar_prompt(job_id, ia)
        console.print("Prompts gerados para chatgpt, claude e gemini.")
    elif opcao == "8":
        job_id = _pedir_job_id()
        ia = console.input("IA (chatgpt/claude/gemini): ").strip()
        texto = job_manager.ler_arquivo_trabalho(job_id, f"prompt_{ia}.md")
        clipboard_tools.copiar_para_clipboard(texto)
        console.print("Prompt copiado. Cole manualmente na IA, revise e envie voce mesmo.")
    elif opcao == "9":
        job_id = _pedir_job_id()
        ia = console.input("IA (chatgpt/claude/gemini): ").strip()
        console.print("Cole a resposta e finalize com uma linha contendo apenas: FIM")
        linhas = []
        while True:
            linha = console.input()
            if linha.strip() == "FIM":
                break
            linhas.append(linha)
        response_collector.salvar_resposta(job_id, ia, "\n".join(linhas))
        console.print("Resposta salva.")
    elif opcao == "10":
        job_id = _pedir_job_id()
        response_comparer.comparar_respostas(job_id)
        console.print("Comparacao gerada.")
    elif opcao == "11":
        job_id = _pedir_job_id()
        response_consolidator.consolidar(job_id)
        response_consolidator.gerar_final(job_id)
        console.print("Consolidacao e versao final geradas.")
    elif opcao == "12":
        cliente = console.input("Nome do cliente: ").strip()
        organizador_clientes.criar_cliente(cliente)
        console.print(f"Pasta do cliente garantida em {config.PASTA_CLIENTES / cliente}")
    elif opcao == "13":
        origem_texto = console.input("Caminhos dos PDFs (separados por ; ): ").strip()
        destino_texto = console.input("Caminho do PDF de destino: ").strip()
        caminhos = [Path(c.strip()) for c in origem_texto.split(";") if c.strip()]
        pdf_tools.unir_pdfs(caminhos, Path(destino_texto))
        console.print("PDFs unidos.")
    elif opcao == "14":
        origem = Path(console.input("Caminho do PDF a separar: ").strip())
        destino = Path(console.input("Pasta de destino: ").strip())
        pdf_tools.separar_pdf(origem, destino)
        console.print("PDF separado.")
    elif opcao == "15":
        origem = Path(console.input("Caminho do PDF: ").strip())
        texto = pdf_tools.extrair_texto(origem)
        console.print(texto[:2000])
    elif opcao == "16":
        job_id = _pedir_job_id()
        checklist_protocolo.gerar_checklist_protocolo(job_id)
        console.print("Checklist de protocolo gerado.")
    elif opcao == "17":
        console.print(f"Rode 06_N8N_LOCAL/start_n8n.ps1 e acesse {config.URL_N8N}")
    elif opcao == "18":
        job_id = _pedir_job_id()
        destino = job_manager.fazer_backup_trabalho(job_id)
        console.print(f"Backup gerado em {destino}")
    elif opcao == "19":
        console.print("Rode 12_RELATORIOS/diagnostico.ps1 no PowerShell para o diagnostico completo do Windows.")
    elif opcao == "20":
        return False
    else:
        console.print("Opcao invalida.")
    return True


def rodar_menu() -> None:
    config.garantir_estrutura_minima()
    continuar = True
    while continuar:
        console.print(OPCOES)
        opcao = console.input("Escolha uma opcao: ").strip()
        try:
            continuar = executar_opcao(opcao)
        except Exception as exc:
            console.print(f"[erro] {exc}")
