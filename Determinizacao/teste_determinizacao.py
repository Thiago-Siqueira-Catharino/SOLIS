"""
Teste da determinização (determinizacao.py), passos 12 a 17 do roteiro do guia
"Implementação em C++: Thompson, determinização e minimização".

Os valores esperados saem do guia: a tabela de (a|b)*c (seção 1.5.6), as
cadeias da seção 1.5.9, as contagens da seção 1.7.3 e a bateria da seção
1.8.5. Nenhum valor esperado foi tirado da execução deste código.

Ao terminar, devolve código 1 se alguma verificação falhar e 0 se todas
passarem.
"""

import sys
from itertools import product

from determinizacao import (determinizar, alfabeto_do_afn, chave_do_conjunto,
                            mover_e_fechar)
from afn import AFN
from leitor_padroes import ler_padrao
from thompson import construir_thompson

#Guarda o resultado de cada verificação, para o placar do fim.
resultados = []


def conferir(descricao, obtido, esperado):
    situacao = "OK" if obtido == esperado else "FALHOU"
    resultados.append(obtido == esperado)
    print(f"[{situacao}] {descricao}: obtido {obtido}, esperado {esperado}")


def conferir_erro(descricao, acao, mensagem_esperada):

    #Verifica um erro proposital: passa se a ação gerar exatamente esse erro.
    #Se a ação não gerar erro nenhum, ou gerar outro, a verificação falha.

    try:
        acao()
        obtido = "nenhum erro"
    except ValueError as erro:
        obtido = str(erro)
    passou = obtido == mensagem_esperada
    resultados.append(passou)
    if passou:
        print(f"[OK] erro esperado ({descricao}): {obtido}")
    else:
        print(f"[FALHOU] erro esperado ({descricao}): obtido {obtido}, esperado {mensagem_esperada}")


def montar(padrao):

    #O caminho inteiro até o AFN: texto do padrão -> leitor -> Thompson

    return construir_thompson(ler_padrao(padrao))


def mostrar(resultado):

    #Mostra a tabela do AFD como a do guia: estado, conjunto do AFN, setas e aceitação. O conjunto vazio aparece como ∅.

    afd = resultado.afd
    for estado, conjunto in enumerate(resultado.conjuntos):
        texto = "{" + ", ".join(str(e) for e in conjunto) + "}" if conjunto else "∅"
        setas = "  ".join(f"{simbolo}->D{afd.transicoes[estado][simbolo]}" for simbolo in afd.alfabeto)
        nome = f"D{estado} (inicial)" if estado == afd.inicial else f"D{estado}"
        aceita = "Sim" if afd.eh_final(estado) else "Não"
        print(f"    {nome:<13} {texto:<24} {setas}   aceita? {aceita}")


afn = montar("(a|b)*c")
resultado = determinizar(afn)
afd = resultado.afd

print("--- a tabela do AFD de (a|b)*c ---")
mostrar(resultado)

print("\n--- 1) o catálogo: a chave de um conjunto (passo 12) ---")

#A mesma coleção de estados, em ordens diferentes e com repetição, precisa cair na mesma chave.

conferir("chave de [4, 0, 2, 2]", chave_do_conjunto([4, 0, 2, 2]), (0, 2, 4))
conferir("[0, 2, 4] e [4, 0, 2] caem na mesma chave",
         chave_do_conjunto([0, 2, 4]) == chave_do_conjunto([4, 0, 2]), True)
conferir("chave do conjunto vazio", chave_do_conjunto([]), ())

print("\n--- 2) o alfabeto da determinização (seção 1.5.4) ---")

#Os símbolos das setas, sem ε e sem coringa. Em a.c o coringa fica de fora: o alfabeto é {a, c}.

conferir("alfabeto de (a|b)*c", alfabeto_do_afn(afn), ["a", "b", "c"])
conferir("alfabeto de a.c", alfabeto_do_afn(montar("a.c")), ["a", "c"])

print("\n--- 3) o estado inicial (passo 13) ---")

#O inicial é o fecho vazio do inicial do AFN: em (a|b)*c, seis estados, e não só o estado 6.

conferir("estado inicial do AFD", afd.inicial, 0)
conferir("conjunto do estado inicial", resultado.conjuntos[0], (0, 2, 4, 6, 7, 8))
conferir("o inicial não é de aceitação", afd.eh_final(0), False)

print("\n--- 4) movimento seguido de fecho (passo 14) ---")

#Os destinos de D0 na tabela da seção 1.5.6: lendo a vai a D1, lendo c vai a D3. De D3 = {9}, qualquer símbolo leva ao vazio.

conferir("D0 lendo a", chave_do_conjunto(mover_e_fechar(afn, (0, 2, 4, 6, 7, 8), "a")), (0, 1, 2, 4, 5, 7, 8))
conferir("D0 lendo c", chave_do_conjunto(mover_e_fechar(afn, (0, 2, 4, 6, 7, 8), "c")), (9,))
conferir("{9} lendo a", chave_do_conjunto(mover_e_fechar(afn, (9,), "a")), ())

print("\n--- 5) o laço dos pendentes: a tabela da seção 1.5.6 (passo 15) ---")

#A tabela inteira do guia: os cinco conjuntos, na ordem em que entram no catálogo, e as setas de cada um.

