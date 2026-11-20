"""
Minimização: reduz um AFD (afd.py) ao autômato mínimo pelo refinamento de
partições. Segue a seção 1.6 e os passos 18 a 23 do roteiro do guia
"Implementação em C++: Thompson, determinização e minimização".

A ideia: dois estados são equivalentes quando nenhuma continuação os
distingue quanto à aceitação. Estados equivalentes podem ser fundidos num só
sem mudar a linguagem. O algoritmo:

    1. completa o AFD (toda seta que falta vai para um estado de erro);
    2. descarta os estados inacessíveis (nenhuma cadeia chega neles);
    3. parte dos estados em dois blocos: os que aceitam e os que não aceitam;
    4. a cada rodada, divide os blocos cujos estados vão, com algum símbolo,
       para blocos diferentes (a assinatura de cada estado);
    5. para quando uma rodada não divide nada (o ponto fixo);
    6. cada bloco do ponto fixo vira um estado do AFD mínimo.

Aqui, "bloco" é um grupo da partição dos estados, e não o Bloco de Thompson
(Afn/thompson.py). Por isso, no código, ele se chama grupo, como no guia.

É o refinamento ingênuo, escolhido por ser direto de ler e de conferir, e
não o algoritmo de Hopcroft (seção 1.6.11 do guia).
"""

import copy
from collections import deque
from dataclasses import dataclass

from afd import AFD


@dataclass
class Minimizacao:

    #O resultado: o AFD mínimo, os grupos e a contagem de grupos a cada rodada.
    #grupos[0] são os estados do AFD original que viraram o estado 0 do mínimo, grupos[1] os do estado 1, e assim por diante.
    #contagens: o número de grupos da partição inicial e de cada rodada. No exemplo da seção 1.6.2 do guia, [2, 3, 3].

    afd: AFD
    grupos: list
    contagens: list


def completar_afd(afd):

    #Passo 18 do roteiro: se faltar alguma seta, cria um estado de erro, que não aceita, e manda para ele todas as setas que faltam, inclusive as dele mesmo.
    #Devolve o número do estado de erro criado, ou None se o AFD já estava completo.
    #O AFD que sai da determinização já é completo, e para ele nada muda. A função existe para que a minimização aceite também um AFD escrito à mão.

    if afd.esta_completo():
        return None

    erro = afd.novo_estado()
    for estado in range(afd.quantidade_de_estados()):
        for simbolo in afd.alfabeto:
            if afd.destino(estado, simbolo) is None:
                afd.adicionar_transicao(estado, simbolo, erro)
    return erro


def estados_alcancaveis(afd):

    #Passo 19 do roteiro: os estados a que alguma cadeia chega a partir do inicial, por uma busca em largura.
    #O inacessível não muda a linguagem, mas sem descartá-lo o resultado não seria o mínimo.

    visitados = {afd.inicial}
    fila = deque([afd.inicial])

    while fila:
        atual = fila.popleft()
        for destino in afd.transicoes[atual].values():
            if destino not in visitados:
                visitados.add(destino)
                fila.append(destino)

    return visitados


def particao_inicial(afd, alcancaveis):

    #Passo 20 do roteiro: um estado que aceita nunca é equivalente a um que não aceita, porque a cadeia vazia já os distingue.
    #Primeiro os que não aceitam, depois os que aceitam. Um grupo vazio não entra: se todos aceitam (ou nenhum aceita), a partição começa com um grupo só.

    nao_finais = sorted(estado for estado in alcancaveis if not afd.eh_final(estado))
    finais = sorted(estado for estado in alcancaveis if afd.eh_final(estado))
    return [grupo for grupo in (nao_finais, finais) if grupo]


def grupo_de(particao, estado):

    #Em que grupo da partição o estado está: devolve a posição do grupo. É a busca simples da seção 1.6.6 do guia.

    for posicao, grupo in enumerate(particao):
        if estado in grupo:
            return posicao
    raise ValueError(f"Estado não encontrado na partição: {estado}")


def assinatura(afd, particao, estado):

    #Passo 21 do roteiro: para cada símbolo do alfabeto, em que grupo cai o destino da seta. Vira uma tupla, para servir de chave de dicionário.
    #Não inclui o grupo do próprio estado: só se comparam estados que já estão no mesmo grupo.

    return tuple(grupo_de(particao, afd.transicoes[estado][simbolo]) for simbolo in afd.alfabeto)


def refinar_particao(afd, atual):

    #Uma rodada de refinamento: cada grupo se divide pelas assinaturas dos seus estados.
    #Todas as assinaturas da rodada são calculadas contra a mesma partição "atual", que não muda durante a rodada. Por isso as posições de grupo são comparáveis entre si.

    nova = []
    for grupo in atual:
        subdivisoes = {}
        for estado in grupo:
            subdivisoes.setdefault(assinatura(afd, atual, estado), []).append(estado)

        #Os subgrupos entram em ordem de assinatura, como no map do guia. A ordem não muda a máquina, só a numeração dos estados.

        for chave in sorted(subdivisoes):
            nova.append(subdivisoes[chave])

    return nova


def minimizar(afd_original):

    if afd_original.inicial is None:
        raise ValueError("Defina o estado inicial antes de minimizar")

    #Trabalha numa cópia: completar acrescenta estado e setas, e o AFD recebido fica intacto.

    afd = copy.deepcopy(afd_original)
    completar_afd(afd)

    alcancaveis = estados_alcancaveis(afd)
    particao = particao_inicial(afd, alcancaveis)
    contagens = [len(particao)]

    #Passo 22 do roteiro: uma rodada só divide grupos, nunca junta. Se o número de grupos não mudou, nenhum grupo se dividiu: é o ponto fixo.
    #Compara a contagem com a da rodada anterior, e não com um número esperado: parar num valor que se supõe final pode deixar estados distinguíveis no mesmo grupo.

    while True:
        nova = refinar_particao(afd, particao)
        contagens.append(len(nova))
        if len(nova) == len(particao):
            break
        particao = nova

    #Passo 23 do roteiro: cada grupo do ponto fixo vira um estado do AFD mínimo.

    minimo = AFD()
    minimo.definir_alfabeto(afd.alfabeto)

    #representante[estado antigo] = estado novo. Os inacessíveis ficam de fora, porque não estão em nenhum grupo.

    representante = {}
    for grupo in particao:
        novo = minimo.novo_estado()
        for estado in grupo:
            representante[estado] = novo

    minimo.definir_inicial(representante[afd.inicial])
    for estado in afd.finais:
        if estado in alcancaveis:
            minimo.adicionar_final(representante[estado])

    #Basta copiar as setas de um estado por grupo: no ponto fixo, todos os estados de um grupo vão, com cada símbolo, para o mesmo grupo.
    #Se isso não valesse, o refinamento ainda teria um grupo a dividir.

    for grupo in particao:
        origem = grupo[0]
        for simbolo in afd.alfabeto:
            minimo.adicionar_transicao(representante[origem], simbolo,
                                       representante[afd.transicoes[origem][simbolo]])

    return Minimizacao(minimo, particao, contagens)