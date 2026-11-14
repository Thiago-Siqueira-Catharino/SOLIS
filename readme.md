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
<Tipo> <variavel> recebe <valor>;
```

Exemplo:

```sol
Linha x recebe "texto aleatorio";
```

## Estruturas de Controle

### Condicionais

```sol
se (condicao) {
    // bloco executado se verdadeiro
} senao {
    // bloco executado se falso
};
```

### Loops

**Enquanto** (equivalente ao `while`):

```sol
enquanto (condicao) {
    // corpo do loop
};
```

**Para** (equivalente ao `for ... in`):

```sol
para <variavel> em <iteravel> {
    // corpo do loop
};
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
funcao soma pede (Quebrado a, Quebrado b) e retorna Quebrado {
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
        funcao soma pede (Quebrado a, Quebrado b) e retorna Quebrado {
            devolve a + b;
        };
        funcao multiplicar pede (Quebrado a, Quebrado b) e retorna Quebrado {
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
funcao soma pede (Quebrado a, Quebrado b) e retorna Quebrado {
    devolve a + b;
};

Classe Matematica {
    Possui {
    };
    Faz {
        funcao soma pede (Quebrado a, Quebrado b) e retorna Quebrado {
            devolve a + b;
        };
        funcao multiplicar pede (Quebrado a, Quebrado b) e retorna Quebrado {
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

---

## Como rodar tudo

Requer Python 3. Na raiz do projeto, um comando roda todas as verificações do projeto:

```
python rodar_tudo.py
```

O script roda, uma a uma, as nove partes descritas nas seções abaixo, na ordem em que as peças do
compilador foram construídas. Cada parte confere o próprio resultado e termina com código 0 quando
tudo passou, ou 1 quando alguma verificação falhou. A saída esperada é:

```
[OK]     AFD de dígitos                 6/6 casos passaram.
[OK]     AFD de letras                  6/6 casos passaram.
[OK]     AFD de letras e dígitos        8/8 casos passaram.
[OK]     Leitor de padrões              36/36 verificações passaram.
[OK]     AFN, passo 1: estrutura        9/9 verificações passaram.
[OK]     AFN, passo 2: fecho vazio      11/11 verificações passaram.
[OK]     AFN, passo 3: simulação        26/26 verificações passaram.
[OK]     AFN, passo 4: Thompson         38/38 verificações passaram.
[OK]     AFN, bateria conferida à mão   50/50 casos passaram.

Solis: 9/9 partes passaram.
```

Se uma parte falhar, a linha dela começa com `[FALHOU]`, logo abaixo aparecem as verificações que
falharam e o comando para ver a saída completa daquela parte, e o script termina com código 1.

---

## Análise Léxica

Autômatos finitos determinísticos (AFD) que reconhecem as partes do alfabeto da Solis, escritos em Python a partir do modelo de AFD apresentado em aula.

### Estrutura

| Pasta | O que contém |
|---|---|
| `Afds/Afd_Solis` | Motor genérico do AFD (`afd.py`): estados, alfabeto, transições, estado inicial e estados finais |
| `Afds/Alfabeto_0_ate_9` | AFD de dígitos |
| `Afds/Alfabeto_A_ate_Z` | AFD de letras |
| `Afds/Alfabeto_0_ate_Z` | AFD de letras e dígitos |

### Padrões reconhecidos

| AFD | Padrão | Aceita | Rejeita |
|---|---|---|---|
| Dígitos | `[0-9]+` | `42`, `7` | vazio, `4a`, `-5`, `4.5` |
| Letras | `[a-zA-Z]+` | `abacate`, `Ana` | vazio, `a1`, `ana@` |
| Letras e dígitos | `[a-zA-Z][a-zA-Z0-9]*` | `resultado`, `resultado2`, `Ana` | vazio, `1a`, `123`, `meu_nome` |

### Como executar

Requer Python 3. Na raiz do projeto, execute o arquivo do AFD desejado. Cada um roda os próprios
testes e mostra, para cada palavra, o veredito obtido e o esperado:

```
python Afds/Alfabeto_0_ate_9/afd_numeros.py
```

Saída esperada:

```
[OK] '42': obtido Aceita, esperado Aceita
[OK] '7': obtido Aceita, esperado Aceita
[OK] '': obtido Rejeitada, esperado Rejeitada
[OK] '4a': obtido Rejeitada, esperado Rejeitada
[OK] '-5': obtido Rejeitada, esperado Rejeitada
[OK] '4.5': obtido Rejeitada, esperado Rejeitada
AFD de dígitos: 6/6 casos passaram.
```

| Arquivo | Última linha esperada |
|---|---|
| `Afds/Alfabeto_0_ate_9/afd_numeros.py` | `AFD de dígitos: 6/6 casos passaram.` |
| `Afds/Alfabeto_A_ate_Z/afd_letras.py` | `AFD de letras: 6/6 casos passaram.` |
| `Afds/Alfabeto_0_ate_Z/afd_letras_numeros.py` | `AFD de letras e dígitos: 8/8 casos passaram.` |

Se algum caso falhar, a linha dele mostra `[FALHOU]` e o programa termina com código de saída 1.

---

## Leitor de Padrões

A pasta `Leitor_De_Padroes/` é a primeira peça do compilador: lê o texto de um padrão, como
`[0-9]+`, decide se ele é um padrão, monta a árvore dele e, quando o texto é malformado, diz em que
posição a leitura constatou o problema. A árvore que ele monta é a que a construção de Thompson,
na pasta `Afn/`, consome.

### Estrutura

| Arquivo | O que faz |
|---|---|
| `Leitor_De_Padroes/leitor_padroes.py` | lê o padrão por descida recursiva e reduz o açúcar (`x+`, `x?`, `[abc]`, `[a-c]`) na leitura |
| `Leitor_De_Padroes/arvore.py` | os 6 tipos de nó, a forma da árvore em texto e a contagem de nós |
| `Leitor_De_Padroes/demonstrar_leitor.py` | mostra o leitor funcionando, com o resultado esperado ao lado de cada linha |

### Como executar

Requer Python 3. Na raiz do projeto:

```
python Leitor_De_Padroes/demonstrar_leitor.py
```

A saída tem quatro partes, na ordem da seção 1.8 do material:

1. as cinco expressões do material, com a forma da árvore e o número de nós (1, 3, 5, 6 e 16);
2. os padrões das classes léxicas da Solis, com os nós contados à mão antes de rodar: Inteiro 40,
   Quebrado 83, Identificador 232, Booleano 29, Delimitador 17, Palavra reservada 337 e
   Operador 187;
3. a convergência: `a+` e `aa*`, `[abc]` e `a|b|c`, `[a-c]` e `[abc]`, `(ab)c` e `abc`, `[0-9]+` e
   `[0-9][0-9]*` dão a mesma árvore; `[a-z0-9]` e `([a-z]|[0-9])` dão árvores diferentes, com os
   mesmos 71 nós;
4. oito textos malformados, cada um com a marca `^` sob a posição do problema.

A última linha esperada é `Leitor de padrões: 36/36 verificações passaram.` Se alguma verificação
falhar, a linha correspondente mostra `[FALHOU]` com o valor obtido e o esperado, e o programa
termina com código de saída 1.

As posições são contadas a partir de 1. Quando algo abre e não fecha, a marca fica no fim do texto,
onde a falta foi constatada, e a mensagem diz em que posição o grupo ou a classe abriu.

**Limite conhecido:** a Linha (`'[^'\n]*'`) usa classe negada, que o leitor não aceita.

---

## Autômato Finito Não Determinístico (AFN)

A pasta `Afn/` recebe a árvore de um padrão, montada pelo leitor de padrões da pasta
`Leitor_De_Padroes/`, transforma essa árvore numa máquina não determinística, pela construção de
Thompson, e executa essa máquina sobre uma cadeia. O registro das decisões está em
`docs/diario_construcao.md`.

### Estrutura

| Arquivo | O que faz |
|---|---|
| `Leitor_De_Padroes/leitor_padroes.py` | transforma o texto do padrão (ex.: `[0-9]+`) na árvore |
| `Leitor_De_Padroes/arvore.py` | os 6 tipos de nó da árvore de um padrão |
| `Afn/afn.py` | a máquina: estados, transições, fecho vazio e simulação |
| `Afn/thompson.py` | transforma a árvore na máquina |
| `Afn/bateria.py` | roda os casos de `casos_afn.txt` e compara com o veredito |
| `Afn/casos_afn.txt` | os casos de teste, com vereditos decididos à mão |
| `Afn/teste_passo1.py` a `teste_passo4.py` | testes de cada etapa da construção |

### Como executar

Requer Python 3. Na raiz do projeto:

```
python Afn/bateria.py
```

A saída esperada é `Bateria conferida à mão: 50/50 casos passaram.` Se algum caso falhar, a bateria
mostra o arquivo, a linha, o veredito esperado e o obtido, e termina com código de saída 1.

Os testes de cada etapa rodam da mesma forma, por exemplo `python Afn/teste_passo3.py`. Cada linha
mostra o valor obtido e o esperado, e os erros provocados de propósito aparecem como
`[OK] erro esperado (...)`. A última linha esperada de cada um:

| Arquivo | O que testa | Última linha esperada |
|---|---|---|
| `Afn/teste_passo1.py` | estados, setas, contagens e validações | `teste_passo1: 9/9 verificações passaram.` |
| `Afn/teste_passo2.py` | o fecho vazio | `teste_passo2: 11/11 verificações passaram.` |
| `Afn/teste_passo3.py` | a simulação | `teste_passo3: 26/26 verificações passaram.` |
| `Afn/teste_passo4.py` | a construção de Thompson | `teste_passo4: 38/38 verificações passaram.` |

Se alguma verificação falhar, a linha dela mostra `[FALHOU]` e o teste termina com código de saída 1.

### Acrescentar um caso de teste

Cada linha de `Afn/casos_afn.txt` tem três campos separados por **Tab**:

```
padrão <Tab> cadeia <Tab> aceita|recusa
```

A cadeia vazia é o campo vazio entre dois Tabs, e linhas começando com `#` são comentários. O
veredito precisa ser decidido à mão, seguindo o padrão, **antes** de rodar a bateria.
