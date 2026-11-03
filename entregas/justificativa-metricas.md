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
- **Justificativa autoral:** _Explique, com suas palavras, por que conhecer o porte típico do investimento é útil para esse público._
- **Qual decisão pode apoiar:** comparar o nível de investimento do segmento analisado com a capacidade financeira de um projeto.
- **O que comunica ao público-alvo:** uma referência de quanto os filmes de ação do recorte costumam demandar em produção.

## Métrica 2: Bilheteria mundial mediana

- **Variável:** `bilheteria_mundial`.
- **O que mede:** a receita mundial nominal central dos filmes selecionados.
- **Fórmula:** mediana de `bilheteria_mundial`.
- **Justificativa autoral:** _Explique por que a mediana mundial representa melhor o resultado típico do que destacar apenas grandes sucessos._
- **Qual decisão pode apoiar:** estimar uma referência comercial para comparar títulos e recortes de mercado.
- **O que comunica ao público-alvo:** o desempenho mundial típico dos filmes de ação presentes na amostra.

## Métrica 3: Múltiplo bruto mediano de bilheteria/orçamento

- **Variáveis:** `bilheteria_mundial` e `orcamento`.
- **O que mede:** quantas vezes a bilheteria mundial bruta corresponde ao orçamento informado em cada filme.
- **Fórmula:** mediana de `bilheteria_mundial / orcamento`, considerando somente orçamentos positivos.
- **Justificativa autoral:** _Explique por que relacionar escala de receita e investimento ajuda a comparar filmes de tamanhos diferentes._
- **Qual decisão pode apoiar:** comparar a eficiência bruta de projetos com orçamentos distintos.
- **O que comunica ao público-alvo:** uma relação simples entre arrecadação e investimento de produção.
- **Limitação importante:** o múltiplo **não representa lucro**, pois não inclui custos de marketing, distribuição, participação de exibidores, impostos ou outras despesas.

## Métrica 4: Participação internacional mediana

- **Variáveis:** `bilheteria_internacional` e `bilheteria_mundial`.
- **O que mede:** a parcela da bilheteria mundial obtida fora do mercado doméstico em cada filme.
- **Fórmula:** mediana de `(bilheteria_internacional / bilheteria_mundial) × 100`, considerando bilheterias mundiais positivas.
- **Justificativa autoral:** _Explique por que o alcance internacional é relevante para a estratégia comercial de filmes de ação._
- **Qual decisão pode apoiar:** avaliar a importância de distribuição, lançamento e comunicação voltados a mercados internacionais.
- **O que comunica ao público-alvo:** quanto do resultado típico depende do público internacional.

## Métrica 5: Abertura doméstica mediana

- **Variável:** `abertura_domestica`.
- **O que mede:** a receita mediana do fim de semana de estreia no mercado doméstico.
- **Fórmula:** mediana de `abertura_domestica`.
- **Justificativa autoral:** _Explique por que a força da estreia pode orientar decisões de lançamento e promoção._
- **Qual decisão pode apoiar:** comparar estratégias de lançamento e dimensionar a importância do desempenho inicial.
- **O que comunica ao público-alvo:** uma referência de tração comercial no início da exibição doméstica.

## Leitura conjunta e limitações

Os indicadores devem ser lidos em conjunto: orçamento e abertura descrevem escala e início do lançamento; bilheteria mundial e participação internacional descrevem alcance; o múltiplo bruto relaciona arrecadação e orçamento sem estimar lucro. Os valores financeiros são nominais e não foram corrigidos pela inflação. Além disso, a base contém 1.000 filmes entre as maiores bilheterias mundiais, portanto há viés de seleção e os resultados não representam todos os filmes de ação.
