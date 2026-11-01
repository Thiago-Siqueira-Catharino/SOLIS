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

afn.definir_inicial(e0)
afn.definir_aceitacao(e2)

print("\n--- a máquina por dentro ---")
mostrar(afn)

print("\n--- contagens ---")

print("estados:", afn.quantidade_de_estados())                       
print("transições:", afn.quantidade_de_transicoes())                 
print("transições vazias:", afn.quantidade_de_transicoes_vazias())

print("\n--- o mesmo símbolo com dois destinos (não determinismo) ---")

afn.adicionar_transicao(e0, "a", e1)
mostrar(afn)
print("transições:", afn.quantidade_de_transicoes())

print("\n--- validações ---")

lista = [[], [], []]
lista[-1].append("seta")
print("lista[-1] em Python não dá erro, foi parar no último:", lista)

for origem, simbolo, destino in [(-1, "a", e0), (e0, "a", 9), (e0, "ab", e1)]:
    try:
        afn.adicionar_transicao(origem, simbolo, destino)
    except ValueError as erro:
        print("Erro:", erro)