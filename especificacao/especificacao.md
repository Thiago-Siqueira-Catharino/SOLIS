# Especificação da Solis

Este documento descreve, por extenso, o que a Solis fará. Ele descreve comportamento: o que existe
na cena, o que a pessoa escreve, o que o sistema aceita, o que recusa e como avisa. Não descreve
como cada peça é construída por dentro, decisão que fica para os módulos que constroem cada peça.

As decisões em que ele se apoia estão no [recorte da linguagem](../Recorte_Da_Linguagem/recorte_da_linguagem.md),
no [alfabeto](alfabeto.md) e nas [classes léxicas](classes_lexicas.md). O executor descrito na
seção 6 ainda não foi construído.

---

## 1. O domínio e a cena

**Sobre o que a Solis fala:** registros com campos, e a forma que cada campo pode ter. Um registro é
uma linha de texto com campos separados por um sinal, como uma linha de planilha exportada:

```
Ana Souza;ana@empresa.com;Marília;R$ 120,00;pedido #102
```

Os padrões da Solis descrevem a forma de um campo: "um ou mais dígitos", "um nome, uma arroba e um
domínio", "R$ seguido de reais e centavos". Com eles, um script **identifica** os registros que têm
um campo de certa forma, **filtra** os que interessam e **organiza** o que encontrou.

**Quem escreve:** uma pessoa que precisa automatizar uma tarefa e não domina o inglês nem uma
linguagem em inglês. A cena típica é a de um júnior numa equipe que recebe registros todos os dias,
de clientes, de pedidos, de cadastros, e precisa separar os que importam: os que têm um e-mail
válido, os que citam um pedido atrasado, os que trazem um valor em dinheiro. Ele escreve o script em
Solis, em português, e o script é incorporado ao projeto da equipe.

**O que ela quer obter:** de uma pilha de registros, só os que interessam, sem precisar conferir um
por um à mão e sem ter de aprender antes uma linguagem em inglês. A Solis é, para essa pessoa, a
porta de entrada para os fundamentos de programação.

---

## 2. O que se escreve na linguagem

Cinco exemplos, do mais simples ao mais elaborado. Os registros e os valores são inventados. Em
todos, o projeto entrega ao script um registro por vez: a função `principal` recebe o registro e
devolve `verdadeiro` para mantê-lo ou `falso` para descartá-lo.

**Exemplo 1: manter os registros que são só um número.**

```sol
funcao principal pede (Linha registro) e retorna Booleano {
    Padrao numero recebe `[0-9]+`;
    devolve numero.casa(registro);
};
```

Com os registros `2041`, `pedido 2041` e `20.41`, o script mantém só o primeiro: `casa` pergunta se o
registro **inteiro** tem a forma do padrão.

**Exemplo 2: manter os registros que têm um campo de e-mail.**

```sol
funcao principal pede (Linha registro) e retorna Booleano {
    Padrao email recebe `[a-z0-9_]+@[a-z]+\.com(\.br)?`;
    Lista campos recebe registro.separa(';');
    para campo em campos {
        se (email.casa(campo)) {
            devolve verdadeiro;
        };
    };
    devolve falso;
};
```

`separa` divide o registro nos campos, e o laço testa cada um. O registro
`Ana Souza;ana@empresa.com;Marília` é mantido; `Bruno Lima;sem contato;Garça` é descartado.

**Exemplo 3: manter os registros que citam um pedido atrasado, em qualquer lugar do texto.**

```sol
funcao atrasado pede (Linha pedido) e retorna Booleano {
    Lista atrasados recebe ['#102', '#215', '#330'];
    para item em atrasados {
        se (item == pedido) {
            devolve verdadeiro;
        };
    };
    devolve falso;
};

funcao principal pede (Linha registro) e retorna Booleano {
    Padrao pedido recebe `#[0-9]+`;
    para achado em pedido.procura(registro) {
        se (atrasado(achado)) {
            devolve verdadeiro;
        };
    };
    devolve falso;
};
```

Aqui o padrão não testa o registro inteiro: `procura` acha os trechos com a forma `#` seguido de
dígitos, onde quer que estejam. No registro `cliente pediu #215 e depois #400`, os trechos achados são
`#215` e `#400`, e o registro é mantido porque `#215` está na lista.

**Exemplo 4: manter os registros que têm, ao mesmo tempo, um e-mail e um valor em dinheiro.**

