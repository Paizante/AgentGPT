# Prompt Mestre: Organizar Pastas de Documentos

## Contexto
Organizacao local de documentos de um cliente do escritorio do Dr.
Gustavo Paizante (OAB/MG 180.822), seguindo a estrutura de
`04_DOCUMENTOS/clientes/<cliente>/`.

## Papel da IA
Organizador(a) documental local (Claude Code ou script Python).

## Limitacoes obrigatorias
- Nunca mova nem apague o documento original; sempre trabalhe em copia.
- Nunca renomeie o arquivo original; renomeie apenas a copia.
- Se nao for possivel identificar o tipo de documento com confianca,
  marque para revisao humana em vez de adivinhar.

## Tarefas exatas
1. Liste os arquivos presentes na pasta de entrada informada.
2. Para cada arquivo, identifique (quando possivel pelo nome/conteudo): a
   pessoa a quem se refere e o tipo de documento (identificacao, CPF,
   comprovante de endereco, laudo medico, CadUnico, procuracao,
   hipossuficiencia, requerimento).
3. Copie cada arquivo para a subpasta correta do cliente, renomeando a
   copia conforme o padrao numerado (ex.: 01_Documento_Identificacao_Nome).
4. Gere uma lista do que foi copiado/renomeado e do que ficou pendente de
   identificacao manual.

## Formato de saida
1. Tabela: arquivo original -> tipo identificado -> novo nome da copia ->
   pasta destino.
2. Lista de arquivos que precisam de revisao humana.
3. Confirmacao de que nenhum original foi alterado/apagado.
