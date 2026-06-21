# LGPD e Sigilo Profissional

## Fundamento

A advocacia exige sigilo profissional (Estatuto da OAB, art. 7º, II e
Código de Ética e Disciplina da OAB) e o tratamento de dados pessoais de
clientes esta sujeito a Lei Geral de Protecao de Dados (Lei 13.709/2018).
Esta central foi desenhada para reduzir risco, nao para eliminar a
responsabilidade humana sobre cada envio de dado.

## Regras praticas adotadas

1. **Minimizacao.** Antes de gerar um prompt para qualquer IA externa
   (ChatGPT, Claude, Gemini), pergunte-se: este dado pessoal/sensivel é
   realmente necessario para a tarefa? Prefira anonimizar nomes, CPF,
   numero de processo e dados de saude quando o raciocinio juridico nao
   depender deles.
2. **Autorizacao humana explicita.** Nenhum script desta central envia
   documento, prompt ou dado automaticamente para ChatGPT, Claude ou
   Gemini. O envio so ocorre quando o proprio usuario cola e confirma na
   interface web da IA.
3. **Documentos sensiveis ficam locais por padrao.** Laudos medicos,
   documentos de identificacao e CadUnico permanecem em
   `04_DOCUMENTOS/clientes/<cliente>/` e só sao referenciados (nao
   necessariamente enviados na integra) nos prompts.
4. **Registro de uso.** Cada vez que um prompt e copiado e uma IA e
   aberta, a central registra data/hora e tipo de tarefa em log (sem
   registrar senha ou conteudo de autenticacao), permitindo auditoria
   posterior do que foi compartilhado.
5. **Backups locais e criptografaveis.** `10_BACKUPS` guarda copias
   localmente. Recomenda-se que o usuario habilite criptografia de disco
   (BitLocker) na maquina onde a central roda.
6. **Retencao e descarte.** Revise periodicamente
   `04_DOCUMENTOS/clientes/<cliente>/13_Backups` e `10_BACKUPS` para
   descartar dados que nao precisam mais ser retidos, conforme a politica
   de retencao do escritorio.
7. **Base legal.** Para tratamento de dados de clientes, a base legal
   tipica é execucao de contrato/mandato e cumprimento de obrigacao legal
   ou exercicio regular de direitos em processo judicial/administrativo
   (art. 7º, V e art. 11, II, "d", da LGPD, quando aplicavel a dado
   sensivel de saude).

## Checklist antes de colar um prompt em uma IA externa

- [ ] O prompt contem apenas os dados estritamente necessarios?
- [ ] Dados sensiveis (saude, biometria, dados de menores) foram
      minimizados ou anonimizados quando possivel?
- [ ] O cliente já foi informado/autorizou o uso de ferramentas de IA no
      caso (cláusula no contrato de honorários ou comunicação especifica)?
- [ ] A resposta da IA sera revisada por humano antes de qualquer uso
      processual?
