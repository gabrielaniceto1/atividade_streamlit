# Declaração de Uso de IA

**Nome:** Gabriel Aniceto

**Data:** 02/11/2026

## Ferramenta

ChatGPT Codex, modelo GPT-5.

## Prompt usado

> Quero que você use como base os PDFs das aulas e as instruções.txt para fazer a atividade que está nos arquivos Markdown (o roteiro e o README). Analise todo o projeto e, conforme for fazendo, divida em commits com funções específicas implementadas para subir no GitHub. Depois, leia o documento de declaração de uso de IA e preencha.

Complemento enviado durante a atividade:

> Sou da turma 5A. O público-alvo são empresários interessados em filmes de ação. Corrija o que for necessário, faça também a parte de entregas e conclua os arquivos Markdown.

## O que foi aceito, modificado ou rejeitado e por quê

- **Aceito:** estrutura de cache e validação do CSV; adaptação do Dashboard 1 para a base de filmes; sintaxe dos widgets e gráficos Altair; testes com `AppTest`; organização visual e tema nativo do Streamlit; revisão dos arquivos de documentação.
- **Modificado:** o código inicial tratava um dataset de doença cardíaca. Ele foi revisado para usar as colunas da EDA de filmes, preservar as limitações descritas no notebook e lidar com valores ausentes em orçamento e abertura doméstica.
- **Rejeitado:** omitir o uso de IA e deixar que a ferramenta escolhesse ou justificasse sozinha os KPIs do Dashboard 2. Essas solicitações conflitam com as diretrizes da atividade; as marcações `# [IA]` foram mantidas e a escolha final das métricas foi reservada ao aluno.
