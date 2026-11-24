# Solis — Recorte da Peneira

### Decisões fixadas no primeiro módulo

---

## Visão Geral

| | |
|---|---|
| **Nome** | Solis |
| **Extensão** | `.solx` (o script) e `.solxo` (o objeto gravado) |
| **Base** | Java |
| **Inspiração** | Lua (compilada e fortemente tipada) |
| **Objetivo** | Linguagem para scripts, integrável com outras linguagens, inteiramente em português brasileiro |
| **Domínio** | Scripts que identificam, organizam e filtram registros com campos, descritos por padrões |
| **Para quem** | Quem precisa automatizar uma tarefa e não domina o inglês nem uma linguagem em inglês: a Solis é a porta de entrada para os fundamentos |

---

## Forma da Descrição Escrita pelo Usuário

**Decisão — Condições encadeadas**
Não existe `senao se` como construção própria. Para encadear condições, um `se` vai dentro do bloco do `senao`, e as condições são testadas uma de cada vez, na ordem em que foram escritas.

**Decisão — Dispensa do operador ternário**
O usuário dispensa a necessidade de utilizar o operador ternário: a escolha entre dois caminhos se escreve com `se` e `senao`.

**Decisão — Paradigma**
Base em POO (Programação Orientada a Objetos), para que classes possam ser reutilizadas criando objetos com `Novo`, com definições simples de métodos e declarações de instâncias. Não há herança: uma classe não herda de outra. A herança fica fora do escopo por agora e pode entrar depois.
Também funcional: um programa em Solis pode ser escrito só com funções, sem nenhuma classe. As funções existem fora das classes, como `soma` e `principal` em `docs/exemplos.solx`.

**Decisão — Atributos da classe**
Um atributo é declarado dentro do `Possui` como uma variável comum, com o tipo, o nome e o valor: `<Tipo> <atributo> recebe <valor>;`. Ele vale na classe toda, e não só até o `}` do `Possui`: os métodos do `Faz` usam o atributo pelo nome. De fora da classe, o atributo é usado pelo objeto, com o `.`: `p.frete` lê o valor, e `p.frete recebe 20.00;` guarda um valor novo, que precisa ser do tipo da declaração. Um método não pode declarar uma variável com o mesmo nome de um atributo da classe: dois `frete` no mesmo método confundiriam quem está lendo, e isso é um erro apontado antes de gravar o objeto.

```solx
Classe Pedido {
    Possui {
        Quebrado frete recebe 15.00;
    };
    Faz {
        funcao total pede (Quebrado preco) e retorna Quebrado {
            devolve preco + frete;
        };
    };
}
```

**Decisão — Operadores e tipos primitivos**
Por se tratar de uma linguagem para scripts, os operadores básicos são:

- Adição `+`
- Multiplicação `*`
- Subtração `-`
- Divisão `/`
- Resto `%`

Tipos primitivos:

| Tipo na Solis | O que representa | Equivalente |
|---|---|---|
| `Linha` | cadeia de caracteres | `String` |
| `Inteiro` | número inteiro | `int` |
| `Quebrado` | número com casas decimais (ponto flutuante) | `Float` |
| `Booleano` | valor lógico | `bool` |
| `Vazio` | ausência de valor | `Void` |
| `Lista` | coleção ordenada de valores | `List` |
| `Padrao` | descrição da forma que um trecho de texto pode ter | expressão regular |

**Decisão — Operadores de comparação**

- Maior que `>`
- Menor que `<`
- Maior ou igual `>=`
- Menor ou igual `<=`
- Igual `==`
- Diferença `!=`

Por extenso, `>=` é `maior-ou-igual-a` e `<=` é `menor-ou-igual-a`. O `==` e o `!=` também comparam
duas `Linha`: `item == pedido` é verdadeiro quando os dois textos são iguais.

**Decisão — Padrões**
Quem escreve em Solis declara padrões: descrições da forma que um trecho de texto pode ter, como "um ou mais dígitos". É o que dá à linguagem o seu domínio: identificar, organizar e filtrar registros pela forma dos campos.

- O padrão é escrito entre crases e guardado numa variável do tipo `Padrao`: ``Padrao numero recebe `[0-9]+`;``
- `casa` diz se um texto **inteiro** tem a forma do padrão e devolve `Booleano`: `numero.casa(campo)`
- `procura` devolve uma `Lista` de `Linha` com os trechos de um texto que têm a forma do padrão, ficando sempre com o trecho mais longo: `numero.procura(registro)`
- As duas operações são métodos do padrão, chamados com o `.` que já existe: não entra operador novo.
- Não há captura: o sistema não guarda qual trecho casou com cada parte do padrão.
- Um `Padrao` é um valor como os outros: pode ser parâmetro de função e ser passado de uma função para outra: `funcao tem pede (Padrao forma, Lista campos) e retorna Booleano`.

**Decisão — Separar os campos**
`separa` é um método da `Linha`: divide o texto nos pedaços entre cada ocorrência do separador e devolve uma `Lista` de `Linha`: `registro.separa(';')`. O separador é escolhido por quem escreve o script. Como `casa` e `procura`, é chamado com o `.` e não é palavra reservada.

