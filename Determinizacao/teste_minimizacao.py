"""
Teste da minimização (minimizacao.py), passos 18 a 23 do roteiro do guia
"Implementação em C++: Thompson, determinização e minimização".

Os valores esperados saem do guia (o exemplo da seção 1.6.2 e a tabela da
seção 1.6.3, as contagens das seções 1.7.3 e 1.8.5), do material (os
conjuntos 0 e 2 de (a|b)*abb e a partição de um grupo só) ou foram contados à
mão, com a conta escrita ao lado. Nenhum valor esperado foi tirado da execução
deste código.

Ao terminar, devolve código 1 se alguma verificação falhar e 0 se todas
passarem.
"""

import sys
from itertools import product

from afd import AFD
from minimizacao import (minimizar, completar_afd, estados_alcancaveis,
                         particao_inicial, grupo_de, assinatura, refinar_particao)
from determinizacao import determinizar
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

    #O caminho inteiro até o AFD: texto do padrão -> leitor -> Thompson -> determinização

    afn = construir_thompson(ler_padrao(padrao))
    return afn, determinizar(afn).afd


def montar_exemplo_do_guia():

    #O AFD da seção 1.6.2 do guia, com os estados A, B, C, D, E numerados de 0 a 4 e o alfabeto {0, 1}.
    #A é o inicial, D e E são de aceitação.

    exemplo = AFD()
    exemplo.definir_alfabeto("01")
    for _ in range(5):
        exemplo.novo_estado()
    for origem, lendo_0, lendo_1 in [(0, 1, 2), (1, 3, 4), (2, 3, 4), (3, 3, 3), (4, 4, 4)]:
        exemplo.adicionar_transicao(origem, "0", lendo_0)
        exemplo.adicionar_transicao(origem, "1", lendo_1)
    exemplo.definir_inicial(0)
    exemplo.adicionar_final(3)
    exemplo.adicionar_final(4)
    return exemplo


def montar_incompleto():

    #Um AFD escrito à mão, com setas faltando e um estado inacessível, sobre {a, b}:
    #    0 --a--> 1      2 --a--> 1      inicial 0, aceitação 1
    #Nenhuma seta chega no 2, e só a cadeia "a" é aceita.

    incompleto = AFD()
    incompleto.definir_alfabeto("ab")
    for _ in range(3):
        incompleto.novo_estado()
    incompleto.adicionar_transicao(0, "a", 1)
    incompleto.adicionar_transicao(2, "a", 1)
    incompleto.definir_inicial(0)
    incompleto.adicionar_final(1)
    return incompleto


print("--- 1) completar o AFD (passo 18) ---")

#Faltam 4 setas: 0 lendo b, 1 lendo a, 1 lendo b e 2 lendo b. O estado de erro é o 3, e as duas setas dele voltam para ele.

incompleto = montar_incompleto()
erro = completar_afd(incompleto)
conferir("estado de erro criado", erro, 3)
conferir("estados depois de completar", incompleto.quantidade_de_estados(), 4)
conferir("o AFD ficou completo", incompleto.esta_completo(), True)
conferir("setas que foram para o erro", [incompleto.destino(0, "b"), incompleto.destino(1, "a"),
                                         incompleto.destino(1, "b"), incompleto.destino(2, "b")], [3, 3, 3, 3])
conferir("setas do erro", incompleto.transicoes[3], {"a": 3, "b": 3})
conferir("o erro não é de aceitação", incompleto.eh_final(3), False)

#O AFD da determinização já sai completo (seção 1.6.4 do guia): para ele, nada muda.

_, afd_c = montar("(a|b)*c")
conferir("AFD da determinização: nada a completar", completar_afd(afd_c), None)

print("\n--- 2) descartar os estados inacessíveis (passo 19) ---")

#Depois de completar: do 0 se chega ao 1 (lendo a) e ao 3 (lendo b). O 2 fica de fora.

conferir("alcançáveis", estados_alcancaveis(incompleto), {0, 1, 3})

#A minimização trabalha numa cópia: o AFD de entrada continua com 3 estados e incompleto.

original = montar_incompleto()
minimo_incompleto = minimizar(original)
conferir("o AFD de entrada fica intacto", (original.quantidade_de_estados(), original.esta_completo()), (3, False))

#Grupos à mão: partição inicial {0, 3} e {1}. O 0 lendo a vai para o grupo do 1, e o 3 não: os dois se separam.
#Ficam {3}, {0} e {1}: 3 estados, e o 2 não está em nenhum grupo.

conferir("grupos do mínimo", minimo_incompleto.grupos, [[3], [0], [1]])
conferir("o inacessível 2 não está em nenhum grupo",
         any(2 in grupo for grupo in minimo_incompleto.grupos), False)
conferir("o mínimo ainda aceita só a cadeia 'a'",
         [minimo_incompleto.afd.aceita(c) for c in ["a", "", "b", "aa", "ab"]], [True, False, False, False, False])

print("\n--- 3) a partição inicial (passo 20) ---")

#Seção 1.6.2 do guia: P0 = {{A, B, C}, {D, E}}.

exemplo = montar_exemplo_do_guia()
p0 = particao_inicial(exemplo, estados_alcancaveis(exemplo))
conferir("P0 do exemplo do guia", p0, [[0, 1, 2], [3, 4]])

#Material: quando todos os estados aceitam, a partição começa com um grupo só.
#Em a*, os dois estados do AFD aceitam (o inicial aceita a cadeia vazia, e lendo a continua aceitando).

