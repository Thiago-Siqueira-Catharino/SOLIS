# Solis

Linguagem de script compilada e fortemente tipada, escrita inteiramente em português brasileiro.

## Sobre o Projeto

A **Solis** é uma linguagem de programação criada para o desenvolvimento de scripts que podem ser integrados a aplicações desenvolvidas em outras linguagens.

A linguagem combina a organização e a segurança inspiradas em **Java** com a simplicidade e a flexibilidade de **Lua**. Seu modelo de programação contempla os paradigmas de programação orientada a objetos e funcional.

O domínio da Solis são os scripts que **identificam, organizam e filtram registros com campos**, descritos por **padrões**: quem escreve declara a forma que um campo pode ter (por exemplo, "um ou mais dígitos") e testa os registros com ela. A Solis é pensada como porta de entrada para quem precisa automatizar uma tarefa e não domina o inglês nem uma linguagem em inglês.

Ao compilar, o compilador grava um **objeto** com as tabelas dos autômatos dos padrões e as instruções do script, sem executar nada. Quem executa é um **executor**, uma máquina virtual própria embutida no projeto que incorpora o script. O executor ainda não foi construído.

## Características da Linguagem

| Característica | Detalhes |
|---|---|
| Nome | Solis |
| Extensão de arquivo | `.sol` |
| Base conceitual | Java |
| Inspiração | Lua |
| Tipagem | Forte |
| Execução | Compilada: grava um objeto, executado depois por uma máquina virtual |
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
| `Padrao` | Representa a forma que um trecho de texto pode ter. | `` `[0-9]+` `` |

## Operadores

Quase todo operador pode ser escrito com o símbolo ou por extenso: `a + b` e `a mais b` são a mesma
coisa. Só `%` e `!` não têm forma por extenso. A lista completa está em
`especificacao/classes_lexicas.md`.

### Matemáticos

| Operador | Por extenso | Significado |
|---|---|---|
| `+` | `mais` | adição |
| `-` | `menos` | subtração |
| `*` | `multiplica` | multiplicação |
| `/` | `dividido-por` | divisão |
| `%` | — | resto |

### Atribuição

| Operador | Por extenso | Significado |
|---|---|---|
| `=` | `recebe` | guarda um valor na variável |

### Comparação

| Operador | Por extenso | Significado |
|---|---|---|
| `>` | `maior-que` | maior que |
| `<` | `menor-que` | menor que |
| `>=` | `maior-ou-igual-a` | maior ou igual |
| `<=` | `menor-ou-igual-a` | menor ou igual |
| `==` | `igual-a` | igual |
| `!=` | `diferente-de` | diferente |

### Lógicos

| Operador | Por extenso | Significado |
|---|---|---|
| `&&` | `e` | e lógico |
| `\|\|` | `ou` | ou lógico |
| `!` | — | negação |

## Variáveis

Declaração e atribuição seguem o formato:

```sol
<Tipo> <variavel> recebe <valor>;
```

Exemplo:

```sol
Linha x recebe "texto aleatorio";
```

## Comentários

Um comentário começa com `//` e vai até o fim da linha. Ele não muda nada no programa: o
analisador léxico o descarta, como os espaços em branco. Pode ter acento.

```sol
Linha x recebe "texto aleatorio"; // daqui até o fim da linha é comentário
```

## Padrões

Um padrão é escrito entre crases, numa linha só, e guardado numa variável do tipo `Padrao`:

```sol
Padrao numero recebe `[0-9]+`;
```

Dentro das crases vale o núcleo de operadores de padrão descrito em `docs/02nucleo_minimo.md`
(`|`, `*`, `+`, `?`, `[a-z]`, `.`, `\.`...), e também letras acentuadas: ``Padrao cidade recebe `São Paulo`;``.

O padrão tem dois métodos, chamados com o `.`:

| Método | Devolve | O que faz |
|---|---|---|
| `casa(texto)` | `Booleano` | diz se o texto **inteiro** tem a forma do padrão |
| `procura(texto)` | `Lista` de `Linha` | os trechos do texto que têm a forma do padrão, ficando sempre com o trecho mais longo |

```sol
se (numero.casa(campo)) {
    Imprime(campo);
};
Lista achados recebe numero.procura(registro);
```

Não há captura: o sistema não guarda qual trecho casou com cada parte do padrão. O padrão vazio,
duas crases seguidas, só casa com a Linha vazia.

**Limite da linguagem:** parênteses balanceados, em que cada `(` tem o seu `)` mais adiante em
qualquer profundidade, não podem ser descritos por nenhum padrão da Solis. É o limite do
reconhecimento por autômato finito.

## Estruturas de Controle

### Condicionais

