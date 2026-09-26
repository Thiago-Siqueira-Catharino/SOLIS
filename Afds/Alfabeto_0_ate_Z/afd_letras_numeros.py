"""
AFD da parte [0-z] do alfabeto da Solis (letras e dígitos).

Padrão reconhecido: [a-zA-Z][a-zA-Z0-9]*
    - o primeiro símbolo é obrigatório e precisa ser uma letra
    - depois dele, zero ou mais letras ou dígitos
"""

import os
import sys

# Estas linhas adicionam essa pasta aos lugares onde o Python procura imports.
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Afd_Solis"))

from afd import AFD

#Simbolos que podem começar
Letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

#Simbolos que podem ser colocados após a primeira letra
Digitos = "0123456789"

def criar_afd_letras_digitos():
    afd = AFD()

    #Alfabeto(Σ): as 52 letras (minúsculo e maiúsculo) e os 10 digitos ao todo são 62 símbolos
    for simbolo in Letras + Digitos:
        afd.adicionar_simbolo(simbolo)

    #Conjunto de Estados(Q)
        #q0 -> ainda não leu nenhum simbolo
        #q1 -> já leu a primeira letra, daqui para frente pode colocar outra letra ou digito
    afd.adicionar_estado("q0")
    afd.adicionar_estado("q1")

    #Q0 : A leitura começa sem nenhum símbolo lido
    afd.definir_estado_inicial("q0")

    #Conjunto de estados finais(F): Apenas q1 é final, isso faz com que seja obrigatório ter uma letra, string vazia termina em q0 e é rejeitada
    afd.adicionar_estado_final("q1")

    #Transição(δ) : na primeira parte a letra é obrigatória, de q0 qualquer letra leva a q1
    for simbolo in Letras:
        afd.adicionar_transicao("q0", simbolo, "q1")
 
    #Transição(δ), na segunda parte vem o fecho (zero ou mais letras ou dígitos depois): em q1, qualquer letra ou dígito mantém em q1
    for simbolo in Letras + Digitos:
        afd.adicionar_transicao("q1", simbolo, "q1")

    return afd

#Testes, só roda quando este arquivo é executado diretamente

if __name__ == "__main__" :
    afd = criar_afd_letras_digitos()

    testes = [
        "resultado", #varias letras
        "a", #Uma letra
        "resultado2", #letras com um numero
        "Ana", #Nome com letra maiúscula
        "", #vazio
        "1a", #O 1 está no alfabeto(Σ), mas não existe transição de q0 com dígito, vai ser rejeitado
        "123", #Vai ser rejeitado, pois começa com digito e não existe transição de q0 com dígito
        "meu_nome", #Vai ser rejeitado, pois o (_) não está no alfabeto(Σ)
    ]

    for palavra in testes:
        resultado = "Aceita" if afd.aceita(palavra) else "Rejeitada"
        print(f"{palavra!r:<14} -> {resultado}")