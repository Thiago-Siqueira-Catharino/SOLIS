"""
Demonstração do leitor de padrões: mostra, com o resultado esperado ao lado
de cada linha, que o leitor cumpre as tarefas do módulo
"Expressões Regulares e Linguagens Regulares".

Quatro partes, na mesma ordem da seção 1.8 do material do professor:
  1. as cinco expressões do material: forma da árvore e número de nós;
  2. os padrões das classes léxicas da Solis: número de nós;
  3. a convergência: escritas diferentes que chegam (ou não) à mesma árvore;
  4. as recusas: texto malformado, com a marca ^ na posição do problema.

Todo valor esperado foi decidido ANTES de rodar: os da parte 1 vêm impressos
no material; os da parte 2 foram contados à mão, pela tabela de nós do
material (seção 1.8.3); os das partes 3 e 4 vêm do material e do trabalho
"Do padrão à árvore". Um valor copiado da própria saída do programa
conferiria o programa com ele mesmo.

Ao terminar, devolve código 1 se alguma verificação falhar e 0 se todas
passarem.
"""

import sys

from arvore import forma_linear, contar_nos
from leitor_padroes import ler_padrao, ErroDeLeitura, mostrar_erro

#Formas muito longas são cortadas na tela, como no material.
LIMITE_DE_EXIBICAO = 96

resultados = []


def conferir(descricao, obtido, esperado):
    passou = obtido == esperado
    resultados.append(passou)
    situacao = "OK" if passou else "FALHOU"
    print(f"[{situacao}] {descricao}: obtido {obtido}, esperado {esperado}")


def exibir(forma):
    if len(forma) <= LIMITE_DE_EXIBICAO:
        return forma
    return forma[:LIMITE_DE_EXIBICAO] + " ... (truncado para exibição)"


#1) As cinco expressões do material (seção 1.4), da menor para a maior.
#   A forma esperada é o texto do material, caractere por caractere.

EXPRESSOES_DO_MATERIAL = [
    ("a", "'a'", 1),
    ("ab", "concat('a', 'b')", 3),
    ("a|bc", "alt('a', concat('b', 'c'))", 5),
    ("(a|b)*c", "concat(fecho(alt('a', 'b')), 'c')", 6),
    ("(ab|c)*d[0-2]?",
     "concat(concat(fecho(alt(concat('a', 'b'), 'c')), 'd'), alt(alt(alt('0', '1'), '2'), vazio))", 16),
]

#2) Os padrões das classes léxicas da Solis (especificacao/classes_lexicas.md).
#   Os nós esperados foram contados à mão:
#     Inteiro            [0-9] = 19; o + repete e soma 2         -> 19 + 19 + 2         = 40
#     Quebrado           40 + 1 (o \.) + 40 + 2 junções                                 = 83
#     Identificador      classe de 53 = 105; classe de 63 = 125, + * = 126; + 1 junção = 232
#     Booleano           verdadeiro 19 + falso 9 + 1 barra                              = 29
#     Delimitador        9 símbolos + 8 barras                                          = 17
#     Palavra reservada  21 palavras com 121 letras: 2x121 - 21 = 221; + 20 barras      = 241
#     Operador           símbolos 21 + palavras 2x77 - 11 = 143 + 23 barras             = 187
#   Os símbolos especiais do leitor (+ * | ( ) [ ]) vão escapados com \.

PALAVRAS_RESERVADAS = ("funcao|pede|retorna|devolve|Classe|Possui|Faz|principal|Linha|Inteiro"
                       "|Quebrado|Booleano|Vazio|Lista|Dicionario|enquanto|para|em|se|senao|pare")

PADROES_DA_SOLIS = [
    ("Inteiro", r"[0-9]+", 40),
    ("Quebrado", r"[0-9]+\.[0-9]+", 83),
    ("Identificador", r"[a-zA-Z_][a-zA-Z0-9_]*", 232),
    ("Booleano", r"verdadeiro|falso", 29),
    ("Delimitador", r"{|}|\(|\)|\[|\]|:|;|,", 17),
    ("Palavra reservada", PALAVRAS_RESERVADAS, 241),
    ("Operador", r"\+|-|\*|/|%|=|==|<|>|!=|&&|\|\||!"
                 r"|mais|menos|multiplica|dividido-por|recebe|igual-a|menor-que|maior-que|diferente-de|e|ou", 187),
]

#3) Pares de escritas. Os quatro primeiros são do material (seção 1.8);
#   os dois últimos, do trabalho "Do padrão à árvore" (seções 3 e 4).