```sol
// tem: diz se algum campo da lista tem a forma do padrão
funcao tem pede (Padrao forma, Lista campos) e retorna Booleano {
    para campo em campos {
        se (forma.casa(campo)) {
            devolve verdadeiro;
        };
    };
    devolve falso;
};

funcao principal pede (Linha registro) e retorna Booleano {
    Padrao email recebe `[a-z0-9_]+@[a-z]+\.com(\.br)?`;
    Padrao valor recebe `R$ [0-9]+,[0-9][0-9]`;
    Lista campos recebe registro.separa(';');
    devolve tem(email, campos) e tem(valor, campos);
};
```

Um padrão é um valor como os outros: vai de uma função para outra como argumento. O registro
`Ana Souza;ana@empresa.com;R$ 120,00` é mantido; `Ana Souza;ana@empresa.com;cento e vinte` é
descartado, porque nenhum campo tem a forma de `valor`.

**Exemplo 5: manter os pedidos de R$ 300,00 ou mais, calculando preço vezes quantidade.**

Os registros deste exemplo têm quatro campos: nome, e-mail, preço e quantidade, nessa ordem.

```sol
Classe Matematica {
    Possui {
    };
    Faz {
        funcao multiplicar pede (Quebrado a, Quebrado b) e retorna Quebrado {
            devolve a * b;
        };
    };
}

funcao principal pede (Linha registro) e retorna Booleano {
    Padrao preco recebe `[0-9]+(,|\.)[0-9][0-9]`;
    Padrao quantidade recebe `[0-9]+`;
    Matematica mat recebe Novo Matematica;
    Lista campos recebe registro.separa(';');
    se (campos.tamanho() < 4) {
        Imprime('registro com menos de 4 campos');
        devolve falso;
    };
    se (!preco.casa(campos[3]) ou !quantidade.casa(campos[4])) {
        Imprime('preço ou quantidade fora da forma');
        devolve falso;
    };
    Quebrado total recebe mat.multiplicar(campos[3].quebrado(), campos[4].inteiro());
    devolve total >= 300;
};
```

Todo campo é uma `Linha`: para fazer a conta, `quebrado()` e `inteiro()` convertem o texto em número.
Antes de converter, o script confere se o registro tem os quatro campos e se o preço e a quantidade
têm a forma de número; sem essa conferência, um registro fora do formato daria um erro de execução
(seção 6). Com os registros abaixo:

| Registro | O que acontece |
|---|---|
| `Ana Souza;ana@empresa.com;120,50;3` | 120,50 × 3 = 361,50: mantido |
| `Bruno Lima;bruno@empresa.com;99,90;2` | 99,90 × 2 = 199,80: descartado |
| `Carla Dias;carla@empresa.com;sem preço;5` | descartado, com a mensagem `preço ou quantidade fora da forma` |
| `Davi Rocha;davi@empresa.com` | descartado, com a mensagem `registro com menos de 4 campos` |

---

## 3. O que o sistema aceita e o que recusa

### O que é aceito

Um texto Solis é aceito quando:

