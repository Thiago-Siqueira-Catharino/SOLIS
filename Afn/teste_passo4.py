"""
Seis verificações:
  1. os 6 tipos de nó viram máquina, sem nenhum de fora;
  2. o custo de cada peça (estados, setas e setas vazias), contado antes de rodar;
  3. a máquina de (a|b)*c gerada pelo código é IGUAL à montada à mão nos Passos 2 e 3;
  4. o fecho: as quatro cadeias que detectam qualquer seta ε faltando;
  5. as árvores do trabalho "Do padrão à árvore" ([0-9]+ e o Identificador);
  6. o padrão vazio e um tipo de nó desconhecido.
"""

from afn import AFN, EPSILON
from arvore import (No, TipoDeNo, simbolo, qualquer, vazio, concatenacao,
                    alternancia, fecho, contar_nos)
from thompson import construir_thompson


def conferir(descricao, obtido, esperado):
    situacao = "OK" if obtido == esperado else "FALHOU"
    print(f"[{situacao}] {descricao}: obtido {obtido}, esperado {esperado}")


def custo(afn):
    # (estados, setas, setas vazias) de uma máquina
    return (afn.quantidade_de_estados(), afn.quantidade_de_transicoes(),
            afn.quantidade_de_transicoes_vazias())


def setas(afn, estado):
    # As setas que saem de um estado, em ordem, com o ε escrito como "ε"
    return sorted(("ε" if t.simbolo == EPSILON else t.simbolo, t.destino)
                  for t in afn.transicoes[estado])


def classe(caracteres):
    # Monta a alternância de vários símbolos, aninhada pela esquerda,
    # no mesmo formato do D do trabalho anterior: alt(alt(alt('0','1'),'2'),...)
    no = simbolo(caracteres[0])
    for c in caracteres[1:]:
        no = alternancia(no, simbolo(c))
    return no



# 1) Os 6 tipos de nó viram máquina

print("--- 1) os 6 tipos de nó ---")
a, b = simbolo("a"), simbolo("b")
arvores = {
    TipoDeNo.SIMBOLO: a,
    TipoDeNo.QUALQUER: qualquer(),
    TipoDeNo.VAZIO: vazio(),
    TipoDeNo.CONCATENACAO: concatenacao(a, b),
    TipoDeNo.ALTERNANCIA: alternancia(a, b),
    TipoDeNo.FECHO: fecho(a),
}
for tipo in TipoDeNo:
    construida = construir_thompson(arvores[tipo]).quantidade_de_estados() > 0
    conferir(f"{tipo.name} vira máquina", construida, True)


# 2) Custo de cada peça: (estados, setas, setas vazias)
#    folha 2 estados e 1 seta; concat 0 estados e 1 ε; alt 2 e 4 ε; fecho 2 e 4 ε

print("\n--- 2) custo de cada peça ---")
conferir("símbolo a", custo(construir_thompson(a)), (2, 1, 0))
conferir("coringa", custo(construir_thompson(qualquer())), (2, 1, 0))
conferir("vazio", custo(construir_thompson(vazio())), (2, 1, 1))
conferir("ab  = 2+2 estados, 1+1+1 setas", custo(construir_thompson(concatenacao(a, b))), (4, 3, 1))
conferir("a|b = 2+2+2 estados, 1+1+4 setas", custo(construir_thompson(alternancia(a, b))), (6, 6, 4))
conferir("a*  = 2+2 estados, 1+4 setas", custo(construir_thompson(fecho(a))), (4, 5, 4))
conferir("(a|b)*c = 3x2+2+2 estados, 3+4+4+1 setas",
         custo(construir_thompson(concatenacao(fecho(alternancia(a, b)), simbolo("c")))),
         (10, 12, 9))


# 3) (a|b)*c gerada pelo código x montada à mão nos testes dos Passos 2 e 3

print("\n--- 3) máquina gerada x máquina montada à mão ---")
gerada = construir_thompson(concatenacao(fecho(alternancia(a, b)), simbolo("c")))

mao = AFN()
for _ in range(10):
    mao.novo_estado()
