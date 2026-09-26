"""
AFD da parte [0-9] do alfabeto da Solis.
 
"""

import os
import sys

# Estas linhas adicionam essa pasta aos lugares onde o Python procura imports.
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Afd_Solis"))

from afd import AFD

#Abaixo estão os símbolos númericos desta parte do alfabeto

Digitos = "0123456789"

def criar_afd_digitos():
    afd = AFD()

    #O alfabeto(Σ) aqui são os 10 digitos
    for simbolo in Digitos:
        afd.adicionar_simbolo(simbolo)

    #Conjunto de estados(Q)
        #q0 -> ainda não leu nenhum dígito
        #q1 -> já leu pelo menos um dígito
    afd.adicionar_estado("q0")
    afd.adicionar_estado("q1")

    #Q0: A leitura começa sem nenhum dígito lido
    afd.definir_estado_inicial("q0")

    #Conjunto de Estados finais (F) : Apenas o Q1 é final. Isso obriga a pelo menos ter um dígito, a string vazia termina em Q0 e é rejeitada
    afd.adicionar_estado_final("q1")

    #Transição(δ), a primeira parte exige que tenha um dígito, de q0, qualquer dígito vai levar a q1

    for simbolo in Digitos:
        afd.adicionar_transicao("q0", simbolo, "q1")

    #Transicao(δ): fecho(D), (zero ou mais dígitos depois), em q1 qualquer dígito mantém em q1

    for simbolo in Digitos:
        afd.adicionar_transicao("q1", simbolo, "q1")
    return afd

#Testes: roda apenas quando este arquivo é executado diretamente

if __name__ == "__main__":
    afd = criar_afd_digitos()

    testes = [
        "42", #varios digitos -> deve aceitar
        "7", #um dígito -> deve aceitar
        "", #vazio -> deve rejeitar (precisa de um digito obrigatório)
        "4a", #a não está neste alfabeto(Σ) -> deve rejeitar
        "-5", #Sinal de menos(-) não está neste alfabeto(Σ)
        "4.5", #Ponto(.) não está neste alfabeto -> deve rejeitar
    ]

    for palavra in testes:
        resultado = "Aceita" if afd.aceita(palavra) else "Rejeitada"
        print(f"{palavra!r:<8} -> {resultado}")
