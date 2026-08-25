
# O recorte da Peneira — decisões fixadas no primeiro módulo

O nome da Linguagem é solis, a extensão dela terminará com .sol.

Tem como base a linguagem java e inspiração na lingaugem Lua, que é compilada e fortemente tipada.

E o objetivo dela é ser uma linguagem para scripts que pode ser integrada com outras linguagens e inteiramente em portugês brasileiro


## Que forma tem a descrição escrita pelo usuário

Decisão de otimização : Quando o usuário fizer uma comparação usando os comparadores, Se e senão na mesma ordem, ela organiza para SenãoSe, onde as duas comparações são executadas ao mesmo tempo, onde prevalece aquela condição que se tornar verdadeira primeiro.

Decisão : Usuário dispensa a necessidade de utilizar o operador ternário, pois será nescessário apenas uma estrutura de condição, para cair na regra que foi descrita acima

Decisão: Ter como paradigma a base de POO, para que classes possam ser reutilizadas em outras dependências filhos, simples definições dos métodos e declarações de instâncias.

Decisão : Por se tratar de uma linguagem para scripts, temos como operadores basicos : adição (+) , multiplicação (*), subtração (-), divisão (/) e o resto (%), alem dos tipos primitivos : Cadeia de caracteres(String), Inteiro (int), Ponto Flutuante (Float), Booleano (bool), Vazio (Void) e Lista (listz)

Decisão : Simplificação dos operadores lógicos , Maior que (>) Menor que : (<), Igual (==), Diferença (!=), se for escrito numa mesma frase, : Maior ou igual | menor ou igual o compilador junta os dois operadores (+=) (-=)


Os Loops : Equanto "Equivalente ao do Python", para {variavel} em {Iteravel}

Atribuição de varíavel : {Tipo} {variavel} recebe {valor}; Exemplo Linha x recebe "texto aleatorio";

Condicionais: se/senao

Interrupção de codigo (loops): pare

## O que o sistema produz

O sistema ao ser compilado, produz um arquivo executavel, onde nele será a base para executar o programa

Vendo se as sintaxes estão corretas, será executado, caso algo esteja faltado, não será compilado, fazendo com que assim, emita um alerta de erro para o usuário

alfabeto da linguagem : 

Σ={ funcao, pede, retorna, devolve, Classe, Possui, Faz, principal, Linha, Inteiro, Quebrado, Booleano, Vazio, Lista, Dicionario, {, }, (, ), [, ], :, ;, mais, +, menos, -, multiplica, *, dividido-por /, %, recebe, =, igual-a, ==, menor-que, <, maior-que, >, diferente-de, !=, Enquanto, Para, em, se, senao, pare, , }

Classes Lexicas : 

Operadores: {
    +, mais,
    -, menos, 
    *, multiplica,
    /, dividido-por,
    %,
    =, recebe,
    ==, igual-a, 
    <, menor-que, 
    >, maior-que, 
    !=, diferente-de
};
Palavras reservadas: {
    funcao,
    pede,
    retorna,
    devolve,
    Classe,
    Possui,
    Faz,
    principal,
    Linha,
    Inteiro,
    Quebrado,
    Booleano,
    Vazio,
    Lista,
    Dicionario
};
Identificadores: {
    
};
Constantes/Literais: {

};
Delimitadores/Pontuação: {
    {,
    },
    (,
    ),
    [,
    ],
    :,  
    ;
};