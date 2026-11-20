# Solis — Recorte da Peneira

### Decisões fixadas no primeiro módulo

---

## Visão Geral

| | |
|---|---|
| **Nome** | Solis |
| **Extensão** | `.sol` |
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
Também funcional: um programa em Solis pode ser escrito só com funções, sem nenhuma classe. As funções existem fora das classes, como `soma` e `principal` em `docs/exemplos.sol`.

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

Por extenso, `>=` é `maior-ou-igual-a` e `<=` é `menor-ou-igual-a`.

**Decisão — Padrões**
Quem escreve em Solis declara padrões: descrições da forma que um trecho de texto pode ter, como "um ou mais dígitos". É o que dá à linguagem o seu domínio: identificar, organizar e filtrar registros pela forma dos campos.

- O padrão é escrito entre crases e guardado numa variável do tipo `Padrao`: ``Padrao numero recebe `[0-9]+`;``
- `casa` diz se um texto **inteiro** tem a forma do padrão e devolve `Booleano`: `numero.casa(campo)`
- `procura` devolve uma `Lista` de `Linha` com os trechos de um texto que têm a forma do padrão, ficando sempre com o trecho mais longo: `numero.procura(registro)`
- As duas operações são métodos do padrão, chamados com o `.` que já existe: não entra operador novo.
- Não há captura: o sistema não guarda qual trecho casou com cada parte do padrão.

**Decisão — O pedido que o padrão não atende**
Parênteses balanceados, em que cada `(` tem o seu `)` mais adiante, em qualquer profundidade, são um pedido natural de quem escreve padrões, e nenhum padrão da Solis o reconhece. É a demonstração do limite do reconhecimento por autômato finito.

### Estruturas de Controle

| Estrutura | Sintaxe |
|---|---|
| Loop (equivalente ao `while` do Python) | `enquanto (<condição>) { ... }` |
| Loop (equivalente ao `for` do Python) | `para <variável> em <iterável> { ... }` |
| Atribuição de variável | `<Tipo> <variável> recebe <valor>;` |
| Condicionais | `se (<condição>) { ... } senao { ... }` |
| Interrupção de loop | `pare` |

**Exemplo de atribuição:**
```
Linha x recebe "texto aleatorio";
```

---

## O Que o Sistema Produz

Ao ser compilado, o sistema grava um **objeto**: um arquivo com as tabelas dos autômatos dos padrões declarados e as instruções do script. O compilador termina aí, sem executar nada.

Quem executa é outro componente, o **executor**: uma máquina virtual própria, embutida no projeto que incorpora o script. Depois, e com o compilador já encerrado, o executor lê o objeto e o roda sobre os registros reais que o projeto recebe. O objeto não depende do sistema operacional.

O compilador verifica o texto antes de gravar o objeto:

- Se estiver correto → o objeto é gravado.
- Se algo estiver errado → nenhum objeto é gravado, e um **alerta de erro** é emitido para o usuário.

---

## Alfabeto da Linguagem (Σ)

Σ tem **116 símbolos**: letras minúsculas e maiúsculas, dígitos, operadores, delimitadores, ponto,
sublinhado, aspas simples e dupla, crase, espaços em branco (espaço, Tab e quebra de linha), letras
acentuadas, que só valem dentro de uma `Linha`, e `?` e `\`, que só valem dentro de um padrão.

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