- todo símbolo pertence ao [alfabeto](alfabeto.md), e os que só valem em Linha, comentário ou padrão
  (letras acentuadas, símbolos de registro, `?` e `\`) aparecem só nesses lugares;
- todo trecho do texto se divide nas [classes léxicas](classes_lexicas.md), com cada Linha e cada
  padrão abertos e fechados na mesma linha;
- todo padrão entre crases é um padrão bem escrito, com o núcleo de operadores de
  [`docs/02nucleo_minimo.md`](../docs/02nucleo_minimo.md);
- as instruções seguem as formas da linguagem: declarações, `se`/`senao`, `enquanto`, `para ... em`,
  funções, classes, cada instrução terminada em `;` e cada bloco `{` fechado com o seu `}`;
- passa por todas as verificações da seção 5;
- existe a função `principal`, na forma `funcao principal pede (Linha registro) e retorna Booleano`.

### O que é recusado, e como o sistema avisa

Quando o erro está num ponto do texto, a mensagem tem sempre a mesma forma: a linha do arquivo, o
que está errado, o texto daquela linha repetido e a marca `^` embaixo do ponto do problema. Com qualquer erro, **nenhum objeto é gravado**:
a pessoa corrige o ponto marcado e compila de novo. Os erros de verificação estão na seção 5, e os
erros que só aparecem durante a execução, na seção 6.

**Um símbolo fora do alfabeto.** A pessoa sabe qual símbolo tirar ou trocar.

```
linha 4: símbolo fora do alfabeto: '€'
    Linha moeda recebe €;
                       ^
```

**Um símbolo que só vale em Linha, comentário ou padrão, usado fora deles.** Aqui, um nome com
acento: a pessoa troca `número` por `numero`.

```
linha 2: letra acentuada fora de Linha, comentário ou padrão: 'ú'
    Inteiro número recebe 5;
             ^
```

**Uma Linha ou um padrão que abre e não fecha na mesma linha.** A marca fica onde a aspa ou a crase
abriu, que é onde a pessoa vai procurar a que falta.

```
linha 3: Linha aberta não foi fechada nesta linha
    Linha nome recebe 'Ana;
                      ^
```

```
linha 3: padrão aberto não foi fechado nesta linha
    Padrao pedido recebe `#[0-9]+;
                         ^
```

**Um padrão malformado.** O texto entre as crases é um token válido, mas não é um padrão bem
escrito. A mensagem repete a do leitor de padrões, que diz em que posição do padrão o problema
começou, e a marca fica onde a leitura o constatou: aqui, no fim do padrão, onde falta o `]`.

```
linha 3: padrão malformado: Classe aberta na posição 1 do padrão não foi fechada com ]
    Padrao pedido recebe `[0-9+`;
                               ^
```

**Uma instrução sem `;`, ou um bloco sem o seu `}`.** A marca fica no último trecho da instrução,
ou na `{` que abriu o bloco.

```
linha 5: esperava ';' depois da instrução
    Inteiro limite recebe 10
                          ^
```

```
linha 2: o bloco aberto aqui não foi fechado com }: o arquivo terminou antes
    funcao principal pede (Linha registro) e retorna Booleano {
                                                              ^
```

**Falta a função `principal`.** Sem ela, o executor não teria o que chamar para cada registro. É o
único erro que não está num ponto do texto, e por isso a mensagem não tem linha nem marca.

```
falta a função principal: funcao principal pede (Linha registro) e retorna Booleano
```

### O que não se consegue escrever

Um pedido natural de quem escreve padrões fica sem resposta: **parênteses balanceados**, em que cada
`(` tem o seu `)` mais adiante, em qualquer profundidade, como em `(a(b)c)`. Nenhum padrão da Solis
descreve essa forma, por mais longo que seja. Não é um erro de quem escreve nem uma falta do
sistema: é o limite do que um padrão desse tipo consegue reconhecer, e será demonstrado quando o
percurso chegar a ele.

---

## 4. Onde a linguagem se aninha

O **bloco**. Um bloco `{ ... }` contém instruções, e uma instrução pode ser um `se`, um `enquanto`
ou um `para ... em`, que têm o seu próprio bloco dentro. Não há profundidade máxima.

Três níveis, todos tirados do exemplo 2 da seção 2:

```sol
funcao principal pede (Linha registro) e retorna Booleano {     // nível 1: o bloco da função
    Padrao email recebe `[a-z0-9_]+@[a-z]+\.com(\.br)?`;
    Lista campos recebe registro.separa(';');
    para campo em campos {                                       // nível 2: o bloco do laço
        se (email.casa(campo)) {                                 // nível 3: o bloco da condição
            devolve verdadeiro;
        };
    };
    devolve falso;
};
```

As condições encadeadas também se aninham: como não existe `senao se`, cada condição a mais é um
`se` dentro do bloco do `senao` anterior. Num trecho em que `nota` é um `Inteiro` já declarado:

```sol
se (nota >= 7) {
    Imprime('aprovado');
} senao {
    se (nota >= 5) {
        Imprime('recuperação');
    } senao {
        Imprime('reprovado');
    };
};
```

Dentro dos padrões há um segundo aninhamento, o dos grupos: `(\.[a-z]+(\.br)?)?` tem um grupo
dentro de outro, também sem profundidade máxima.

---

## 5. O que se verifica antes de rodar

### As naturezas de valor

A Solis distingue estas naturezas de valor, e toda variável, todo parâmetro e todo retorno de
função tem uma delas, escrita por quem programa:

| Natureza | O que é |
|---|---|
| `Linha` | texto |
| `Inteiro` | número sem casas decimais |
| `Quebrado` | número com casas decimais |
| `Booleano` | `verdadeiro` ou `falso` |
| `Lista` | coleção ordenada de valores |
| `Padrao` | a forma que um trecho de texto pode ter |
| `Vazio` | a ausência de valor; só aparece como retorno de função |
| cada `Classe` declarada | os objetos criados com `Novo` |

Um `Inteiro` pode entrar onde se espera um `Quebrado`. Nenhuma outra troca é aceita: em particular,
uma `Linha` não vira `Padrao`, mesmo que o texto dela se pareça com um padrão.

### Os erros apontados antes de executar

Estes textos estão bem escritos, passam pela seção 3, e mesmo assim não fazem sentido. O sistema os
aponta antes de gravar o objeto, na mesma forma de mensagem.

**Um nome usado sem ter sido declarado.** Muitas vezes, um erro de digitação.

```
linha 4: nome usado sem ter sido declarado: 'emial'
    devolve emial.casa(registro);
            ^
```

**Um nome usado fora do bloco em que foi declarado.** Uma variável vale do ponto em que foi
declarada até o `}` que fecha o bloco dela.

```
linha 8: nome usado fora do bloco em que foi declarado: 'campos'
    devolve campos;
            ^
```

**Dois valores de naturezas incompatíveis.** Um `Quebrado` onde se espera um `Inteiro`, uma
`Linha` onde se espera um `Padrao`, ou uma reatribuição que muda o tipo da variável (`total` foi
declarado `Quebrado`):

```
linha 3: tipos incompatíveis: Inteiro espera um valor Inteiro, e recebeu Quebrado
    Inteiro total recebe 10.5;
                         ^
```

```
linha 2: tipos incompatíveis: Padrao espera um padrão entre crases, e recebeu Linha
    Padrao numero recebe '[0-9]+';
                         ^
```

```
linha 6: tipos incompatíveis: total é Quebrado, e recebeu Linha
    total recebe 'cento e vinte';
                 ^
```

**Uma referência a algo que não existe.** Um método que a natureza do valor não tem, ou uma função
chamada com o número errado de argumentos:

```
linha 5: a Linha não tem o método 'casa': casa e procura são métodos de Padrao
    se (registro.casa(numero)) {
                 ^
```

```
linha 9: a função 'tem' pede 2 argumentos, e recebeu 1
    devolve tem(email);
            ^
```

**Um `devolve` que não combina com o retorno da função**, ou uma condição que não é `Booleano`:

```
linha 3: devolve incompatível: a função retorna Booleano, e o valor é Linha
    devolve registro;
            ^
```

```
linha 4: a condição do se precisa ser Booleano, e é Lista
    se (campos) {
        ^
```

---

## 6. O que o sistema produz, e quem executa

### O objeto

Quando a compilação termina sem erro, o compilador grava **um objeto**: um arquivo com tudo o que é
preciso para rodar o script, e nada do texto Solis. O compilador termina aí, sem executar nada.
O objeto contém, nesta ordem:

1. **o cabeçalho**: a marca de que o arquivo é um objeto Solis e a versão do formato, para que o
   executor recuse um arquivo que não é dele ou de uma versão que não conhece;
2. **a máquina de cada padrão** do script, na ordem em que os padrões foram declarados: os estados,
   para onde cada símbolo leva a partir de cada estado, o estado inicial e os estados que aceitam.
   Os símbolos fora do alfabeto entram como um só, o **outro**, que só o coringa reconhece;
3. **as instruções do script**, função por função, a começar pela `principal`.

### Quem executa

O **executor** é uma máquina virtual própria, embutida no projeto que incorpora o script. Ele é
outro componente, que roda depois e sem o compilador:

1. lê o objeto e confere o cabeçalho;
2. para cada registro que o projeto recebe, chama a função `principal` com o registro;
3. mantém o registro se a `principal` devolver `verdadeiro`, e o descarta se devolver `falso`.

Durante a execução, cada `Imprime` vira uma mensagem que o executor entrega ao projeto. O executor
não escreve em lugar nenhum por conta própria: é o projeto que decide onde mostrar as mensagens, na
tela, num arquivo ou em lugar nenhum. As mensagens ficam separadas dos registros mantidos, e
quem decide o que fica é só o `devolve` da `principal`.

Um registro nunca é recusado por causa dos símbolos que tem: os que estão fora do alfabeto contam
como o outro. O mesmo objeto roda em qualquer sistema operacional em que o executor rode, e pode ser
executado muitas vezes, sobre registros diferentes, sem compilar de novo.

### Os erros de execução

Dois erros não podem ser apontados antes de rodar, porque dependem do conteúdo de um registro, que
só existe na execução:

- **converter um texto que não é número**: `campo.quebrado()` com o campo `'sem preço'`;
- **pegar uma posição que não existe**: `campos[4]` num registro com dois campos.

Os dois são tratados do mesmo jeito: o executor para de processar **aquele** registro, o descarta,
entrega ao projeto uma mensagem dizendo o que aconteceu e em que registro, e segue para o próximo.
Um registro fora do formato não derruba os outros. As mensagens têm esta forma:

```
registro 3: o texto 'sem preço' não é um número
registro 4: a lista tem 2 itens, e foi pedida a posição 4
```

A mensagem não repete a linha do script, porque o objeto não guarda o texto Solis. Para evitar esses
erros, o script confere a forma do campo com um padrão e o `tamanho()` da lista antes de converter,
como no exemplo 5 da seção 2.

---

## 7. A pergunta que você vai responder medindo

**A pergunta:** processar os registros com a máquina determinística mínima de cada padrão é mais
rápido do que simular a máquina não determinística construída direto do padrão?

**A grandeza:** o tempo médio para decidir um registro, medido sobre o mesmo conjunto de registros
e os mesmos padrões nas duas abordagens. Junto, o tamanho do objeto em cada abordagem, porque a
máquina determinística pode ter muito mais estados.

**A referência:** a simulação da máquina não determinística, que acompanha um conjunto de estados
ativos a cada símbolo lido. Ela já existe no projeto (`Afn/`), e é contra ela que a máquina
determinística, que acompanha um estado só, é comparada.

**A expectativa:** a máquina determinística ganha em tempo por registro, porque faz um passo só
por símbolo lido.

**O resultado que contrariaria a expectativa:** a máquina determinística **não** ser mais rápida.
Dois casos fariam isso acontecer, e a medida precisa incluí-los:

- registros curtos e padrões simples, em que o conjunto de estados ativos da simulação já é
  pequeno e o ganho de acompanhar um estado só desaparece;
- padrões como "o n-ésimo símbolo contado do fim é `a`", em que a máquina determinística chega a
  2ⁿ estados (256 para n = 8, contra 52 da não determinística, como medido no módulo da
  determinização): o objeto cresce tanto que carregá-lo custa mais do que o tempo ganho nos
  registros.

---

## O Teste que Fecha a Escolha

A Solis é um assunto próprio, fora dos vinte propostos no Projeto Integrador. Por isso, respondemos
por escrito às cinco perguntas que fecham aquela lista.

**1. Existe, em algum ponto, um artefato de código que é saída do tradutor e entrada de outra coisa,
ou o texto de partida é executado direto?**
Existe: o objeto da seção 6. O compilador o grava e termina; o executor, embutido no projeto, o lê
depois e o roda sobre os registros. O texto Solis nunca é executado direto.

**2. A linguagem tem alguma construção que se aninha sem limite fixo, ou todo comando é de formato
fixo e reconhecível linha a linha?**
Tem: o bloco, que contém `se`, `enquanto` e `para`, que contêm blocos, sem profundidade máxima
(seção 4). Dentro dos padrões, os grupos também se aninham.

**3. Você consegue escrever três padrões na sua linguagem e dizer, para cinco trechos de entrada
escritos à mão, quais deles cada padrão reconhece e quais recusa?**
Sim. Com o `casa`, que testa o trecho inteiro:

| Trecho | ``Padrao numero recebe `[0-9]+`;`` | ``Padrao pedido recebe `#[0-9]+`;`` | ``Padrao email recebe `[a-z]+@[a-z]+\.com`;`` |
|---|---|---|---|
| `123` | reconhece | recusa | recusa |
| `#123` | recusa | reconhece | recusa |
| `#12a` | recusa | recusa | recusa |
| `ana@empresa.com` | recusa | recusa | reconhece |
| `ana@empresacom` | recusa | recusa | recusa |

O `#12a` termina com uma letra, que nem o `numero` nem o `pedido` aceitam; o `ana@empresacom` não
tem o `.` antes do `com`.

**4. Existe entrada em que usar um nome antes de declará-lo, ou combinar valores incompatíveis, é
apontado antes de qualquer execução?**
Existe: a seção 5. Um nome não declarado, um nome fora do seu bloco, um `Quebrado` onde se espera
um `Inteiro`, uma `Linha` onde se espera um `Padrao`, um método que não existe e um `devolve` que
não combina com o retorno são apontados antes de o objeto ser gravado.

**5. A pergunta investigativa tem uma referência contra a qual medir, e você consegue enunciar
hoje o resultado que a contrariaria?**
Tem: a seção 7. A referência é a simulação da máquina não determinística, que já existe no
projeto, e o resultado que contrariaria a expectativa é a máquina determinística não ser mais
rápida, em registros curtos ou em padrões que fazem o número de estados explodir.
