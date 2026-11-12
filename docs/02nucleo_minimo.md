# O núcleo mínimo de operadores de padrão

Os padrões das classes léxicas da Solis (`[0-9]+`, `[a-zA-Z_][a-zA-Z0-9_]*`...) são lidos pelo
leitor de padrões (`Leitor_De_Padroes/`), que monta a árvore de cada um. Este documento registra
quais operadores de padrão essa árvore conhece e quais notações são só conveniência de quem
escreve, reduzidas ao núcleo durante a leitura.

O critério de inclusão no núcleo é um só: **a impossibilidade de reduzir**. Um operador que se
escreve pela composição de outros é conveniência de quem escreve o padrão, e não capacidade nova
do sistema. Mantê-lo no núcleo acrescentaria um caso a tratar na construção de Thompson, a peça que
percorre a árvore para montar a máquina, sem que a máquina passasse a reconhecer nada a mais.

## O núcleo

Três operadores e três folhas.

| Construção | Papel |
|---|---|
| concatenação | núcleo: uma coisa seguida de outra |
| alternância | núcleo: uma coisa ou outra |
| fecho | núcleo: zero ou mais repetições |
| símbolo | folha: um símbolo do alfabeto |
| cadeia vazia | folha: produzida pela redução do opcional `x?` |
| coringa | folha: qualquer símbolo; é a exceção ao critério, explicada abaixo |

São os 6 tipos de nó de `Leitor_De_Padroes/arvore.py`. Tudo o mais que se escreve num padrão é
reduzido a eles durante a leitura, em `Leitor_De_Padroes/leitor_padroes.py`. Por isso a construção
de Thompson (`Afn/thompson.py`) tem um trecho para cada operador e um trecho para as três folhas, e
nenhum para as notações de conveniência.

## As reduções, em pares

| Quem escreve o padrão escreve | A árvore recebe | Nós |
|---|---|---|
| `x+` | `concat(x, fecho(x))` | os de `x` duas vezes, mais 2 |
| `x?` | `alt(x, vazio)` | os de `x`, mais 2 |
| `[abc]` | `alt(alt('a', 'b'), 'c')` | 2n − 1, para n símbolos |
| `[a-c]` | `alt(alt('a', 'b'), 'c')`, a mesma árvore de `[abc]` | 2n − 1 |
| `[aa]` | `'a'`: um símbolo repetido na classe entra uma vez só | 2n − 1, contando cada símbolo uma vez |
| `(x)` | `x`: o grupo não sobrevive à leitura | os de `x` |
| `\.` | `'.'`: o ponto como símbolo comum | 1 |

Os parênteses servem para quem escreve dizer onde a precedência muda. Montada a árvore, a forma dela
**já é** a precedência, e um nó de grupo não teria o que guardar: `(ab)c` e `abc` dão a mesma
árvore, o que o `demonstrar_leitor.py` confere.

Na redução de `x+`, a subárvore de `x` aparece duas vezes, mas o leitor não a copia: os dois lugares
apontam para a mesma subárvore. Isso é seguro porque os nós não podem ser alterados depois de
criados. A contagem de nós e a construção de Thompson passam pelas duas ocorrências, uma de cada
vez, e por isso `x+` conta os nós de `x` duas vezes e a máquina ganha estados novos em cada
passagem. Exemplo: `a+` tem 4 nós (1 + 1 + 2).

## A exceção: o coringa

O coringa `.` poderia ser reduzido: ele é a alternância de todos os símbolos do alfabeto. Mas o
alfabeto da Solis tem 113 símbolos (`especificacao/alfabeto.md`), e a redução trocaria **1 folha
por 2 × 113 − 1 = 225 nós** em cada ocorrência, uma árvore que ninguém consegue ler, para dizer o que
uma folha só já diz.

Por isso ele fica como folha própria, e o custo dessa escolha tem endereço certo: a construção de
Thompson leva o coringa como rótulo de uma seta, e a simulação do AFN aceita qualquer símbolo
nessa seta. A exceção tem razão de tamanho, e não de capacidade, e fica escrita para que quem a
encontrar saiba que ela foi decidida, e não esquecida. Hoje nenhuma classe léxica da Solis usa o
coringa.

A classe de símbolos, ao contrário, **é** reduzida, mesmo custando caro: a primeira classe do
Identificador, `[a-zA-Z_]`, vira 105 nós. A diferença é que quem escreve a classe escolhe o tamanho
dela; o coringa tem sempre o custo máximo.

## Fora do núcleo

**Classe negada (`[^...]`).** Ela também se reduz: é a alternância dos símbolos do alfabeto que não
estão na lista. Então, se entrar, entra como redução, nunca como operador do núcleo. Hoje o leitor a
recusa, e isso é um limite conhecido: o padrão da Linha (`'[^'\n]*'`) depende dela.

**Quantificador contado (`x{3,5}`).** Também se reduz, a concatenações e opcionais, então o
critério já o deixaria fora do núcleo. E ele não entra nem como notação, porque na Solis `{` e `}`
são delimitadores: o padrão dos delimitadores (`{|}|\(|\)|...`) precisa deles como símbolos
comuns. Por isso o leitor lê `x{3,5}` como seis símbolos seguidos.

**Simplificar repetições seguidas.** O leitor aceita `a**` e monta `fecho(fecho('a'))`, sem trocar
por `fecho('a')`, que reconhece as mesmas cadeias. A simplificação não acrescenta capacidade
nenhuma, e a máquina gerada continua correta.
