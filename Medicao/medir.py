"""
Medição da seção 7 da especificação: processar os registros com a máquina
determinística mínima de cada padrão é mais rápido do que simular a máquina
não determinística construída direto do padrão?

Para cada padrão:
  1. monta as duas máquinas: o AFN de Thompson (a referência) e o AFD mínimo
     (determinização + minimização), anotando o tamanho e o tempo de montagem;
  2. gera os registros com uma semente fixa, só com os símbolos do alfabeto do
     padrão, em três tamanhos (curto, médio e longo), metade que casa e metade
     que não casa;
  3. confere se as duas máquinas dão a mesma resposta que um oráculo de fora
     (o re.fullmatch do Python) em todos os registros. Sem isso, comparar
     tempo não vale nada;
  4. cronometra as duas máquinas decidindo os mesmos registros, repetindo
     várias vezes e ficando com a mediana.

A simulação do AFN usada aqui é a do Afn/afn.py (fecho_vazio e mover), sem
guardar o traço de cada passo: o simular() guarda o traço para o
formatar_simulacao mostrar, e esse custo não tem a ver com decidir o registro.

Os tempos dependem do computador e da versão do Python. O que se compara é a
proporção entre as duas máquinas no mesmo computador.

Ao terminar, devolve código 1 se alguma máquina discordar do oráculo e 0 se
todas concordarem.
"""

import os
import platform
import random
import re
import statistics
import sys
import time

#As pastas dos outros módulos, a partir da pasta deste arquivo, para rodar de qualquer lugar.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for pasta in ("Determinizacao", "Afn", "Leitor_De_Padroes"):
    sys.path.insert(0, os.path.join(RAIZ, pasta))

from determinizacao import determinizar
from minimizacao import minimizar
from leitor_padroes import ler_padrao
from thompson import construir_thompson

#A semente fixa: rodando de novo, os registros são os mesmos.
SEMENTE = 2026

#Quantos registros de cada tamanho, e quantas vezes cada medida se repete.
REGISTROS_POR_TAMANHO = 60
REPETICOES = 5

#Os três tamanhos de registro, em símbolos. Um registro que casa pode sair um pouco maior,
#porque o caminho até um estado de aceitação pode pedir mais símbolos.
TAMANHOS = [("curto", 5), ("médio", 50), ("longo", 500)]

#Os padrões medidos: (nome, padrão na Solis, o mesmo padrão para o oráculo).
#Na Solis o $ é um símbolo comum; no re do Python ele marca o fim do texto, e por isso vai escapado.
#O coringa da Solis lê qualquer símbolo; os registros só têm os símbolos do padrão, então o "." do re basta.

PADROES = [
    ("quantidade", "[0-9]+", r"[0-9]+"),
    ("preço", "[0-9]+(,|\\.)[0-9][0-9]", r"[0-9]+(,|\.)[0-9][0-9]"),
    ("preço com coringa", "[0-9]+.[0-9][0-9]", r"[0-9]+.[0-9][0-9]"),
    ("pedido", "#[0-9]+", r"#[0-9]+"),
    ("e-mail", "[a-z0-9_]+@[a-z]+\\.com(\\.br)?", r"[a-z0-9_]+@[a-z]+\.com(\.br)?"),
    ("valor", "R$ [0-9]+,[0-9][0-9]", r"R\$ [0-9]+,[0-9][0-9]"),
]

#A explosão de estados: "o n-ésimo símbolo contado do fim é a", para n de 1 a 8.
for n in range(1, 9):
    texto = "(a|b)*a" + "(a|b)" * (n - 1)
    PADROES.append((f"n-ésimo do fim, n = {n}", texto, texto))


#1) A simulação do AFN sem o traço: o simular() do Afn/afn.py, passo a passo, sem guardar os passos.

def afn_aceita(afn, cadeia):
    presente = [False] * len(afn.transicoes)
    ativos = afn.fecho_vazio([afn.inicial])
    for simbolo in cadeia:
        ativos = afn.fecho_vazio(afn.mover(ativos, simbolo, presente))
        #Sem estado ativo, nenhum símbolo seguinte reativa nada: pode parar, como no simular().
        if not ativos:
            break
    return afn.aceitacao in ativos


#2) As duas máquinas, com o tamanho e o tempo de montagem.

def montar(padrao):
    inicio = time.perf_counter()
    afn = construir_thompson(ler_padrao(padrao))
    meio = time.perf_counter()
    minimo = minimizar(determinizar(afn).afd).afd
    fim = time.perf_counter()
    return afn, minimo, meio - inicio, fim - meio


#3) Os registros: gerados a partir do AFD mínimo, e conferidos depois pelo oráculo.

def estados_vivos(afd):

    #Os estados de onde ainda se chega a um estado de aceitação. Só eles servem para montar um registro que casa.

    vivos = set(afd.finais)
    mudou = True
    while mudou:
        mudou = False
        for estado, setas in enumerate(afd.transicoes):
            if estado not in vivos and any(destino in vivos for destino in setas.values()):
                vivos.add(estado)
                mudou = True
    return vivos


def caminho_ate_final(afd, origem):

    #O caminho mais curto de origem até um estado de aceitação (busca em largura), como uma lista de símbolos.

    anterior = {origem: None}
    fila = [origem]
    while fila:
        estado = fila.pop(0)
        if estado in afd.finais:
            simbolos = []
            while anterior[estado] is not None:
                estado, simbolo = anterior[estado]
                simbolos.append(simbolo)
            return list(reversed(simbolos))
        for simbolo, destino in sorted(afd.transicoes[estado].items()):
            if destino not in anterior:
                anterior[destino] = (estado, simbolo)
                fila.append(destino)
    return None


