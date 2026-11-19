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
