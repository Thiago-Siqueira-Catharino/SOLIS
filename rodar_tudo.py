"""
Roda todas as verificações do projeto Solis com um comando só:

    python rodar_tudo.py

Cada parte é um programa do repositório que confere o próprio resultado e
termina com código 0 quando tudo passou, ou 1 quando alguma verificação
falhou. Este script roda as partes uma a uma, mostra a última linha (o
placar) de cada uma e, no fim, o placar geral.

Termina com código 0 se todas as partes passarem, e 1 se alguma falhar.
"""

import os
import subprocess
import sys

#As partes, na ordem em que as peças do compilador foram construídas.
PARTES = [
    ("AFD de dígitos", "Afds/Alfabeto_0_ate_9/afd_numeros.py"),
    ("AFD de letras", "Afds/Alfabeto_A_ate_Z/afd_letras.py"),
    ("AFD de letras e dígitos", "Afds/Alfabeto_0_ate_Z/afd_letras_numeros.py"),
    ("Leitor de padrões", "Leitor_De_Padroes/demonstrar_leitor.py"),
    ("AFN, passo 1: estrutura", "Afn/teste_passo1.py"),
    ("AFN, passo 2: fecho vazio", "Afn/teste_passo2.py"),
    ("AFN, passo 3: simulação", "Afn/teste_passo3.py"),
    ("AFN, passo 4: Thompson", "Afn/teste_passo4.py"),
    ("AFN, bateria conferida à mão", "Afn/bateria.py"),
]

RAIZ = os.path.dirname(os.path.abspath(__file__))


def rodar(caminho):

    #Roda uma parte e devolve o código de saída e as linhas que ela imprimiu.
    #PYTHONIOENCODING garante que acentos e o ε passem pelo cano no Windows,
    #onde a saída redirecionada não usa UTF-8 por padrão.

    ambiente = dict(os.environ, PYTHONIOENCODING="utf-8")
    processo = subprocess.run([sys.executable, os.path.join(RAIZ, caminho)],
                              capture_output=True, text=True, encoding="utf-8",
                              cwd=RAIZ, env=ambiente)
    linhas = (processo.stdout + processo.stderr).splitlines()
    return processo.returncode, linhas


def main():
    passaram = 0
    for nome, caminho in PARTES:
        codigo, linhas = rodar(caminho)
        ultima = next((linha for linha in reversed(linhas) if linha.strip()), "(sem saída)")
        #A última linha de cada parte é o placar dela, "nome: X/Y ...": fica só o "X/Y ...".
        placar = ultima.rsplit(": ", 1)[-1]

        if codigo == 0:
            passaram += 1
            print(f"[OK]     {nome:<30} {placar}")
        else:
            #Quando falha, mostra só as linhas que explicam a falha.
            print(f"[FALHOU] {nome:<30} {placar} (código {codigo})")
            for linha in linhas:
                if "FALHOU" in linha or "Traceback" in linha or "Error" in linha:
                    print(f"         {linha.strip()}")
            print(f"         para ver tudo: python {caminho}")

    print(f"\nSolis: {passaram}/{len(PARTES)} partes passaram.")
    return 0 if passaram == len(PARTES) else 1


if __name__ == "__main__":
    sys.exit(main())