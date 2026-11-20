"""
Demonstração das três máquinas: o AFN de Thompson, o AFD da determinização e
o AFD mínimo. São os passos 24 e 25 do roteiro do guia "Implementação em
C++: Thompson, determinização e minimização".

Três partes:
  1. os padrões do guia: número de estados antes e depois da minimização, e
     as três máquinas comparadas em todas as cadeias até um comprimento;
  2. a bateria do AFN (Afn/casos_afn.txt): cada caso rodado nas três
     máquinas e comparado com o veredito decidido à mão;
  3. a explosão de estados: "o n-ésimo símbolo contado do fim é a", para n de
     1 a 8.

Como no guia (seções 1.5.4 e 1.7.2), as máquinas só são comparadas em
cadeias sobre o alfabeto do padrão. Fora dele, o AFN e o AFD seguem regras
diferentes (o coringa), e a divergência não indicaria defeito.

Ao terminar, devolve código 1 se alguma verificação falhar e 0 se todas
passarem.
"""

import os
import sys
from itertools import product

from determinizacao import determinizar
from minimizacao import minimizar
from leitor_padroes import ler_padrao
from thompson import construir_thompson
from bateria import ler_casos

#Guarda o resultado de cada verificação, para o placar do fim.
resultados = []


def conferir(descricao, obtido, esperado):
    passou = obtido == esperado
    resultados.append(passou)
    situacao = "OK" if passou else "FALHOU"
    print(f"[{situacao}] {descricao}: obtido {obtido}, esperado {esperado}")


def tres_maquinas(padrao):

    #O caminho inteiro: texto do padrão -> leitor -> Thompson -> determinização -> minimização.
    #Devolve as três máquinas e as contagens de grupos de cada rodada da minimização.

    afn = construir_thompson(ler_padrao(padrao))
    afd = determinizar(afn).afd
    minimizacao = minimizar(afd)
    return afn, afd, minimizacao.afd, minimizacao.contagens


def sobre_o_alfabeto(afd, cadeia):

    #A cadeia só tem símbolos do alfabeto do padrão (seção 1.7.2 do guia)

    return all(simbolo in afd.alfabeto for simbolo in cadeia)


def todas_as_cadeias(alfabeto, comprimento):

    #Todas as cadeias sobre o alfabeto até o comprimento, contada a vazia

    return ["".join(letras) for tamanho in range(comprimento + 1) for letras in product(alfabeto, repeat=tamanho)]


def estados(maquina):
    return maquina.quantidade_de_estados()


#1) Os padrões do guia, com os estados esperados de cada máquina.
#   Thompson: seção 1.8.1. AFD e mínimo: seções 1.7.3 e 1.8.5.

PADROES_DO_GUIA = [
    ("(a|b)*c", (10, 5, 3)),
    ("(a|b)*abb", (14, 5, 4)),
    ("a.c", (6, 5, 5)),
]


def parte1():
    print("--- 1) Os padrões do guia: estados antes e depois da minimização ---\n")

    for padrao, esperado in PADROES_DO_GUIA:
        afn, afd, minimo, contagens = tres_maquinas(padrao)
        print(f"    {padrao}: AFN {estados(afn)} -> AFD {estados(afd)} -> mínimo {estados(minimo)}"
              f"   (grupos por rodada: {contagens})")
        conferir(f"estados de {padrao}", (estados(afn), estados(afd), estados(minimo)), esperado)

        #Seção 1.8.5: entre dois AFDs completos, concordar até o comprimento (estados do AFD + estados do mínimo - 2) garante concordar em todas as cadeias.
        #O AFN entra na mesma comparação; para ele, a concordância é evidência, e a garantia vem da prova da construção de subconjuntos.

        comprimento = estados(afd) + estados(minimo) - 2
        cadeias = todas_as_cadeias(afd.alfabeto, comprimento)
        iguais = all(afn.aceita(c) == afd.aceita(c) == minimo.aceita(c) for c in cadeias)
        conferir(f"as três concordam nas {len(cadeias)} cadeias sobre {afd.alfabeto} até o comprimento {comprimento}",
                 iguais, True)
        print()


