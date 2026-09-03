1: Identificador
	Exemplo: soma
	Padrão: [a-z][az0-9_]*
	Padrão no núcleo: L|(L|D|_)*
	Forma linear: concat(L, fecho(alt(alt(L, D), '_'))
	Nós: (26 símbolos + 25 alternâncias) + (37 símbolos + 36 alternâncias) + 1 fecho + concatenação = 126 nós
