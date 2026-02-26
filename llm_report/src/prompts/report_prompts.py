PROMPTS = {
"estoque_baixo": """
Você está gerando APENAS blocos de registros de produtos com estoque abaixo do mínimo.

REGRAS:

- Liste todos os registros recebidos
- Use numeração iniciando em {start_index}
- Numere sequencialmente
- Não gere cabeçalhos
- Não gere totais
- Não gere análises
- Utilize apenas os campos fornecidos

FORMATO:

<indice>. Produto: <nome_produto>
   Descrição: <descricao>
   Estoque Atual: <estoque_atual>
   Estoque Mínimo: <estoque_minimo>

DADOS:
{dados}
""",

"inventario": """
Você está gerando APENAS blocos de registros de inventário.

REGRAS:

- Use numeração iniciando em {start_index}
- Numere sequencialmente
- Não reinicie contagem
- Não gere cabeçalhos
- Caso data_validade seja nula escreva "Não informado"

FORMATO:

<indice>. Produto: <nome_produto>
   Descrição: <descricao>
   Estoque Atual: <estoque_atual>
   Status Ativo: <ativo>
   Data de Validade: <data_validade>

DADOS:
{dados}
""",

"saldo_estoque": """
Você está gerando APENAS blocos de saldo de estoque.

REGRAS:

- Liste todos os registros
- Use numeração iniciando em {start_index}
- Não gere cabeçalhos
- Não gere totais
- Não substitua valores

FORMATO:

<indice>. Produto: <nome_produto>
   Quantidade em Estoque: <estoque_atual>

DADOS:
{dados}
""",

"movimentacao_periodo": """
Você está gerando SOMENTE blocos de registros.

REGRAS OBRIGATÓRIAS:

- NÃO gerar títulos
- NÃO gerar totais
- NÃO gerar explicações
- NÃO gerar cabeçalhos
- NÃO gerar comentários
- NÃO adicionar campos extras
- NÃO remover campos
- NÃO alterar valores
- NÃO alterar ordem dos registros
- NÃO inserir linhas em branco entre registros

- Cada registro deve conter EXATAMENTE 5 linhas.

- Se algum campo estiver vazio ou nulo, escrever "Não informado".

Use numeração iniciando em {start_index}.

FORMATO OBRIGATÓRIO (seguir exatamente):

<indice>. Produto: <nome_produto>
   Tipo: <tipo_movimentacao>
   Quantidade: <quantidade>
   Entidade: <entidade>
   Data: <data_movimentacao>

DADOS:
{dados}
""",

"entradas_saidas": """
Você está gerando APENAS blocos consolidados de entradas e saídas por produto.

OBJETIVO:
Transformar TODOS os registros recebidos em blocos textuais estruturados.

REGRAS ABSOLUTAS:

1. Gere EXATAMENTE um bloco para CADA item existente em {dados}.
2. A quantidade de blocos gerados deve ser IGUAL à quantidade de itens em {dados}.
3. Nunca omita produtos.
4. Nunca duplique produtos.
5. Nunca reorganize ou reagrupe dados.
6. Preserve exatamente os valores recebidos.
7. Use numeração sequencial iniciando em {start_index}.
8. Nunca reinicie a numeração.
9. Não gere cabeçalhos adicionais.
10. Não gere totais.
11. Caso a lista "entradas" esteja vazia, escreva exatamente:
   Nenhuma movimentação registrada
12. Caso a lista "saidas" esteja vazia, escreva exatamente:
   Nenhuma movimentação registrada
13. Nunca invente dados.
14. Nunca resuma informações.
15. Nunca altere nomes de produtos ou entidades.

FORMATO OBRIGATÓRIO:

<indice>. Produto: <nome_produto>

   ENTRADAS:
   <entidade> (<quantidade>)
   <repetir para todas as entradas ou escrever "Nenhuma movimentação registrada">

   SAÍDAS:
   <entidade> (<quantidade>)
   <repetir para todas as saídas ou escrever "Nenhuma movimentação registrada">

IMPORTANTE:
- Cada produto deve possuir exatamente um bloco.
- Não deixe produtos sem bloco.
- Não combine produtos no mesmo bloco.

DADOS RECEBIDOS:
{dados}
"""
,

"produtos_sem_giro": """
Você está gerando APENAS blocos de produtos sem movimentação.

REGRAS OBRIGATÓRIAS:

- Use numeração sequencial iniciando exatamente em {start_index}
- Não pule números
- Não reinicie a numeração
- Não gere cabeçalhos
- Não gere totais
- Não agrupe registros
- Não interprete dados
- Não adicione explicações
- Preserve exatamente a ordem recebida

TRATAMENTO DE CAMPOS:

- Se alguma data for nula ou vazia, escreva:
  "Nenhuma movimentação registrada"

FORMATO EXATO DE SAÍDA:

<indice>. Produto: <nome_produto>
   Última Movimentação: <ultima_movimentacao ou mensagem substituta>

DADOS RECEBIDOS:
{dados}
""",

"validade_proxima": """
Você está gerando APENAS blocos de produtos com validade próxima.

REGRAS OBRIGATÓRIAS:

1. A numeração DEVE iniciar exatamente em {start_index}
2. A numeração DEVE ser sequencial e contínua
3. É PROIBIDO pular números
4. É PROIBIDO reiniciar a contagem
5. Gere apenas os blocos de listagem
6. Não gere cabeçalhos
7. Não gere totais
8. Liste TODOS os registros recebidos
9. Utilize exclusivamente os dados fornecidos
10. Caso "data_validade" esteja ausente ou nula, escrever:
"Não informado"

FORMATO OBRIGATÓRIO:

<indice>. Produto: <nome_produto>
   Data de Validade: <data_validade>

IMPORTANTE:
- O próximo índice deve sempre ser o índice anterior + 1
- A quantidade de itens gerados deve ser exatamente igual à quantidade de registros recebidos

DADOS RECEBIDOS:
{dados}
""",

"giro_estoque": """
Você está gerando APENAS blocos de indicadores de giro de estoque.

REGRAS:

- Use numeração iniciando em {start_index}
- Não gere cabeçalhos
- Não gere totais
- Não interpretar indicadores

FORMATO:

<indice>. Produto: <nome_produto>
   Total Entradas: <total_entradas>
   Total Saídas: <total_saidas>
   Total Movimentações: <total_movimentacoes>

DADOS:
{dados}
""",

"curva_abc": """
Você deve gerar APENAS os itens da Curva ABC com base nos dados fornecidos.

INSTRUÇÕES OBRIGATÓRIAS:

- NÃO gere título, cabeçalho ou introdução.
- NÃO gere totais ou resumos.
- NÃO explique nada.
- NÃO recalcul​e valores.
- NÃO altere percentuais ou classes.
- Preserve exatamente os valores recebidos.
- Use a numeração iniciando em {start_index}.
- Respeite rigorosamente o formato abaixo.
- Gere somente os itens contidos em {dados}.

FORMATO EXATO DE SAÍDA:

<indice>. Produto: <nome_produto>
   Valor Total: <valor_total>
   Percentual: <percentual>%
   Classe ABC: <classe_abc>

DADOS:
{dados}
""",
"produtos_custo": """
Você está gerando APENAS blocos de produtos e seus custos.

REGRAS:

- Use numeração iniciando em {start_index}
- Não gere cabeçalhos
- Não gere totais
- Não interpretar dados

FORMATO:

<indice>. Produto: <nome_produto>
   Estoque Atual: <estoque_atual>
   Custo Médio: <custo_medio>
   Valor Total: <valor_total>

DADOS:
{dados}
"""
}
