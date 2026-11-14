"""
Seis verificações:
  1. a máquina pequena de a*b: aceita e recusa, com vereditos decididos à mão;
  2. a máquina de (a|b)*c: o traço completo, passo a passo, conferido à mão;
  3. a parada: quando o conjunto ativo fica vazio, a simulação para de ler;
  4. o coringa em a.c: casa qualquer símbolo, mas não a falta de símbolo;
  5. a seta ε nunca casa com o caractere usado como rótulo de ε ("\\0");
  6. simular sem estado inicial definido gera erro.
"""

import sys

from afn import AFN, EPSILON, QUALQUER


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


# ---------------------------------------------------------------
# 1) a*b:  0 --a--> 0,  0 --ε--> 1,  1 --b--> 2   (inicial 0, aceitação 2)
# ---------------------------------------------------------------
print("--- 1) a*b: aceita e recusa ---")
m = AFN()
for _ in range(3):
    m.novo_estado()
m.adicionar_transicao(0, "a", 0)
m.adicionar_transicao(0, EPSILON, 1)
m.adicionar_transicao(1, "b", 2)
m.definir_inicial(0)
m.definir_aceitacao(2)

conferir("'ab'", m.aceita("ab"), True)      # um a, depois o b
conferir("'b'", m.aceita("b"), True)        # zero a: só funciona por causa do fecho do inicial
conferir("'aab'", m.aceita("aab"), True)    # vários a
conferir("'aa'", m.aceita("aa"), False)     # falta o b no fim
conferir("''", m.aceita(""), False)         # termina em {0, 1}, sem o 2
conferir("'ba'", m.aceita("ba"), False)     # depois do b, nada lê a

# ---------------------------------------------------------------
# 2) (a|b)*c, montada na ordem da construção de Thompson
# ---------------------------------------------------------------
print("\n--- 2) (a|b)*c: o traço passo a passo ---")
t = AFN()
for _ in range(10):
    t.novo_estado()
t.adicionar_transicao(0, "a", 1)        # folha a: estados 0 e 1
t.adicionar_transicao(2, "b", 3)        # folha b: estados 2 e 3
t.adicionar_transicao(4, EPSILON, 0)    # alternância: entrada 4, saída 5
t.adicionar_transicao(4, EPSILON, 2)
t.adicionar_transicao(1, EPSILON, 5)
t.adicionar_transicao(3, EPSILON, 5)
t.adicionar_transicao(6, EPSILON, 4)    # fecho: entrada 6, saída 7
t.adicionar_transicao(6, EPSILON, 7)
t.adicionar_transicao(5, EPSILON, 4)
t.adicionar_transicao(5, EPSILON, 7)
t.adicionar_transicao(8, "c", 9)        # folha c: estados 8 e 9
t.adicionar_transicao(7, EPSILON, 8)    # concatenação: liga o fecho ao c
t.definir_inicial(6)
t.definir_aceitacao(9)

sim = t.simular("abc")
print(t.formatar_simulacao("abc", sim))

conferir("início", sim.passos[0].ativos, [6, 4, 7, 8, 0, 2])
conferir("após 'a'", sim.passos[1].ativos, [1, 5, 4, 7, 8, 0, 2])
conferir("após 'b'", sim.passos[2].ativos, [3, 5, 4, 7, 8, 0, 2])
conferir("após 'c'", sim.passos[3].ativos, [9])
conferir("aceitou", sim.aceitou, True)
conferir("maior conjunto ativo", sim.maior_conjunto_ativo, 7)

# O conjunto inicial precisa ter mais de um estado: a máquina começa por um fecho.
# Se tivesse só o 6, faltaria aplicar o fecho vazio no inicial.
conferir("conjunto inicial tem mais de 1 estado", len(sim.passos[0].ativos) > 1, True)

conferir("'c' (zero repetições)", t.aceita("c"), True)
conferir("'abbac'", t.aceita("abbac"), True)
conferir("'abb' (falta o c)", t.aceita("abb"), False)

# ---------------------------------------------------------------
# 3) Parada: depois do c, só o 9 fica ativo, e do 9 não sai nada.
#    Lendo 'a' em seguida, o conjunto fica vazio e a simulação para.
# ---------------------------------------------------------------
print("\n--- 3) parada com o conjunto vazio ---")
sim = t.simular("cab")
conferir("'cab' recusada", sim.aceitou, False)
# início + 'c' + 'a' = 3 passos. O 'b' não chega a ser lido.
conferir("passos registrados", len(sim.passos), 3)
conferir("último conjunto", sim.passos[-1].ativos, [])

# ---------------------------------------------------------------
# 4) a.c:  0 --a--> 1,  1 --ε--> 2,  2 --qualquer--> 3,  3 --ε--> 4,  4 --c--> 5
# ---------------------------------------------------------------
print("\n--- 4) coringa em a.c ---")
k = AFN()
for _ in range(6):
    k.novo_estado()
k.adicionar_transicao(0, "a", 1)
k.adicionar_transicao(1, EPSILON, 2)
k.adicionar_transicao(2, QUALQUER, 3)
k.adicionar_transicao(3, EPSILON, 4)
k.adicionar_transicao(4, "c", 5)
k.definir_inicial(0)
k.definir_aceitacao(5)

conferir("'abc'", k.aceita("abc"), True)
conferir("'a c'", k.aceita("a c"), True)
conferir("'ac'", k.aceita("ac"), False)
conferir("'abbc'", k.aceita("abbc"), False)

# ---------------------------------------------------------------
# 5) Máquina que aceita só a cadeia vazia:  0 --ε--> 1
# ---------------------------------------------------------------
print("\n--- 5) seta ε não casa com o caractere \\0 ---")
v = AFN()
v.novo_estado()
v.novo_estado()
v.adicionar_transicao(0, EPSILON, 1)
v.definir_inicial(0)
v.definir_aceitacao(1)

conferir("cadeia vazia", v.aceita(""), True)
conferir("cadeia com o caractere \\0", v.aceita("\0"), False)

# ---------------------------------------------------------------
# 6) Simular sem estado inicial definido
# ---------------------------------------------------------------
print("\n--- 6) simular sem inicial ---")
sem_inicial = AFN()
sem_inicial.novo_estado()
conferir_erro("simular sem estado inicial", lambda: sem_inicial.simular("a"),
              "Defina o estado inicial e o de aceitação antes de simular")

#Placar: código de saída 1 se alguma verificação falhar, para quem roda tudo de uma vez saber.
print(f"\nteste_passo3: {sum(resultados)}/{len(resultados)} verificações passaram.")
sys.exit(0 if all(resultados) else 1)