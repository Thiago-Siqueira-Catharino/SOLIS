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
| Sublinhado | `_` | 1 | nomes como `meu_nome` e `_nome`; um nome feito só de `_` não vale |
| Aspas | `'` `"` | 2 | `'Ana'`, `"Olá, Solis!"` |
| Crase | `` ` `` | 1 | abre e fecha um padrão: ``Padrao numero recebe `[0-9]+`;`` |
| Símbolos de registro | `@` `#` `$` `º` `ª` `°` | 6 | só dentro de padrão, de Linha ou de comentário: ``Padrao email recebe `[a-z]+@[a-z]+\.com`;``, `'pedido #123'`, `'R$ 10,50'`, `'nº 5'`, `'25°'` |
| Interrogação e barra invertida | `?` `\` | 2 | só dentro de padrão, de Linha ou de comentário: ``Padrao inteiro recebe `-?[0-9]+`;``, `'Qual o seu nome?'` |
| Espaços em branco | espaço, Tab, quebra de linha | 3 | entre as palavras e no fim de cada linha |
| Letras acentuadas | `á` `à` `â` `ã` `é` `ê` `í` `ó` `ô` `õ` `ú` `ç` e as maiúsculas `Á` `À` `Â` `Ã` `É` `Ê` `Í` `Ó` `Ô` `Õ` `Ú` `Ç` | 24 | só dentro de Linha, de comentário ou de padrão: `'Digite um número :'`, `// número de alunos`, ``Padrao cidade recebe `São Paulo`;`` |

**Total: 122 símbolos.**

## Regras de uso

- **Espaços em branco** separam os símbolos da linguagem e são descartados pelo analisador
  léxico: não viram token. O Tab entra para que um arquivo indentado com Tab não seja recusado.
- **Letras acentuadas** pertencem a Σ, mas só são válidas **dentro de uma Linha, de um
  comentário ou de um padrão**. Palavras reservadas e identificadores continuam sem acento. Dentro
  de um padrão, os acentos existem porque os registros que os padrões leem estão em português.
- **Comentários** começam com `//` e vão até o fim da linha. Como os espaços em branco, são
  descartados pelo analisador léxico e não viram token.
- **O ponto tem dois usos.** Entre dígitos, faz parte do Quebrado (`3.14`); depois de um
  identificador, é acesso a membro (`mat.multiplicar`). O analisador léxico distingue os dois pelo
  casamento mais longo.
- **A crase abre e fecha um padrão.** Tudo o que vem entre as duas crases é o texto do padrão, lido
  com o núcleo de operadores de [`docs/02nucleo_minimo.md`](../docs/02nucleo_minimo.md). O padrão
  termina na crase seguinte, então um padrão não contém crase, do mesmo jeito que uma Linha aberta
  com `'` não contém `'`.
- **Os símbolos de registro (`@`, `#`, `$`, `º`, `ª`, `°`) só valem dentro de um padrão, de uma
  Linha ou de um comentário**, como as letras acentuadas. Eles existem porque aparecem nos registros
  que os padrões leem: e-mails, números de pedido, valores em dinheiro, ordinais, graus. O `º` (de
  `nº`) e o `°` (de `25°`) são símbolos diferentes, embora pareçam iguais: um padrão com um não casa
  com o outro.
- **`?` e `\` só valem dentro de um padrão, de uma Linha ou de um comentário**, como as letras
  acentuadas. No padrão, o `?` marca o que é opcional (`-?` é "com ou sem sinal"), e a `\` faz o
  símbolo seguinte valer como símbolo comum (`\.` é o ponto, e não o coringa). Na Linha e no
  comentário, os dois são símbolos comuns: `'Qual o seu nome?'`. Fora desses três lugares, são
  erro léxico.
- **Dentro de um padrão, os símbolos mudam de papel.** `|`, `*`, `+`, `(`, `)`, `[`, `]` e `.` são
  operadores do padrão, e não os operadores e delimitadores da linguagem. Em
  ``Padrao sinal recebe `\+|-`;``, a `|` é a alternância do padrão, e não metade do `||`.

## O alfabeto dos registros

Σ é o alfabeto do que se **escreve** num arquivo `.sol`. Os registros que o executor **lê** podem ter
qualquer símbolo, inclusive os que não estão em Σ, como `€`, `ñ` ou um emoji.

- Um símbolo do registro que está em Σ é reconhecido por ele mesmo: o `a` de um padrão casa com o
  `a` do registro.
- Todo símbolo do registro que está fora de Σ conta como um único símbolo a mais, o **outro**. Nenhum
  padrão consegue escrever o outro, porque ele não está em Σ: só o coringa `.` o reconhece.
- Um registro nunca é recusado por causa dos símbolos que tem: um símbolo fora de Σ só deixa de
  casar com o que não é coringa.
