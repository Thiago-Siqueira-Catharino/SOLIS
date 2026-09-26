"""
Um AFD é definido formalmente pela quíntupla (Q, Σ, δ, q0, F):

    Q  -> conjunto de estados
    Σ  -> alfabeto (os símbolos que o autômato conhece)
    δ  -> função de transição: dado um estado e um símbolo, diz o próximo estado
    q0 -> estado inicial (onde a leitura começa)
    F  -> conjunto de estados finais (se a leitura terminar num deles, a palavra é aceita)
 
Cada atributo da classe abaixo guarda uma dessas cinco peças.
"""

class AFD:
    def __init__(self):
        #Q : Conjunto de estados.
        self.estados = set()

        #Σ: alfabeto
        self.alfabeto = set()

        # δ: função de transição.
        #É um dicionário de dicionários
        #Transições ["q0"]["5"] = "q1" si
        self.transicoes = {}

        #q0: Estado inicial. Começa vazio até ser definido
        self.estado_inicial = None

        #F: Conjunto de estados finais
        self.estados_finais = set()

    #Métodos para Construção : Montam Q, Σ, δ, q0 e F antes de usar o AFD

    def adicionar_estado(self, estado):
        #Inclui um estado em Q
        #Por enquanto não precisa de validação
        self.estados.add(estado)

    def adicionar_simbolo(self, simbolo):
        # Inclui um símbolo em Σ.
        #Aqui se define quem é o alfabeto
        self.alfabeto.add(simbolo)

    def definir_estado_inicial(self, estado):
        #Aceita como Q0 um estado que já foi declarado em Q
        if estado not in self.estados:
           raise ValueError("O estado inicial dever pertencer a Q")
        self.estado_inicial = estado

    def adicionar_estado_final(self, estado):
        #Aceita em F um estado que foi declarado em Q
        if estado not in self.estados:
            raise ValueError("O estado final deve pertencer a Q")
        self.estados_finais.add(estado)

    def adicionar_transicao(self, estado, simbolo, proximo_estado):
        #Registra uma transição δ(estado, simbolo) = proximo_estado.

        #1) O estado de origem precisa existir em Q
        if estado not in self.estados:
            raise ValueError("Estado de origem inexistente")

        #2) O estado de destino precisa existir em Q
        if proximo_estado not in self.estados:
            raise ValueError("Estado de destino inexistente")

        #3) O símbolo precisa pertencer ao Σ
        if simbolo not in self.alfabeto:
            raise ValueError("Símbolo inexistente no alfabeto")

        #Passou nas três verificações, ele grava a transição

        #setdefault cria o dicionário interno do estado se ele ainda não existir

        self.transicoes.setdefault(estado, {})[simbolo] = proximo_estado

    #Execução - Usa o AFD já montado pra testar uma palavra

    def aceita(self, palavra):
        #A leitura sempre começa no estado inicial (Q0)
        estado = self.estado_inicial

        #Lê a palavra um símbolo por vez, da esquerda para a direita
        
        for simbolo in palavra:

            #Se o símbolo não pertencer ao Σ, a palavra é rejeitada na hora

            if simbolo not in self.alfabeto:
                return False

            #Procura as transições que saem do estado atual

            transicoes_do_estado = self.transicoes.get(estado)

            #Se não tem nehuma transição saindo deste estado, ou nenhuma com esse símbolo, não tem aonde ir, é rejeitado

            if transicoes_do_estado is None or simbolo not in transicoes_do_estado:
                return False

            #Avança : q <- δ(q, símbolo)
            estado = transicoes_do_estado[simbolo]

        #Terminou de ler a palavra inteira e ela é aceita somente se o estado onde paraou pertence a F
        
        return estado in self.estados_finais