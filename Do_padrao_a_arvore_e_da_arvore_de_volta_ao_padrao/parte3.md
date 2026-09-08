## Reduções

| Escrita de conveniência | No núcleo | Como se confere |
|---|---|---|
| `[0-9]` | `0\|1\|2\|3\|4\|5\|6\|7\|8\|9` | a faixa vira união símbolo por símbolo — confere contando 0, 1, 2... até 9, sem pular nenhum |
| `[a-z]` | `a\|b\|c\|...\|z` | a faixa vira união símbolo por símbolo — confere contando a, b .. até z, sem pular nenhum |
| `[a-z0-9]` | `a\|b\|c\|...\|z\|0\|1\|...\|9` | duas faixas conferidas separadamente e depois juntadas dois a dois |
