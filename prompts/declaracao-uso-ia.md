
# Declaração de Uso de IA

**Nome:** Gabriel Aniceto
**Data:** 02/11/2026

## Ferramenta utilizada

ChatGPT Codex (GPT-5).

## Prompts utilizados

**Prompt 1 — Análise inicial do projeto**

> Dá uma olhada nos arquivos do projeto, principalmente nos PDFs das aulas, no roteiro da atividade e no README. Quero entender o que já está implementado e o que ainda falta fazer para atender aos requisitos. Antes de alterar alguma coisa, me explica o que precisa ser ajustado.

**Prompt 2 — Adaptação da base de dados**

> O projeto estava utilizando uma base de doenças cardíacas, mas nossa atividade é sobre filmes. Preciso adaptar o código para trabalhar com os dados que analisamos na EDA. Confere as colunas do CSV, implementa o cache e trata os valores ausentes para evitar erros. Tenta aproveitar a estrutura atual e me mostra o que precisou ser alterado.

**Prompt 3 — Implementação do Dashboard 1**

> Agora precisamos ajustar o Dashboard 1 de acordo com o roteiro. Quero implementar a seleção de variáveis, filtros numéricos, histogramas e a correlação de Spearman. Usa os componentes do Streamlit e os gráficos do Altair. Também verifica se os filtros funcionam corretamente quando nenhuma opção é selecionada e adiciona testes para as principais funcionalidades.

**Prompt 4 — Desenvolvimento do Dashboard 2**

> Sou da turma 5A e nosso público-alvo são empresários interessados em filmes de ação. Para o Dashboard 2, quero trabalhar com cinco métricas: orçamento mediano, bilheteria mundial mediana, múltiplo bruto de bilheteria/orçamento, participação internacional mediana e abertura doméstica mediana. Também quero incluir quatro visualizações para ajudar a analisar os dados e comparar os filmes. Me ajuda a implementar esses indicadores e gráficos usando as colunas disponíveis no CSV, com os filtros de década e classificação indicativa. Confere também se os cálculos estão corretos e se os resultados fazem sentido para o público-alvo.

**Prompt 5 — Revisão e testes**

> Agora revisa o que foi implementado nos dois dashboards. Confere os cálculos, o funcionamento dos filtros e o tratamento dos dados ausentes. Quero garantir que não aconteçam erros com divisões por zero ou valores inválidos. Também verifica os testes com AppTest e se todos os gráficos estão sendo exibidos corretamente.

**Prompt 6 — Organização visual e entregas**

> Confere novamente o roteiro da atividade e o que já foi implementado. Quero que o dashboard tenha um tema visual relacionado a cinema, mas sem comprometer a leitura dos gráficos. Também me ajuda a organizar o README, os arquivos de entrega e os wireframes. Separa as mudanças em commits por funcionalidade e identifica as partes que tiveram auxílio da IA.

*Os prompts apresentados são reconstruções resumidas das solicitações e etapas do desenvolvimento, e não transcrições literais do histórico do Codex.*

## O que foi aceito, modificado ou rejeitado e por quê

### Aceito

Utilizei a IA como apoio principalmente na implementação e organização do código. Aproveitei sugestões para o carregamento dos dados, implementação do cache, validação do CSV e organização da estrutura do Streamlit.

No Dashboard 1, utilizei o auxílio da ferramenta para implementar os filtros, histogramas, correlação de Spearman e gráficos com Altair. Também aproveitei sugestões para tratar seleções vazias e implementar testes automatizados com AppTest.

No Dashboard 2, defini as cinco métricas que queria utilizar e solicitei quatro visualizações para apresentar os resultados. A IA auxiliou na implementação dos indicadores, nas fórmulas, na organização dos gráficos e no tratamento dos dados ausentes.

Além disso, utilizei sugestões para a organização da documentação, aplicação do tema visual relacionado a cinema e revisão dos arquivos de entrega.

### Modificado

A principal alteração foi adaptar o código inicial, que trabalhava com dados de doenças cardíacas, para a base de filmes utilizada na atividade. Foi necessário ajustar variáveis, filtros e gráficos de acordo com as colunas disponíveis e as limitações identificadas na EDA.

Também solicitei alterações na apresentação das informações para que os dashboards fizessem sentido para empresários interessados em filmes de ação.

Na parte das métricas, tive o cuidado de diferenciar a arrecadação de um filme do lucro real. Por exemplo, o múltiplo entre bilheteria e orçamento foi utilizado apenas como uma comparação entre os valores, já que existem outros custos que não estão presentes na base.

A organização visual e os materiais de documentação também passaram por revisões para manter a identidade do projeto e atender às exigências da atividade.

### Rejeitado

Não considerei adequado utilizar os resultados dos indicadores como se representassem todo o mercado de filmes de ação, pois a base contém apenas uma seleção de filmes entre as maiores bilheterias mundiais.

Também não seria correto interpretar diretamente a relação entre bilheteria e orçamento como lucro. Por isso, essa limitação foi mantida na explicação da métrica.

Além disso, preservei as identificações de uso de IA exigidas pela atividade e não utilizei a ferramenta como substituta da revisão final dos resultados.

## Como os resultados foram verificados

A verificação envolveu a execução local da aplicação, a conferência das colunas da base de dados e a utilização de testes automatizados.

No Dashboard 1, foram realizados testes com AppTest para verificar os componentes, as abas e os gráficos, incluindo situações em que os filtros não retornavam resultados.

No Dashboard 2, foram utilizados testes com dados sintéticos para conferir os cálculos e o tratamento de divisões inválidas. Também foi verificado o funcionamento do painel completo.

Por fim, a organização das entregas foi conferida por meio da revisão dos arquivos Markdown, das alterações registradas no Git e da inspeção visual dos materiais gerados.

## Considerações finais

O Codex foi utilizado em diferentes etapas do desenvolvimento, principalmente para auxiliar na programação, identificar possíveis erros, implementar testes e organizar a documentação.

No Dashboard 2, a escolha das cinco métricas e a solicitação das quatro visualizações partiram de mim, considerando o público-alvo de empresários interessados em filmes de ação. A ferramenta auxiliou na implementação técnica, nos cálculos e na organização das informações.

A IA facilitou bastante algumas partes da atividade, mas ainda foi necessário direcionar o desenvolvimento, solicitar alterações e verificar se os resultados estavam coerentes com o que foi pedido no roteiro.
