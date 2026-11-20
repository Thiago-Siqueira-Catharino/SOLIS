"""
Autômato Finito Determinístico (AFD) da determinização e da minimização.

É a máquina que a construção de subconjuntos produz a partir do AFN, e que a
minimização reduz. Segue a estrutura do guia "Implementação em C++: Thompson,
determinização e minimização" (seções 1.5.2 e 1.7.1).

Diferença para o AFN (Afn/afn.py):
    - No AFN, um estado e um símbolo podem ter VÁRIOS destinos, e existem
      transições vazias (ε) e o coringa. Por isso ele guarda uma LISTA de setas
      por estado.
    - No AFD, cada par (estado, símbolo) tem UM destino só, e não existe ε nem
      coringa. Por isso cada estado guarda um DICIONÁRIO {símbolo: destino}:
      gravar de novo o mesmo símbolo substitui o destino antigo, em vez de somar
      uma segunda seta.
    - O AFN de Thompson tem UM estado de aceitação; o AFD pode ter VÁRIOS.

Diferença para o AFD dos alfabetos (Afds/Afd_Solis/afd.py):
    - Lá os estados têm nome ("q0", "q1"); aqui são números, como no AFN, porque
      a determinização cria os estados um a um, na ordem em que os conjuntos
      aparecem.
    - Lá, faltar transição só quer dizer "não aceita"; aqui a determinização
      sempre produz o AFD completo, e o conjunto vazio vira um estado como os
      outros: o estado de erro.
"""

from dataclasses import dataclass, field


@dataclass
class AFD:

    #transicoes[estado] é o dicionário das setas que saem daquele estado.
    #Exemplo: transicoes[0] = {"a": 1, "b": 2} significa que do estado 0, lendo "a", vai-se ao 1, e lendo "b", ao 2.
    #O número de estados é o tamanho desta lista.

    transicoes: list = field(default_factory=list)

    #Estado inicial: começa como None, porque ainda não se sabe qual será

    inicial: object = None

    #Estados de aceitação: um conjunto, porque o AFD pode ter vários

    finais: set = field(default_factory=set)

    #Alfabeto: os símbolos que a máquina lê, sem repetição e em ordem

    alfabeto: list = field(default_factory=list)

    #Validação: o estado deve existir, e o símbolo deve ser 1 caractere do alfabeto

    def _validar_estado(self, estado, papel):

        #Como no AFN: o Python aceita índice negativo em lista, e não queremos aceitar estados negativos.

        if not isinstance(estado, int) or estado < 0 or estado >= len(self.transicoes):
            raise ValueError(f"Estado {papel} inexistente: {estado}")

    def _validar_simbolo(self, simbolo):

        #Uma seta com um símbolo fora do alfabeto nunca seria usada pela determinização nem pela minimização, que percorrem só o alfabeto.

        if not isinstance(simbolo, str) or len(simbolo) != 1:
            raise ValueError(f"Símbolo inválido: {simbolo!r} (precisa ser 1 caractere)")
        if simbolo not in self.alfabeto:
            raise ValueError(f"Símbolo fora do alfabeto: {simbolo!r}")

    #Construção da máquina

    def definir_alfabeto(self, simbolos):

        #Guarda os símbolos sem repetição e em ordem. Cada um precisa ter 1 caractere.

        for simbolo in simbolos:
            if not isinstance(simbolo, str) or len(simbolo) != 1:
                raise ValueError(f"Símbolo inválido: {simbolo!r} (precisa ser 1 caractere)")
        self.alfabeto = sorted(set(simbolos))

    def novo_estado(self):

        #Cria um estado acrescentando um dicionário vazio de setas e devolve o número dele

        self.transicoes.append({})
        return len(self.transicoes) - 1

    def adicionar_transicao(self, origem, simbolo, destino):

        #Grava a seta origem --simbolo--> destino. Diferente do AFN, se já houver uma seta com esse símbolo saindo da origem, ela é substituída: é isso que mantém um destino só por par (estado, símbolo).

        self._validar_estado(origem, "de origem")
        self._validar_estado(destino, "de destino")
        self._validar_simbolo(simbolo)
        self.transicoes[origem][simbolo] = destino

    def definir_inicial(self, estado):

        self._validar_estado(estado, "inicial")
        self.inicial = estado

    def adicionar_final(self, estado):

        self._validar_estado(estado, "de aceitação")
        self.finais.add(estado)

    #Consultas

    def destino(self, estado, simbolo):

        #O destino da seta que sai do estado lendo o símbolo, ou None se ela não existir

        self._validar_estado(estado, "consultado")
        return self.transicoes[estado].get(simbolo)

    def eh_final(self, estado):
        return estado in self.finais

    def quantidade_de_estados(self):
        return len(self.transicoes)

    def quantidade_de_transicoes(self):

        #Soma o tamanho dos dicionários de cada estado

        return sum(len(saidas) for saidas in self.transicoes)

    def esta_completo(self):

        #Completo: todo estado tem uma seta para cada símbolo do alfabeto. A minimização só funciona com o AFD completo.

        return all(simbolo in saidas for saidas in self.transicoes for simbolo in self.alfabeto)

    #Simulação (seção 1.7.1 do guia): um estado ativo só, e não um conjunto

    def aceita(self, cadeia):

        if self.inicial is None:
            raise ValueError("Defina o estado inicial antes de simular")

        atual = self.inicial
        for simbolo in cadeia:

            #Sem seta para o símbolo, a cadeia é rejeitada. Num AFD completo, isso só acontece com símbolo fora do alfabeto.

            proximo = self.transicoes[atual].get(simbolo)
            if proximo is None:
                return False
            atual = proximo

        return atual in self.finais