mao.adicionar_transicao(0, "a", 1)
mao.adicionar_transicao(2, "b", 3)
mao.adicionar_transicao(4, EPSILON, 0)
mao.adicionar_transicao(4, EPSILON, 2)
mao.adicionar_transicao(1, EPSILON, 5)
mao.adicionar_transicao(3, EPSILON, 5)
mao.adicionar_transicao(6, EPSILON, 4)
mao.adicionar_transicao(6, EPSILON, 7)
mao.adicionar_transicao(5, EPSILON, 4)
mao.adicionar_transicao(5, EPSILON, 7)
mao.adicionar_transicao(8, "c", 9)
mao.adicionar_transicao(7, EPSILON, 8)
mao.definir_inicial(6)
mao.definir_aceitacao(9)

# Compara estado por estado o conjunto de setas que saem dele
for estado in range(10):
    conferir(f"setas do estado {estado}", setas(gerada, estado), setas(mao, estado))
conferir("inicial", gerada.inicial, mao.inicial)
conferir("aceitação", gerada.aceitacao, mao.aceitacao)
conferir("traço de 'abc'",
         [p.ativos for p in gerada.simular("abc").passos],
         [[6, 4, 7, 8, 0, 2], [1, 5, 4, 7, 8, 0, 2], [3, 5, 4, 7, 8, 0, 2], [9]])


# 4) Fecho: a vazia, uma repetição, três repetições e uma que não casa.
#    Depois, a mesma bateria contra máquinas com UMA seta ε faltando.

print("\n--- 4) o fecho e as quatro setas ε ---")
cadeias = ["", "a", "aaa", "b"]
esperado = [True, True, True, False]
f = construir_thompson(fecho(a))
conferir("a* sobre '', 'a', 'aaa', 'b'", [f.aceita(c) for c in cadeias], esperado)

# a*: folha a (0 -> 1), fecho com entrada 2 e saída 3
setas_do_fecho = {
    "uma vez ou mais (2 -> 0)": (2, 0),
    "zero vezes (2 -> 3)": (2, 3),
    "de novo (1 -> 0)": (1, 0),
    "basta (1 -> 3)": (1, 3),
}
for nome, faltando in setas_do_fecho.items():
    quebrada = AFN()
    for _ in range(4):
        quebrada.novo_estado()
    quebrada.adicionar_transicao(0, "a", 1)
    for seta in setas_do_fecho.values():
        if seta != faltando:
            quebrada.adicionar_transicao(seta[0], EPSILON, seta[1])
    quebrada.definir_inicial(2)
    quebrada.definir_aceitacao(3)
    erradas = [repr(c) for c, e in zip(cadeias, esperado) if quebrada.aceita(c) != e]
    conferir(f"sem a seta '{nome}', a bateria acusa", len(erradas) > 0, True)
    print(f"        cadeias que denunciam: {', '.join(erradas)}")


# 5) Árvores do trabalho "Do padrão à árvore"

print("\n--- 5) árvores da Solis ---")
D = classe("0123456789")
inteiro = concatenacao(D, fecho(D))
conferir("nós de [0-9]+", contar_nos(inteiro), 40)
m = construir_thompson(inteiro)
conferir("[0-9]+ sobre '240', '7', '24a', ''",
         [m.aceita(c) for c in ["240", "7", "24a", ""]], [True, True, False, False])

LETRAS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
L = classe(LETRAS)
LD = classe(LETRAS + "0123456789")
identificador = concatenacao(L, fecho(LD))
# 2x52-1 = 103 (L), 2x62-1 = 123 (LD), +1 do fecho, +1 da concatenação
conferir("nós de [a-zA-Z][a-zA-Z0-9]*", contar_nos(identificador), 228)
m = construir_thompson(identificador)
conferir("identificador sobre 'resultado', 'resultado2', 'Ana', '1a', '123', 'meu_nome', ''",
         [m.aceita(c) for c in ["resultado", "resultado2", "Ana", "1a", "123", "meu_nome", ""]],
         [True, True, True, False, False, False, False])


# 6) Padrão vazio e tipo desconhecido

print("\n--- 6) padrão vazio e tipo desconhecido ---")
p = construir_thompson(None)
conferir("padrão vazio: estados", p.quantidade_de_estados(), 1)
conferir("padrão vazio sobre '' e 'a'", [p.aceita(""), p.aceita("a")], [True, False])
try:
    construir_thompson(No("inventado"))
except ValueError as erro:
    print("Erro:", erro)