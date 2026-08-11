funcao soma pede (a,b) e retorna Quebrado {
    devolve a + b;
};

Classe Matematica {
    Possui {

    };
    Faz {
            funcao soma pede (a,b) e retorna Quebrado {
                devolve a + b;
            };

            funcao multiplicar pede (a,b) e retorna Quebrado {
                devolve a * b;
            };
    };
}

funcao principal pede () e retorna Vazio {
    Quebrado x recebe 3.14;
    Inteiro y recebe 2;
    Matematica mat recebe Novo Matematica;

    Imprime(soma(x,y));
    Imprime(mat.multiplicar(x,y));

    devolve Vazio;
};