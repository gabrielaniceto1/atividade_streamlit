# Justificativa das métricas — Dashboard 2

**Turma:** 5A

**Público-alvo:** empresários interessados em filmes de ação

**Recorte:** filmes cujo `genero_principal` é `Action`, com filtros de década e classificação indicativa.

> Os cinco indicadores abaixo foram escolhidos pelo aluno. A IA apoiou apenas a definição
> técnica, as fórmulas e a implementação. Os campos marcados como **Justificativa autoral**
> devem ser reescritos pelo aluno em suas próprias palavras antes da entrega.

## Métrica 1: Orçamento mediano

- **Variável:** `orcamento`.
- **O que mede:** o valor central dos orçamentos de produção informados no recorte; valores nulos ou não positivos não entram no cálculo.
- **Fórmula:** mediana de `orcamento`.
- **Justificativa autoral:** Escolhi essa métrica porque acredito que o orçamento é uma das primeiras coisas que um empresário precisa analisar antes de investir em um filme. Utilizar a mediana ajuda a ter uma noção mais realista de quanto os filmes de ação da nossa base costumam custar, sem deixar que produções com orçamentos extremamente altos influenciem tanto o resultado. Assim, fica mais fácil comparar o investimento necessário com o dinheiro disponível para um possível projeto.
- **Qual decisão pode apoiar:** comparar o nível de investimento do segmento analisado com a capacidade financeira de um projeto.
- **O que comunica ao público-alvo:** uma referência de quanto os filmes de ação do recorte costumam demandar em produção.

## Métrica 2: Bilheteria mundial mediana

- **Variável:** `bilheteria_mundial`.
- **O que mede:** a receita mundial nominal central dos filmes selecionados.
- **Fórmula:** mediana de `bilheteria_mundial`.
- **Justificativa autoral:** Escolhi a bilheteria mundial mediana porque queria ter uma referência de quanto os filmes de ação da base conseguem arrecadar. Se utilizássemos apenas os maiores sucessos, poderíamos acabar criando uma expectativa muito alta sobre o retorno financeiro. A mediana permite observar um resultado mais representativo dos filmes analisados, ajudando o empresário a comparar o desempenho comercial de diferentes produções.
- **Qual decisão pode apoiar:** estimar uma referência comercial para comparar títulos e recortes de mercado.
- **O que comunica ao público-alvo:** o desempenho mundial típico dos filmes de ação presentes na amostra.

## Métrica 3: Múltiplo bruto mediano de bilheteria/orçamento

- **Variáveis:** `bilheteria_mundial` e `orcamento`.
- **O que mede:** quantas vezes a bilheteria mundial bruta corresponde ao orçamento informado em cada filme.
- **Fórmula:** mediana de `bilheteria_mundial / orcamento`, considerando somente orçamentos positivos.
- **Justificativa autoral:** Achei importante incluir essa métrica porque analisar somente a bilheteria não mostra a relação entre o dinheiro investido e o arrecadado. Por exemplo, um filme que custou 50 milhões e arrecadou 200 milhões pode apresentar uma relação entre arrecadação e orçamento maior do que outro que custou 300 milhões e arrecadou 600 milhões. Com esse indicador, conseguimos comparar filmes de diferentes tamanhos e identificar quais tiveram uma arrecadação proporcionalmente maior em relação ao orçamento. Porém, é importante lembrar que isso não significa necessariamente que o filme deu lucro, já que existem outros custos envolvidos.
- **Qual decisão pode apoiar:** comparar a eficiência bruta de projetos com orçamentos distintos.
- **O que comunica ao público-alvo:** uma relação simples entre arrecadação e investimento de produção.
- **Limitação importante:** o múltiplo **não representa lucro**, pois não inclui custos de marketing, distribuição, participação de exibidores, impostos ou outras despesas.

## Métrica 4: Participação internacional mediana

- **Variáveis:** `bilheteria_internacional` e `bilheteria_mundial`.
- **O que mede:** a parcela da bilheteria mundial obtida fora do mercado doméstico em cada filme.
- **Fórmula:** mediana de `(bilheteria_internacional / bilheteria_mundial) × 100`, considerando bilheterias mundiais positivas.
- **Justificativa autoral:** Escolhi essa métrica porque os filmes de ação podem atingir públicos de vários países, e acredito que isso seja importante para quem pretende investir nesse mercado. Saber qual porcentagem da bilheteria vem do mercado internacional ajuda a entender o quanto o desempenho comercial dos filmes depende do público de fora do mercado doméstico. Essa informação também pode ajudar empresários a pensar em estratégias de distribuição, divulgação e lançamento em outros países.
- **Qual decisão pode apoiar:** avaliar a importância de distribuição, lançamento e comunicação voltados a mercados internacionais.
- **O que comunica ao público-alvo:** quanto do resultado típico depende do público internacional.

## Métrica 5: Abertura doméstica mediana

- **Variável:** `abertura_domestica`.
- **O que mede:** a receita mediana do fim de semana de estreia no mercado doméstico.
- **Fórmula:** mediana de `abertura_domestica`.
- **Justificativa autoral: Escolhi a abertura doméstica mediana porque o desempenho de um filme logo na estreia pode mostrar como o público respondeu inicialmente ao lançamento. Uma boa abertura pode indicar que a campanha de divulgação conseguiu atrair espectadores nos primeiros dias. Para um empresário, considero essa informação útil porque permite comparar o desempenho inicial dos filmes e entender melhor a importância do marketing e do planejamento da estreia. Usei a mediana para evitar que apenas as estreias muito grandes determinem essa referência.**
- **Qual decisão pode apoiar:** comparar estratégias de lançamento e dimensionar a importância do desempenho inicial.
- **O que comunica ao público-alvo:** uma referência de tração comercial no início da exibição doméstica.

## Leitura conjunta e limitações

Os indicadores devem ser lidos em conjunto: orçamento e abertura descrevem escala e início do lançamento; bilheteria mundial e participação internacional descrevem alcance; o múltiplo bruto relaciona arrecadação e orçamento sem estimar lucro. Os valores financeiros são nominais e não foram corrigidos pela inflação. Além disso, a base contém 1.000 filmes entre as maiores bilheterias mundiais, portanto há viés de seleção e os resultados não representam todos os filmes de ação.
