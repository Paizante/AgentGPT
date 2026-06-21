# Prompt Mestre: Checar Alucinacoes

## Contexto
Verificacao especifica de possiveis alucinacoes (informacoes inventadas)
em uma resposta de IA, antes de uso no escritorio do Dr. Gustavo
Paizante (OAB/MG 180.822).

## Papel da IA
Verificador(a) de fidelidade factual.

## Dados de entrada
- Contexto/fonte original (documentos, resumo do caso):
- Resposta da IA a verificar:

## Limitacoes obrigatorias
- Compare apenas com o contexto/fonte fornecidos; se nao houver fonte
  para checar algo, marque como "nao verificavel com o material
  disponivel" em vez de presumir certo ou errado.

## Tarefas exatas
1. Para cada afirmacao factual relevante na resposta, verifique se ela
   esta sustentada pelo contexto/fonte fornecido.
2. Classifique cada afirmacao como: "sustentada pela fonte", "nao
   sustentada/possivel alucinacao" ou "nao verificavel com o material
   disponivel".
3. Para citacoes de lei/jurisprudencia, marque sempre como "verificar
   atualidade externamente", pois a IA pode estar desatualizada.

## Formato de saida
1. Tabela: afirmacao -> classificacao -> observacao.
2. Lista de afirmacoes que precisam de verificacao externa antes de usar
   a resposta.

## CONTEXTO/FONTE
(cole aqui)

## RESPOSTA A VERIFICAR
(cole aqui)
