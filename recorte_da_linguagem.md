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
Quando o usuário fizer uma comparação usando os comparadores *Se* e *Senão* na mesma ordem, o compilador organiza para **SenãoSe**, onde as duas comparações são executadas ao mesmo tempo e prevalece a condição que se tornar verdadeira primeiro.

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

- Cadeia de caracteres (`String`)
- Inteiro (`int`)
- Ponto Flutuante (`Float`)
- Booleano (`bool`)
- Vazio (`Void`)
- Lista (`listz`)

**Decisão — Simplificação dos operadores lógicos**

- Maior que `>`
- Menor que `<`
- Igual `==`
- Diferença `!=`

Se escritos numa mesma frase, *maior ou igual* / *menor ou igual*, o compilador junta os dois operadores (`+=`, `-=`).

### Estruturas de Controle

| Estrutura | Sintaxe |
|---|---|
| Loop (equivalente ao `while` do Python) | `Enquanto` |
| Loop (equivalente ao `for` do Python) | `para {variável} em {iterável}` |
| Atribuição de variável | `{Tipo} {variável} recebe {valor};` |
| Condicionais | `se` / `senao` |
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

```
Σ = { 
    a, b, c, d, e, f, g, h, i, j, k, l, m, n, 
    o, p, q, r, s, t, u, v, w, x, y, z, ,, {, },
    (, ), [, ], :, ;, +, -, *, /, %, =, <, >, !,
    1, 2, 3, 4, 5, 6, 7, 8, 9, 0, _, ', &, |
}
```

---

## Classes Léxicas

### Operadores

| Símbolo | Palavra-chave |
|---|---|
| `+` | mais |
| `-` | menos |
| `*` | multiplica |
| `/` | dividido-por |
| `%` | — |
| `=` | recebe |
| `==` | igual-a |
| `<` | menor-que |
| `>` | maior-que |
| `!=` | diferente-de |
| `&&` | e |
| `||` | ou |
| `!` | — |

### Palavras Reservadas

```
funcao      pede        retorna     devolve
Classe      Possui      Faz         principal
Linha       Inteiro     Quebrado    Booleano
Vazio       Lista       Dicionario
Enquanto
Para        em
se          senao
pare
```

### Delimitadores / Pontuação

| Símbolo | Função |
|---|---|
| `{` `}` | Bloco |
| `(` `)` | Agrupamento / parâmetros |
| `[` `]` | Lista |
| `:` | Separador |
| `;` | Fim de instrução |
| `'` | Atribuição de String |