"""
Bateria de casos

Lê os casos de casos_afn.txt, roda cada um pelo caminho inteiro
(texto do padrão -> leitor -> Thompson -> simulação) e compara com o
veredito decidido à mão.

Formato de cada linha do arquivo (campos separados por TAB):
    padrão <TAB> cadeia <TAB> aceita|recusa
A cadeia vazia é o campo vazio entre dois TABs.
Linhas vazias e linhas começando com # são ignoradas.

Ao terminar, devolve código 1 se algum caso discordar e 0 se todos
passarem. Assim a falha interrompe qualquer comando que dependa dela.
"""

import os
import sys
from dataclasses import dataclass

#O leitor de padrões fica na pasta Leitor_De_Padroes, ao lado desta pasta Afn.
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Leitor_De_Padroes"))
from leitor_padroes import ler_padrao, ErroDeLeitura
from thompson import construir_thompson


@dataclass
class CasoDeTeste:

    #Um caso: o padrão, a cadeia, o veredito esperado e de onde ele veio (arquivo:linha).

    padrao: str
    cadeia: str
    esperado: bool
    origem: str


def ler_casos(caminho):

    #Lê o arquivo e devolve (casos, linhas_malformadas).
    #Uma linha malformada NÃO é pulada em silêncio: ela volta como problema,
    #para aparecer no relatório. Um caso escrito errado não pode sumir da bateria.

    casos = []
    malformadas = []

    with open(caminho, encoding="utf-8") as arquivo:
        for numero, linha in enumerate(arquivo, start=1):
            linha = linha.rstrip("\r\n")
            origem = f"{os.path.basename(caminho)}:{numero}"

            if linha == "" or linha.startswith("#"):
                continue

            campos = linha.split("\t")
            if len(campos) != 3:
                malformadas.append(f"{origem}: linha malformada, esperava 3 campos separados por TAB "
                                   f"e encontrou {len(campos)} (o editor pode ter trocado o TAB por espaços)")
                continue

            padrao, cadeia, veredito = campos
            if veredito not in ("aceita", "recusa"):
                malformadas.append(f"{origem}: veredito inválido {veredito!r} (use aceita ou recusa)")
                continue

            casos.append(CasoDeTeste(padrao, cadeia, veredito == "aceita", origem))

    return casos, malformadas


def rodar_bateria(casos):

    #Roda todos os casos e devolve (quantos passaram, lista de falhas).
    #Não para no primeiro que discordar: junta todas as falhas de uma vez.

    passaram = 0
    falhas = []

    for caso in casos:
        try:
            arvore = ler_padrao(caso.padrao)
        except ErroDeLeitura as erro:
            falhas.append(f"{caso.origem}: padrão /{caso.padrao}/ recusado pela leitura ({erro})")
            continue

        obtido = construir_thompson(arvore).aceita(caso.cadeia)
        if obtido == caso.esperado:
            passaram += 1
        else:
            esperado = "aceita" if caso.esperado else "recusa"
            resposta = "aceita" if obtido else "recusa"
            falhas.append(f'{caso.origem}: /{caso.padrao}/ sobre "{caso.cadeia}" '
                          f"esperado {esperado}, obtido {resposta}")

    return passaram, falhas


def main():

    #O arquivo de casos fica na mesma pasta deste arquivo,
    #então a bateria funciona de qualquer pasta em que o terminal esteja.
    caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "casos_afn.txt")

    if not os.path.exists(caminho):
        print(f"Arquivo de casos não encontrado: {caminho}")
        return 1

    casos, malformadas = ler_casos(caminho)

    #Uma bateria sem nenhum caso não verifica nada: conta como falha, e diz por quê.
    if not casos and not malformadas:
        print("Nenhum caso encontrado no arquivo: uma bateria vazia não verifica nada.")
        return 1

    passaram, falhas = rodar_bateria(casos)
    problemas = malformadas + falhas
    total = len(casos) + len(malformadas)

    print(f"Bateria conferida à mão: {passaram}/{total} casos passaram.")
    for problema in problemas:
        print("  FALHA", problema)

    #Código de saída: 0 se tudo passou, 1 se algum caso discordou ou estava malformado.
    return 0 if not problemas and total > 0 else 1


if __name__ == "__main__":
    sys.exit(main())