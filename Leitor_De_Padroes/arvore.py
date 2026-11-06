"""
A árvore tem 6 tipos de nó:
    - 3 folhas (casos base): Símbolo, Qualquer (o coringa ".") e Vazio (ε)
    - 3 operadores (casos compostos): Concatenação, Alternância e Fecho

Não existem nós para +, ? ou classes como [0-9]: são açúcar, e o leitor de
padrões os reduz a estes 6 tipos.

Cada nó guarda os próprios filhos. Assim, o código tem a mesma forma da
forma linear: [0-9]+ vira concatenacao(D, fecho(D)).
"""

from dataclasses import dataclass
from enum import Enum


class TipoDeNo(Enum):

    #Os 6 tipos de nó. Usar Enum, e não texto solto, impede erro de digitação
    #como "concatenaçao" passar despercebido.

    SIMBOLO = "simbolo"
    QUALQUER = "qualquer"
    VAZIO = "vazio"
    CONCATENACAO = "concatenacao"
    ALTERNANCIA = "alternancia"
    FECHO = "fecho"


@dataclass(frozen=True)
class No:

    #Um nó da árvore. Quais campos são usados depende do tipo:
    #  SIMBOLO:                    só "simbolo"
    #  QUALQUER e VAZIO:           nenhum
    #  CONCATENACAO e ALTERNANCIA: "esquerda" e "direita"
    #  FECHO:                      só "esquerda" (o trecho que se repete)

    tipo: TipoDeNo
    simbolo: str = None
    esquerda: "No" = None
    direita: "No" = None


#Funções que montam cada tipo de nó. Elas validam as peças, para que uma
#árvore malformada (um fecho sem filho, um símbolo "ab") seja recusada na hora.

def _validar_filho(filho, papel):
    if not isinstance(filho, No):
        raise ValueError(f"Filho {papel} inválido: {filho!r} (precisa ser um nó)")


def simbolo(caractere):
    if not isinstance(caractere, str) or len(caractere) != 1:
        raise ValueError(f"Símbolo inválido: {caractere!r} (precisa ser 1 caractere)")
    return No(TipoDeNo.SIMBOLO, simbolo=caractere)


def qualquer():
    return No(TipoDeNo.QUALQUER)


def vazio():
    return No(TipoDeNo.VAZIO)


def concatenacao(esquerda, direita):
    _validar_filho(esquerda, "esquerdo")
    _validar_filho(direita, "direito")
    return No(TipoDeNo.CONCATENACAO, esquerda=esquerda, direita=direita)


def alternancia(esquerda, direita):
    _validar_filho(esquerda, "esquerdo")
    _validar_filho(direita, "direito")
    return No(TipoDeNo.ALTERNANCIA, esquerda=esquerda, direita=direita)


def fecho(interior):
    _validar_filho(interior, "do fecho")
    return No(TipoDeNo.FECHO, esquerda=interior)


#Forma linear e contagem: as mesmas do trabalho "Do padrão à árvore".

def forma_linear(no):

    #Escreve a árvore como texto: o rótulo do nó e, entre parênteses, os filhos.
    #Os rótulos são os mesmos do material do professor (qualquer, vazio, concat,
    #alt, fecho), para que a saída possa ser comparada caractere por caractere.

    if no.tipo == TipoDeNo.SIMBOLO:
        return repr(no.simbolo)
    if no.tipo == TipoDeNo.QUALQUER:
        return "qualquer"
    if no.tipo == TipoDeNo.VAZIO:
        return "vazio"
    if no.tipo == TipoDeNo.CONCATENACAO:
        return f"concat({forma_linear(no.esquerda)}, {forma_linear(no.direita)})"
    if no.tipo == TipoDeNo.ALTERNANCIA:
        return f"alt({forma_linear(no.esquerda)}, {forma_linear(no.direita)})"
    if no.tipo == TipoDeNo.FECHO:
        return f"fecho({forma_linear(no.esquerda)})"
    raise ValueError(f"Tipo de nó desconhecido: {no.tipo}")


def contar_nos(no):

    #Conta os nós da árvore: 1 pelo próprio nó, mais os nós dos filhos.

    if no.tipo in (TipoDeNo.SIMBOLO, TipoDeNo.QUALQUER, TipoDeNo.VAZIO):
        return 1
    if no.tipo in (TipoDeNo.CONCATENACAO, TipoDeNo.ALTERNANCIA):
        return 1 + contar_nos(no.esquerda) + contar_nos(no.direita)
    if no.tipo == TipoDeNo.FECHO:
        return 1 + contar_nos(no.esquerda)
    raise ValueError(f"Tipo de nó desconhecido: {no.tipo}")