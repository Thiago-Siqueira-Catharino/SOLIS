# Solis

Linguagem de script compilada e fortemente tipada, escrita inteiramente em português brasileiro.

## Sobre o Projeto

A **Solis** é uma linguagem de programação criada para o desenvolvimento de scripts que podem ser integrados a aplicações desenvolvidas em outras linguagens.

A linguagem combina a organização e a segurança inspiradas em **Java** com a simplicidade e a flexibilidade de **Lua**. Seu modelo de programação contempla os paradigmas de programação orientada a objetos e funcional.

## Características da Linguagem

| Característica | Detalhes |
|---|---|
| Nome | Solis |
| Extensão de arquivo | `.sol` |
| Base conceitual | Java |
| Inspiração | Lua |
| Tipagem | Forte |
| Execução | Compilada |
| Paradigmas | Orientado a objetos e funcional |
| Idioma | Português brasileiro |

## Tipos Primitivos

| Tipo em Solis | Descrição | Exemplo |
|---|---|---|
| `Linha` | Representa textos e sequências de caracteres. | `"Olá, Solis!"` |
| `Inteiro` | Representa números inteiros. | `42` |
| `Quebrado` | Representa números com casas decimais. | `3.14` |
| `Booleano` | Representa valores lógicos. | `verdadeiro` |
| `Vazio` | Representa a ausência de valor de retorno. | `Vazio` |
| `Lista` | Representa uma coleção ordenada de valores. | `['Ana', 'Beatriz']` |

## Operadores

### Matemáticos

| Operador | Significado |
|---|---|
| `+` | adição |
| `-` | subtração |
| `*` | multiplicação |
| `/` | divisão |
| `%` | resto |

### Lógicos

| Operador | Forma alternativa | Significado |
|---|---|---|
| `>` | `{maior}` | maior que |
| `<` | `{menor}` | menor que |
| `==` | `{igual}` | igual |
| `!=` | `{diferente}` | diferença |

## Variáveis

Declaração e atribuição seguem o formato:

```sol
{Tipo} {variavel} recebe {valor};
```

Exemplo:

```sol
Linha x recebe "texto aleatorio";
```

## Estruturas de Controle

### Condicionais

```sol
se (condicao) (
    // bloco executado se verdadeiro
) senao (
    // bloco executado se falso
);
```

### Loops

**Enquanto** (equivalente ao `while`):

```sol
enquanto (condicao) (
    // corpo do loop
);
```

**Para** (equivalente ao `for ... in`):

```sol
para {variavel} em {iteravel} (
    // corpo do loop
);
```

Interromper um loop:

```sol
pare;
```

## Funções

Sintaxe geral:

```sol
funcao <nome_da_funcao> pede (<tipo> <arg>, ...) e retorna <tipo> {
    // corpo
    devolve <valor>;
};
```

Exemplo:

```sol
funcao soma pede (a, b) e retorna Quebrado {
    devolve a + b;
};
```

## Classes

Classes usam os blocos `Possui` (atributos) e `Faz` (métodos):

```sol
Classe Matematica {
    Possui {
    };
    Faz {
        funcao soma pede (a, b) e retorna Quebrado {
            devolve a + b;
        };
        funcao multiplicar pede (a, b) e retorna Quebrado {
            devolve a * b;
        };
    };
}
```

Instanciação de um objeto com `Novo`:

```sol
Matematica mat recebe Novo Matematica;
```

---

## Exemplo Completo

```sol
funcao soma pede (a, b) e retorna Quebrado {
    devolve a + b;
};

Classe Matematica {
    Possui {
    };
    Faz {
        funcao soma pede (a, b) e retorna Quebrado {
            devolve a + b;
        };
        funcao multiplicar pede (a, b) e retorna Quebrado {
            devolve a * b;
        };
    };
}

funcao principal pede () e retorna Vazio {
    Quebrado x recebe 3.14;
    Inteiro y recebe 2;
    Matematica mat recebe Novo Matematica;
    Imprime(soma(x, y));
    Imprime(mat.multiplicar(x, y));
    devolve Vazio;
};
```