def parte2():
    print("\n--- 2) A bateria do AFN nas três máquinas ---\n")

    caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Afn", "casos_afn.txt")
    casos, malformadas = ler_casos(caminho)
    conferir("linhas malformadas na bateria", malformadas, [])

    #As três máquinas de cada padrão são montadas uma vez só, e reaproveitadas pelos casos do mesmo padrão.

    maquinas = {}
    comparados = 0
    ignorados = 0
    print(f"    {'padrão':<32} {'cadeia':<15} {'à mão':<7} {'AFN':<8}{'AFD':<8}mínimo")

    for caso in casos:
        if caso.padrao not in maquinas:
            maquinas[caso.padrao] = tres_maquinas(caso.padrao)
        afn, afd, minimo, _ = maquinas[caso.padrao]

        padrao = caso.padrao if len(caso.padrao) <= 32 else caso.padrao[:29] + "..."
        cadeia = repr(caso.cadeia)

        if not sobre_o_alfabeto(afd, caso.cadeia):
            ignorados += 1
            print(f"    {padrao:<32} {cadeia:<15} fora do alfabeto do padrão: ignorada")
            continue

        comparados += 1
        respostas = [maquina.aceita(caso.cadeia) for maquina in (afn, afd, minimo)]
        texto = "  ".join(f"{'aceita' if r else 'recusa':<5}" for r in respostas)
        mao = "aceita" if caso.esperado else "recusa"
        print(f"    {padrao:<32} {cadeia:<15} {mao:<7} {texto}")

        #Um caso só passa se as três máquinas derem a resposta decidida à mão.

        resultados.append(respostas == [caso.esperado] * 3)
        if respostas != [caso.esperado] * 3:
            print(f"    [FALHOU] {caso.origem}: as máquinas não deram o veredito decidido à mão")

    print()
    conferir("casos da bateria", len(casos), 59)
    print(f"    {comparados} casos comparados nas três máquinas e {ignorados} ignorados por estarem fora do alfabeto.")

    #Os estados de cada padrão da bateria. Estes números são medidos, e não conferidos: não há valor esperado para eles no guia.

    print("\n    Estados de cada padrão da bateria (medidos):")
    print(f"    {'padrão':<52} {'AFN':>5} {'AFD':>5} {'mínimo':>7}")
    for padrao, (afn, afd, minimo, _) in maquinas.items():
        print(f"    {padrao:<52} {estados(afn):>5} {estados(afd):>5} {estados(minimo):>7}")


#3) A explosão de estados: "o n-ésimo símbolo contado do fim é a".
#   O padrão é (a|b)*a seguido de n - 1 cópias de (a|b).
#   Os estados esperados saem das fórmulas do material:
#     Thompson     6n + 4   (a tabela de custos: (a|b)*a dá 10, e cada (a|b) a mais dá 6)
#     AFD          2^n + 1  (o material mede 2^n + 2, contando o estado de erro que ele cria sempre;
#                            aqui o erro só existe se o vazio for alcançável, e o material mostra que,
#                            nesse padrão, nenhum conjunto dá vazio)
#     mínimo       2^n      (o piso que o material prova: 2^n cadeias distinguíveis duas a duas. O
#                            material mede 2^n + 1, que é o piso mais o erro inalcançável; aqui os
#                            inacessíveis são descartados)

COMPRIMENTO_DA_EXPLOSAO = 10


def no_lugar_certo(cadeia, n):

    #A linguagem pela definição, sem máquina nenhuma: a cadeia tem pelo menos n símbolos, e o n-ésimo contado do fim é a

    return len(cadeia) >= n and cadeia[-n] == "a"


def parte3():
    print("\n--- 3) A explosão de estados: o n-ésimo símbolo contado do fim é a ---\n")

    #As três máquinas são comparadas com a própria definição da linguagem, em todas as cadeias sobre {a, b} até o comprimento 10.

    cadeias = todas_as_cadeias("ab", COMPRIMENTO_DA_EXPLOSAO)
    print(f"    {'n':>2} {'AFN':>5} {'AFD':>5} {'mínimo':>7}   piso 2^n")

    for n in range(1, 9):
        padrao = "(a|b)*a" + "(a|b)" * (n - 1)
        afn, afd, minimo, _ = tres_maquinas(padrao)
        print(f"    {n:>2} {estados(afn):>5} {estados(afd):>5} {estados(minimo):>7}   {2 ** n:>8}")

        conferir(f"n = {n}: estados", (estados(afn), estados(afd), estados(minimo)), (6 * n + 4, 2 ** n + 1, 2 ** n))
        iguais = all(afn.aceita(c) == afd.aceita(c) == minimo.aceita(c) == no_lugar_certo(c, n) for c in cadeias)
        conferir(f"n = {n}: as três seguem a definição nas {len(cadeias)} cadeias até o comprimento "
                 f"{COMPRIMENTO_DA_EXPLOSAO}", iguais, True)

    #O AFN cresce 6 estados por n; o AFD dobra. Até n = 5 o AFD ainda é menor que o AFN (33 contra 34); a partir de n = 6, maior.

    print("\n    O AFN cresce em linha reta e o AFD dobra a cada n. O mínimo fica no piso:")
    print("    o crescimento é da linguagem, e nenhum programa o evita.")


def main():
    parte1()
    parte2()
    parte3()

    passaram = sum(resultados)
    print(f"\ndemonstrar_determinizacao: {passaram}/{len(resultados)} verificações passaram.")
    return 0 if passaram == len(resultados) else 1


if __name__ == "__main__":
    sys.exit(main())