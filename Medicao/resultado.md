# Resultado da medição da seção 7

## A pergunta

A [seção 7 da especificação](../especificacao/especificacao.md) pergunta: processar os registros com
a máquina determinística mínima de cada padrão é mais rápido do que simular a máquina não
determinística construída direto do padrão? A expectativa escrita antes de medir era que sim, porque
a máquina determinística faz um passo só por símbolo lido. Dois casos poderiam contrariá-la:
registros curtos com padrões simples, e o padrão "o n-ésimo símbolo contado do fim é `a`", em que a
máquina determinística chega a 2ⁿ estados.

## Como foi medido

Pelo [`medir.py`](medir.py), que roda com `python Medicao/medir.py` a partir da raiz do projeto (e
também faz parte do `rodar_tudo.py`). Para cada padrão, ele monta o AFN de Thompson e o AFD mínimo,
gera registros com a semente fixa 2026 e cronometra as duas máquinas decidindo os mesmos registros.
Os registros têm só os símbolos do alfabeto do padrão, metade casa e metade não casa, e são 60 de
cada tamanho: curto, com 5 símbolos; médio, com 50; e longo, com 500. Um registro que casa pode sair
um pouco maior, porque o caminho até a aceitação pode pedir mais símbolos. Cada tempo é a mediana
de 5 repetições, dividida pelo número de registros.

Os padrões são os da especificação (quantidade, preço, pedido, e-mail e valor), o preço escrito com
o coringa no lugar de `(,|\.)`, e o n-ésimo do fim, com n de 1 a 8.

Os números abaixo vêm de três execuções: duas num computador com Linux (x86_64, Python 3.13.18) e uma
num computador com Windows (AMD64, Python 3.13.17). Mais duas execuções, uma em cada computador,
deram a mesma direção e não entram nas tabelas.

## A conferência

Antes de comparar tempo, as duas máquinas foram comparadas com um oráculo de fora, o `re.fullmatch`
do Python. Nas três execuções, **2520 de 2520 registros** tiveram a mesma resposta nas duas máquinas
e no oráculo. Sem isso, a comparação de tempo não valeria nada.

## O tamanho das máquinas

O tamanho é o mesmo em qualquer computador, porque a construção não depende dele. O tempo de montagem
varia, e a tabela mostra o menor e o maior das três execuções.

| Padrão | AFN (estados/setas) | AFD mínimo (estados/setas) | Montar o AFN (ms) | Montar o AFD (ms) |
|---|---|---|---|---|
| quantidade | 78/97 | 2/20 | 0,14 a 0,33 | 2,61 a 2,95 |
| preço | 160/198 | 6/72 | 0,22 a 0,30 | 5,09 a 6,45 |
| preço com coringa | 156/193 | 5/50 | 0,21 a 0,29 | 9,24 a 12,54 |
| pedido | 80/99 | 4/44 | 0,12 a 0,19 | 2,63 a 3,42 |
| e-mail | 520/646 | 12/468 | 0,71 a 0,92 | 155,04 a 219,86 |
| valor | 162/199 | 9/126 | 0,22 a 0,40 | 6,09 a 9,01 |
| n-ésimo do fim, n = 1 | 10/12 | 2/4 | 0,04 a 0,06 | 0,10 a 0,14 |
| n-ésimo do fim, n = 2 | 16/19 | 4/8 | 0,04 a 0,07 | 0,14 a 0,21 |
| n-ésimo do fim, n = 3 | 22/26 | 8/16 | 0,05 a 0,05 | 0,22 a 0,24 |
| n-ésimo do fim, n = 4 | 28/33 | 16/32 | 0,05 a 0,06 | 0,41 a 0,57 |
| n-ésimo do fim, n = 5 | 34/40 | 32/64 | 0,06 a 0,07 | 0,84 a 1,23 |
| n-ésimo do fim, n = 6 | 40/47 | 64/128 | 0,07 a 0,08 | 1,94 a 3,42 |
| n-ésimo do fim, n = 7 | 46/54 | 128/256 | 0,08 a 0,18 | 8,32 a 10,51 |
| n-ésimo do fim, n = 8 | 52/61 | 256/512 | 0,09 a 0,12 | 13,20 a 18,43 |

