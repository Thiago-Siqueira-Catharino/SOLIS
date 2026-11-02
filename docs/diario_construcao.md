# Diário da construção

Registro, módulo a módulo, do que foi construído, em que ordem, e por que cada decisão foi
tomada, com a alternativa descartada ao lado. A cada módulo, entra uma seção nova no fim do
arquivo, sem apagar as anteriores.

---

## Módulo: AFN e construção de Thompson

O código deste módulo fica em `Afn/`.

### A observação que a Tarefa 1 pede

**Neste módulo, a definição virou código quase sem adaptação.**

A construção de Thompson tem uma regra para cada tipo de nó da árvore, e a árvore tem seis tipos:
três folhas (símbolo, coringa e vazio) e três operadores (concatenação, alternância e fecho). A
definição é indutiva: as folhas não dependem de nada, e cada operador só depende do bloco já
construído para os filhos, nunca da forma deles.

No `thompson.py`, isso aparece de forma quase literal: a função `_construir` tem um trecho por
regra, e o trecho de cada operador chama a própria função para os filhos. Não houve decisão a
tomar sobre *o que* o código faz; as únicas adaptações foram da linguagem Python, e não da
definição:

- o C++ avisa quando um `switch` esquece um tipo de nó; o Python não avisa. Por isso o código
  termina com um erro para tipo desconhecido, e o `teste_passo4.py` passa pelos seis tipos;
- a função recursiva tem o limite de chamadas aninhadas do Python (cerca de 1000). As árvores da
  Solis ficam longe disso.

**Isso não vai se repetir.** A determinização calcula conjuntos de estados até o resultado parar de
mudar, e não há uma estrutura sobre a qual fazer indução. A análise sintática segue uma gramática,
que também é indutiva, mas exige adaptações como tirar a recursão à esquerda. A geração de código
não sai de definição nenhuma. Nos próximos módulos, cada linha passa a ser uma escolha que alguém
precisa justificar. Registrado agora, isso evita concluir depois que o projeto ficou difícil só
porque o assunto ficou difícil.

---

### A ordem da construção

| Passo | Arquivo | O que entrou | Teste |
|---|---|---|---|
| 1 | `afn.py` | estrutura da máquina, construção, validações e contagens | `teste_passo1.py` |
| 2 | `afn.py` | fecho vazio (fecho-ε) | `teste_passo2.py` |
| 3 | `afn.py` | simulação com conjunto de estados ativos | `teste_passo3.py` |
| 4 | `arvore.py`, `thompson.py` | os seis tipos de nó e a construção de Thompson | `teste_passo4.py` |
| 5 | `leitor_padroes.py` | o texto do padrão vira árvore | — |
| 6 | `bateria.py`, `casos_afn.txt` | a bateria conferida à mão | 50/50 |

A ordem foi da máquina para a árvore, e não o contrário: primeiro a máquina montada à mão e a
simulação funcionando, depois o código que monta a máquina sozinho. Assim, quando o Thompson ficou
pronto, já existia uma máquina conferida à mão para comparar com a que ele gera, e as duas saíram
iguais, seta por seta.

---

### Decisões e o que elas descartaram

#### A máquina (`afn.py`)

**Cada estado guarda uma lista de setas (símbolo, destino), e os estados são números.**
Descartado: o dicionário do AFD (`transicoes["q0"]["5"] = "q1"`). Nele, gravar uma segunda seta com
o mesmo símbolo apaga a primeira, e o AFN precisa das duas. A classe AFD do módulo anterior não é
reaproveitada.

**Estados e rótulos são validados.**
O Python aceita índice negativo em lista (`lista[-1]` é o último elemento) e aceita texto de
qualquer tamanho. Sem validação, um estado `-1` iria parar no último estado, e uma seta `"ab"` nunca
casaria na simulação, os dois em silêncio. Os dois casos geram erro na hora.

**ε é o caractere `"\0"` e o coringa é `"\x01"`.**
Todo rótulo continua sendo um caractere só. E uma seta ε **nunca** casa com um símbolo lido, nem
quando a cadeia contém o próprio `"\0"`. Descartado: a comparação direta do projeto de referência,
em que uma cadeia com `"\0"` seria aceita por uma máquina que só aceita a cadeia vazia.

**O fecho vazio marca os estados visitados.**
A marcação é obrigatória, e não só por eficiência: em `a**` existe um ciclo só de setas ε, e sem
ela a busca não termina. O `teste_passo2.py` mostra isso: a busca sem marcação é interrompida à
força depois de 50 voltas.