```sol
se (condicao) {
    // bloco executado se verdadeiro
} senao {
    // bloco executado se falso
};
```

Não existe `senao se`. Para encadear condições, um `se` vai dentro do bloco do `senao`, e as
condições são testadas uma de cada vez, na ordem em que foram escritas:

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

Uma função que retorna `Vazio` termina com `devolve;` sozinho, sem valor: `Vazio` é só tipo.

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

Não há herança: uma classe não herda de outra. A herança fica fora do escopo por agora.

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
    devolve;
};
```

---

## Como rodar tudo

Requer Python 3. Na raiz do projeto, um comando roda todas as verificações do projeto:

```
python rodar_tudo.py
```

O script roda, uma a uma, as doze partes descritas nas seções abaixo, na ordem em que as peças do
compilador foram construídas. Cada parte confere o próprio resultado e termina com código 0 quando
tudo passou, ou 1 quando alguma verificação falhou. A saída esperada é:

```
[OK]     AFD de dígitos                 6/6 casos passaram.
[OK]     AFD de letras                  6/6 casos passaram.
[OK]     AFD de letras e dígitos        14/14 casos passaram.
[OK]     Leitor de padrões              37/37 verificações passaram.
[OK]     AFN, passo 1: estrutura        9/9 verificações passaram.
[OK]     AFN, passo 2: fecho vazio      11/11 verificações passaram.
[OK]     AFN, passo 3: simulação        35/35 verificações passaram.
[OK]     AFN, passo 4: Thompson         38/38 verificações passaram.
[OK]     AFN, bateria conferida à mão   59/59 casos passaram.
[OK]     Determinização                 39/39 verificações passaram.
[OK]     Minimização                    36/36 verificações passaram.
[OK]     Três máquinas e explosão       71/71 verificações passaram.

Solis: 12/12 partes passaram.
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
| Letras e dígitos | `[a-zA-Z][a-zA-Z0-9_]* \| _+[a-zA-Z0-9][a-zA-Z0-9_]*` | `resultado`, `Ana`, `meu_nome`, `_nome`, `_1` | vazio, `1a`, `2_nome`, `_`, `___` |

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
| `Afds/Alfabeto_0_ate_Z/afd_letras_numeros.py` | `AFD de letras e dígitos: 14/14 casos passaram.` |

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
   Quebrado 83, Identificador 486, Booleano 29, Delimitador 19, Palavra reservada 319 e
   Operador 259;
3. a convergência: `a+` e `aa*`, `[abc]` e `a|b|c`, `[a-c]` e `[abc]`, `(ab)c` e `abc`, `[0-9]+` e
   `[0-9][0-9]*` dão a mesma árvore; `[a-z0-9]` e `([a-z]|[0-9])` dão árvores diferentes, com os
   mesmos 71 nós;
4. oito textos malformados, cada um com a marca `^` sob a posição do problema.

A última linha esperada é `Leitor de padrões: 37/37 verificações passaram.` Se alguma verificação
falhar, a linha correspondente mostra `[FALHOU]` com o valor obtido e o esperado, e o programa
termina com código de saída 1.

As posições são contadas a partir de 1. Quando algo abre e não fecha, a marca fica no fim do texto,
onde a falta foi constatada, e a mensagem diz em que posição o grupo ou a classe abriu.

**Limite conhecido:** a Linha (`'[^'\n]*'`) e o literal Padrão (`` `[^`\n]*` ``) usam classe negada,
que o leitor não aceita.

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

A saída esperada é `Bateria conferida à mão: 59/59 casos passaram.` Se algum caso falhar, a bateria
mostra o arquivo, a linha, o veredito esperado e o obtido, e termina com código de saída 1.

Os testes de cada etapa rodam da mesma forma, por exemplo `python Afn/teste_passo3.py`. Cada linha
mostra o valor obtido e o esperado, e os erros provocados de propósito aparecem como
`[OK] erro esperado (...)`. A última linha esperada de cada um:

| Arquivo | O que testa | Última linha esperada |
|---|---|---|
| `Afn/teste_passo1.py` | estados, setas, contagens e validações | `teste_passo1: 9/9 verificações passaram.` |
| `Afn/teste_passo2.py` | o fecho vazio | `teste_passo2: 11/11 verificações passaram.` |
| `Afn/teste_passo3.py` | a simulação e o movimento por símbolo | `teste_passo3: 35/35 verificações passaram.` |
| `Afn/teste_passo4.py` | a construção de Thompson | `teste_passo4: 38/38 verificações passaram.` |

Se alguma verificação falhar, a linha dela mostra `[FALHOU]` e o teste termina com código de saída 1.

### Acrescentar um caso de teste

Cada linha de `Afn/casos_afn.txt` tem três campos separados por **Tab**:

```
padrão <Tab> cadeia <Tab> aceita|recusa
```

A cadeia vazia é o campo vazio entre dois Tabs, e linhas começando com `#` são comentários. O
veredito precisa ser decidido à mão, seguindo o padrão, **antes** de rodar a bateria.