_, afd_a = montar("a*")
conferir("a*: todos aceitam, um grupo só", particao_inicial(afd_a, estados_alcancaveis(afd_a)), [[0, 1]])

print("\n--- 4) assinaturas e a rodada de refinamento (passo 21) ---")

#Seção 1.6.2: contra P0, o A cai com os dois símbolos no grupo {A, B, C} (o 0), e o B e o C caem no {D, E} (o 1).

conferir("grupo do D em P0", grupo_de(p0, 3), 1)
conferir("assinaturas de A, B e C", [assinatura(exemplo, p0, e) for e in (0, 1, 2)], [(0, 0), (1, 1), (1, 1)])

#A primeira rodada separa o A: P1 = {{A}, {B, C}, {D, E}}. A segunda não separa ninguém: P2 = P1.

p1 = refinar_particao(exemplo, p0)
conferir("P1", p1, [[0], [1, 2], [3, 4]])
conferir("P2 é igual a P1", refinar_particao(exemplo, p1), p1)
conferir_erro("estado fora da partição", lambda: grupo_de(p0, 9), "Estado não encontrado na partição: 9")

print("\n--- 5) o ponto fixo (passo 22) ---")

#Seção 1.6.2: a sequência de contagens de grupos é 2, 3, 3.

resultado = minimizar(exemplo)
conferir("contagens de grupos por rodada", resultado.contagens, [2, 3, 3])

#Seção 1.8.4: o refinamento para em no máximo tantas rodadas quanto estados.

conferir("rodadas (2) não passam do número de estados (5)", len(resultado.contagens) - 1 <= 5, True)

print("\n--- 6) a reconstrução do AFD mínimo (passo 23) ---")

#Seção 1.6.3: [A] (inicial) vai a [BC] com os dois símbolos, [BC] vai a [DE], [DE] fica em [DE], e só [DE] aceita.
#Numerados na ordem dos grupos: [A] = 0, [BC] = 1, [DE] = 2.

minimo = resultado.afd
conferir("grupos do ponto fixo", resultado.grupos, [[0], [1, 2], [3, 4]])
conferir("estados: antes e depois", (exemplo.quantidade_de_estados(), minimo.quantidade_de_estados()), (5, 3))
conferir("estado inicial ([A])", minimo.inicial, 0)
conferir("setas do mínimo", minimo.transicoes,
         [{"0": 1, "1": 1}, {"0": 2, "1": 2}, {"0": 2, "1": 2}])
conferir("aceitação (só [DE])", minimo.finais, {2})

print("\n--- 7) os padrões do guia ---")

#Seções 1.8.5 e 1.7.3: estados do AFD e do mínimo.

for padrao, esperado in [("(a|b)*c", (5, 3)), ("(a|b)*abb", (5, 4)), ("a.c", (5, 5))]:
    _, afd = montar(padrao)
    conferir(f"{padrao}: AFD e mínimo", (afd.quantidade_de_estados(), minimizar(afd).afd.quantidade_de_estados()), esperado)

#Material: a minimização junta os conjuntos 0 e 2 de (a|b)*abb, o inicial e o que se alcança lendo b.

_, afd_abb = montar("(a|b)*abb")
conferir("(a|b)*abb: o 0 e o 2 no mesmo grupo",
         any(0 in grupo and 2 in grupo for grupo in minimizar(afd_abb).grupos), True)

#a*: com um grupo só, o mínimo tem um estado, que aceita e volta para ele mesmo lendo a.

minimo_a = minimizar(afd_a)
conferir("a*: o mínimo", (minimo_a.afd.quantidade_de_estados(), minimo_a.afd.finais, minimo_a.afd.transicoes),
         (1, {0}, [{"a": 0}]))

print("\n--- 8) a linguagem é preservada ---")

#Seção 1.8.5: as três máquinas de (a|b)*c, em todas as 121 cadeias sobre {a, b, c} até o comprimento 4, aceitam as mesmas 15.

afn_c, afd_c = montar("(a|b)*c")
minimo_c = minimizar(afd_c).afd

ate_4 = ["".join(letras) for tamanho in range(5) for letras in product("abc", repeat=tamanho)]
aceitas = [[c for c in ate_4 if maquina.aceita(c)] for maquina in (afn_c, afd_c, minimo_c)]
conferir("aceitas por AFN, AFD e mínimo, entre 121", [len(lista) for lista in aceitas], [15, 15, 15])
conferir("as três aceitam as mesmas cadeias", aceitas[0] == aceitas[1] == aceitas[2], True)

#Seção 1.8.5: entre dois AFDs completos, concordar até o comprimento 5 + 3 - 2 = 6 garante concordar em todas as cadeias.
#São (3^7 - 1) / 2 = 1093 cadeias.

ate_6 = ["".join(letras) for tamanho in range(7) for letras in product("abc", repeat=tamanho)]
conferir("cadeias até o comprimento 6", len(ate_6), 1093)
conferir("o AFD e o mínimo concordam em todas",
         all(afd_c.aceita(c) == minimo_c.aceita(c) for c in ate_6), True)

print("\n--- validações ---")

#Um AFD sem estado inicial não tem o que minimizar.

sem_inicial = AFD()
sem_inicial.novo_estado()
conferir_erro("AFD sem inicial", lambda: minimizar(sem_inicial), "Defina o estado inicial antes de minimizar")

#Placar: código de saída 1 se alguma verificação falhar, para quem roda tudo de uma vez saber.
print(f"\nteste_minimizacao: {sum(resultados)}/{len(resultados)} verificações passaram.")
sys.exit(0 if all(resultados) else 1)