**Decisão — Converter um campo em número**
Todo campo é uma `Linha`, mesmo quando parece um número. Para fazer conta com ele, a `Linha` tem dois métodos, que também não são palavras reservadas:

- `inteiro()` devolve o `Inteiro` escrito no texto, que precisa ser só dígitos: `'3'` dá `3`.
- `quebrado()` devolve o `Quebrado` escrito no texto, com vírgula ou com ponto: `'120,50'` e `'120.50'` dão `120.50`. Não há separador de milhar: `'1.234,56'` não é um número.

O conteúdo de um registro só existe na execução, então converter um texto que não é número (um campo `'abc'` com `campo.quebrado()`) não pode ser apontado antes de rodar: é um **erro de execução**. O executor para de processar aquele registro, o descarta, entrega ao projeto uma mensagem dizendo qual texto não era número e segue para o próximo registro. Um registro ruim não derruba os outros. Para evitar o erro, o script testa a forma do campo com um padrão antes de converter.

**Decisão — Onde se chama um método**
Um método é sempre chamado numa variável, nunca direto num literal, seja ele uma `Linha` ou um `Padrao`. `'a;b'.separa(';')` não é aceito: se escreve `Linha texto recebe 'a;b';` e depois `texto.separa(';')`. `` `[0-9]+`.casa(campo) `` também não é aceito: se escreve ``Padrao numero recebe `[0-9]+`;`` e depois `numero.casa(campo)`. O motivo é que o método depende da classe: `separa` existe na `Linha` e não existe no `Inteiro`. As aspas e as crases mostram de que tipo é o literal, mas o tipo não está declarado. Com a variável, a classe fica escrita no código, à vista de quem lê, e o nome da variável diz o que o valor significa. Usar o literal como valor continua aceito: guardar com `recebe`, passar como argumento (o `';'` de `registro.separa(';')`) e comparar com `==`. A posição de uma lista guardada numa variável conta como variável: `campos[3].quebrado()` é aceito. Também não se chama um método no resultado de outra chamada: `registro.separa(';').tamanho()` não é aceito, e se escreve `Lista campos recebe registro.separa(';');` e depois `campos.tamanho()`. Quem usa a Solis está aprendendo, e um código explícito, com um passo por vez, é mais fácil de ler. Chamar um método direto num literal é um erro apontado antes de gravar o objeto.

**Decisão — O pedido que o padrão não atende**
Parênteses balanceados, em que cada `(` tem o seu `)` mais adiante, em qualquer profundidade, são um pedido natural de quem escreve padrões, e nenhum padrão da Solis o reconhece. É a demonstração do limite do reconhecimento por autômato finito.

### Estruturas de Controle

| Estrutura | Sintaxe |
|---|---|
| Loop (equivalente ao `while` do Python) | `enquanto (<condição>) { ... }` |
| Loop (equivalente ao `for` do Python) | `para <variável> em <iterável> { ... }`; o iterável pode ser uma `Lista` guardada numa variável ou o resultado direto de uma chamada: `para achado em pedido.procura(registro) { ... }` |
| Atribuição de variável | `<Tipo> <variável> recebe <valor>;` |
| Reatribuição de variável | `<variável> recebe <valor>;` |
| Condicionais | `se (<condição>) { ... } senao { ... }` |
| Interrupção de loop | `pare` |

**Exemplo de atribuição:**
```
Linha x recebe "texto aleatorio";
```

**Decisão — Reatribuição**
Uma variável já declarada recebe um valor novo sem repetir o tipo: `total recebe total + 1;`. O tipo continua o da declaração, e guardar um valor de outro tipo é um erro apontado antes de gravar o objeto. Sem reatribuição, a condição de um `enquanto` nunca mudaria lá dentro, e o laço só terminaria com `pare` ou `devolve`.

**Decisão — Acesso por posição**
Um item de uma `Lista` é pego pela posição, entre colchetes, contando a partir de 1, como no Lua: `campos[1]` é o primeiro campo. O método `tamanho()` diz quantos itens a lista tem: `campos.tamanho()`. Uma posição que não existe (`campos[9]` numa lista de 4 itens) só aparece na execução, e é um erro de execução tratado como o da conversão: o executor descarta aquele registro, avisa o projeto e segue para o próximo. Para evitar o erro, o script confere o `tamanho()` antes de pegar a posição.

**Decisão — Precedência dos operadores**
A mesma ordem do Java. O que está mais acima é feito primeiro, e operadores do mesmo nível são feitos da esquerda para a direita (`10 - 3 - 2` dá `5`). A forma por extenso tem a mesma precedência do símbolo.

| Ordem | Operadores |
|---|---|
| 1 | `( )`, chamada de função, `.` e acesso por posição `[ ]` |
| 2 | `!` e o `-` de sinal (`-5`) |
| 3 | `*` `/` `%` (`multiplica`, `dividido-por`) |
| 4 | `+` `-` (`mais`, `menos`) |
| 5 | `<` `>` `<=` `>=` (`menor-que`, `maior-que`, `menor-ou-igual-a`, `maior-ou-igual-a`) |
| 6 | `==` `!=` (`igual-a`, `diferente-de`) |
| 7 | `&&` (`e`) |
| 8 | `\|\|` (`ou`) |

