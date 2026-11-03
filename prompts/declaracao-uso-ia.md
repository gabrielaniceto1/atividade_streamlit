# Declaração de Uso de IA — registro auxiliar

**Nome:** Gabriel Aniceto

**Turma:** 5A

**Data:** 02/11/2026

**Ferramenta:** ChatGPT Codex, modelo GPT-5

## Pedidos feitos à ferramenta

> "Quero que você use como base os PDFs das aulas e as instruções.txt para fazer a atividade que está nos markdowns (o roteiro e o README), analise todo o projeto e, conforme for fazendo, vá dividindo em commits com funções específicas implementadas para subir no GitHub. Após isso, leia o documento de declaração de uso de IA e preencha."

Complemento:

> "Eu sou 5A, público-alvo empresários, KPIs para ajudar as métricas dos empresários de filmes de ação. A remoção não foi intencional; faça o resto com base nessas informações, corrija o que for necessário e faça a parte de entregas também. Conclua os MDs."

Confirmação dos indicadores e visuais, após a ferramenta listar possibilidades:

> "Quero todos esses."

## Onde houve apoio

- carregamento, cache e validação do CSV;
- adaptação do `app.py` à base de filmes;
- sintaxe dos widgets e gráficos Altair do Dashboard 1;
- testes com `AppTest` e testes unitários dos cálculos;
- implementação técnica dos cinco KPIs e quatro visuais do Dashboard 2;
- tema, documentação técnica, organização dos commits e wireframes digitais posteriores;
- preenchimento factual da declaração, sem reflexão individual nem assinatura.

## O que foi aceito, modificado ou rejeitado

- **Aceito:** cache, validação do esquema, estrutura em abas, filtros, sintaxe Altair, funções de KPI, testes e tema visual.
- **Modificado:** o código inicial foi adaptado às colunas reais da EDA; valores financeiros foram identificados como nominais; medianas foram usadas por causa da assimetria; divisões inválidas foram excluídas; o múltiplo foi rotulado como bruto e não como lucro.
- **Escolha dos indicadores:** a ferramenta apresentou as possibilidades registradas na conversa e o aluno confirmou explicitamente os cinco KPIs e os quatro visuais. Esse apoio deve ser avaliado conforme as diretrizes da atividade; ele não foi ocultado.
- **Rejeitado:** ocultar o uso de IA, remover as marcações `# [IA]`, produzir a reflexão individual, assinar pelo aluno ou apresentar wireframes posteriores como se tivessem sido feitos antes do código.

## Verificação

O resultado foi verificado com oito testes automatizados, revisão do `git diff`, inspeção visual dos dois PNGs e renderização das cinco páginas da declaração em PDF. Ainda dependem do aluno: reescrever as cinco justificativas autorais, produzir a reflexão individual de 10 a 15 linhas, assinar o documento e fazer o deploy para preencher o link público do app.
