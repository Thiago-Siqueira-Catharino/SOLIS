# Alfabeto da Solis (Σ)

Σ é o conjunto de todos os símbolos que podem aparecer num arquivo `.sol`. Um símbolo fora de Σ
é erro léxico. Σ é a união dos grupos abaixo.

| Grupo | Símbolos | Qtd | Onde aparece nos exemplos |
|---|---|---|---|
| Letras minúsculas | `a` a `z` | 26 | palavras reservadas e identificadores: `funcao`, `soma` |
| Letras maiúsculas | `A` a `Z` | 26 | `Classe`, `Inteiro`, `Matematica` |
| Dígitos | `0` a `9` | 10 | `2`, `3.14` |
| Operadores | `+` `-` `*` `/` `%` `=` `<` `>` `!` `&` `\|` | 11 | `a + b`, `a * b` |
| Delimitadores | `{` `}` `(` `)` `[` `]` `:` `;` `,` | 9 | `{ ... };`, `(a,b)` |
| Ponto | `.` | 1 | o Quebrado `3.14` e o acesso a método `mat.multiplicar` |
| Sublinhado | `_` | 1 | (nenhum exemplo usa ainda; o uso é definido nas classes léxicas) |
| Aspas | `'` `"` | 2 | `'Ana'`, `"Olá, Solis!"` |
| Espaços em branco | espaço, Tab, quebra de linha | 3 | entre as palavras e no fim de cada linha |
| Letras acentuadas | `á` `à` `â` `ã` `é` `ê` `í` `ó` `ô` `õ` `ú` `ç` e as maiúsculas `Á` `À` `Â` `Ã` `É` `Ê` `Í` `Ó` `Ô` `Õ` `Ú` `Ç` | 24 | só dentro de Linha: `'Digite um número :'` |

**Total: 113 símbolos.**

## Regras de uso

- **Espaços em branco** separam os símbolos da linguagem e são descartados pelo analisador
  léxico: não viram token. O Tab entra para que um arquivo indentado com Tab não seja recusado.
- **Letras acentuadas** pertencem a Σ, mas só são válidas **dentro de uma Linha**. Palavras
  reservadas e identificadores continuam sem acento.
- **O ponto tem dois usos.** Entre dígitos, faz parte do Quebrado (`3.14`); depois de um
  identificador, é acesso a membro (`mat.multiplicar`). O analisador léxico distingue os dois pelo
  casamento mais longo.
