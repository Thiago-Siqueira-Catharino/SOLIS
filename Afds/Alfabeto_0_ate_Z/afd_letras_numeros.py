"""
AFD da parte [0-z] do alfabeto da Solis (letras, dígitos e sublinhado).

Padrão reconhecido: [a-zA-Z][a-zA-Z0-9_]* | _+[a-zA-Z0-9][a-zA-Z0-9_]*
    - o primeiro símbolo é obrigatório e precisa ser uma letra ou um _
    - depois dele, zero ou mais letras, dígitos ou _
    - o nome precisa ter pelo menos uma letra ou dígito: _ sozinho (ou ___) não vale
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

#Sublinhado: pode começar o nome e aparecer em qualquer posição, mas não pode ser o nome inteiro
Sublinhado = "_"

def criar_afd_letras_digitos():
    afd = AFD()

    #Alfabeto(Σ): as 52 letras (minúsculo e maiúsculo), os 10 digitos e o _ ao todo são 63 símbolos
    for simbolo in Letras + Digitos + Sublinhado:
        afd.adicionar_simbolo(simbolo)

    #Conjunto de Estados(Q)
        #q0 -> ainda não leu nenhum simbolo
        #q1 -> já leu uma letra ou digito valido, daqui para frente pode colocar outra letra, digito ou _
        #q2 -> até agora só leu _, ainda falta uma letra ou digito para o nome valer
    afd.adicionar_estado("q0")
    afd.adicionar_estado("q1")
    afd.adicionar_estado("q2")

    #Q0 : A leitura começa sem nenhum símbolo lido
    afd.definir_estado_inicial("q0")

    #Conjunto de estados finais(F): Apenas q1 é final, isso faz com que seja obrigatório ter uma letra ou digito, string vazia termina em q0 e é rejeitada, e só _ termina em q2 e também é rejeitado
    afd.adicionar_estado_final("q1")

    #Transição(δ) : na primeira parte a letra ou o _ é obrigatório, de q0 qualquer letra leva a q1 e o _ leva a q2
    for simbolo in Letras:
        afd.adicionar_transicao("q0", simbolo, "q1")
    afd.adicionar_transicao("q0", Sublinhado, "q2")

    #Transição(δ), enquanto só leu _: em q2, outro _ mantém em q2, e uma letra ou digito leva a q1
    afd.adicionar_transicao("q2", Sublinhado, "q2")
    for simbolo in Letras + Digitos:
        afd.adicionar_transicao("q2", simbolo, "q1")
 
    #Transição(δ), na segunda parte vem o fecho (zero ou mais letras, dígitos ou _ depois): em q1, qualquer letra, dígito ou _ mantém em q1
    for simbolo in Letras + Digitos + Sublinhado:
        afd.adicionar_transicao("q1", simbolo, "q1")

    return afd

#Testes, só roda quando este arquivo é executado diretamente

if __name__ == "__main__" :
    afd = criar_afd_letras_digitos()

    #Cada caso tem a palavra e o veredito esperado, decidido à mão pelo padrão [a-zA-Z][a-zA-Z0-9_]* | _+[a-zA-Z0-9][a-zA-Z0-9_]*
    testes = [
        ("resultado", "Aceita"), #varias letras
        ("a", "Aceita"), #Uma letra
        ("resultado2", "Aceita"), #letras com um numero
        ("Ana", "Aceita"), #Nome com letra maiúscula
        ("", "Rejeitada"), #vazio
        ("1a", "Rejeitada"), #O 1 está no alfabeto(Σ), mas não existe transição de q0 com dígito, vai ser rejeitado
        ("123", "Rejeitada"), #Vai ser rejeitado, pois começa com digito e não existe transição de q0 com dígito
        ("meu_nome", "Aceita"), #O (_) está no alfabeto(Σ) e pode aparecer depois da primeira letra
        ("_nome", "Aceita"), #O (_) pode começar o nome, depois vem uma letra
        ("nome_", "Aceita"), #O (_) pode terminar o nome
        ("_1", "Aceita"), #Começa com (_) e depois tem um digito, então tem algo além de _
        ("2_nome", "Rejeitada"), #Vai ser rejeitado, pois começa com digito e não existe transição de q0 com dígito
        ("_", "Rejeitada"), #Só o (_) sozinho não vale como nome, termina em q2 que não é final
        ("___", "Rejeitada"), #Vários (_) sem nenhuma letra ou digito também não valem
    ]

    passaram = 0
    for palavra, esperado in testes:
        obtido = "Aceita" if afd.aceita(palavra) else "Rejeitada"
        situacao = "OK" if obtido == esperado else "FALHOU"
        if obtido == esperado:
            passaram += 1
        print(f"[{situacao}] {palavra!r}: obtido {obtido}, esperado {esperado}")

    #Placar: código de saída 1 se algum caso falhar, para quem roda tudo de uma vez saber
    print(f"AFD de letras e dígitos: {passaram}/{len(testes)} casos passaram.")
    sys.exit(0 if passaram == len(testes) else 1)