"""
Autômato Finito Não Determinístico (AFN) da Solis.
 
Passos 1 e 2: a estrutura da máquina, os métodos que a montam, as contagens e o fecho vazio.
(A simulação entra no Passo 3.)
 
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
    #Frozen=True: depois de criada, a transição não pode ser alterada.

    simbolo: str
    destino: int

class AFN:

    def __init__(self):

        # transições [estado] é a lista de setas que saem daquele estado
        #Exemplo: transições[0] = [Transicao("a", 0), Transicao(EPSILON, 1)] significa que do estado 0 saem duas setas: uma que lê "a" e volta para 0, e outra que lê ε e vai para 1.
        #O número de estados é o tamanho desta lista

        self.transicoes = []

        #Estado inicial e estado de aceitação, começam como None, por que ainda não se sabe quais serão

        self.inicial = None
        self.aceitacao = None

    #Validação: o estado deve existir, e o símbolo deve ser exatamente 1 caractere (string de tamanho 1)

    def _validar_estado(self, estado, papel):

        #No python, o índice de uma lista pode ser negativo, e isso é válido. Mas não queremos aceitar estados negativos.

        if not isinstance(estado, int) or estado < 0 or estado >= len(self.transicoes):
            raise ValueError(f"Estado {papel} inexistente: {estado}")

    def _validar_simbolo(self, simbolo):

        #O rótulo precisa ser exatamente 1 caractere, uma seta "ab" nunca casaria na simulação que lê um símbolo por vez.

        if not isinstance(simbolo, str) or len(simbolo) != 1:
            raise ValueError(f"Símbolo inválido: {simbolo!r} (precisa ser 1 caractere)")

    #Construção da máquina: adiciona um estado, define o inicial e o de aceitação, adiciona transições.

    def novo_estado(self):

        #Cria um estado acrescentando uma lista vazia de transições e devolve o número dele (a posição dessa lista)

        self.transicoes.append([])
        return len(self.transicoes) - 1

    def adicionar_transicao(self, origem, simbolo, destino):

        #Acrescenta uma seta origem -- simbolo--> destino.
        #Diferente do AFD, nada é sobrescrito, se já houver uma seta com o mesmo símbolo saindo da origem, as duas ficam. É isso que permite o não-determinismo.

        self._validar_estado(origem, "de origem")
        self._validar_estado(destino, "de destino")
        self._validar_simbolo(simbolo)
        self.transicoes[origem].append(Transicao(simbolo, destino))

    def definir_inicial(self, estado):

        self._validar_estado(estado, "inicial")
        self.inicial = estado

    def definir_aceitacao(self, estado):

        self._validar_estado(estado, "de aceitação")
        self.aceitacao = estado

    #Contagem de estados e transições

    def quantidade_de_estados(self):
        return len(self.transicoes)

    def quantidade_de_transicoes(self):
        #Soma o tamanho das listas de transições de cada estado
        return sum(len(saidas) for saidas in self.transicoes)

    def quantidade_de_transicoes_vazias(self):
        #Percorre todas as setas e conta as que têm rótulo ε.
        #Contamos varrendo a máquina, e não com um contador somado em adicionar_transicao(), um contador contaria quantas vezes se inseriu, e não o que a máquina tem de fato

        total = 0
        for saidas in self.transicoes:
            for transicao in saidas:
                if transicao.simbolo == EPSILON:
                    total += 1
        return total

    #Fecho vazio (fecho-ε): dado um conjunto de estados, devolve os estados que se pode alcançar a partir deles usando apenas transições vazias (ε), incluindo os próprios estados de partida.
    
    def fecho_vazio(self, conjunto):

        #Visitado[estado] diz se o estado já entrou no resultado, sem essa marcação, um ciclo de setas ε (como em a** ou (a?)*) faria a busca girar para sempre.

        visitado = [False] * len(self.transicoes)

        #pilha: estados de onde ainda falta procurar setas ε.
        
        pilha = []

        #resultado: estados do fecho, na ordem em que entraram (por isso é lista e não set)

        resultado = []

        #1) Os estados de partida entram primeiro

        for estado in conjunto:
            self._validar_estado(estado, "do conjunto")
            if not visitado[estado]:
                visitado[estado] = True
                pilha.append(estado)
                resultado.append(estado)

        #2) Enquanto houver estados na pilha, pega um e procura setas ε saindo dele

        while pilha:
            atual = pilha.pop()
            for transicao in self.transicoes[atual]:

                #Seta que lê símbolo não entra no fecho

                if transicao.simbolo != EPSILON:
                    continue

                #Destino novo, marca, empilha e acrescenta no resultado

                if not visitado[transicao.destino]:
                    visitado[transicao.destino] = True
                    pilha.append(transicao.destino)
                    resultado.append(transicao.destino)

        #3)Pilha vazia, não há mais para onde ir só com ε
        return resultado