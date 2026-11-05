# Classes léxicas da Solis

Cada token de um arquivo `.sol` pertence a uma das classes abaixo. Os símbolos que podem aparecer
estão em [`alfabeto.md`](alfabeto.md).

## Resumo

| Classe | Padrão |
|---|---|
| Operadores | lista fechada (ver tabela) |
| Palavras reservadas | lista fechada (ver lista) |
| Identificadores | `[a-zA-Z_][a-zA-Z0-9_]*` |
| Literal Inteiro | `[0-9]+` |
| Literal Quebrado | `[0-9]+\.[0-9]+` |
| Literal Linha | `'[^'\n]*' \| "[^"\n]*"` |
| Literal Booleano | `verdadeiro \| falso` |
| Delimitadores/Pontuação | lista fechada (ver tabela) |

---

## Operadores

Os operadores podem ser escritos com o símbolo ou por extenso, menos `%` e `!`, que só têm o
símbolo.

| Símbolo | Por extenso |
|---|---|
| `+` | `mais` |
| `-` | `menos` |
| `*` | `multiplica` |
| `/` | `dividido-por` |
| `%` | — |
| `=` | `recebe` |
| `==` | `igual-a` |
| `<` | `menor-que` |
| `>` | `maior-que` |
| `!=` | `diferente-de` |
| `&&` | `e` |
| `\|\|` | `ou` |
| `!` | — |

## Palavras reservadas

`funcao` · `pede` · `retorna` · `devolve` · `Classe` · `Possui` · `Faz` · `principal` · `Linha` ·
`Inteiro` · `Quebrado` · `Booleano` · `Vazio` · `Lista` · `Dicionario` · `enquanto` · `para` ·
`em` · `se` · `senao` · `pare`

## Identificadores

```
[a-zA-Z_][a-zA-Z0-9_]*
```

Começa com letra (minúscula ou maiúscula) ou `_`, depois zero ou mais letras, dígitos ou `_`.
Sem acento.

| Válidos | Inválidos |
|---|---|
| `resultado`, `resultado2`, `x`, `mat`, `Matematica`, `meu_nome`, `_nome` | `1a` (começa com dígito), `meu-nome` (tem `-`), `número` (tem acento) |

## Constantes/Literais

### Inteiro

```
[0-9]+
```

Um ou mais dígitos, sem sinal. O número negativo é montado pela gramática, com o operador `-`
(`menos`), e não pelo token.

| Válidos | Inválidos |
|---|---|
| `2`, `42` | `-5` (tem sinal), `4.5` (é Quebrado) |

### Quebrado

```
[0-9]+\.[0-9]+
```

Dígitos, um ponto e dígitos: precisa de dígito dos dois lados do ponto.

| Válidos | Inválidos |
|---|---|
| `3.14`, `4.5` | `.5`, `3.`, `3.1.4` |

### Linha

```
'[^'\n]*' | "[^"\n]*"
```

Abre e fecha com a mesma aspa, simples ou dupla. Dentro, vale qualquer símbolo do alfabeto,
inclusive letras acentuadas, menos a aspa que abriu e a quebra de linha. Uma Linha com aspa dupla
pode conter aspa simples, e o contrário.

| Válidos | Inválidos |
|---|---|
| `'Ana'`, `"Olá, Solis!"`, `'O número é primo'`, `"it's"` | `'Ana"` (aspas diferentes), `'Ana` (não fecha) |

### Booleano

```
verdadeiro | falso
```

As duas palavras exatas. Como também casam o padrão de Identificador, valem como Booleano, do
mesmo jeito que uma palavra reservada vale como reservada.

## Delimitadores/Pontuação

| Símbolo | Função |
|---|---|
| `{` `}` | bloco |
| `(` `)` | agrupamento / parâmetros |
| `[` `]` | lista |
| `:` | separador |
| `;` | fim de instrução |
| `,` | separa parâmetros e itens de lista |

---

## Notação usada nos padrões

| Notação | Significado |
|---|---|
| `[a-z]` | um símbolo da faixa |
| `[^...]` | um símbolo do alfabeto que **não** esteja na lista |
| `\n` | a quebra de linha |
| `\.` | o ponto como símbolo comum, e não como coringa |
| `x+` | uma ou mais vezes |
| `x*` | zero ou mais vezes |
| `a \| b` | um ou outro |