**O conjunto ativo é guardado em duas listas: `proximos` e `presente`.**
`proximos` guarda os estados na ordem em que entraram; `presente` tem um verdadeiro/falso por
estado e responde "já entrou?" lendo uma posição. A cada símbolo, só se desmarcam os estados que
entraram. É o mesmo modelo do `visitado` do fecho.
Descartado: o `set` do Python. Ele responderia igualmente rápido, mas não guarda a ordem de entrada,
e é a ordem que permite comparar o traço da simulação com o traço conferido à mão.

**A simulação começa no fecho vazio do estado inicial**, e não no estado inicial sozinho. Sem isso,
em `a*b`, a cadeia `"b"` seria recusada.

#### A árvore (`arvore.py`)

**Cada nó guarda os próprios filhos.**
Descartado: uma lista única de nós ligados pela posição, como no projeto de referência. Com os
filhos dentro do nó, o código tem a mesma forma da forma linear do trabalho "Do padrão à árvore":
`[0-9]+` vira `concatenacao(D, fecho(D))`. E as contagens de nós que fizemos à mão naquele trabalho
(40 para `[0-9]+` e 124 para `[a-z][a-z0-9]*`) conferem com o código.

#### A construção de Thompson (`thompson.py`)

**Toda regra devolve um bloco com uma entrada e uma saída.**
É o que permite juntar blocos sem olhar dentro deles. A concatenação liga os dois blocos por uma
seta ε, em vez de fundir os estados: fundir deixaria a máquina menor, mas exigiria olhar dentro dos
blocos. O estado a mais sai na minimização.

**O fecho tem quatro setas ε**, uma para cada frase da definição: uma vez ou mais, zero vezes, de
novo e basta. O `teste_passo4.py` monta quatro máquinas com uma seta faltando cada e mostra que as
cadeias `""`, `"a"`, `"aaa"` e `"b"` denunciam todas.

#### O leitor de padrões (`leitor_padroes.py`)

Não existia leitor de padrões no projeto: as árvores do trabalho anterior foram feitas no papel. A
bateria precisa receber os padrões como texto, então ele foi escrito neste módulo.

**O açúcar é reduzido na leitura**: `x+` vira `concatenacao(x, fecho(x))`, `x?` vira
`alternancia(x, vazio())` e as classes viram alternâncias. A árvore só conhece os seis tipos.

**Aceita vários operadores seguidos (`a**`) e aceita escape com barra (`\+`, `\.`).**
A gramática do projeto de referência não permite nenhum dos dois, mas a bateria dele usa os dois.
Ficamos com a bateria. O escape é necessário para a Solis: o padrão dos operadores aritméticos é
`\+|-|\*|/|%`.

**Classe negada (`[^...]`) é recusada.** Ela não está na gramática.

**As recusas são as que definimos no trabalho anterior**, com as mesmas posições: grupo que não
fecha, repetição sem operando, classe sem colchete final e símbolo sobrando depois do fim.

#### A bateria (`bateria.py`, `casos_afn.txt`)

**Os casos ficam num arquivo, e não no código**, para que acrescentar um caso seja só acrescentar
uma linha.

**Uma linha malformada aparece como falha.**
Descartado: pular a linha em silêncio. Se o editor trocar o Tab por espaços, todas as linhas ficam
malformadas, e pulando em silêncio a bateria rodaria zero casos sem reclamar. Pelo mesmo motivo, um
arquivo sem nenhum caso também conta como falha.

**A bateria não para no primeiro caso que falha**: mostra todos de uma vez, com o arquivo, a linha,
o veredito esperado e o obtido, e termina com código 1.

**Como os vereditos foram decididos:** à mão, grupo por grupo, seguindo cada padrão símbolo por
símbolo, **antes** de rodar o programa. Só depois de os 50 estarem decididos a bateria foi rodada,
com resultado 50/50. Uma bateria escrita depois de rodar o programa copiaria os defeitos dele como
resposta certa.

---

### Limites conhecidos

- Os arquivos `teste_passo1.py` a `teste_passo4.py` imprimem `[FALHOU]` quando algo dá errado, mas
  terminam com código 0. Quem interrompe a execução em caso de falha é a bateria.
- A construção de Thompson é recursiva e tem o limite de chamadas aninhadas do Python.

### Pendências encontradas, para os próximos módulos

- **`Se` com maiúscula:** o `parte1.md` escreve `Se A%2 igual-a 0`, mas a palavra reservada é `se`.
  Pelo padrão, `Se` é recusada. É preciso decidir se o exemplo ou a lista está errado.
- **A vírgula:** está no alfabeto, mas não na lista de delimitadores de `classes_lexicas.md`, embora
  apareça em listas e parâmetros.
- **A Linha** (`'[^']*'`) depende de classe negada, que o leitor recusa.
- **O Quebrado** depende do `.`, que não está no alfabeto.
