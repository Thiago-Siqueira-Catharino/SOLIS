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

funcao principal pede (Linha registro) e retorna Booleano {
    Quebrado x recebe 3.14;
    Inteiro y recebe 2;
    Matematica mat recebe Novo Matematica;

    Imprime(soma(x,y));
    Imprime(mat.multiplicar(x,y));

    Padrao numero recebe `[0-9]+`;
    devolve numero.casa(registro);
};