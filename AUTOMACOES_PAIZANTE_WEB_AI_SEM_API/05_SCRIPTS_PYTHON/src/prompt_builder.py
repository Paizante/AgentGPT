"""
Construtor de prompts especificos por IA.

Cada IA recebe um prompt com perfil diferente:

- ChatGPT: raciocinio juridico, estrategia de caso, construcao de tese,
  redacao final de peca, matriz fato-prova-direito-pedido, argumentacao
  persuasiva, esquemas de Visual Law, mapeamento de riscos e simulacao de
  decisao.
- Claude: analise longa de documentos, reestruturacao e clareza de texto,
  revisao extensa, comparacao detalhada entre versoes, prompts para
  Claude Code (execucao local de arquivos/scripts), checagem de
  consistencia interna e refinamento fino de redacao.
- Gemini: documentos longos, conteudo multimodal (imagens, PDFs grandes),
  resumo extenso, extracao de dados estruturados e preparacao de resumos.
- Claude Code: execucao local - arquivos, codigo, pastas, PDF/DOCX,
  planilhas, scripts, workflows n8n, backups e relatorios.

Todo prompt gerado inclui: contexto, papel da IA, objetivo, documentos
disponiveis, limitacoes, tarefas exatas, formato de saida, checklist final
e os pedidos de nao inventar fatos, apontar lacunas, distinguir
fato/inferencia/opiniao, indicar pontos frageis e sugerir melhorias.
"""
from __future__ import annotations

from . import config, job_manager

PAPEL_POR_IA = {
    "chatgpt": (
        "Voce atua como assistente de raciocinio juridico estrategico: "
        "construcao de tese, argumentacao persuasiva, matriz "
        "fato-prova-direito-pedido, redacao final de peca, esquemas de "
        "Visual Law, mapeamento de riscos e simulacao de possiveis "
        "decisoes judiciais/administrativas."
    ),
    "claude": (
        "Voce atua como revisor(a) e analista de textos longos: analise "
        "extensa de documentos, reestruturacao e clareza de redacao, "
        "comparacao detalhada entre versoes de um texto, checagem de "
        "consistencia interna e refinamento fino da linguagem juridica."
    ),
    "gemini": (
        "Voce atua como processador de documentos longos e multimodais: "
        "leitura de PDFs grandes e imagens, resumo extenso, extracao de "
        "dados estruturados (datas, valores, partes, numeros de processo) "
        "e preparacao de resumos de apoio para as demais etapas."
    ),
}

INSTRUCOES_PADRAO = """
## Papel da IA
{papel}

## Objetivo da tarefa
Tipo de tarefa: {tipo_tarefa}
Cliente (referencia interna, nao publicar): {cliente}

## Contexto e resumo do caso
{resumo}

## Documentos disponiveis
- Os documentos do caso estao organizados localmente em
  04_DOCUMENTOS/clientes/{cliente}/. Caso precise de um documento
  especifico que nao foi colado aqui, informe explicitamente que ele e
  necessario e qual e o documento, em vez de presumir o conteudo.

## Limitacoes obrigatorias
- Nao invente fatos, numeros, datas, nomes, valores ou jurisprudencia.
- Se faltar informacao para responder com seguranca, diga exatamente o
  que falta (lacuna), em vez de preencher com suposicoes.
- Distinga claramente, ao longo da resposta: (a) FATO (o que esta
  comprovado nos documentos/contexto), (b) INFERENCIA (conclusao logica
  a partir dos fatos, mas nao explicitamente provada) e (c) OPINIAO
  (juizo de valor ou recomendacao estrategica).
- Se citar legislacao ou jurisprudencia, identifique a fonte e, se nao
  tiver certeza de que esta atualizada, recomende explicitamente que o
  advogado confirme a vigencia/atualidade antes de usar.
- Aponte pontos frageis do raciocinio ou da peca e sugira melhorias
  concretas.

## Tarefas exatas
{tarefas}

## Formato de saida esperado
1. Resumo executivo (3-5 linhas).
2. Desenvolvimento (organizado por topicos/secoes).
3. Fatos x Inferencias x Opinioes (lista separada).
4. Riscos e pontos frageis identificados.
5. Lacunas (o que falta para concluir com seguranca).
6. Sugestoes de melhoria.
7. Texto final pronto para revisao humana (quando aplicavel), terminando
   com a assinatura: {assinatura}

## Checklist final (responda sim/nao para cada item antes de encerrar)
- [ ] Não inventei fatos nem jurisprudencia.
- [ ] Apontei as lacunas que encontrei.
- [ ] Separei fato, inferencia e opiniao.
- [ ] Indiquei os pontos frageis da analise/peca.
- [ ] Sugeri melhorias concretas.
""".strip()

