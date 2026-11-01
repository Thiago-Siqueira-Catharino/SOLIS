from afn import AFN, EPSILON

def mostrar(afn):

    #Mostra a listra de setas de cada estado, trocando o caractere de ε por "ε".

    for estado, saidas in enumerate(afn.transicoes):
        setas = ", ".join(f"({'ε' if t.simbolo == EPSILON else t.simbolo!r} -> {t.destino})" for t in saidas)
        print(f"estado {estado}: [{setas}]")

