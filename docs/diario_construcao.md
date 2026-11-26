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

---

## Correções a partir do feedback do professor

Depois do módulo do AFN, o professor revisou o repositório e deixou comentários em cada atividade.
Esta seção registra o que mudou por causa deles, na ordem em que foi feito, com o número do pull
request entre parênteses.

### O alfabeto e as classes léxicas

O feedback: "Faltam maiúsculas, espaço, `"` e `.` no alfabeto, e Identificadores e Literais estão
vazios."

**O alfabeto passou a ter 113 símbolos** (#54). As decisões, tiradas dos exemplos que o próprio
repositório já usava:

- **as duas aspas** valem, porque o recorte usa `"texto aleatorio"` e o README usa `'Ana'`;
- **espaço, Tab e quebra de linha** entram. O Tab entra para que um arquivo indentado com Tab não
  seja recusado;
- **letras acentuadas** entram, mas só valem dentro de uma Linha (`'O número é ímpar'`). Palavras
  reservadas e identificadores continuam sem acento.

**Identificadores e Literais foram preenchidos com padrões** (#55, #57). Descartado: descrever a
classe só em texto. Uma classe infinita não se lista, e a frase sozinha deixa brecha ("letra"
inclui acento?); o padrão é o que entra direto no leitor de padrões. Cada padrão ficou com uma
frase que o explica e com exemplos válidos e inválidos.

- **Quebrado:** `[0-9]+\.[0-9]+`, com dígito dos dois lados do ponto. `.5` e `3.` são recusados.
- **Inteiro sem sinal:** o negativo vem do operador `-`, na gramática.

**O recorte deixou de copiar o alfabeto e as classes** (#56). Ficou um resumo e o link para
`especificacao/`. Descartado: manter a cópia completa. Foi a cópia que deixou o recorte diferente
da especificação, e com uma cópia só isso não se repete.

### Os exemplos escritos em Solis

Antes da especificação, os exemplos tinham de concordar entre si (#64 a #70):

- **bloco é `{ }`** também em `se`, `senao`, `enquanto` e `para`, como em `funcao` e `Classe`. Os
  marcadores de lugar passaram de `{Tipo}` para `<Tipo>`, porque `{ }` agora é bloco;
- **parâmetro tem tipo** (`pede (Quebrado a, Quebrado b)`), porque a linguagem é fortemente tipada;
- **Inteiro entra onde se espera Quebrado; o contrário é recusado.** É o que permite
  `soma(x, y)` com `y` Inteiro;
- **as palavras de controle valem com inicial maiúscula ou minúscula** (`se`/`Se`, `senao`/`Senao`,
  `enquanto`/`Enquanto`, `para`/`Para`, `em`/`Em`, `pare`/`Pare`). As outras palavras têm uma
  grafia só;
- entraram **`Imprime`/`imprime`**, sempre chamados com parênteses, **`Novo`** e **`lista`**, que os
  exemplos já usavam. As palavras reservadas passaram de 21 para 31.

O `parte1.md` tinha erros que um compilador recusaria: a variável `c` que não existia (o parâmetro
era `C`), uma Linha usada com `%`, uma lista guardada numa Linha e as mensagens do verificador
trocadas. Foram corrigidos. Os dois primeiros são o tipo de erro que a especificação deve
descrever na seção de verificação antes de rodar.

### O leitor de padrões

O feedback da atividade "Expressões Regulares e Linguagens Regulares": "Faltam o código do parser e
as 7 seções." O parser já existia, escrito durante o AFN, mas estava dentro de `Afn/` e nada
mostrava que ele cumpria a tarefa.

**Pasta própria, `Leitor_De_Padroes/`** (#59). Descartado: deixar dentro de `Afn/`, que dá menos
trabalho. A pasta própria deixa o repositório na ordem em que as peças acontecem: o leitor monta a
árvore, e o AFN só a consome. Os dois arquivos foram movidos sem alteração.

**A folha vazia passou a se escrever `vazio`, e não `ε`** (#60), para que a árvore possa ser
comparada com a do material caractere por caractere. A seta vazia do AFN continua `ε`: é outro
conceito.

**A recusa tem duas posições** (#61): onde a leitura constatou o problema e onde ele começou. Em
`a(b|c`, a falta é constatada no fim do texto (posição 6), onde a pessoa vai digitar a correção, e o
grupo abriu na posição 2. Descartado: só a posição do material, o fim, porque perderia a decisão do
trabalho "Do padrão à árvore", que apontava o `(` aberto; e só a nossa, porque o material pede a
posição constatada. As posições continuam contadas a partir de 1, e a marca `^` vai na linha de
baixo.

**O `demonstrar_leitor.py`** (#62) mostra o leitor cumprindo as tarefas: as cinco expressões do
material, os padrões da Solis, a convergência e as recusas. Os nós esperados dos padrões da Solis
foram contados à mão, em quizzes, antes de rodar. Descartado: tirar o esperado da própria saída do
programa, que conferiria o programa com ele mesmo.

**O núcleo mínimo foi reescrito** (#73). O arquivo antigo tratava dos operadores aritméticos, mas a
tarefa pede os operadores de padrão: concatenação, alternância e fecho, e as reduções em pares.

### O resultado esperado e o script que roda tudo

O feedback: "Deixem explícito o resultado esperado e incluam um script que rode tudo."

**Cada parte mostra o esperado e termina com código 0 ou 1** (#74 a #80). Os AFDs só mostravam o
resultado obtido; os testes do AFN terminavam com uma linha `Erro: ...` proposital, que parecia
falha, e com código 0 mesmo quando mostravam `[FALHOU]`. Agora cada caso sai com `[OK]` ou
`[FALHOU]` e o esperado ao lado, os erros propositais aparecem como `[OK] erro esperado (...)`, e
cada programa termina com placar e código 1 se algo falhar. Isso resolve o limite registrado na
seção do AFN.

**O `rodar_tudo.py`, na raiz** (#81), roda as nove partes e mostra um placar geral. Ele decide se
cada parte passou pelo código de saída, e não lendo o texto que ela imprime. Força UTF-8 na saída
das partes, porque no Windows a saída redirecionada não usa UTF-8 e o `ε` dos testes do AFN
quebraria. Descartado: `.bat` ou `.sh`, porque um script Python funciona igual em Windows e Linux.

O README ganhou a seção "Como rodar tudo", com a saída esperada completa (#82).

### O `_` no identificador

O identificador passou a aceitar `_` em qualquer posição, mas um nome feito só de `_` (`_`, `___`)
não vale (#83 a #89). O padrão ficou `[a-zA-Z][a-zA-Z0-9_]* | _+[a-zA-Z0-9][a-zA-Z0-9_]*`, e `_1`
vale. O analisador léxico não sabe se um nome é de variável, função ou classe; quem sabe é a
análise sintática. Por isso a regra vale para todo nome.

**A mesma regra custou muito diferente em cada peça.** No AFD, custou **um estado a mais** (o `q2`,
"até agora só leu `_`"). Na árvore, o Identificador foi de **232 para 486 nós**: a regra "pelo
menos uma letra ou dígito" não se escreve com um caminho só, e cada um dos dois caminhos repete as
classes grandes. O AFD foi conferido contra o padrão em todas as 3.906 palavras de até 5 símbolos
sobre {a, Z, 0, _, -}, sem diferença.

A bateria do AFN manteve os casos do identificador antigo, que continuam certos para aquele padrão,
e ganhou um grupo com o identificador de hoje e a vírgula nos delimitadores: de 50 para 57 casos.

### O que a seção do AFN registrava e foi resolvido

- os testes dos passos terminarem com código 0 (#74 a #80);
- o `Se` com maiúscula, que agora é palavra reservada (#68);
- a vírgula fora dos delimitadores (#57);
- o `.` fora do alfabeto (#54).

### Pendências

- **As 7 seções da especificação**, da atividade "Expressões Regulares e Linguagens Regulares",
  esperam o grupo decidir o assunto do Projeto Integrador. A seção 1, domínio e cena, depende dele,
  e os exemplos das outras seções dependem da seção 1.
- **A Linha** depende de classe negada (`[^...]`), que o leitor ainda recusa.
- **A faixa numérica**, sugerida pelo professor para o requisito que parece sair da classe, na
  seção 5 do trabalho "Do padrão à árvore".
- **O cabeçalho do `afd_letras.py`** diz `[a-z]+`, mas o padrão reconhecido é `[a-zA-Z]+`.

### Segunda leva de correções

Depois de fechar os feedbacks, uma varredura no repositório inteiro procurou o que tinha ficado para
trás: padrões antigos, números que mudaram e exemplos que não batiam com as decisões.

**O requisito que parece sair da classe** (#92, #93). O professor sugeriu uma faixa numérica para a
seção 5 do trabalho "Do padrão à árvore". O requisito "palavra reservada ou identificador", que
nem parecia sair da classe, foi trocado por "o literal Inteiro cabe no `int` (de 0 a 2147483647)?".
Ele parece sair, porque a máquina teria de comparar o valor do número, mas não sai: o teto é o do
`int` do Java, base da Solis, e a máquina só precisa lembrar quantos dígitos leu e se o número está
igual ao limite ou abaixo dele. A expressão aceita zeros à esquerda (`0*`), como o Inteiro. Tem 13
alternativas e 392 caracteres, e o leitor conta 1.298 nós; foi conferida contra o valor real de
2.515 números, sem erro. Descartado: a faixa de 0 a 255, mais curta, mas que não vem de nenhuma
decisão da Solis; e acrescentar a faixa como terceiro requisito, porque a seção pede dois, um de
cada lado.

**Os operadores do README** (#94) passaram a ser os do `classes_lexicas.md`: `maior-que` no lugar
de `{maior}`, a forma por extenso de cada operador e as tabelas de atribuição e de operadores
lógicos. Os 13 pares símbolo e forma por extenso foram conferidos um a um contra as classes
léxicas.

**O `Dicionario` saiu das palavras reservadas** (#96 a #98). Nenhum arquivo dizia o que ele é nem
como se escreve, e o grupo decidiu tirá-lo. As palavras reservadas passaram
de 31 para 30; os nós esperados do padrão, contados à mão antes de rodar, passaram de 337 para 317.
Descartado: pôr na tabela de tipos com a sintaxe "a definir", que registraria um tipo sem nenhuma
decisão por trás.

**A descrição do primeiro módulo** (`docs/descricao_linguagem.md`) ficou como estava, com um aviso
de registro histórico no topo apontando para o recorte e para `especificacao/` (#99). Descartado:
atualizar o arquivo. Duas descrições para manter foi o que deixou as duas diferentes.

**A classe do comentário** (#100 a #103). Os exemplos do README usavam `//`, mas não existia classe
para ele, e o analisador leria `//` como duas divisões. O comentário começa com `//`, vai até o fim
da linha, pode ter acento e é descartado como os espaços em branco: o padrão é `//[^\n]*`. Pelo
casamento mais longo, `//` começa um comentário e uma `/` sozinha é a divisão. Descartado: tirar
os `//` dos exemplos. Como a Linha, o padrão usa classe negada, que o leitor ainda não aceita, então
foi conferido montando a máquina à mão sobre os 113 símbolos do alfabeto.

Também entraram ajustes menores: o cabeçalho do `afd_letras.py` passou a dizer `[a-zA-Z]+` (#91),
e o alfabeto passou a mostrar o uso do sublinhado (#95).

**Ficou como está, de propósito:** a parte 5 do `teste_passo4.py` continua testando o identificador
antigo (`[a-zA-Z][a-zA-Z0-9]*`). O teste está certo para aquele padrão, e o identificador de hoje
já é conferido no `demonstrar_leitor.py`.

### Pendências, depois da segunda leva

- **As 7 seções da especificação**, da atividade "Expressões Regulares e Linguagens Regulares",
  esperam o grupo decidir o assunto do Projeto Integrador.
- **A Linha e o comentário** dependem de classe negada (`[^...]`), que o leitor ainda recusa.
- **Para a análise sintática:** `e` é operador lógico e também parte da sintaxe de função
  (`pede (...) e retorna`), e `pede` marca os parâmetros e também a leitura de entrada
  (`Inteiro A pede '...'`). Para o analisador léxico, cada um é um token só; a gramática vai
  precisar distinguir os dois usos.

A faixa numérica e o cabeçalho do `afd_letras.py`, da lista anterior, foram resolvidos nesta leva.

### Terceira leva: a revisão do projeto inteiro

Uma revisão de todos os arquivos procurou o que ainda estava diferente entre o código, a
especificação e os exemplos. A conferência nova desta leva foi **passar todo exemplo de código Solis
do repositório pelas classes léxicas que o próprio grupo definiu**: o `exemplos.sol`, os blocos do
README, o `parte1.md` e o recorte, lidos pelo casamento mais longo. Foi a primeira vez que os
exemplos e a especificação se encontraram de verdade.

**O ponto de acesso a membro não tinha classe** (#113 a #117). A varredura achou um símbolo só sem
classe: o `.` de `mat.multiplicar`. O alfabeto dizia que o ponto tem dois usos, mas as classes só
cobriam o do Quebrado, e o analisador léxico recusaria o exemplo completo do README. O `.` entrou
nos **delimitadores**, com a função "acesso a membro". Descartado: pôr nos operadores. Depois do
ponto vem sempre um nome, e não uma expressão qualquer (`mat.multiplicar`, nunca `mat.(x + y)`):
é uma regra de forma, não de cálculo, e assim a tabela de precedência fica só com operadores de
verdade. O Java, base da Solis, também lista o `.` entre os separadores. Pelo casamento mais longo,
o ponto entre dígitos continua sendo parte do Quebrado (`3.14`). No padrão da demonstração ele vai
escapado (`\.`), porque sozinho seria o coringa; o Delimitador passou de 17 para 19 nós. A bateria
do AFN ganhou dois casos: `.` aceita e `a` recusa, que prova que, dentro dos colchetes, o ponto é
símbolo comum. Ela passou de 57 para 59 casos. Depois da mudança, nenhum exemplo do repositório
tem símbolo sem classe.

**A `lista` minúscula saiu** (#105 a #109). `Lista` é o tipo e aparece só na declaração; os itens
vêm direto entre colchetes: `Lista Colaboradores recebe ['Ana', 'Beatriz', 'Luana'];`. As
palavras reservadas passaram de 30 para 29, e o padrão delas, de 317 para 307 nós, contados à mão
antes de rodar.

**O `devolve` tem duas formas** (#110 a #112): `devolve <valor>;` numa função que retorna um valor,
e `devolve;` sozinho numa função que retorna `Vazio`. `Vazio` é só tipo. Descartado: `devolve
Vazio;`, que deixaria a gramática com uma forma só, mas faria `Vazio` ser tipo e valor ao mesmo
tempo, e a verificação de tipos precisaria de uma regra para impedir `Inteiro x recebe Vazio;`. O
grupo preferiu pagar o custo agora, na gramática, a deixar essa exceção para a verificação.

**A classe termina com `}`, sem `;`.** Funções, `Possui`, `Faz` e os blocos de controle terminam
com `};`. Os exemplos já seguiam essa regra, que entra escrita na especificação.

**O paradigma é também funcional** (#118). O recorte registrava só a orientação a objetos, e o
README dizia "orientado a objetos e funcional". Agora o recorte diz que um programa em Solis pode
ser escrito só com funções, sem nenhuma classe, como a `soma` e a `principal` do `exemplos.sol`.

### O assunto do Projeto Integrador

A Tarefa 1 do módulo "Expressões Regulares e Linguagens Regulares" pede começar pelo domínio que o
recorte fixou, e diz que o assunto é a decisão mais cara de desfazer do percurso. O recorte fixou
uma linguagem para scripts, integrável com outras linguagens, em português e inspirada em Lua. O
material também lista quatro sinais de um assunto que "parece bom e falha": executar direto sem
gravar objeto, comandos de formato fixo sem aninhamento, todo valor da mesma natureza e usar um
reconhecedor pronto de biblioteca. A Solis passa nos quatro, desde que a especificação diga o que
o compilador grava e quem executa depois.

O que falta é a cena: quem escreveria em Solis e para obter o quê. Foram levantados três caminhos:
o do Lua, de scripts embutidos num programa maior, para quem usa esse programa automatizá-lo ou
personalizá-lo em português; o do ensino de programação em português; e um dos vinte assuntos do
Projeto Integrador. **O caminho escolhido para o grupo discutir é o primeiro**, por ser o que menos
contradiz o recorte e o que já foi construído. Falta escolher o programa e a pessoa, e conferir a
escolha contra as cinco perguntas de "O Teste que Fecha a Escolha", que estão no texto do Projeto
Integrador.

### Pendências, depois da terceira leva

- **As 7 seções da especificação**, que esperam a cena do caminho escolhido.
- **A Linha e o comentário** dependem de classe negada (`[^...]`), que o leitor ainda recusa.
- **Para a análise sintática:** os dois usos de `e` (operador lógico e `pede (...) e retorna`) e de
  `pede` (parâmetros e leitura de entrada); a regra de que o valor de `devolve` combina com o tipo
  de retorno da função; e a classe terminada em `}`, sem `;`.

---

## Módulo: Determinização e minimização

O código deste módulo fica em `Determinizacao/`. Ele segue o guia "Implementação em C++: Thompson,
determinização e minimização", passos 12 a 25 do roteiro; os passos 1 a 11 são os do módulo do
AFN, na pasta `Afn/`.

### O que a observação do módulo do AFN previu

No módulo do AFN, este diário registrou que a definição tinha virado código quase sem adaptação, e
que isso não ia se repetir. **Não se repetiu.** A construção de subconjuntos não é indutiva: ela
calcula conjuntos até não aparecer nenhum novo, e o código precisou de escolhas que a definição
não faz: como guardar um conjunto para reconhecê-lo depois, em que ordem tirar os pendentes, o que
fazer com o conjunto vazio, qual é o alfabeto. A minimização também: o que fazer com os estados
que nenhuma cadeia alcança, e quando parar. Cada uma dessas escolhas está registrada abaixo, com a
alternativa descartada.

### A ordem da construção

| Passo do roteiro | Arquivo | O que entrou | Teste |
|---|---|---|---|
| 12 a 16 | `afd.py`, `determinizacao.py` | o AFD, o catálogo, o estado inicial, movimento seguido de fecho, o laço dos pendentes e o vazio | `teste_determinizacao.py` |
| 17 | `teste_determinizacao.py` | a equivalência entre o AFN e o AFD sobre o alfabeto | 39/39 |
| 18 a 23 | `minimizacao.py` | completar, inacessíveis, partição inicial, assinaturas, ponto fixo e reconstrução | `teste_minimizacao.py`, 36/36 |
| 24 e 25 | `demonstrar_determinizacao.py` | as três máquinas comparadas e a explosão de estados | 71/71 |

Um detalhe da ordem: o passo 2 do roteiro cria as estruturas do AFN, do AFD e do Bloco juntas.
Aqui o AFD só foi criado no passo 12, quando a determinização passou a usá-lo. O resultado não
muda.

---

### Decisões e o que elas descartaram

#### O AFD (`afd.py`)

**Um AFD novo, com estados numerados e um dicionário `{símbolo: destino}` por estado.**
Gravar de novo o mesmo símbolo substitui o destino, e é isso que mantém um destino só por par
(estado, símbolo). Descartado: reaproveitar o AFD de `Afds/Afd_Solis/`, que tem estados com nome
(`"q0"`) e não tem estado de erro; a determinização cria os estados um a um, e o número de cada um
é a ordem em que o conjunto apareceu. Descartado também: a lista de setas do AFN, que aceitaria
dois destinos para o mesmo símbolo.

**Uma seta com símbolo fora do alfabeto é recusada na hora**, porque a determinização e a
minimização só percorrem o alfabeto, e essa seta nunca seria usada.

#### A determinização (`determinizacao.py`)

**O alfabeto é fechado: os símbolos das setas do AFN, sem ε e sem o coringa.**
O coringa vira, no AFD, uma seta para cada símbolo desse alfabeto. A consequência, que o guia
avisa: em `a.c` o alfabeto é {a, c}, o AFN aceita `abc` pelo coringa e o AFD recusa. Por isso as
máquinas só são comparadas em cadeias sobre o alfabeto, e na bateria do AFN 12 dos 59 casos ficam
de fora da comparação.

**A chave do catálogo é uma tupla com os estados sem repetição e em ordem.**
Assim `[0, 2, 4]` e `[4, 0, 2]` caem na mesma chave. Descartado: a lista, que não serve de chave de
dicionário no Python. O `frozenset` também serviria de chave, mas não tem ordem, e a tupla em
ordem é a forma que aparece na tabela do guia e na tela.

**Os pendentes são uma pilha: sai o último que entrou**, como no guia. A ordem não muda a máquina,
só a numeração dos estados; com a mesma ordem do guia, a numeração também sai igual, e a tabela
de `(a|b)*c` pôde ser conferida estado por estado (D0 a D4).

**O conjunto vazio não tem caso especial: na primeira vez que aparece, recebe número e vira o
estado de erro.** O AFD sai completo. Descartado: criar o estado de erro de antemão, como faz o
projeto do material. Com ele, o erro existiria mesmo quando nenhuma cadeia chega nele, e as
contagens mudariam: em `(a|b)*abb`, 6 estados em vez de 5. As duas formas aceitam as mesmas
cadeias; a escolhida conta só estados que alguma cadeia alcança.

#### A minimização (`minimizacao.py`)

**A minimização trabalha numa cópia do AFD.** Completar acrescenta estado e setas; sem a cópia, o
AFD recebido mudaria por baixo de quem o passou. Em Python a cópia é explícita (`deepcopy`), porque
passar um objeto não o copia; no guia, a cópia vem de receber o AFD por valor.

**Os estados inacessíveis são descartados antes do refinamento.** O resultado é o autômato
mínimo. Descartado: conservar o erro inalcançável, como o material faz, o que entrega a máquina
que ele chama de reduzida, com um estado a mais (`(a|b)*abb`: 5 em vez de 4).

**O ponto fixo é detectado comparando o número de grupos com o da rodada anterior.** Uma rodada só
divide grupos, nunca junta; se o número não mudou, nada se dividiu. Descartado: parar quando a
contagem chega a um número esperado, que pode deixar estados distinguíveis no mesmo grupo.

**O refinamento é o simples do guia, com a busca do grupo de cada estado feita grupo por grupo.**
Descartado, por enquanto: o algoritmo de Hopcroft e o vetor que guarda o grupo de cada estado. O
guia pede a versão simples primeiro, conferida com a bateria, e o maior AFD da bateria, o do
Identificador, tem 244 estados.

**Os subgrupos de uma rodada entram em ordem de assinatura**, como no `map` do guia. A ordem não
muda a máquina, mas deixa a numeração sempre igual, e os grupos podem ser conferidos com os do
exemplo do guia ({A}, {B, C}, {D, E}).

**No código, o grupo da partição se chama `grupo`**, como no guia, para não confundir com o
`Bloco` da construção de Thompson.

---

### Como os valores esperados foram decididos

Os testes só usam valores que existiam antes de o código rodar:

- **do guia:** a tabela de `(a|b)*c` (seção 1.5.6), as sete cadeias da seção 1.5.9, o exemplo de
  minimização das seções 1.6.2 e 1.6.3, as contagens da seção 1.7.3 e a bateria da seção 1.8.5
  (121 cadeias, 15 aceitas);
- **do material:** os conjuntos 0 e 2 de `(a|b)*abb` no mesmo grupo, a partição de um grupo só
  quando todos os estados aceitam, e as fórmulas da explosão;
- **contados à mão:** o AFD escrito com setas faltando e um estado inacessível, com a conta escrita
  ao lado de cada verificação.

**Os números do material não foram usados direto.** O material cria o estado de erro de antemão e
o conserva na minimização, e por isso conta um estado a mais no AFD e no mínimo sempre que o vazio
não é alcançável. O guia mostra essa diferença em `(a|b)*abb` (6 e 5 no material, 5 e 4 aqui). Nos
casos em que o vazio é alcançável, como `a.c`, as contagens coincidem.

**Na explosão, a conferência não depende de nenhuma das máquinas.** As três são comparadas com a
definição da linguagem escrita direto em Python ("a cadeia tem pelo menos n símbolos e o n-ésimo
contado do fim é `a`"), em todas as 2047 cadeias sobre {a, b} até o comprimento 10.

### A explosão de estados

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| AFN | 10 | 16 | 22 | 28 | 34 | 40 | 46 | 52 |
| AFD | 3 | 5 | 9 | 17 | 33 | 65 | 129 | 257 |
| Mínimo | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 |

O AFN cresce 6 estados por n (6n + 4); o AFD dobra (2ⁿ + 1). Até n = 5 o AFD ainda é menor que o
AFN (33 contra 34); a partir de n = 6, é maior. O mínimo fica exatamente no piso de 2ⁿ que o
material prova, e então o crescimento é da linguagem, e não do algoritmo: nenhum AFD reconhece essa
linguagem com menos estados. No material, as duas colunas empatam em n = 5 (34 e 34), porque o AFD
de lá conta o estado de erro inalcançável.

---

### Limites conhecidos

- O refinamento simples tem custo cúbico no número de estados, no pior caso (seção 1.9 do guia).
  Os AFDs do projeto ficam longe de pesar; para AFDs grandes, o caminho é o algoritmo de Hopcroft.
- O alfabeto fechado vale para comparar máquinas de um padrão só. Para o analisador léxico, o
  alfabeto precisa ser o da Solis (`especificacao/alfabeto.md`), e não o de cada padrão: uma
  classe negada como a da Linha (`[^'\n]`) só tem sentido em relação ao alfabeto inteiro.

### Pendências, depois deste módulo

- **As 7 seções da especificação**, que esperam a cena do caminho escolhido para o assunto.
- **A Linha e o comentário** dependem de classe negada (`[^...]`), que o leitor ainda recusa, e do
  alfabeto inteiro da Solis, que a determinização ainda não recebe.
- **Para a análise sintática:** os dois usos de `e` e de `pede`; a regra de que o valor de
  `devolve` combina com o tipo de retorno; e a classe terminada em `}`, sem `;`.

---

## Módulo: A especificação e os padrões na Solis

O trabalho deste módulo fica na branch `Especificacao_Modulo_02`. Ele fecha a Tarefa 1 do módulo
"Expressões Regulares e Linguagens Regulares": a especificação em sete seções, em
`especificacao/especificacao.md`. Para escrevê-la, o grupo precisou mudar o que a Solis é, e as
mudanças passaram pelo recorte, pelo alfabeto, pelas classes léxicas, pelo núcleo mínimo, pelo
README, pelo exemplo e pela demonstração do leitor.

### O que o texto do Projeto Integrador mostrou

A terceira leva deste diário registrou que a Solis "passa nos quatro" sinais de assunto que falha.
Aqueles quatro sinais eram só os da Tarefa 1. O texto do Projeto Integrador traz **seis
propriedades** que um assunto precisa ter, e a Solis, como estava, não cumpria duas delas: quem
usava a linguagem **não escrevia padrões**, e o domínio **não tinha um pedido que a máquina finita
não atende**. O mesmo texto descreve, como "o erro previsível", a escolha de "uma pequena linguagem
imperativa", que era o caso da Solis. Das cinco perguntas de "O Teste que Fecha a Escolha", a
terceira (escrever três padrões na linguagem e dizer o que cada um reconhece) ficava sem resposta.

Foram três caminhos: **A**, manter a Solis como estava, com a pergunta 3 sem resposta e o capítulo
do limite sem demonstração; **B**, dar padrões à Solis; **C**, trocar para um dos vinte assuntos.
**O grupo escolheu o B.** O C foi descartado por ser inviável: descartaria a Solis inteira. O A
foi descartado porque deixaria a primeira parte do que já foi construído (leitor, Thompson,
determinização e minimização) servindo só aos tokens da própria Solis; no B, a mesma peça compila
também os padrões de quem escreve.

### A cena

A Solis passa a ter um domínio: **registros com campos**, e a forma que cada campo pode ter. Quem
escreve é uma pessoa que precisa automatizar uma tarefa e não domina o inglês nem uma linguagem em
inglês, como um júnior que precisa identificar, organizar ou filtrar registros; o script que ele
escreve é incorporado ao projeto da equipe. A Solis é, para essa pessoa, a porta de entrada.

---

### Decisões e o que elas descartaram

#### Os padrões

**O padrão é escrito entre crases, numa linha só, e guardado no tipo `Padrao`.** Descartado: entre
barras, porque a `/` já é a divisão e `a / b / c` ficaria ambíguo; e dentro de aspas, porque uma
`Linha` viraria `Padrao` pela atribuição e a fronteira entre os dois tipos ficaria borrada.
Descartado também: o padrão ocupar várias linhas, porque uma crase esquecida só seria apontada
longe de onde está.

**O padrão vazio (duas crases seguidas) é permitido**, e só casa com a Linha vazia. Descartado:
proibi-lo, trocando o `*` da classe por `+`.

**As operações são `casa` (o texto inteiro tem a forma) e `procura` (os trechos com a forma, o mais
longo de cada vez), sem captura.** Descartado: só `casa`, porque o executor quase não trabalharia
sobre a entrada; e a captura, que o próprio Projeto Integrador trata como uma proposta inteira e
difícil.

**As operações são métodos, chamados com o `.`**: `numero.casa(campo)`. Descartado: um operador por
extenso (`campo casa numero`), que entraria na tabela de precedência.

**O pedido que nenhum padrão atende são os parênteses balanceados.** Descartados: blocos que abrem
e fecham com outras marcas (o mesmo problema) e o trecho que volta invertido, menos natural para
quem escreve scripts.

#### O alfabeto

**Entram a crase, o `?` e a `\`**, para escrever os padrões, e **os símbolos de registro `@`, `#`,
`$`, `º`, `ª` e `°`**, que aparecem nos registros: e-mails, números de pedido, dinheiro, ordinais e
graus. Todos, e também as letras acentuadas, valem só dentro de padrão, de Linha e de comentário.
O alfabeto passa de 113 para **122 símbolos**. Que o `?` e a `\` valessem também na Linha e no
comentário foi uma decisão tomada sem perguntar antes e aprovada depois: sem ela, `'Qual o seu
nome?'` seria erro léxico. O `^` ficou de fora, porque o leitor o usa para marcar a classe negada.

**Os registros podem ter qualquer símbolo: os que estão fora do alfabeto contam como um só, o
outro, que só o coringa reconhece.** Descartado: recusar o registro, porque um filtro que trava no
primeiro `€` não cumpre o domínio.

#### O que o sistema produz

**O compilador grava um objeto, e um executor, máquina virtual embutida no projeto, o roda
depois.** Descartados: gravar código de outra linguagem (o executor deixaria de ser do grupo) e um
executável nativo (preso a um sistema operacional, contra a restrição do Projeto Integrador). O
recorte dizia "o programa é executado", que o material aponta como sinal de erro.

**O objeto guarda o cabeçalho, a máquina de cada padrão e as instruções, nessa ordem, e cada
instrução leva o número da linha do script.** Descartado: as instruções antes dos padrões. O número
da linha entrou para que as mensagens de erro de execução digam a linha; descartado: dizer só o
registro.

**As extensões são `.solx` para o script e `.solxo` para o objeto.** A extensão `.sol`, usada até
aqui, já é a dos contratos da linguagem Solidity, e por isso foi trocada. Descartado: a mesma
extensão para os dois, porque compilar `filtro.solx` gravaria o objeto por cima do script. Os
blocos de código dos documentos passam a ser marcados como `solx`, e ficam sem cor no GitHub;
descartado: manter `sol`, que os pintava com as cores do Solidity. As entradas antigas deste diário
continuam com `.sol`, como foram escritas.

**O executor chama a `principal` uma vez por registro**: `pede (Linha registro) e retorna
Booleano`, e `verdadeiro` mantém o registro. Descartados: todos os registros de uma vez numa
`Lista`, e uma função de leitura, que pediria palavra reservada nova.

**O `Imprime` vira uma mensagem que o executor entrega ao projeto**, que decide onde mostrá-la.
Descartado: escrever no terminal, que um projeto com tela própria não tem.

#### A linguagem

- **Sai o SenãoSe**, que executava duas comparações "ao mesmo tempo" (uma condição de corrida). As
  condições encadeadas são um `se` dentro do `senao`. Descartado: um `senao se` como o `else if` do
  C#, que o grupo considerou desnecessário.
- **Não há herança.** Descartado: herança com palavra reservada própria, pelo custo na gramática,
  na verificação e no executor; fica fora do escopo por agora.
- **Entram `>=` e `<=`**, por extenso `maior-ou-igual-a` e `menor-ou-igual-a`. O recorte falava em
  "juntar" os operadores, sem que eles existissem nas classes léxicas.
- **`separa` é um método da `Linha`** e devolve os campos; dois separadores seguidos dão um campo
  vazio. Descartados: separar com `procura` (o leitor recusa a classe negada `[^;]`) e o projeto
  entregar os campos já separados.
- **Escopo por bloco**: a variável vale até o `}` do bloco dela. Descartado: valer na função inteira.
- **`inteiro()` e `quebrado()` convertem um campo em número**; o `quebrado()` aceita vírgula ou
  ponto, sem separador de milhar. Um texto que não é número é o primeiro **erro de execução**: o
  executor descarta aquele registro, avisa o projeto e segue. Descartados: não ter conversão, e,
  para o erro, devolver `0` (esconde o erro) ou parar o script (derruba todos os registros).
- **Reatribuição sem repetir o tipo** (`total recebe total + 1;`); sem ela, um `enquanto` não
  terminaria sozinho.
- **Acesso por posição a partir de 1** (`campos[1]`), como no Lua, com o método `tamanho()`; a
  posição que não existe é erro de execução, como a conversão. Descartado: começar em 0, como no
  Java.
- **A precedência dos operadores é a do Java**, com a forma por extenso no mesmo nível do símbolo.
- Também ficaram decididos: a `Lista` recebe o resultado de uma chamada; o `==` compara `Linha`; o
  `para` percorre o resultado direto de uma chamada; e um `Padrao` pode ser parâmetro de função.

#### A especificação

**As mensagens de erro seguem o formato do leitor**: a linha, o problema, o texto repetido e a
marca `^`. Descartado: uma linha só, sem o texto. As frases das mensagens são uma proposta, aceita
pelo grupo como estão.

**A pergunta medida é se a máquina determinística mínima é mais rápida que a simulação da não
determinística**, com a simulação do AFN, que já existe, como referência. Descartadas: comparar um
autômato só contra um por padrão, e medir o crescimento do objeto.

---

### O que mudou no código e nos números

- O `demonstrar_leitor.py` recontou à mão os padrões que mudaram: Palavra reservada 307 → **319**
  (com o `Padrao`, 30 palavras) e Operador 187 → **259** (com `>=`, `<=` e as formas por extenso). A
  verificação de que o literal Padrão é recusado entrou, e o placar foi de 36 para **37**.
- O `docs/02nucleo_minimo.md` ainda usava o Identificador antigo (`[a-zA-Z_]`, 105 nós); passou ao
  atual (`[a-zA-Z]`, **103** nós). O coringa reduzido, com 122 símbolos, custaria **243** nós.
- O `docs/exemplos.solx` e o exemplo completo do README passaram a ter a `principal` nova, e a
  classe `Matematica` passou a fazer conta com os campos do registro.

### Pendências, depois deste módulo

- **O executor ainda não existe.** Quando for construído, a máquina do objeto precisa da coluna do
  outro: hoje a determinização recusa os símbolos fora do alfabeto do padrão (o caso de `abc` em
  `a.c`).
- **A Linha, o comentário e o literal Padrão** dependem de classe negada (`[^...]`), que o leitor
  ainda recusa.
- **Não foram decididos:** como se declaram os atributos dentro do `Possui`, e se um método pode ser
  chamado direto num literal (`'a;b'.separa(';')`).
- **Para a análise sintática:** os dois usos de `e` (operador lógico e `pede (...) e retorna`) e de
  `pede`; e a classe terminada em `}`, sem `;`.

---

### As duas pendências decididas: os atributos e a chamada de método

Duas perguntas tinham ficado sem resposta no fim deste módulo: como se declaram os atributos dentro
do `Possui`, e se um método pode ser chamado direto num literal. O grupo respondeu as duas, e cada
resposta abriu outras perguntas, que foram feitas antes de qualquer arquivo ser escrito. A
prioridade que guiou as respostas foi a da cena: quem escreve em Solis está aprendendo, e um código
**explícito e legível** vem antes de um código curto.

#### Decisões e o que elas descartaram

**O atributo é declarado no `Possui` como uma variável comum**, com tipo, nome e valor:
`Quebrado frete recebe 15.00;`. É a mesma forma de toda declaração da Solis, que sempre nasce com
um valor.

**O atributo vale na classe toda**, e os métodos do `Faz` o usam pelo nome. É a exceção à regra do
escopo por bloco. Descartado: seguir a regra ao pé da letra, porque o atributo morreria no `}` do
`Possui` e nenhum método conseguiria usá-lo.

**De fora da classe, o atributo é usado pelo objeto, com o `.`**: `p.frete` lê o valor, e
`p.frete recebe 20.00;` guarda um valor novo, do tipo da declaração. Descartados: o atributo só
poder ser usado dentro da classe, e o atributo como uma constante, sem reatribuição.

**Um método é sempre chamado numa variável, nunca direto num literal**, seja uma Linha entre aspas
(`'a;b'.separa(';')`) ou um padrão entre crases (`` `[0-9]+`.casa(campo) ``). O motivo é que o
método depende da classe: `separa` existe na `Linha` e não existe no `Inteiro`. As aspas e as
crases mostram de que tipo é o literal, mas o tipo não está declarado; com a variável, a classe
fica escrita no código, e o nome diz o que o valor significa. Descartado: proibir só na Linha.
Usar o literal como valor continua aceito: guardar com `recebe`, passar como argumento (o `';'` de
`registro.separa(';')`) e comparar com `==`.

Proibir o método no literal é uma **escolha de projeto, e não um limite técnico**. O leitor já
separa o Literal Linha e o Literal Padrão em classes léxicas diferentes, e o compilador saberia o
tipo de `'a;b'` sem declaração nenhuma. Para comparar, cada caso abaixo foi rodado no compilador ou
no interpretador de verdade:

| Linguagem | Chamada direto no literal | O que acontece |
|---|---|---|
| Java | `"a;b".split(";")` | funciona: o literal de texto já é um objeto `String` |
| Java | `(5).toString()` | não compila: `int cannot be dereferenced`, porque o `int` é primitivo |
| Python | `"a;b".split(";")` | funciona |
| Python | `5.bit_length()` | erro de sintaxe; com parênteses, `(5).bit_length()` funciona |
| JavaScript | `/[0-9]+/.test("123")` | funciona: o JavaScript tem literal de expressão regular |
| Lua | `"abc":upper()` | erro de sintaxe; com parênteses, `("abc"):upper()` funciona |

O Java não tem literal de padrão: a expressão regular é uma `String` passada a `Pattern.compile`, e
a forma completa, `Pattern.compile("[0-9]+").matcher("123").matches()`, é um encadeamento. A Solis
fica mais restrita que o Java e o Python, e perto da Lua, que inspira a linguagem.

**A posição de uma lista guardada numa variável conta como variável**: `campos[3].quebrado()` é
aceito. Descartado: exigir uma variável no meio (`Linha textoPreco recebe campos[3];`), que obrigaria
a reescrever o Exemplo 5 da especificação e o exemplo completo do README.

**Não se chama um método no resultado de outra chamada**: `registro.separa(';').tamanho()` não é
aceito, e se escreve `Lista campos recebe registro.separa(';');` e depois `campos.tamanho()`. Dois
motivos: a regra que acabou de ser definida, porque o resultado de uma chamada não é uma variável; e
a cena, porque um passo por vez é mais fácil de ler para quem está aprendendo.

**Um método não pode ter um parâmetro nem declarar uma variável com o nome de um atributo da
classe.** Com dois `frete` no mesmo método, quem lê não saberia qual deles é usado. Descartado:
permitir, com o nome de dentro do método escondendo o atributo. A variável foi decidida primeiro, e
o parâmetro numa pergunta à parte, com a mesma resposta.

#### O que mudou nos documentos

- **O recorte** ganhou as decisões "Atributos da classe" e "Onde se chama um método", e a regra do
  escopo passou a citar a exceção dos atributos.
- **A especificação** separou as regras novas pelo que cada uma precisa para ser verificada. O
  método num literal e o encadeamento se reconhecem só pela forma do texto, e foram para a seção 3,
  com três mensagens de erro (literal Linha, literal Padrão e encadeamento). O nome de atributo
  repetido só se reconhece sabendo quais atributos a classe tem, e foi para a seção 5, com duas
  mensagens (parâmetro e variável). A seção 5 também passou a citar a exceção dos atributos.
- **O README** ganhou a regra de chamar métodos numa variável, com uma tabela do que não é aceito e
  de como se escreve; a `Classe Pedido`, com o atributo `frete` usado dentro e fora da classe; e a
  exceção dos atributos na regra do bloco.
- **Nenhum exemplo do repositório precisou ser reescrito**: nenhum chamava método num literal nem
  encadeava chamadas. Os blocos de código novos passaram pela verificação léxica.

### Pendências, depois desta decisão

- **O executor ainda não existe.** Quando for construído, a máquina do objeto precisa da coluna do
  outro.
- **A Linha, o comentário e o literal Padrão** dependem de classe negada (`[^...]`), que o leitor
  ainda recusa.
- **Para a análise sintática:** os dois usos de `e` (operador lógico e `pede (...) e retorna`) e de
  `pede`; e a classe terminada em `}`, sem `;`.

---

### As últimas pendências: o leitor, a sintaxe, o AFD do professor e a medição

Depois das decisões dos atributos e da chamada de método, sobravam o executor e quatro pendências: a
classe negada no leitor, os dois pontos da análise sintática, o `afd.cpp` do professor e a medição da
seção 7. A meta desta rodada foi deixar só o executor. Os AFDs em Python não ganharam leitura de
arquivo: a atividade que pediria isso não foi passada pelo professor, e sem enunciado não há
requisito.

#### Decisões e o que elas descartaram

**A classe negada entrou no leitor como redução.** `ler_padrao` recebe o alfabeto como parâmetro
opcional e lê `[^ab]` como a alternância de todos os símbolos do alfabeto, menos `a` e `b`. Era o
que o `docs/02nucleo_minimo.md` já previa: se entrasse, entraria como redução. A árvore não ganhou
nó novo, e o Thompson, o AFN e a determinização não mudaram. Sem o alfabeto, a classe negada
continua recusada, e os módulos que já usavam o leitor não precisaram mudar. Descartado: um nó novo,
"qualquer exceto", que deixaria a árvore menor, mas obrigaria a mudar a árvore, o Thompson, o AFN, a
determinização e os testes dos quatro módulos.

**A classe negada fica só nas classes léxicas, e não dentro das crases.** O complemento é sempre
sobre Σ. No código-fonte isso basta, porque um símbolo fora de Σ já é erro léxico. Num registro, um
símbolo fora de Σ conta como o outro, e `[^;]` não casaria com ele, embora ele não seja `;`: o
juninho teria um resultado sem sentido. Descartado: liberar agora, com o aviso de que `[^;]` não
casa com o outro até o executor existir, que seria uma regra a mais para o iniciante. A decisão pode
ser revista quando o executor tiver a coluna do outro.

**O `pede` já estava resolvido.** A pendência falava em dois usos: os parâmetros e a leitura de
entrada. A leitura de entrada deixou de existir quando a `principal` passou a receber o registro, e
não sobrou nenhum `pede` fora do cabeçalho de função.

**O `e` do cabeçalho continua o mesmo `e` do operador lógico.** Logo depois do `)` que fecha os
parâmetros não cabe expressão nenhuma, e a análise sintática distingue os dois pela posição. Os dois
usos têm o mesmo sentido em português. Descartados: tirar o `e` do cabeçalho (`pede (...) retorna`),
que mudaria todos os exemplos, e tirar o `e` como forma por extenso do `&&`, contra a ideia da
linguagem em português.

**A classe termina com `};`**, como as funções, o `Possui`, o `Faz` e os blocos de controle. Ela era
a única construção que terminava em `}` sem `;`. Descartado: manter a exceção e explicá-la, que
deixaria um caso à parte para quem está aprendendo lembrar.

**O `afd.cpp` do professor foi corrigido.** A primeira linha começava com `to#include`, e o arquivo
não compilava. Tirado o `to`, apareceu um segundo problema: o código usa `contains`, que só existe a
partir do C++20. O comentário do topo diz como compilar (`g++ -std=c++20 -o afd afd.cpp`) e avisa
que uma quebra de linha no fim do `fonte.lin` também é lida: como ela não está em Σ = {0, 1}, a
palavra é rejeitada. Isso foi conferido compilando e rodando: `1101` é aceita, e `1101` com a quebra
de linha no fim é rejeitada. Os sublinhados que o VS Code mostra nos `#include` vêm da falta de um
compilador configurado no editor, e não do arquivo.

#### A medição da seção 7

A medição tinha sido anotada como dependente do executor, e não era: a pergunta compara as
máquinas, e as duas já existiam. O `Medicao/medir.py` mede, e o `Medicao/resultado.md` registra o
resultado.

**Como foi medido, e o que foi descartado em cada ponto:**

- **Os registros têm só os símbolos do alfabeto do padrão.** Assim os padrões com coringa podem
  entrar, e as duas máquinas concordam. Descartado: registros com símbolos de fora, em que o AFD e o
  AFN seguem regras diferentes (o caso de `abc` em `a.c`), que é a coluna do outro, pendência do
  executor.
- **A simulação do AFN não guarda o traço.** O `simular()` guarda cada passo para o
  `formatar_simulacao` mostrar, e esse custo não tem a ver com decidir o registro. Descartado: medir
  o `simular()` como está, que daria ao AFD uma vantagem que não é dele.
- **Antes de comparar tempo, as duas máquinas são comparadas com o `re.fullmatch` do Python**, um
  oráculo de fora. Sem a mesma resposta, comparar tempo não vale nada.
- **Cada tempo é a mediana de 5 repetições**, menos sensível a um travamento do computador.
- **O tamanho do objeto é medido em estados e setas**, e não em bytes, porque o formato do objeto
  ainda não foi escrito.
- **A medição entrou no `rodar_tudo.py`**, com o placar da conferência, e não dos tempos, porque os
  tempos não são certos ou errados. Ela leva uns 35 segundos.

**O resultado:** em três execuções, duas no Linux e uma no Windows, a conferência deu 2520 de 2520,
e o AFD mínimo foi mais rápido em todos os padrões e tamanhos, de 5,2 a 662,8 vezes. A expectativa
se confirmou, inclusive nos dois casos que poderiam contrariá-la: nos registros curtos, de 44,9 a
440,8 vezes; com n = 8, de 82,1 a 235,9 vezes, mesmo com 256 estados contra 52.

**O que o resultado não diz:** o número de vezes é exagerado pela implementação, porque o
`fecho_vazio` cria uma lista do tamanho da máquina a cada símbolo; o AFN para quando fica sem estado
ativo e o AFD lê até o fim, e por isso a vantagem cai para 5 a 8 vezes no preço e no valor longos;
montar o AFD custa mais (o do e-mail, de 155 a 220 ms), mas esse custo é do compilador, e não do
executor; e, nos tempos abaixo de 1 µs, a proporção varia bastante entre execuções. Em nenhuma das
42 linhas, em nenhuma execução, a direção mudou.

#### O que mudou no código e nos números

- O `leitor_padroes.py` lê a classe negada quando recebe o alfabeto. Os nós foram contados à mão
  antes de rodar: `[^'\n]` tem 239 (120 folhas e 119 alternâncias), a Linha 489, o comentário 246 e
  o literal Padrão 244.
- O `demonstrar_leitor.py` ganhou o alfabeto de 122 símbolos e trocou as duas verificações de
  "limite conhecido" pelas de aceitação, com mais duas recusas: sem o alfabeto, e com uma classe
  negada que tira todos os símbolos. O placar foi de 37 para **42**.
- O `classes_lexicas.md` explica o `e` do cabeçalho, o `pede` e a classe negada; o
  `02nucleo_minimo.md` registra que ela entrou como redução; o README atualiza o leitor e fecha as
  classes com `};`, assim como o `docs/exemplos.solx`, a especificação e o recorte, que ganhou as
  decisões do fim da classe e do `e`.
- A seção 7 da especificação ganhou o que a medição mostrou, com o link para o resultado.
- O `rodar_tudo.py` passou de 12 para **13 partes**.

### Pendências, depois desta rodada

- **O executor.** É a única pendência. Quando ele for construído:
  - a máquina do objeto precisa da coluna do outro, para os símbolos fora do alfabeto do padrão;
  - o formato do objeto define o tamanho da tabela em bytes, que a medição contou em estados e
    setas;
  - a classe negada dentro das crases pode ser revista, porque o motivo de deixá-la de fora é a
    falta da coluna do outro.

### Ajustes na documentação, depois desta rodada

Uma varredura no repositório achou o que tinha ficado para trás nos documentos:

- **O README** ganhou a seção "Medição" (a estrutura, o método, como executar e o resultado), o
  "Como rodar tudo" passou a 13 partes, e a Análise Léxica passou a mostrar a pasta do modelo do
  professor, com o comando para compilar em C++20 e o cuidado com a quebra de linha no `fonte.lin`.
- **A especificação** ganhou, na seção 3, o erro da classe negada dentro de um padrão. A regra era
  repetir a mensagem do leitor, mas a do leitor ("só é aceita quando o alfabeto é informado") foi
  escrita para quem programa o compilador, e quem escreve Solis nunca informa alfabeto nenhum. O
  caso ganhou mensagem própria: `a classe negada ([^...]) não é aceita dentro de um padrão`, com a
  marca no `^`. Descartado: trocar a mensagem no próprio leitor, que continuaria servindo aos dois
  casos, com e sem alfabeto, e deixaria um deles mal explicado.
- **O recorte** ganhou, na decisão dos padrões, que não há classe negada dentro das crases, com o
  motivo. A decisão já estava nas classes léxicas, no núcleo mínimo, no README e na especificação,
  mas faltava no lugar onde as decisões da linguagem ficam.
- **As classes léxicas** passaram a apontar para essa mensagem própria, em vez de dizer que o padrão
  é recusado pelo leitor.

As pendências não mudaram: continua só o executor.