**Decisão — Escopo**
Uma variável declarada dentro de um bloco `{ ... }` (de uma função, de um `se`, de um `enquanto` ou de um `para`) vale do ponto em que foi declarada até o `}` que fecha aquele bloco. Usá-la depois disso é um erro apontado antes de gravar o objeto. A exceção são os atributos declarados no `Possui`, que valem na classe toda (ver Atributos da classe).

---

## O Que o Sistema Produz

Ao ser compilado, o sistema grava um **objeto**: um arquivo com as tabelas dos autômatos dos padrões declarados e as instruções do script. O compilador termina aí, sem executar nada.

**Decisão — A ordem do objeto**
O objeto guarda, nesta ordem: o cabeçalho (a marca de que é um objeto Solis e a versão do formato), a máquina de cada padrão, na ordem em que os padrões foram declarados, e as instruções do script, a começar pela `principal`. Cada instrução leva o número da linha do script de onde veio, para que uma mensagem de erro de execução diga em que linha o problema aconteceu: `registro 3, linha 17: o texto 'sem preço' não é um número`.

**Decisão — As extensões**
O script que a pessoa escreve tem a extensão `.solx`, e não `.sol`, que já é a extensão dos contratos da linguagem Solidity. O objeto gravado tem a extensão `.solxo` (o "o" de objeto): compilar `filtro.solx` grava `filtro.solxo`, sem escrever por cima do script.

Quem executa é outro componente, o **executor**: uma máquina virtual própria, embutida no projeto que incorpora o script. Depois, e com o compilador já encerrado, o executor lê o objeto e o roda sobre os registros reais que o projeto recebe. O objeto não depende do sistema operacional.

**Decisão — Um registro por vez**
Todo script tem a função `principal pede (Linha registro) e retorna Booleano`. O executor a chama uma vez para cada registro: `verdadeiro` mantém o registro, `falso` o descarta.

**Decisão — Para onde vai o `Imprime`**
O executor não escreve em lugar nenhum por conta própria: cada `Imprime` vira uma mensagem que ele entrega ao projeto que incorporou o script, e o projeto decide onde mostrá-la (na tela, num arquivo, ou em lugar nenhum). As mensagens ficam separadas dos registros mantidos: quem decide o que fica é o `devolve` da `principal`.

O compilador verifica o texto antes de gravar o objeto:

- Se estiver correto → o objeto é gravado.
- Se algo estiver errado → nenhum objeto é gravado, e um **alerta de erro** é emitido para o usuário.

---

## Alfabeto da Linguagem (Σ)

Σ tem **122 símbolos**: letras minúsculas e maiúsculas, dígitos, operadores, delimitadores, ponto,
sublinhado, aspas simples e dupla, crase, espaços em branco (espaço, Tab e quebra de linha), e
letras acentuadas, os símbolos de registro (`@`, `#`, `$`, `º`, `ª`, `°`), `?` e `\`, que só valem
dentro de uma `Linha`, de um comentário ou de um padrão.

**Decisão — O alfabeto dos registros**
Σ é o alfabeto do que se escreve no arquivo `.solx`. Os registros que o executor lê podem ter
qualquer símbolo: os que estão fora de Σ contam como um único símbolo a mais, o **outro**, que só o
coringa `.` reconhece. Nenhum registro é recusado por causa dos símbolos que tem.

A lista completa, com as regras de uso, está em
[`especificacao/alfabeto.md`](../especificacao/alfabeto.md).

---

## Classes Léxicas

| Classe | O que contém |
|---|---|
| Operadores | aritméticos, atribuição, comparação (inclusive `>=` e `<=`) e lógicos (`&&`, `\|\|`, `!`); quase todos também podem ser escritos por extenso, menos `%` e `!` (`mais`, `recebe`, `igual-a`, `maior-ou-igual-a`, `e`, `ou`...) |
| Palavras reservadas | palavras de funções (`funcao`, `devolve`...), de classes (`Classe`, `Possui`, `Faz`, `Novo`), os tipos (`Linha`, `Inteiro`, `Padrao`...), as de controle (`se`, `senao`, `enquanto`, `para`, `em`, `pare`, com inicial minúscula ou maiúscula) e `Imprime` |
| Identificadores | `[a-zA-Z][a-zA-Z0-9_]* \| _+[a-zA-Z0-9][a-zA-Z0-9_]*` |
| Literais | Inteiro `[0-9]+`, Quebrado `[0-9]+\.[0-9]+`, Linha `'[^'\n]*' \| "[^"\n]*"`, Booleano `verdadeiro \| falso`, Padrão: o texto do padrão entre crases |
| Delimitadores / Pontuação | `{` `}` `(` `)` `[` `]` `:` `;` `,` `.` |
| Comentário (descartado) | `//` até o fim da linha |

A lista completa de cada classe, com exemplos válidos e inválidos, está em
[`especificacao/classes_lexicas.md`](../especificacao/classes_lexicas.md).
