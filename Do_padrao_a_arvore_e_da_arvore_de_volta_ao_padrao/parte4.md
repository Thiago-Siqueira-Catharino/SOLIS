| Peça | Padrão | Caracteres | Nós da árvore reduzida |
|---|---|---|---|
| Inteiro | `[0-9]+` | 6 | 40 |
| Identificador | `[a-z][a-z0-9]*` | 14 | 124 |

## Inteiro — [0-9]+

concat( D, fecho( D ) )
onde D = alt(alt(alt(alt(alt(alt(alt(alt(alt('0','1'),'2'),'3'),'4'),'5'),'6'),'7'),'8'),'9')
(10 folhas, 9 alt → 19 nós)

Filho esquerdo do concat: D sozinho = 19
Filho direito do concat: fecho(D) = D (19) + 1 nó de fecho = 20
Soma do concat: 19 + 20 + 1 (nó do concat) = 40

## Identificador — [a-z][a-z0-9]*

concat(L, fecho(LD))

onde L = alt(alt(alt(alt(alt(alt(alt(alt(alt(alt(alt(alt(alt(alt(alt(alt(alt(alt(alt(alt(alt(alt(alt(alt(alt('a','b'),'c'),'d'),'e'),'f'),'g'),'h'),'i'),'j'),'k'),'l'),'m'),'n'),'o'),'p'),'q'),'r'),'s'),'t'),'u'),'v'),'w'),'x'),'y'),'z')
(26 folhas, 25 alt → 51 nós)

LD = alt(alt(alt(alt(alt(alt(alt(alt(alt(alt(L,'0'),'1'),'2'),'3'),'4'),'5'),'6'),'7'),'8'),'9')
(continua a partir de L: +10 folhas, +10 alt → 51+10+10 = 71 nós)

Filho esquerdo do concat: L sozinho = 51
Filho direito do concat: fecho(LD) = LD (71) + 1 nó de fecho = 72
Soma do concat: 51 + 72 + 1 (nó do concat) = 124