## O tempo por registro

As duas colunas de tempo são da execução no Windows. A última coluna mostra quantas vezes o AFN foi
mais lento que o AFD, do menor ao maior valor nas três execuções.

| Padrão | Tamanho | AFN (µs) | AFD mínimo (µs) | AFN / AFD nas 3 execuções |
|---|---|---|---|---|
| quantidade | curto | 70,4 | 0,5 | 105,2x a 154,4x |
| quantidade | médio | 564,3 | 3,2 | 177,3x a 225,5x |
| quantidade | longo | 5814,4 | 32,7 | 178,0x a 211,7x |
| preço | curto | 68,6 | 0,4 | 128,0x a 161,3x |
| preço | médio | 111,7 | 2,2 | 50,3x a 98,6x |
| preço | longo | 90,4 | 17,4 | 5,2x a 7,8x |
| preço com coringa | curto | 91,3 | 0,5 | 186,4x a 331,3x |
| preço com coringa | médio | 1189,3 | 3,4 | 348,8x a 633,7x |
| preço com coringa | longo | 9983,8 | 17,6 | 565,7x a 662,8x |
| pedido | curto | 14,9 | 0,3 | 55,0x a 67,1x |
| pedido | médio | 214,0 | 1,9 | 96,9x a 110,9x |
| pedido | longo | 1672,5 | 15,9 | 101,1x a 105,0x |
| e-mail | curto | 147,7 | 0,4 | 351,7x a 440,8x |
| e-mail | médio | 736,0 | 1,9 | 377,7x a 433,5x |
| e-mail | longo | 967,3 | 11,7 | 82,5x a 99,9x |
| valor | curto | 18,0 | 0,3 | 55,8x a 69,1x |
| valor | médio | 37,4 | 1,3 | 27,9x a 32,4x |
| valor | longo | 59,6 | 11,1 | 5,4x a 6,7x |
| n-ésimo do fim, n = 1 | curto | 12,1 | 0,3 | 44,9x a 53,1x |
| n-ésimo do fim, n = 1 | médio | 110,9 | 1,7 | 66,0x a 71,7x |
| n-ésimo do fim, n = 1 | longo | 1115,9 | 15,6 | 71,3x a 79,8x |
| n-ésimo do fim, n = 2 | curto | 15,7 | 0,3 | 46,3x a 68,5x |
| n-ésimo do fim, n = 2 | médio | 142,9 | 1,6 | 87,1x a 95,9x |
| n-ésimo do fim, n = 2 | longo | 1434,2 | 15,6 | 92,1x a 104,8x |
| n-ésimo do fim, n = 3 | curto | 17,8 | 0,3 | 66,0x a 100,9x |
| n-ésimo do fim, n = 3 | médio | 176,7 | 1,7 | 107,0x a 118,3x |
| n-ésimo do fim, n = 3 | longo | 1741,4 | 16,2 | 107,5x a 128,3x |
| n-ésimo do fim, n = 4 | curto | 20,5 | 0,3 | 72,7x a 86,4x |
| n-ésimo do fim, n = 4 | médio | 206,2 | 1,7 | 123,2x a 153,1x |
| n-ésimo do fim, n = 4 | longo | 2101,4 | 15,5 | 135,4x a 150,5x |
| n-ésimo do fim, n = 5 | curto | 19,2 | 0,3 | 72,0x a 86,0x |
| n-ésimo do fim, n = 5 | médio | 230,5 | 1,7 | 138,6x a 172,7x |
| n-ésimo do fim, n = 5 | longo | 2450,3 | 15,7 | 156,2x a 175,9x |
| n-ésimo do fim, n = 6 | curto | 25,6 | 0,3 | 87,9x a 108,1x |
| n-ésimo do fim, n = 6 | médio | 277,7 | 1,6 | 168,5x a 185,6x |
| n-ésimo do fim, n = 6 | longo | 2831,5 | 15,5 | 182,7x a 197,3x |
| n-ésimo do fim, n = 7 | curto | 29,7 | 0,3 | 97,5x a 120,7x |
| n-ésimo do fim, n = 7 | médio | 312,6 | 1,8 | 176,6x a 222,6x |
| n-ésimo do fim, n = 7 | longo | 3324,6 | 17,5 | 189,6x a 218,7x |
| n-ésimo do fim, n = 8 | curto | 34,5 | 0,3 | 82,1x a 115,7x |
| n-ésimo do fim, n = 8 | médio | 358,7 | 1,8 | 198,0x a 214,8x |
| n-ésimo do fim, n = 8 | longo | 3728,5 | 15,8 | 228,2x a 235,9x |

