"""
Construção de Thompson: transforma a árvore de um padrão (arvore.py) numa
máquina não determinística (afn.py).

Cada tipo de nó tem uma regra, e a regra de um operador chama a mesma
função para os filhos. Toda regra devolve um BLOCO com exatamente uma
entrada e uma saída: essa interface uniforme deixa juntar blocos sem
olhar dentro deles.

Custo de cada peça:
    - folha:         2 estados, 1 seta
    - concatenação:  0 estados, 1 seta ε
    - alternância:   2 estados, 4 setas ε
    - fecho:         2 estados, 4 setas ε
"""

import os
import sys
from dataclasses import dataclass

from afn import AFN, EPSILON, QUALQUER

#A árvore fica na pasta Leitor_De_Padroes, ao lado desta pasta Afn: o leitor
#de padrões é a peça anterior, e o AFN só consome a árvore que ele monta.
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Leitor_De_Padroes"))
from arvore import TipoDeNo


@dataclass(frozen=True)
class Bloco:

    #Um pedaço de máquina: o estado por onde se entra e o estado por onde se sai.

    entrada: int
    saida: int


def _construir(no, afn):

    #Monta, dentro de "afn", o bloco do nó, e devolve a entrada e a saída dele.
    #Os filhos são sempre construídos ANTES dos estados do próprio nó: é isso
    #que define a numeração dos estados.

    #1) Folhas: dois estados e uma seta. Os três tipos só mudam o rótulo.
    if no.tipo in (TipoDeNo.SIMBOLO, TipoDeNo.QUALQUER, TipoDeNo.VAZIO):
        entrada = afn.novo_estado()
        saida = afn.novo_estado()
        if no.tipo == TipoDeNo.SIMBOLO:
            rotulo = no.simbolo
        elif no.tipo == TipoDeNo.QUALQUER:
            rotulo = QUALQUER
        else:
            rotulo = EPSILON
        afn.adicionar_transicao(entrada, rotulo, saida)
        return Bloco(entrada, saida)

    #2) Concatenação: a saída do primeiro alimenta a entrada do segundo por ε.
    #Não funde os dois estados: fundir exigiria olhar dentro dos blocos.
    if no.tipo == TipoDeNo.CONCATENACAO:
        esquerdo = _construir(no.esquerda, afn)
        direito = _construir(no.direita, afn)
        afn.adicionar_transicao(esquerdo.saida, EPSILON, direito.entrada)
        return Bloco(esquerdo.entrada, direito.saida)

    #3) Alternância: entrada nova que leva aos dois blocos, saída nova que recebe dos dois.
    if no.tipo == TipoDeNo.ALTERNANCIA:
        esquerdo = _construir(no.esquerda, afn)
        direito = _construir(no.direita, afn)
        entrada = afn.novo_estado()
        saida = afn.novo_estado()
        afn.adicionar_transicao(entrada, EPSILON, esquerdo.entrada)
        afn.adicionar_transicao(entrada, EPSILON, direito.entrada)
        afn.adicionar_transicao(esquerdo.saida, EPSILON, saida)
        afn.adicionar_transicao(direito.saida, EPSILON, saida)
        return Bloco(entrada, saida)

    #4) Fecho: quatro setas ε, cada uma é uma frase da definição.
    if no.tipo == TipoDeNo.FECHO:
        interior = _construir(no.esquerda, afn)
        entrada = afn.novo_estado()
        saida = afn.novo_estado()
        afn.adicionar_transicao(entrada, EPSILON, interior.entrada)        # uma vez ou mais
        afn.adicionar_transicao(entrada, EPSILON, saida)                   # zero vezes
        afn.adicionar_transicao(interior.saida, EPSILON, interior.entrada) # de novo
        afn.adicionar_transicao(interior.saida, EPSILON, saida)            # basta
        return Bloco(entrada, saida)

    #Nenhum tipo pode ficar de fora. O Python não avisa sobre um tipo esquecido,
    #então um tipo desconhecido para tudo aqui, em vez de falhar em silêncio.
    raise ValueError(f"Tipo de nó desconhecido: {no.tipo}")


def construir_thompson(raiz):

    #Constrói a máquina inteira a partir da raiz da árvore.

    afn = AFN()

    #Padrão vazio (sem árvore): um estado só, que é inicial e aceitação.
    #A máquina aceita apenas a cadeia vazia.
    if raiz is None:
        unico = afn.novo_estado()
        afn.definir_inicial(unico)
        afn.definir_aceitacao(unico)
        return afn

    #A máquina inteira é um bloco: a entrada dele é o inicial e a saída é a aceitação.
    bloco = _construir(raiz, afn)
    afn.definir_inicial(bloco.entrada)
    afn.definir_aceitacao(bloco.saida)
    return afn