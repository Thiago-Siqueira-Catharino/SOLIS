## O que a máquina precisaria lembrar

| Requisito | O que precisaria lembrar | Tem teto? | Onde se resolve |
|---|---|---|---|
| Palavra é reservada ou é Identificador? | em que ponto da palavra-candidata está, comparando contra a lista fixa (`funcao`, `pede`, ..., `pare`) | Sim — 15 palavras, sempre o mesmo tanto | Cabe nos três operadores (alternância de strings) |
| Variável usada foi declarada antes? | todos os nomes de variável já vistos no programa até aquele ponto | Não — cresce com o tamanho do programa | Fora da classe léxica; verificação de fase posterior (tabela de símbolos) |