---

## Determinização e Minimização

A pasta `Determinizacao/` recebe o AFN da construção de Thompson, da pasta `Afn/`, e o transforma
num AFD pela construção de subconjuntos. Depois, reduz esse AFD ao autômato mínimo pelo
refinamento de partições. Segue o guia "Implementação em C++: Thompson, determinização e
minimização", passos 12 a 25 do roteiro, traduzido para Python.

### Estrutura

| Arquivo | O que faz |
|---|---|
| `Determinizacao/afd.py` | o AFD: estados numerados, um destino por estado e símbolo, vários estados de aceitação |
| `Determinizacao/determinizacao.py` | a construção de subconjuntos: cada conjunto de estados do AFN vira um estado do AFD |
| `Determinizacao/minimizacao.py` | completa o AFD, descarta os inacessíveis e junta os estados equivalentes |
| `Determinizacao/teste_determinizacao.py` | testa a determinização com os valores do guia |
| `Determinizacao/teste_minimizacao.py` | testa a minimização com os valores do guia |
| `Determinizacao/demonstrar_determinizacao.py` | compara as três máquinas e monta a explosão de estados |

O conjunto vazio não tem caso especial: quando aparece, recebe número como os outros e vira o
estado de erro, e o AFD sai completo. Quando nenhuma cadeia leva ao vazio, ele não é criado.

### Como executar

Requer Python 3. Na raiz do projeto:

```
python Determinizacao/demonstrar_determinizacao.py
```

A saída tem três partes:

1. os padrões do guia, com os estados antes e depois da minimização, e as três máquinas comparadas
   em todas as cadeias sobre o alfabeto até um comprimento;
2. os 59 casos de `Afn/casos_afn.txt` rodados nas três máquinas e comparados com o veredito decidido
   à mão (47 comparados; 12 ignorados por terem símbolos fora do alfabeto do padrão, onde o AFN e o
   AFD seguem regras diferentes);
3. a explosão de estados, para n de 1 a 8.

| Arquivo | Última linha esperada |
|---|---|
| `Determinizacao/teste_determinizacao.py` | `teste_determinizacao: 39/39 verificações passaram.` |
| `Determinizacao/teste_minimizacao.py` | `teste_minimizacao: 36/36 verificações passaram.` |
| `Determinizacao/demonstrar_determinizacao.py` | `demonstrar_determinizacao: 71/71 verificações passaram.` |

Se alguma verificação falhar, a linha dela mostra `[FALHOU]` e o programa termina com código de
saída 1.

### Estados antes e depois da minimização

| Padrão | AFN | AFD | Mínimo |
|---|---|---|---|
| `(a\|b)*c` | 10 | 5 | 3 |
| `(a\|b)*abb` | 14 | 5 | 4 |
| `a.c` | 6 | 5 | 5 |

São os números do guia (seções 1.7.3, 1.8.1 e 1.8.5). O material dá 6 e 5 para o AFD e o mínimo de
`(a|b)*abb` porque cria o estado de erro de antemão e o conta mesmo quando nenhuma seta chega nele;
aqui ele só existe quando é alcançável. As linguagens são as mesmas.

### Explosão de estados

A linguagem das cadeias sobre {a, b} em que o n-ésimo símbolo contado do fim é `a`, com o padrão
`(a|b)*a` seguido de n − 1 cópias de `(a|b)`:

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Fórmula |
|---|---|---|---|---|---|---|---|---|---|
| AFN | 10 | 16 | 22 | 28 | 34 | 40 | 46 | 52 | 6n + 4 |
| AFD | 3 | 5 | 9 | 17 | 33 | 65 | 129 | 257 | 2ⁿ + 1 |
| Mínimo | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 2ⁿ |

O AFN cresce 6 estados por n, e o AFD dobra: até n = 5 o AFD ainda é menor que o AFN (33 contra 34);
a partir de n = 6, é maior. O mínimo fica exatamente no piso de 2ⁿ estados que o material prova, e
por isso o crescimento é da linguagem, e não do algoritmo: nenhum AFD reconhece essa linguagem com
menos estados. O material mede 2ⁿ + 2 e 2ⁿ + 1 porque conta o estado de erro inalcançável; aqui ele
não é criado. A demonstração confere as três máquinas contra a definição da linguagem, escrita
sem máquina nenhuma, em todas as 2047 cadeias sobre {a, b} até o comprimento 10.