conferir("estados do AFD", afd.quantidade_de_estados(), 5)
conferir("conjuntos D0 a D4", resultado.conjuntos,
         [(0, 2, 4, 6, 7, 8), (0, 1, 2, 4, 5, 7, 8), (0, 2, 3, 4, 5, 7, 8), (9,), ()])
conferir("setas de D0, D1 e D2", [afd.transicoes[e] for e in (0, 1, 2)],
         [{"a": 1, "b": 2, "c": 3}] * 3)
conferir("setas de D3 e D4", [afd.transicoes[e] for e in (3, 4)],
         [{"a": 4, "b": 4, "c": 4}] * 2)
conferir("estados de aceitação (só o D3, que contém o 9)", afd.finais, {3})

#As verificações da seção 1.8.3 do guia que não estão na tabela acima.
#Um destino só por par (estado, símbolo): cada seta aponta para um número de estado, e não para uma lista.

conferir("um destino só por estado e símbolo",
         all(isinstance(destino, int) for saidas in afd.transicoes for destino in saidas.values()), True)

#Nenhuma seta com ε nem com coringa: todo símbolo das setas está no alfabeto, que não tem nenhum dos dois.

conferir("nenhuma seta fora do alfabeto (sem ε e sem coringa)",
         all(simbolo in afd.alfabeto for saidas in afd.transicoes for simbolo in saidas), True)

#Todos os conjuntos processados: se algum tivesse ficado nos pendentes, teria estado sem setas, e o AFD não sairia completo.

conferir("AFD completo (todos os conjuntos processados)", afd.esta_completo(), True)

print("\n--- 6) o conjunto vazio aparece quando é alcançável (passo 16) ---")

#Em (a|b)*c, o vazio é o D4: não aceita, e todas as setas dele voltam para ele mesmo.

conferir("D4 é o conjunto vazio", resultado.conjuntos[4], ())
conferir("D4 não é de aceitação", afd.eh_final(4), False)

#Seção 1.7.3: em a.c, o vazio é alcançável (de {0}, lendo c), e o AFD tem 5 estados.

resultado_ac = determinizar(montar("a.c"))
conferir("a.c: o vazio está entre os conjuntos", () in resultado_ac.conjuntos, True)
conferir("a.c: estados do AFD", resultado_ac.afd.quantidade_de_estados(), 5)

#Seção 1.7.3: em (a|b)*abb, nenhuma cadeia leva ao vazio, e ele nunca é criado: 5 estados, contra 6 do material.

resultado_abb = determinizar(montar("(a|b)*abb"))
conferir("(a|b)*abb: o vazio não está entre os conjuntos", () in resultado_abb.conjuntos, False)
conferir("(a|b)*abb: estados do AFD", resultado_abb.afd.quantidade_de_estados(), 5)

print("\n--- 7) a equivalência entre o AFN e o AFD, sobre o alfabeto (passo 17) ---")

#As sete cadeias da seção 1.5.9: a resposta do guia, e as duas máquinas dando essa resposta.

for cadeia, esperado in [("c", True), ("ac", True), ("bc", True), ("abc", True),
                         ("abababc", True), ("ab", False), ("ca", False)]:
    conferir(f"{cadeia!r} no AFN e no AFD", (afn.aceita(cadeia), afd.aceita(cadeia)), (esperado, esperado))

#A bateria da seção 1.8.5: todas as cadeias sobre {a, b, c} até o comprimento 4.
#São 1 + 3 + 9 + 27 + 81 = 121 cadeias; o guia diz que as máquinas aceitam as mesmas 15 e rejeitam as mesmas 106.

cadeias = ["".join(letras) for tamanho in range(5) for letras in product(afd.alfabeto, repeat=tamanho)]
aceitas_afn = [c for c in cadeias if afn.aceita(c)]
aceitas_afd = [c for c in cadeias if afd.aceita(c)]

conferir("cadeias da bateria", len(cadeias), 121)
conferir("aceitas pelo AFN", len(aceitas_afn), 15)
conferir("aceitas pelo AFD", len(aceitas_afd), 15)
conferir("rejeitadas pelo AFD", len(cadeias) - len(aceitas_afd), 106)
conferir("o AFN e o AFD aceitam exatamente as mesmas cadeias", aceitas_afn == aceitas_afd, True)

#Fora do alfabeto, cada máquina segue a sua regra (seção 1.5.4): em a.c, o AFN aceita abc pelo coringa, e o AFD, sem seta para b, rejeita.
#Não é defeito, e por isso a comparação só usa cadeias sobre o alfabeto.

conferir("a.c com 'abc' (fora do alfabeto): AFN e AFD",
         (montar("a.c").aceita("abc"), resultado_ac.afd.aceita("abc")), (True, False))

print("\n--- validações ---")

#Um AFN sem estado inicial não tem o que determinizar.

incompleto = AFN()
incompleto.novo_estado()
conferir_erro("AFN sem inicial", lambda: determinizar(incompleto),
              "Defina o estado inicial e o de aceitação antes de determinizar")

#Placar: código de saída 1 se alguma verificação falhar, para quem roda tudo de uma vez saber.
print(f"\nteste_determinizacao: {sum(resultados)}/{len(resultados)} verificações passaram.")
sys.exit(0 if all(resultados) else 1)