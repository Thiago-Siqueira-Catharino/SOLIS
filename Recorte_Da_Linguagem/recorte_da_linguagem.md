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

---

## Forma da Descrição Escrita pelo Usuário

**Decisão de otimização — SenãoSe**
Quando o usuário fizer uma comparação usando os comparadores `se` e `senao` na mesma ordem, o compilador organiza para **SenãoSe**, onde as duas comparações são executadas ao mesmo tempo e prevalece a condição que se tornar verdadeira primeiro.

**Decisão — Dispensa do operador ternário**
O usuário dispensa a necessidade de utilizar o operador ternário, pois será necessária apenas uma estrutura de condição para cair na regra descrita acima.

**Decisão — Paradigma**
Base em POO (Programação Orientada a Objetos), para que classes possam ser reutilizadas em outras dependências filhas, com definições simples de métodos e declarações de instâncias.

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

**Decisão — Simplificação dos operadores lógicos**

- Maior que `>`
- Menor que `<`
- Igual `==`
- Diferença `!=`

Se escritos numa mesma frase, *maior ou igual* / *menor ou igual*, o compilador junta os dois operadores (`>=`, `<=`).

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

Ao ser compilado, o sistema produz um **arquivo executável**, que serve de base para executar o programa.

O compilador verifica se as sintaxes estão corretas:

- Se estiverem corretas → o programa é executado.
- Se algo estiver faltando → a compilação não ocorre e um **alerta de erro** é emitido para o usuário.

---

## Alfabeto da Linguagem (Σ)

Σ tem **113 símbolos**: letras minúsculas e maiúsculas, dígitos, operadores, delimitadores, ponto,
sublinhado, aspas simples e dupla, espaços em branco (espaço, Tab e quebra de linha) e letras
acentuadas, que só valem dentro de uma `Linha`.

A lista completa, com as regras de uso, está em
[`especificacao/alfabeto.md`](../especificacao/alfabeto.md).

---

## Classes Léxicas

| Classe | O que contém |
|---|---|
| Operadores | aritméticos, atribuição, comparação e lógicos (`&&`, `\|\|`, `!`); quase todos também podem ser escritos por extenso, menos `%` e `!` (`mais`, `recebe`, `igual-a`, `e`, `ou`...) |
| Palavras reservadas | palavras de funções (`funcao`, `devolve`...), de classes (`Classe`, `Possui`, `Faz`, `Novo`), os tipos (`Linha`, `Inteiro`...), as de controle (`se`, `senao`, `enquanto`, `para`, `em`, `pare`, com inicial minúscula ou maiúscula), `Imprime` e `lista` |
| Identificadores | `[a-zA-Z_][a-zA-Z0-9_]*` |
| Literais | Inteiro `[0-9]+`, Quebrado `[0-9]+\.[0-9]+`, Linha `'[^'\n]*' \| "[^"\n]*"`, Booleano `verdadeiro \| falso` |
| Delimitadores / Pontuação | `{` `}` `(` `)` `[` `]` `:` `;` `,` |

A lista completa de cada classe, com exemplos válidos e inválidos, está em
[`especificacao/classes_lexicas.md`](../especificacao/classes_lexicas.md).