PARES = [
    ("a+", "aa*", "mesma árvore"),
    ("[abc]", "a|b|c", "mesma árvore"),
    ("[a-c]", "[abc]", "mesma árvore"),
    ("(ab)c", "abc", "mesma árvore"),
    ("[0-9]+", "[0-9][0-9]*", "mesma árvore"),
    ("[a-z0-9]", "([a-z]|[0-9])", "árvores diferentes"),
]

#4) Textos malformados: (texto, posição constatada, origem), contadas a partir de 1.
#   Os quatro primeiros são os do material, que conta a partir de 0: por isso
#   cada posição aqui é a do material mais 1. Os quatro últimos são os do
#   trabalho "Do padrão à árvore"; lá a posição registrada é a origem.

RECUSAS = [
    ("a(b|c", 6, 2),
    ("*ab", 1, None),
    ("[a-z", 5, 1),
    ("ab)c", 3, None),
    ("([a-z]|[0-9]", 13, 1),
    ("*[0-9]", 1, None),
    ("[0-9+", 6, 1),
    ("[0-9]+)", 7, None),
]


def parte1():
    print("--- 1) As cinco expressões do material ---\n")
    for texto, forma_esperada, nos_esperados in EXPRESSOES_DO_MATERIAL:
        arvore = ler_padrao(texto)
        print(f"    {texto}")
        print(f"    -> {forma_linear(arvore)}")
        conferir("forma igual à do material", forma_linear(arvore) == forma_esperada, True)
        conferir("nós", contar_nos(arvore), nos_esperados)
        print()

    #A conferência do açúcar do quinto exemplo, como no material.
    conferir("[0-2] e 0|1|2 dão a mesma árvore", ler_padrao("[0-2]") == ler_padrao("0|1|2"), True)


def parte2():
    print("\n--- 2) Os padrões das classes léxicas da Solis ---\n")
    for nome, texto, nos_esperados in PADROES_DA_SOLIS:
        arvore = ler_padrao(texto)
        print(f"    {nome}: {exibir(texto)}")
        print(f"    -> {exibir(forma_linear(arvore))}")
        conferir(f"nós de {nome}", contar_nos(arvore), nos_esperados)
        print()

    #O padrão mais longo do projeto: caracteres escritos e nós, lado a lado
    #(a conta que o material pede no fim da seção 1.8).
    print("    O padrão mais longo é o das palavras reservadas:")
    conferir("caracteres escritos (121 letras + 20 barras)", len(PALAVRAS_RESERVADAS), 141)
    conferir("nós da árvore", contar_nos(ler_padrao(PALAVRAS_RESERVADAS)), 241)

    #Limite conhecido: a Linha usa classe negada, que o leitor não aceita.
    linha = "'[^'\n]*'"
    print("\n    Linha: '[^'\\n]*'  (limite conhecido: usa classe negada)")
    try:
        ler_padrao(linha)
        recusada = False
    except ErroDeLeitura:
        recusada = True
    conferir("a Linha é recusada pelo leitor", recusada, True)


def parte3():
    print("\n--- 3) Convergência de escritas diferentes ---\n")
    for primeira, segunda, esperado in PARES:
        arvore1 = ler_padrao(primeira)
        arvore2 = ler_padrao(segunda)
        obtido = "mesma árvore" if arvore1 == arvore2 else "árvores diferentes"
        conferir(f"{primeira}  vs  {segunda}", obtido, esperado)

    #O par que não converge tem o mesmo tamanho: 71 nós dos dois lados.
    conferir("nós de [a-z0-9] e de ([a-z]|[0-9])",
             (contar_nos(ler_padrao("[a-z0-9]")), contar_nos(ler_padrao("([a-z]|[0-9])"))), (71, 71))


def parte4():
    print("\n--- 4) Expressões malformadas, recusadas com a posição do problema ---\n")
    for texto, posicao_esperada, origem_esperada in RECUSAS:
        try:
            ler_padrao(texto)
            conferir(f"{texto} é recusado", False, True)
        except ErroDeLeitura as erro:
            for linha in mostrar_erro(texto, erro).splitlines():
                print(f"    {linha}")
            conferir("(posição, origem)", (erro.posicao, erro.origem), (posicao_esperada, origem_esperada))
        print()


def main():
    parte1()
    parte2()
    parte3()
    parte4()

    passaram = sum(resultados)
    print(f"Leitor de padrões: {passaram}/{len(resultados)} verificações passaram.")
    return 0 if passaram == len(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())