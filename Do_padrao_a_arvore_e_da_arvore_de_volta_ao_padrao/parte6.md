## O que a máquina precisaria lembrar

| Requisito | O que precisaria lembrar | Tem teto? | Onde se resolve |
|---|---|---|---|
| O literal Inteiro cabe no `int` (de 0 a 2147483647)? | quantos dígitos significativos já leu e se, até ali, o número está igual ao limite ou já ficou abaixo dele | Sim — no máximo 10 dígitos significativos; o limite é o do `int` do Java, base da Solis | Cabe nos três operadores: uma alternativa por posição em que o número fica abaixo do limite (expressão no item 5 do `Estruturacao_Completa.md`) |
| Variável usada foi declarada antes? | todos os nomes de variável já vistos no programa até aquele ponto | Não — cresce com o tamanho do programa | Fora da classe léxica; verificação de fase posterior (tabela de símbolos) |