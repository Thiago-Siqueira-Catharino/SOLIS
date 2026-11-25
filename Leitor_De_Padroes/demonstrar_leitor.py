"""
Demonstração do leitor de padrões: mostra, com o resultado esperado ao lado
de cada linha.

Quatro partes:
  1. as cinco expressões: forma da árvore e número de nós;
  2. os padrões das classes léxicas: número de nós, inclusive os que usam
     classe negada (Linha, comentário e literal Padrão), lidos com o alfabeto;
  3. a convergência: escritas diferentes que chegam (ou não) à mesma árvore;
  4. as recusas: texto malformado, com a marca ^ na posição do problema.

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
#     Identificador      esquerda: classe de 52 = 103; classe de 63 = 125, + * = 126; + 1 junção = 230
#                        direita: _+ = 4; classe de 62 = 123; 126; + 2 junções                     = 255
#                        230 + 255 + 1 barra                                                       = 486
#     Booleano           verdadeiro 19 + falso 9 + 1 barra                              = 29
#     Delimitador        10 símbolos (o \. conta como um só) + 9 barras                 = 19
#     Palavra reservada  30 palavras com 160 letras: 2x160 - 30 = 290; + 29 barras      = 319
#     Operador           símbolos 27 + palavras 2x109 - 13 = 205 + 27 barras            = 259
#   Os símbolos especiais do leitor (+ * | ( ) [ ]) vão escapados com \.

PALAVRAS_RESERVADAS = ("funcao|pede|retorna|devolve|Classe|Possui|Faz|principal|Linha|Inteiro"
                       "|Quebrado|Booleano|Vazio|Lista|Padrao|Novo|Imprime|imprime"
                       "|enquanto|Enquanto|para|Para|em|Em|se|Se|senao|Senao|pare|Pare")

#O alfabeto da Solis (especificacao/alfabeto.md), grupo por grupo, na ordem da tabela.
#É com ele que a classe negada é lida: [^ab] vira todos estes símbolos, menos a e b.

ALFABETO_DA_SOLIS = (
    list("abcdefghijklmnopqrstuvwxyz")              # letras minúsculas: 26
    + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")            # letras maiúsculas: 26
    + list("0123456789")                            # dígitos: 10
    + list("+-*/%=<>!&|")                           # operadores: 11
    + list("{}()[]:;,")                             # delimitadores: 9
    + ["."]                                         # ponto: 1
    + ["_"]                                         # sublinhado: 1
    + ["'", '"']                                    # aspas: 2
    + ["`"]                                         # crase: 1
    + list("@#$ºª°")                                # símbolos de registro: 6
    + ["?", "\\"]                                   # interrogação e barra invertida: 2
    + [" ", "\t", "\n"]                             # espaço, Tab e quebra de linha: 3
    + list("áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ")              # letras acentuadas: 24
)

#As classes léxicas que usam classe negada. Os nós esperados foram contados à mão:
#     [^'\n]             122 símbolos menos 2 = 120 folhas + 119 alternâncias            = 239
#     Linha              '[^'\n]*' = 239 + 1 fecho + 2 aspas + 2 junções = 244;
#                        "[^"\n]*" também 244; 244 + 244 + 1 barra                       = 489
#     Comentário         [^\n] = 121 folhas + 120 alternâncias = 241;
#                        241 + 1 fecho + 2 símbolos / + 2 junções                        = 246
#     Literal Padrão     igual à Linha de aspas simples, com a crase no lugar da aspa    = 244

PADROES_COM_CLASSE_NEGADA = [
    ("Linha", "'[^'\n]*'|\"[^\"\n]*\"", 489),
    ("Comentário", "//[^\n]*", 246),
    ("Literal Padrão", "`[^`\n]*`", 244),
]

PADROES_DA_SOLIS = [
    ("Inteiro", r"[0-9]+", 40),
    ("Quebrado", r"[0-9]+\.[0-9]+", 83),
    ("Identificador", r"[a-zA-Z][a-zA-Z0-9_]*|_+[a-zA-Z0-9][a-zA-Z0-9_]*", 486),
    ("Booleano", r"verdadeiro|falso", 29),
    ("Delimitador", r"{|}|\(|\)|\[|\]|:|;|,|\.", 19),
    ("Palavra reservada", PALAVRAS_RESERVADAS, 319),
    ("Operador", r"\+|-|\*|/|%|=|==|<|>|>=|<=|!=|&&|\|\||!"
                 r"|mais|menos|multiplica|dividido-por|recebe|igual-a|menor-que|maior-que"
                 r"|maior-ou-igual-a|menor-ou-igual-a|diferente-de|e|ou", 259),
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
    conferir("caracteres escritos (160 letras + 29 barras)", len(PALAVRAS_RESERVADAS), 189)
    conferir("nós da árvore", contar_nos(ler_padrao(PALAVRAS_RESERVADAS)), 319)

    #As classes que usam classe negada precisam do alfabeto: o complemento é "o alfabeto menos a lista".
    print("\n    As classes com classe negada, lidas com o alfabeto da Solis:")
    conferir("símbolos do alfabeto", len(ALFABETO_DA_SOLIS), 122)
    conferir("nós de [^'\\n]", contar_nos(ler_padrao("[^'\n]", ALFABETO_DA_SOLIS)), 239)
    for nome, texto, nos_esperados in PADROES_COM_CLASSE_NEGADA:
        arvore = ler_padrao(texto, ALFABETO_DA_SOLIS)
        #A quebra de linha aparece escrita como \n, como em classes_lexicas.md.
        escrito = texto.replace("\n", "\\n")
        print(f"    {nome}: {exibir(escrito)}")
        conferir(f"nós de {nome}", contar_nos(arvore), nos_esperados)

    #Sem o alfabeto, a classe negada continua recusada: não há como saber o que é "todo o resto".
    try:
        ler_padrao("'[^'\n]*'")
        recusada = False
    except ErroDeLeitura:
        recusada = True
    conferir("sem o alfabeto, a Linha é recusada", recusada, True)

    #Uma classe negada que tira todos os símbolos do alfabeto não sobra nada para casar.
    try:
        ler_padrao("[^ab]", ["a", "b"])
        recusada = False
    except ErroDeLeitura:
        recusada = True
    conferir("[^ab] sobre o alfabeto {a, b} é recusada", recusada, True)


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