TAREFAS_POR_TIPO = {
    "analise_juridica": "Faca uma analise juridica completa do caso descrito, identificando teses possiveis, riscos e proximos passos.",
    "revisao_peca": "Revise a peca/redacao fornecida quanto a clareza, consistencia, fundamentacao e eventuais riscos processuais.",
    "criacao_peticao": "Redija uma peticao completa para o caso descrito, com fundamentacao, pedidos principais e subsidiarios.",
    "requerimento_administrativo": "Redija um requerimento administrativo adequado ao caso, com fundamentacao e pedido claros.",
    "loas_bpc": "Monte um requerimento/peticao de LOAS/BPC, incluindo requisitos legais, prova de hipossuficiencia e pedido.",
    "auxilio_doenca": "Monte um requerimento/peticao de auxilio-doenca/incapacidade, incluindo nexo, incapacidade e pedido.",
    "reclamacao_trabalhista": "Redija uma reclamacao trabalhista com qualificacao das partes, fatos, fundamentos e pedidos.",
    "mandado_seguranca": "Redija um mandado de seguranca, identificando ato coator, direito liquido e certo, e pedido de liminar se cabivel.",
    "procuracao": "Redija uma procuracao adequada ao caso, com poderes especificos quando necessario.",
    "contrato_honorarios": "Redija um contrato de honorarios adequado ao caso, com forma de pagamento e clausulas essenciais.",
    "declaracao": "Redija a declaracao necessaria para o caso (ex.: hipossuficiencia, residencia, uniao estavel etc.).",
    "organizacao_documental": "Sugira a melhor forma de organizar e nomear os documentos deste caso para protocolo.",
    "analise_documentos": "Analise os documentos descritos/colados e extraia os pontos juridicamente relevantes.",
    "prompt_claude_code": "Gere um prompt detalhado para o Claude Code executar localmente a tarefa tecnica descrita.",
    "automacao_n8n": "Descreva o workflow n8n necessario (gatilhos, etapas, nós) para automatizar a tarefa local descrita.",
    "edicao_video": "Descreva o roteiro de cortes/edicao para o video descrito (reels/highlights/cortes virais).",
    "relatorio_reuniao": "Gere um relatorio estruturado da reuniao descrita, com decisoes, pendencias e responsaveis.",
    "resumo_emails": "Gere um resumo executivo dos e-mails/conversas descritas, destacando pendencias e prazos.",
    "plano_de_acao": "Gere um plano de acao com etapas, responsaveis e prazos para o objetivo descrito.",
    "comparacao_ias": "Compare as respostas fornecidas de diferentes IAs, indicando divergencias e a melhor versao combinada.",
}


def construir_prompt(ia: str, tipo_tarefa: str, cliente: str, resumo: str, contexto_extra: str = "") -> str:
    papel = PAPEL_POR_IA.get(ia, PAPEL_POR_IA["chatgpt"])
    tarefas = TAREFAS_POR_TIPO.get(tipo_tarefa, "Execute a tarefa descrita no resumo do caso, com rigor tecnico-juridico.")
    if contexto_extra:
        tarefas = f"{tarefas}\n\nContexto adicional:\n{contexto_extra}"
    texto = INSTRUCOES_PADRAO.format(
        papel=papel,
        tipo_tarefa=config.TIPOS_TAREFA.get(tipo_tarefa, tipo_tarefa),
        cliente=cliente,
        resumo=resumo or "(resumo nao informado - preencha antes de enviar)",
        tarefas=tarefas,
        assinatura=config.ASSINATURA,
    )
    return texto


def gerar_e_salvar_prompt(job_id: str, ia: str) -> str:
    dados = job_manager.carregar_trabalho(job_id)
    texto = construir_prompt(
        ia=ia,
        tipo_tarefa=dados.get("tipo_tarefa", ""),
        cliente=dados.get("cliente", ""),
        resumo=dados.get("resumo", ""),
    )
    job_manager.escrever_arquivo_trabalho(job_id, f"prompt_{ia}.md", texto)

    fila = config.FILA_PARA.get(ia)
    if fila:
        destino = config.PASTA_FILAS / fila / f"{job_id}.md"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto, encoding="utf-8")

    return texto
