"""
confere o fecho vazio (fecho-ε) do AFN.
 
Três verificações:
  1. a máquina pequena de a*b do Passo 1 (conferível de cabeça);
  2. a máquina de (a|b)*c, com o fecho conferido à mão seguindo as setas;
  3. uma máquina com ciclo de setas ε (a**), que só termina por causa do visitado.
"""

import sys

from afn import AFN, EPSILON

#Guarda o resultado de cada verificação, para o placar do fim.
resultados = []


def conferir(descricao, obtido, esperado):
    situacao = "OK" if obtido == esperado else "FALHOU"
    resultados.append(obtido == esperado)
    print(f"[{situacao}] {descricao}: obtido {obtido}, esperado {esperado}")


def conferir_erro(descricao, acao, mensagem_esperada):

    #Verifica um erro proposital: passa se a ação gerar exatamente esse erro.
    #Se a ação não gerar erro nenhum, ou gerar outro, a verificação falha.

    try:
        acao()
        obtido = "nenhum erro"
    except ValueError as erro:
        obtido = str(erro)
    passou = obtido == mensagem_esperada
    resultados.append(passou)
    if passou:
        print(f"[OK] erro esperado ({descricao}): {obtido}")
    else:
        print(f"[FALHOU] erro esperado ({descricao}): obtido {obtido}, esperado {mensagem_esperada}")

# 1) a*b do Passo 1:  0 --a--> 0,  0 --ε--> 1,  1 --b--> 2

print("--- 1) máquina pequena de a*b ---")
m = AFN()

for _ in range(3):
    m.novo_estado()
m.adicionar_transicao(0, 'a', 0)
m.adicionar_transicao(0, EPSILON, 1)
m.adicionar_transicao(1, 'b', 2)

conferir("fecho de {0}", m.fecho_vazio([0]), [0, 1])
conferir("fecho de {1}", m.fecho_vazio([1]), [1])
conferir("fecho de {2}", m.fecho_vazio([2]), [2])
conferir("fecho de {}", m.fecho_vazio([]), [])

#2) (a|b)*c, montada à mão

#inicio   -> { 6, 4, 7, 8, 0, 2 }
#apos 'a' -> { 1, 5, 4, 7, 8, 0, 2 }

print("\n--- 2) (a|b)*c ---")
t = AFN()
for _ in range(10):
    t.novo_estado()
t.adicionar_transicao(0, "a", 1)       
t.adicionar_transicao(2, "b", 3)        
t.adicionar_transicao(4, EPSILON, 0)    
t.adicionar_transicao(4, EPSILON, 2)
t.adicionar_transicao(1, EPSILON, 5)
t.adicionar_transicao(3, EPSILON, 5)
t.adicionar_transicao(6, EPSILON, 4)    
t.adicionar_transicao(6, EPSILON, 7)
t.adicionar_transicao(5, EPSILON, 4)
t.adicionar_transicao(5, EPSILON, 7)
t.adicionar_transicao(8, "c", 9)        
t.adicionar_transicao(7, EPSILON, 8)  
t.definir_inicial(6)
t.definir_aceitacao(9)
 
conferir("estados", t.quantidade_de_estados(), 10)
conferir("transições", t.quantidade_de_transicoes(), 12)
conferir("transições vazias", t.quantidade_de_transicoes_vazias(), 9)
conferir("fecho do inicial {6}", t.fecho_vazio([6]), [6, 4, 7, 8, 0, 2])
# Depois de ler 'a', o único estado alcançado pela seta 'a' é o 1:
conferir("fecho de {1} (após 'a')", t.fecho_vazio([1]), [1, 5, 4, 7, 8, 0, 2])

# 3) a**: o fecho de dentro tem um ciclo SÓ de setas ε (2 -> 3 -> 2)

print("\n--- 3) ciclo de setas ε em a** ---")
c = AFN()

for _ in range(6):
    c.novo_estado()
c.adicionar_transicao(0, "a", 1)
c.adicionar_transicao(2, EPSILON, 0)
c.adicionar_transicao(2, EPSILON, 3)
c.adicionar_transicao(1, EPSILON, 0)
c.adicionar_transicao(1, EPSILON, 3)
c.adicionar_transicao(4, EPSILON, 2)
c.adicionar_transicao(4, EPSILON, 5)
c.adicionar_transicao(3, EPSILON, 2)
c.adicionar_transicao(3, EPSILON, 5)

conferir("fecho de {4} terminou", sorted(c.fecho_vazio([4])), [0, 2, 3, 4, 5])

#Sem o visitado, a mesma busca limitada a 50 voltas para não travar o teste

def fecho_sem_visitado(afn, conjunto, limite=50):
    pilha = list(conjunto)
    voltas = 0
    while pilha and voltas < limite:
        atual = pilha.pop()
        voltas += 1
        for transicao in afn.transicoes[atual]:
            if transicao.simbolo == EPSILON:
                pilha.append(transicao.destino)

    return voltas, len(pilha)

voltas, sobrando = fecho_sem_visitado(c, [4])
print(f"sem visitado: parou à força depois de {voltas} voltas, com {sobrando} estados ainda na pilha")

#Validação herdada do Passo 1

print("\n--- validação ---")
conferir_erro("fecho de um estado que não existe", lambda: m.fecho_vazio([-1]),
              "Estado do conjunto inexistente: -1")

#Placar: código de saída 1 se alguma verificação falhar, para quem roda tudo de uma vez saber.
print(f"\nteste_passo2: {sum(resultados)}/{len(resultados)} verificações passaram.")
sys.exit(0 if all(resultados) else 1)