def registro_que_casa(afd, vivos, tamanho, sorteio):

    #Anda ao acaso pelos estados vivos durante "tamanho" símbolos e depois vai pelo caminho mais curto até a aceitação.

    estado = afd.inicial
    simbolos = []
    for _ in range(tamanho):
        opcoes = [(s, d) for s, d in sorted(afd.transicoes[estado].items()) if d in vivos]
        if not opcoes:
            break
        simbolo, estado = sorteio.choice(opcoes)
        simbolos.append(simbolo)
    return "".join(simbolos + caminho_ate_final(afd, estado))


def registro_que_nao_casa(alfabeto, oraculo, tamanho, sorteio):

    #Sorteia textos do tamanho pedido até achar um que o oráculo recusa.
    #Em alguns padrões isso não existe: sobre {0, ..., 9}, todo texto não vazio casa com [0-9]+.
    #Nesse caso devolve None, e o lugar fica com um registro que casa.

    for _ in range(2000):
        texto = "".join(sorteio.choice(alfabeto) for _ in range(tamanho))
        if not oraculo.fullmatch(texto):
            return texto
    return None


def gerar_registros(afd, oraculo, tamanho, sorteio):
    vivos = estados_vivos(afd)
    alfabeto = sorted(afd.alfabeto)
    metade = REGISTROS_POR_TAMANHO // 2
    casam = [registro_que_casa(afd, vivos, tamanho, sorteio) for _ in range(metade)]
    nao_casam = []
    for _ in range(metade):
        registro = registro_que_nao_casa(alfabeto, oraculo, tamanho, sorteio)
        if registro is None:
            registro = registro_que_casa(afd, vivos, tamanho, sorteio)
        nao_casam.append(registro)
    return casam + nao_casam


#4) O cronômetro: a mediana de várias repetições, dividida pelo número de registros.

def tempo_por_registro(decidir, registros):
    medidas = []
    for _ in range(REPETICOES):
        inicio = time.perf_counter()
        for registro in registros:
            decidir(registro)
        medidas.append(time.perf_counter() - inicio)
    return statistics.median(medidas) / len(registros)


def main():
    sorteio = random.Random(SEMENTE)
    concordaram = 0
    conferidos = 0

    print("Medição da seção 7: AFD mínimo contra a simulação do AFN\n")
    print(f"    Computador: {platform.machine()}, {platform.system()} | Python {platform.python_version()}")
    print(f"    Semente {SEMENTE}, {REGISTROS_POR_TAMANHO} registros por tamanho, mediana de {REPETICOES} repetições\n")

    print("--- 1) O tamanho das máquinas e o tempo de montagem ---\n")
    print(f"    {'padrão':<26} {'AFN':>14} {'AFD mínimo':>14} {'montar AFN':>11} {'montar AFD':>11}")
    print(f"    {'':<26} {'estados/setas':>14} {'estados/setas':>14} {'(ms)':>11} {'(ms)':>11}")

    maquinas = []
    for nome, padrao, texto_oraculo in PADROES:
        afn, minimo, tempo_afn, tempo_afd = montar(padrao)
        maquinas.append((nome, afn, minimo, re.compile(texto_oraculo)))
        tamanho_afn = f"{afn.quantidade_de_estados()}/{afn.quantidade_de_transicoes()}"
        tamanho_afd = f"{minimo.quantidade_de_estados()}/{minimo.quantidade_de_transicoes()}"
        print(f"    {nome:<26} {tamanho_afn:>14} {tamanho_afd:>14} {tempo_afn * 1000:>11.2f} {tempo_afd * 1000:>11.2f}")

    print("\n--- 2) A conferência: as duas máquinas contra o oráculo ---\n")
    registros_de = {}
    for nome, afn, minimo, oraculo in maquinas:
        for rotulo, tamanho in TAMANHOS:
            registros = gerar_registros(minimo, oraculo, tamanho, sorteio)
            registros_de[(nome, rotulo)] = registros
            for registro in registros:
                esperado = oraculo.fullmatch(registro) is not None
                conferidos += 1
                if afn_aceita(afn, registro) == esperado and minimo.aceita(registro) == esperado:
                    concordaram += 1
                else:
                    print(f"    [DISCORDA] {nome}, {rotulo}: {registro!r}")
    #Quantos registros casam em cada padrão: onde não há como não casar, todos casam.
    for nome, _, _, oraculo in maquinas:
        casam = sum(oraculo.fullmatch(r) is not None for (n, _), rs in registros_de.items() if n == nome for r in rs)
        total = sum(len(rs) for (n, _), rs in registros_de.items() if n == nome)
        print(f"    {nome:<26} {casam:>4} de {total} registros casam")
    print()
    situacao = "OK" if concordaram == conferidos else "FALHOU"
    print(f"    [{situacao}] {concordaram}/{conferidos} registros com a mesma resposta nas duas máquinas e no oráculo")

    print("\n--- 3) O tempo por registro, em microssegundos ---\n")
    print(f"    {'padrão':<26} {'tamanho':<8} {'AFN':>10} {'AFD mínimo':>11} {'AFN / AFD':>10}")
    for nome, afn, minimo, _ in maquinas:
        for rotulo, _ in TAMANHOS:
            registros = registros_de[(nome, rotulo)]
            tempo_afn = tempo_por_registro(lambda r: afn_aceita(afn, r), registros)
            tempo_afd = tempo_por_registro(minimo.aceita, registros)
            print(f"    {nome:<26} {rotulo:<8} {tempo_afn * 1e6:>10.1f} {tempo_afd * 1e6:>11.1f} "
                  f"{tempo_afn / tempo_afd:>9.1f}x")

    return 0 if concordaram == conferidos else 1


if __name__ == "__main__":
    sys.exit(main())