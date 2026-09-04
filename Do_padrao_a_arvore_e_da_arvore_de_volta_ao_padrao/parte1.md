fazer backup usuários setor_atendimento as 19:00 até as 23:00

funcao adicionar pede (Quebrado a, Quebrado b) e retorna Quebrado {
    Quebrado resultado recebe a mais b;
    devolve resultado;
};

funcao <nome_da_funcao> pede (<tipo> <arg>)

funcao mult pede (Inteiro a, Inteiro C) e retorna Inteiro {
    Inteiro resultado recebe a multiplica c;
    devolve resultado;
};

funcao sub pede (Quebrado P, Quebrado L) e retorna Quebrado {
    Quebrado resultado recebe P menos L;
    devolve resultado; 
};

funcao div pede (Inteiro V, Inteiro Q) e retorna Inteiro {
    Inteiro resultado recebe V dividido-por Q;
    devolve resultado;
};

Linha Colaboradores recebe lista ['Ana', 'Beatriz', 'Luana'];

Linha A pede 'Digite um número :';

Se A%2 igual-a 0 (
    imprime 'O número é primo';
);senao(
    imprime 'O número é par';
);