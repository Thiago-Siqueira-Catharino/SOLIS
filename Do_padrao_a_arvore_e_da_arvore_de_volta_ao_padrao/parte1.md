
---

## Exemplos de Funções matemáticas e seus resultados

| Função     | Parâmetros              | Retorno   | Descrição                     |
|------------|--------------------------|-----------|--------------------------------|
| adicionar  | Quebrado a, Quebrado b   | Quebrado  | Soma dois números decimais     |
| sub        | Quebrado P, Quebrado L   | Quebrado  | Subtrai dois números decimais  |
| mult       | Inteiro a, Inteiro C     | Inteiro   | Multiplica dois inteiros       |
| div        | Inteiro V, Inteiro Q     | Inteiro   | Divide dois inteiros           |

```
funcao adicionar pede (Quebrado a, Quebrado b) e retorna Quebrado {
    Quebrado resultado recebe a mais b;
    devolve resultado;
};

funcao sub pede (Quebrado P, Quebrado L) e retorna Quebrado {
    Quebrado resultado recebe P menos L;
    devolve resultado;
};

funcao mult pede (Inteiro a, Inteiro C) e retorna Inteiro {
    Inteiro resultado recebe a multiplica c;
    devolve resultado;
};

funcao div pede (Inteiro V, Inteiro Q) e retorna Inteiro {
    Inteiro resultado recebe V dividido-por Q;
    devolve resultado;
};
```

---

## Template de função

    funcao <nome_da_funcao> pede (<tipo> <arg>)

---

## Exemplo de lista e de um verificador de Par e Impar

```
Linha Colaboradores recebe lista ['Ana', 'Beatriz', 'Luana'];

Linha A pede 'Digite um número :';

Se A%2 igual-a 0 (
    imprime 'O número é primo';
) senao (
    imprime 'O número é par';
);
```