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

from dataclasses import dataclass

# Rótulos especiais de transição

# ε (transição vazia): muda de estado SEM consumir símbolo.
# Usamos o caractere de código 0 porque ele não aparece num padrão escrito à mão. Assim, todo rótulo continua sendo uma string de 1 caractere.

EPSILON = "\0"

#Coringa (o "." do padrão): casa QUALQUER símbolo, mas não é transição vazia.
# Precisa de uma marca própria, diferente de ε.

QUALQUER = "\x01"

@dataclass(frozen=True)
class Transicao:

    #Uma seta da máquina: o rótulo que ela lê e o estado para onde ela leva.
    #Frozen=True: depois de criada, a transição não muda. Isso permite que ela seja usada como chave de dicionário.

    simbolo: str
    destino: int

class AFN:

    def __init__(self):

        # transições [estado] é a lista de seta que saem daquele estado
        #Exemplo: transições[0] = [Transicao("a", 0), TransicaoAFN(EPSILON, 1)] significa que do estado 0 saem duas setas: uma que lê "a" e volta para 0, e outra que lê ε e vai para 1.
        #O número de estados é o tamanho desta lista

        self.transicoes = []

        #Estado inicial e estado de aceitação, começam como None, por que ainda não se sabe quais serão

        self.inicial = None
        self.aceitacao = None