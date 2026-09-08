# Solis — Do padrão à árvore e da árvore de volta ao padrão

---

## 1. Tabela de peças

| Peça | Trecho real | Padrão com açúcar | Reduzido ao núcleo | Forma linear da árvore | Nós |
|---|---|---|---|---|---|
| Inteiro | `2` (em `A%2 igual-a 0`) | `[0-9]+` | `(0\|1\|2\|3\|4\|5\|6\|7\|8\|9)(0\|1\|2\|3\|4\|5\|6\|7\|8\|9)*` | `concat(D, fecho(D))`, D = alt aninhado dos 10 dígitos | 40 |
| Identificador | `resultado` (em `Quebrado resultado recebe a mais b;`) | `[a-z][a-z0-9]*` | `(a\|b\|...\|z)(a\|b\|...\|z\|0\|1\|...\|9)*` | `concat(L, fecho(LD))`, L = alt aninhado das 26 letras, LD = L continuado pelos 10 dígitos | 124 |
| Operador aritmético | `%` (em `A%2 igual-a 0`) | `+\|-\|*\|/\|%` | igual ao açúcar — não há classe, faixa, `+` nem `?` a reduzir | `alt(alt(alt(alt('+','-'),'*'),'/'),'%')` | 9 |
| Palavra reservada | `funcao` (em `funcao adicionar pede (...)`) | `funcao\|pede\|retorna\|devolve\|Classe\|Possui\|Faz\|principal\|Linha\|Inteiro\|Quebrado\|Booleano\|Vazio\|Lista\|Dicionario\|Enquanto\|Para\|em\|se\|senao\|pare` | igual ao açúcar — cada palavra já é concatenação de letras, sem classe/faixa/`+`/`?` | alternância de 21 subárvores, uma por palavra, cada uma um `concat` de suas letras | 241 |
| Linha (string) | `'Digite um número :'` (em `Linha A pede 'Digite um número :';`) | `'[^']*'` | `'` seguido de `(C)*` seguido de `'`, onde C é a união dos 57 símbolos de Σ exceto a aspa | `concat('aspa', concat(fecho(C), 'aspa'))`, C = LD continuado pelos demais símbolos de Σ | 118 |

**Notas de cálculo das peças novas:**
- *Operador aritmético*: 5 folhas, 4 `alt` → 9 nós.
- *Palavra reservada*: as 21 palavras somam 121 letras. Cada palavra de comprimento k vira 2k−1 nós (folhas + concat); somando as 21 dá 221 nós. Juntar as 21 subárvores por alternância soma mais 20 nós (n−1 uniões para n itens). Total: 221 + 20 = 241.
- *Linha*: C reaproveita LD (71 nós, os 36 símbolos a–z e 0–9 do Identificador) e continua a mesma cadeia pelos 21 símbolos restantes de Σ (pontuação e especiais, exceto a aspa): 71 + 21 folhas + 21 alt = 113 nós. `fecho(C)` = 114. Concatenar com as duas folhas de aspa: 114 + 1 (folha) + 1 (concat interno) + 1 (folha) + 1 (concat externo) = 118.

---

## 2. Cobertura mínima

Fecho aparece em três das cinco peças: Inteiro (`+`, que reduz a fecho via `x+ → x x*`), Identificador (`*` já escrito direto) e Linha (`*` sobre a classe de símbolos do corpo da string).

Nenhuma peça usa opcional. O lugar onde ele apareceria é no sinal negativo do Inteiro: `-?[0-9]+`. Mas isso foi decidido de propósito fora do léxico — o `-` já existe como operador aritmético na gramática de Solis, então o sinal de um número negativo é tratado como expressão unária (`- 5`), não como parte do token numérico. Por isso o opcional nunca chega a aparecer numa peça léxica desta linguagem.

---

## 3. Um par que converge

Inteiro pode ser escrito de duas formas equivalentes:

- `[0-9]+`
- `[0-9][0-9]*`

