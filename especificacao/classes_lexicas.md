# Classes léxicas da Solis

Cada token de um arquivo `.sol` pertence a uma das classes abaixo. Os símbolos que podem aparecer
estão em [`alfabeto.md`](alfabeto.md).

## Resumo

| Classe | Padrão |
|---|---|
| Operadores | lista fechada (ver tabela) |
| Palavras reservadas | lista fechada (ver lista) |
| Identificadores | `[a-zA-Z][a-zA-Z0-9_]* \| _+[a-zA-Z0-9][a-zA-Z0-9_]*` |
| Literal Inteiro | `[0-9]+` |
| Literal Quebrado | `[0-9]+\.[0-9]+` |
| Literal Linha | `'[^'\n]*' \| "[^"\n]*"` |
| Literal Booleano | `verdadeiro \| falso` |
| Literal Padrão | `` `[^`\n]*` `` |
| Delimitadores/Pontuação | lista fechada (ver tabela) |
| Comentário (descartado) | `//[^\n]*` |

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
| `>=` | `maior-ou-igual-a` |
| `<=` | `menor-ou-igual-a` |
| `!=` | `diferente-de` |
| `&&` | `e` |
| `\|\|` | `ou` |
| `!` | — |

Vale o casamento mais longo: `>=` é um operador só, e não `>` seguido de `=`.

## Palavras reservadas

`funcao` · `pede` · `retorna` · `devolve` · `Classe` · `Possui` · `Faz` · `principal` · `Linha` ·
`Inteiro` · `Quebrado` · `Booleano` · `Vazio` · `Lista` · `Padrao` · `Novo` ·
`Imprime` · `imprime` · `enquanto` · `Enquanto` · `para` · `Para` · `em` · `Em` · `se` · `Se` ·
`senao` · `Senao` · `pare` · `Pare`

- As palavras de controle (`se`, `senao`, `enquanto`, `para`, `em`, `pare`) valem com a inicial
  minúscula ou maiúscula: `se` e `Se` são a mesma palavra. As outras têm uma grafia só.
- `Imprime` e `imprime` são a mesma palavra, e a chamada é sempre com parênteses:
  `Imprime(soma(x, y));`.
- `Novo` cria um objeto: `Matematica mat recebe Novo Matematica;`.
- `Lista` é o tipo e aparece só na declaração. Os itens vêm direto entre colchetes:
  `Lista Colaboradores recebe ['Ana', 'Beatriz', 'Luana'];`.
- `Padrao` é o tipo de um padrão: ``Padrao numero recebe `[0-9]+`;``. As operações do padrão,
  `casa` e `procura`, são métodos chamados com o `.` (`numero.casa(campo)`), e por isso não são
  palavras reservadas: o analisador léxico os lê como identificadores.
- `devolve` tem duas formas: `devolve <valor>;` numa função que retorna um valor, e `devolve;`
  sozinho numa função que retorna `Vazio`. `Vazio` é só tipo: não é escrito como valor.

## Identificadores

```
[a-zA-Z][a-zA-Z0-9_]* | _+[a-zA-Z0-9][a-zA-Z0-9_]*
```

Começa com letra (minúscula ou maiúscula) ou `_`, depois zero ou mais letras, dígitos ou `_`.
Precisa ter pelo menos uma letra ou um dígito: um nome feito só de `_` não vale. Sem acento.

| Válidos | Inválidos |
|---|---|
| `resultado`, `resultado2`, `x`, `mat`, `Matematica`, `meu_nome`, `_nome`, `nome_`, `_1` | `1a` e `2_nome` (começam com dígito), `meu-nome` (tem `-`), `número` (tem acento), `_` e `___` (só `_`) |

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
| `'Ana'`, `"Olá, Solis!"`, `'O número é ímpar'`, `"it's"` | `'Ana"` (aspas diferentes), `'Ana` (não fecha) |

### Booleano

```
verdadeiro | falso
```

As duas palavras exatas. Como também casam o padrão de Identificador, valem como Booleano, do
mesmo jeito que uma palavra reservada vale como reservada.

### Padrão

```
`[^`\n]*`
```

Abre e fecha com crase, numa linha só. Dentro, vale qualquer símbolo do alfabeto, inclusive letras
acentuadas, `?` e `\`, menos a crase e a quebra de linha. O analisador léxico só separa o padrão
do resto do texto: se o que está entre as crases é um padrão bem escrito, quem decide é o leitor
de padrões, com o núcleo de operadores de [`docs/02nucleo_minimo.md`](../docs/02nucleo_minimo.md).
Um padrão malformado entre crases é um token Padrão válido e é recusado depois, pelo leitor, com a
posição do problema.

| Válidos | Inválidos |
|---|---|
| `` `[0-9]+` ``, `` `-?[0-9]+` ``, `` `São Paulo` ``, `` `[0-9]+\.[0-9]+` `` | `` `[0-9]+ `` (não fecha na mesma linha), `'[0-9]+'` (é uma Linha, e não um padrão) |

## Delimitadores/Pontuação

| Símbolo | Função |
|---|---|
| `{` `}` | bloco |
| `(` `)` | agrupamento / parâmetros |
| `[` `]` | lista |
| `:` | separador |
| `;` | fim de instrução |
| `,` | separa parâmetros e itens de lista |
| `.` | acesso a membro: `mat.multiplicar` |

O `.` também aparece dentro do Quebrado (`3.14`). Vale o casamento mais longo: entre dígitos, o
ponto faz parte do número; depois de um nome, é o delimitador de acesso a membro.

## Comentários

```
//[^\n]*
```

Começa com `//` e vai até o fim da linha. Dentro, vale qualquer símbolo do alfabeto, inclusive
letras acentuadas, menos a quebra de linha. Não existe comentário de várias linhas.

O comentário **não vira token**: é descartado, como os espaços em branco. Vale o casamento mais
longo: `//` começa um comentário, e uma `/` sozinha é o operador de divisão.

| É comentário | Não é comentário |
|---|---|
| `// corpo do loop`, `// número de alunos`, `//` (vazio) | `/ texto` (uma barra só é a divisão) |

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
