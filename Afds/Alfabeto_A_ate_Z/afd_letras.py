"""
AFD da parte [a-z] do alfabeto da Solis.
 
Padrão reconhecido: [a-z]+  (uma ou mais letras minúsculas)
 
"""

import os
import sys

# Estas linhas adicionam essa pasta aos lugares onde o Python procura imports.
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Afd_Solis"))

from afd import AFD

Letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def criar_afd_letras():
    afd = AFD()

    #Alfabeto(Σ) as 52 letras do alfabeto (minúsculas/maiúsculas)

    for simbolo in Letras:
        afd.adicionar_simbolo(simbolo)

    #Conjunto de Estados(Q)
        #q0 -> ainda não leu nenhuma letra
        #q1 -> já leu pelo menos uma letra
    afd.adicionar_estado("q0")
    afd.adicionar_estado("q1")

    #Q0: A leitura começa sem nenhuma letra lida
    afd.definir_estado_inicial("q0")

    #Conjunto de estados finais(F): Só o q1 é final, isso obriga a ter pelo menos uma letra, a string vazia termina em q0 e é rejeitada

    afd.adicionar_estado_final("q1")

    #Transição(δ), na primeira parte a letra é obrigatória, de q0 qualquer letra leva a q1
    for simbolo in Letras:
        afd.adicionar_transicao("q0", simbolo, "q1")

    #Transição(δ), na segunda parte vem o fecho, (zero ou mais letras depois), em q1, qualquer letra mantém em q1

    for simbolo in Letras:
        afd.adicionar_transicao("q1", simbolo, "q1")

    return afd

#Testes, só roda quando este arquivo é executado diretamente

if __name__ == "__main__" :
    afd = criar_afd_letras()

    testes = [
        "abacate", #varias letras
        "a", #Uma letra
        "", #vazio, recusa pois precisa de uma letra obrigatoriamente
        "a1", #O número 1 não está nesse alfabeto(Σ)
        "ana@", #O caracter @ não está no alfabeto(Σ)
        "Ana", #A letra A em maiúsculo está no alfabeto
    ]

    for palavra in testes:
        resultado = "Aceita" if afd.aceita(palavra) else "Rejeitada"
        print(f"{palavra!r:<10} -> {resultado}")