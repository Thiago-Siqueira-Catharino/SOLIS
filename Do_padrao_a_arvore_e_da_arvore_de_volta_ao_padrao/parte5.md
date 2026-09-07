## Caminho de volta

### Inteiro

Expressão a partir da árvore:
`(0|1|2|3|4|5|6|7|8|9)(0|1|2|3|4|5|6|7|8|9)*`

| Forma | Caracteres |
|---|---|
| Do jeito que se escreve | 6 |
| Usando só união, concatenação e fecho | 43 |

### Identificador

Expressão a partir da árvore:
`(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|0|1|2|3|4|5|6|7|8|9)*`

| Forma | Caracteres |
|---|---|
| Do jeito que se escreve | 14 |
| Usando só união, concatenação e fecho | 127 |

## Convergência

| Peça | Escrita A | Escrita B | Nós (A) | Nós (B) |
|---|---|---|---|---|
| Inteiro | `[0-9]+` | `[0-9][0-9]*` | 40 | 40 |
| Identificador (2ª classe) | `[a-z0-9]` | `([a-z]\|[0-9])` | 71 | 71 |