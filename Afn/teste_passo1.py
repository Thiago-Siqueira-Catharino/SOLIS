import sys

from afn import AFN, EPSILON

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


def mostrar(afn):

    #Mostra a listra de setas de cada estado, trocando o caractere de ε por "ε".

    for estado, saidas in enumerate(afn.transicoes):
        setas = ", ".join(f"({'ε' if t.simbolo == EPSILON else t.simbolo!r} -> {t.destino})" for t in saidas)
        print(f"estado {estado}: [{setas}]")

afn = AFN()

#Q: três estados, cada chamada devolve o número do estado criado

e0 = afn.novo_estado()
e1 = afn.novo_estado()
e2 = afn.novo_estado()
conferir("estados criados", (e0, e1, e2), (0, 1, 2))

# δ: as três setas do desenho

afn.adicionar_transicao(e0, "a", e0)
afn.adicionar_transicao(e0, EPSILON, e1)
afn.adicionar_transicao(e1, "b", e2)

afn.definir_inicial(e0)
afn.definir_aceitacao(e2)

print("\n--- a máquina por dentro ---")
mostrar(afn)

print("\n--- contagens ---")

#Os valores esperados saem do desenho: 3 estados, 3 setas, 1 delas vazia.
conferir("estados", afn.quantidade_de_estados(), 3)
conferir("transições", afn.quantidade_de_transicoes(), 3)
conferir("transições vazias", afn.quantidade_de_transicoes_vazias(), 1)

print("\n--- o mesmo símbolo com dois destinos (não determinismo) ---")

afn.adicionar_transicao(e0, "a", e1)
mostrar(afn)
conferir("transições", afn.quantidade_de_transicoes(), 4)
conferir("destinos de 'a' saindo do estado 0",
         [t.destino for t in afn.transicoes[e0] if t.simbolo == "a"], [0, 1])

print("\n--- validações ---")

lista = [[], [], []]
lista[-1].append("seta")
print("lista[-1] em Python não dá erro, foi parar no último:", lista)

conferir_erro("origem -1", lambda: afn.adicionar_transicao(-1, "a", e0),
              "Estado de origem inexistente: -1")
conferir_erro("destino 9", lambda: afn.adicionar_transicao(e0, "a", 9),
              "Estado de destino inexistente: 9")
conferir_erro("símbolo de 2 caracteres", lambda: afn.adicionar_transicao(e0, "ab", e1),
              "Símbolo inválido: 'ab' (precisa ser 1 caractere)")

#Placar: código de saída 1 se alguma verificação falhar, para quem roda tudo de uma vez saber.
print(f"\nteste_passo1: {sum(resultados)}/{len(resultados)} verificações passaram.")
sys.exit(0 if all(resultados) else 1)