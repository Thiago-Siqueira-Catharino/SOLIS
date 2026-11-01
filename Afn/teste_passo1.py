from afn import AFN, EPSILON

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
print("Estados criados: ", e0, e1, e2)

# δ: as três setas do desenho

afn.adicionar_transicao(e0, "a", e0)
afn.adicionar_transicao(e0, EPSILON, e1)
afn.adicionar_transicao(e1, "b", e2)

