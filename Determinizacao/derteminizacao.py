"""
Determinização: transforma o AFN de Thompson (Afn/afn.py) num AFD (afd.py)
pela construção de subconjuntos. Segue as seções 1.5.3 a 1.5.7 do guia
"Implementação em C++: Thompson, determinização e minimização".

A ideia: na simulação do AFN, o que existe a cada passo é um CONJUNTO de
estados ativos. A determinização calcula de antemão todos os conjuntos que a
simulação pode encontrar, e cada um vira UM estado do AFD:

    estado inicial:   q0' = E({q0})            (o fecho vazio do inicial do AFN)
    transição:        δ'(S, a) = E(mover(S, a))
    aceitação:        S é de aceitação quando contém a aceitação do AFN

Dois registros conduzem o laço:
    - o catálogo: associa cada conjunto que já recebeu número ao estado do AFD;
    - os pendentes: os conjuntos do catálogo cujas transições ainda faltam.
      Ficam numa lista usada como pilha (sai o último que entrou), como no
      guia. A ordem não muda a máquina, só a numeração dos estados.

O conjunto vazio não tem caso especial: na primeira vez que aparece, recebe
número como qualquer outro, e vira o estado de erro (não aceita, e todas as
suas setas voltam para ele). Por isso o AFD sai completo.
"""

import os
import sys
from dataclasses import dataclass

from afd import AFD

#O AFN fica na pasta Afn, ao lado desta pasta Determinizacao: a determinização só consome a máquina que a construção de Thompson monta.
#O leitor de padrões vem junto, porque o thompson.py importa a árvore de lá.

PASTA = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(PASTA, "..", "Afn"))
sys.path.append(os.path.join(PASTA, "..", "Leitor_De_Padroes"))
from afn import EPSILON, QUALQUER


@dataclass
class Determinizacao:

    #O resultado da construção: o AFD e, para cada estado dele, o conjunto do AFN que ele representa.
    #conjuntos[0] é o conjunto do estado 0 do AFD, conjuntos[1] o do estado 1, e assim por diante.

    afd: AFD
    conjuntos: list


def alfabeto_do_afn(afn):

    #O alfabeto da determinização (seção 1.5.4 do guia): os símbolos concretos que aparecem nas setas do AFN.
    #ε e o coringa ficam de fora: ε não lê símbolo, e o coringa vira, no AFD, uma seta para cada símbolo deste alfabeto.

    simbolos = set()
    for saidas in afn.transicoes:
        for transicao in saidas:
            if transicao.simbolo not in (EPSILON, QUALQUER):
                simbolos.add(transicao.simbolo)
    return sorted(simbolos)


def chave_do_conjunto(estados):

    #A chave do catálogo: os estados sem repetição e em ordem, numa tupla.
    #Assim [0, 2, 4] e [4, 0, 2] caem na mesma chave. A lista do Python não serve de chave de dicionário; a tupla serve.

    return tuple(sorted(set(estados)))


def contem_final(afn, conjunto):

    #Um conjunto é de aceitação quando contém o estado de aceitação do AFN

    return afn.aceitacao in conjunto


def mover_e_fechar(afn, conjunto, simbolo):

    #A transição do AFD: o movimento pelo símbolo, seguido do fecho vazio (passo 14 do roteiro)

    return afn.fecho_vazio(afn.mover(conjunto, simbolo))


def determinizar(afn):

    if afn.inicial is None or afn.aceitacao is None:
        raise ValueError("Defina o estado inicial e o de aceitação antes de determinizar")

    afd = AFD()
    afd.definir_alfabeto(alfabeto_do_afn(afn))

    #catalogo: chave do conjunto -> número do estado no AFD
    #conjuntos: o caminho inverso, número do estado -> chave do conjunto

    catalogo = {}
    conjuntos = []
    pendentes = []

    def catalogar(conjunto):

        #Dá número a um conjunto novo: cria o estado no AFD, registra nos dois sentidos, coloca nos pendentes e marca a aceitação

        chave = chave_do_conjunto(conjunto)
        estado = afd.novo_estado()
        catalogo[chave] = estado
        conjuntos.append(chave)
        pendentes.append(chave)
        if contem_final(afn, chave):
            afd.adicionar_final(estado)
        return estado

    #1) Estado inicial: o fecho vazio do inicial do AFN (passo 13 do roteiro)

    afd.definir_inicial(catalogar(afn.fecho_vazio([afn.inicial])))

    #2) Laço dos pendentes (passo 15 do roteiro): tira o último que entrou e calcula uma seta para cada símbolo do alfabeto

    while pendentes:
        atual = pendentes.pop()
        origem = catalogo[atual]

        for simbolo in afd.alfabeto:
            destino = chave_do_conjunto(mover_e_fechar(afn, atual, simbolo))

            #Conjunto já catalogado: reaproveita o número. Conjunto novo (inclusive o vazio): ganha número agora.

            if destino in catalogo:
                estado_destino = catalogo[destino]
            else:
                estado_destino = catalogar(destino)

            afd.adicionar_transicao(origem, simbolo, estado_destino)

    #3) Sem pendentes, todos os conjuntos alcançáveis a partir do inicial já tiveram suas setas calculadas

    return Determinizacao(afd, conjuntos)