A primeira reduz pela regra `x+ → x x*` diretamente na segunda — não é coincidência, é a própria definição da regra. Reduzindo qualquer uma das duas até o núcleo, chega-se exatamente à mesma forma linear:

```
concat(D, fecho(D))
onde D = alt(alt(alt(alt(alt(alt(alt(alt(alt('0','1'),'2'),'3'),'4'),'5'),'6'),'7'),'8'),'9')
```

| Escrita | Forma linear | Nós |
|---|---|---|
| `[0-9]+` | `concat(D, fecho(D))` | 40 |
| `[0-9][0-9]*` | `concat(D, fecho(D))` | 40 |

As duas árvores não são só do mesmo tamanho — são a mesma árvore.

---

## 4. Um par que não converge

A segunda classe do Identificador (`[a-z0-9]`) também pode ser escrita separando as duas faixas com alternância explícita:

- `[a-z0-9]`
- `([a-z]|[0-9])`

Reduzindo as duas, os nós batem (71 = 71), mas as árvores não são iguais:

| Escrita | Forma linear | Nós |
|---|---|---|
| `[a-z0-9]` | `alt` aninhado com 36 folhas simples, uma por símbolo: `alt(alt(...('a','b')...,'8'),'9')` | 71 |
| `([a-z]|[0-9])` | `alt(L, D)` — um único `alt` no topo, juntando duas subárvores prontas (L, 51 nós; D, 19 nós) | 71 |

Que as duas denotam a mesma linguagem dá para mostrar por exibição: peça qualquer símbolo do conjunto — `a`, `t`, `5`, `9` — e confira que ambas as escritas aceitam exatamente esses e nenhum outro. Ou por argumento: as duas são só reagrupamentos da mesma união de 36 símbolos; alternância é associativa, então agrupar `(a|...|z)` de um lado e `(0|...|9)` do outro antes de juntar os dois grupos não muda o conjunto final, só a forma como a árvore desce até as folhas.

Isso diz que comparar árvores (forma linear idêntica) é um teste suficiente, mas não necessário, para linguagens iguais — duas árvores diferentes ainda podem descrever exatamente o mesmo conjunto de cadeias.

---

## 5. Dois requisitos, um de cada lado

| Requisito | Sai da classe? | Expressão / o que precisaria lembrar |
|---|---|---|
| Palavra é reservada ou é Identificador? | Não sai — tem teto fixo (21 palavras) | `funcao\|pede\|retorna\|devolve\|Classe\|Possui\|Faz\|principal\|Linha\|Inteiro\|Quebrado\|Booleano\|Vazio\|Lista\|Dicionario\|Enquanto\|Para\|em\|se\|senao\|pare` (já é a peça "Palavra reservada" da tabela do item 1) |
| Variável usada foi declarada antes? | Sai de verdade | precisaria lembrar todos os nomes de variável já vistos no programa até aquele ponto; esse número não tem teto porque cresce junto com o tamanho do programa — um programa de 5 linhas declara poucas variáveis, um de 5 mil pode declarar milhares, e nada na linguagem limita esse total. Fica fora do léxico, resolvido depois por análise semântica (tabela de símbolos) |

---

## 6. Quatro recusas com posição

| Malformação | Padrão malformado | Mensagem | Posição apontada |
|---|---|---|---|
| Grupo que não fecha | `([a-z]\|[0-9]` | Grupo aberto não foi fechado antes do fim do padrão | 1 (o `(` que ficou pendente) |
| Repetição sem operando | `*[0-9]` | Repetição não tem elemento à esquerda para repetir | 1 (o `*` sem nada antes dele) |
| Classe sem colchete final | `[0-9+` | Classe aberta não foi fechada com `]` | 1 (o `[` que ficou pendente) |
| Símbolo sobrando depois do fim | `[0-9]+)` | Símbolo `)` sobrando; o padrão já havia terminado | 7 (contando `[0-9]+)` símbolo a símbolo) |