## A resposta

**A expectativa se confirma: o AFD mínimo foi mais rápido em todos os padrões, em todos os tamanhos e
nas três execuções**, de 5,2 vezes (preço longo) a 662,8 vezes (preço com coringa longo).

Os dois casos que poderiam contrariar a expectativa não a contrariaram:

- **Registros curtos:** com 5 símbolos, o AFD foi de 44,9 a 440,8 vezes mais rápido. A vantagem
  diminui em alguns padrões, mas não some.
- **O n-ésimo do fim:** com n = 8, o AFD mínimo tem 256 estados e 512 setas, contra 52 estados e 61
  setas do AFN, e mesmo assim foi de 82,1 a 235,9 vezes mais rápido por registro. O AFD passa a ter
  mais setas que o AFN a partir de n = 5 (64 contra 40) e mais estados a partir de n = 6 (64 contra
  40). O custo desse crescimento aparece no tamanho da tabela, e não no tempo por registro.

## O que a medição não diz

- **O tamanho da vantagem é exagerado pela implementação.** A cada símbolo lido, o `fecho_vazio` do
  AFN cria uma lista do tamanho da máquina inteira e valida cada estado. Parte da diferença vem
  disso, e não só de acompanhar um conjunto de estados em vez de um estado só. O que a medição
  sustenta é a direção; o número de vezes não deve ser levado ao pé da letra.
- **O AFN para cedo, e o AFD não.** Quando não sobra estado ativo, a simulação do AFN para. O
  `aceita` do AFD lê o registro até o fim, mesmo depois de cair no estado de erro. É por isso que a
  vantagem é menor no preço e no valor longos (de 5,2 a 7,8 vezes): os registros que não casam
  morrem logo no AFN.
- **Montar o AFD custa mais, mas esse custo é do compilador.** O AFD do e-mail levou de 155 a 220 ms
  para ser montado, contra menos de 1 ms do AFN. Na Solis, a máquina é montada uma vez, na
  compilação, e gravada no objeto: o executor carrega a tabela e não paga a montagem. O que pesa
  para ele é o tamanho da tabela, medido aqui em estados e setas, e não em bytes, porque o formato
  do objeto ainda não foi escrito. No e-mail, a tabela do AFD é menor que a do AFN (468 setas
  contra 646).
- **Em dois padrões, todos os registros casam.** Com só os símbolos do próprio padrão, não existe
  texto de dígitos que não case com `[0-9]+`, nem com o preço com coringa, a partir de 4 dígitos.
  Nesses dois, os 180 registros casam.
- **Os registros só têm os símbolos do padrão.** Um símbolo fora do alfabeto do padrão, como o `b`
  em `abc` lido pelo padrão `a.c`, depende da coluna do outro, que é pendência do executor. Fora
  dessa situação, as duas máquinas concordam, como a conferência mostrou.
- **Os tempos variam entre execuções.** Nos tempos abaixo de 1 µs, a proporção muda bastante de uma
  execução para outra (o preço com coringa médio foi de 348,8 a 633,7 vezes), mas a direção não
  mudou em nenhuma das 42 linhas, em nenhuma execução.
