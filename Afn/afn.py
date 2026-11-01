"""
afn.py — Autômato Finito Não Determinístico (AFN) da Solis.
 
Passo 1: a estrutura da máquina, os métodos que a montam e as contagens.
(O fecho vazio e a simulação entram nos próximos passos.)
 
Diferença para o AFD (Afds/Afd_Solis/afd.py):
    - No AFD, cada par (estado, símbolo) tinha UM destino, guardado num
      dicionário: transicoes["q0"]["5"] = "q1". Gravar de novo apagava o antigo.
    - No AFN, o mesmo estado e o mesmo símbolo podem ter VÁRIOS destinos, e
      existem transições vazias (ε), que mudam de estado sem ler símbolo.
      Por isso, cada estado guarda uma LISTA de transições (símbolo, destino).
    - Os estados são números: o estado 0 é a posição 0 da lista, o estado 1
      é a posição 1, e assim por diante.
    - A máquina tem UM estado inicial e UM estado de aceitação. É o formato
      que a construção de Thompson produz (cada bloco tem uma entrada e uma saída).
 
A classe AFD não é reaproveitada aqui: a forma de guardar as transições é outra.
"""

