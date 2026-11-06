"""
Leitor de padrões: transforma o TEXTO de um padrão, como "[0-9]+", na
árvore de arvore.py, que a construção de Thompson recebe.

Gramática lida (do nível mais fraco para o mais forte):
    alternancia  := concatenacao ( "|" concatenacao )*
    concatenacao := repeticao repeticao*
    repeticao    := atomo ( "*" | "+" | "?" )*
    atomo        := simbolo | "." | "\\" simbolo | "[" classe "]" | "(" alternancia ")"

O açúcar é reduzido aqui, na leitura, e não chega na árvore:
    x+     ->  concatenacao(x, fecho(x))
    x?     ->  alternancia(x, vazio())
    [abc]  ->  alternancia(alternancia(a, b), c)
    [a-c]  ->  a mesma enumeração, com a faixa expandida símbolo por símbolo

Um padrão malformado gera ErroDeLeitura com duas posições, contadas a partir de 1:
    posicao  ->  onde a leitura constatou o problema. Quando algo abre e não
                 fecha, é o fim do texto, onde a pessoa vai digitar a correção.
    origem   ->  onde o defeito começou (o "(" ou o "[" que ficou aberto),
                 quando é diferente da posição constatada.
mostrar_erro repete o texto e põe a marca ^ embaixo da posição constatada.
"""

from arvore import simbolo, qualquer, vazio, concatenacao, alternancia, fecho

#Símbolos com significado especial: | * + ? . ( ) [ ] \
#Para usar um deles como símbolo comum, escreve-se uma barra antes:
#"\+" é o símbolo +, "\." é o ponto.


class ErroDeLeitura(ValueError):

    #Erro de um padrão malformado: a mensagem e a posição do problema.
    #origem fica None quando o defeito começa no mesmo lugar em que foi constatado.

    def __init__(self, mensagem, posicao, origem=None):
        super().__init__(f"posição {posicao}: {mensagem}")
        self.mensagem = mensagem
        self.posicao = posicao
        self.origem = origem


def mostrar_erro(texto, erro):

    #Repete o texto e põe a marca ^ na linha de baixo, sob a posição constatada.
    #Assim quem escreveu não precisa contar caracteres com o dedo.
    #Quando a falta é constatada no fim, a marca fica depois do último caractere.

    marca = " " * (erro.posicao - 1) + "^"
    return f"{texto}\n{marca} {erro.mensagem} (posição {erro.posicao})"


def ler_padrao(texto):

    #Lê o padrão inteiro e devolve a raiz da árvore.
    #Padrão vazio devolve None: a construção de Thompson faz a máquina da cadeia vazia.

    if texto == "":
        return None

    leitor = _Leitor(texto)
    raiz = leitor.alternancia()

    #Se a leitura terminou antes do fim do texto, sobrou alguma coisa.
    if not leitor.no_fim():
        sobra = leitor.atual()
        raise ErroDeLeitura(f"Símbolo {sobra} sobrando; o padrão já havia terminado", leitor.pos + 1)

    return raiz


class _Leitor:

    #Lê o texto da esquerda para a direita. "pos" é a posição do próximo símbolo.

    def __init__(self, texto):
        self.texto = texto
        self.pos = 0

    def no_fim(self):
        return self.pos >= len(self.texto)

    def atual(self):
        return self.texto[self.pos]

    def avancar(self):
        caractere = self.texto[self.pos]
        self.pos += 1
        return caractere

    #Cada regra da gramática vira um método, e um método chama o do nível de baixo.

    def alternancia(self):
        esquerda = self.concatenacao()
        while not self.no_fim() and self.atual() == "|":
            self.avancar()
            direita = self.concatenacao()
            esquerda = alternancia(esquerda, direita)
        return esquerda

    def concatenacao(self):
        #Uma concatenação precisa de pelo menos um elemento.
        if self.no_fim() or self.atual() in "|)":
            raise ErroDeLeitura("Falta um elemento nesta posição (alternativa ou grupo vazio)", self.pos + 1)

        no = self.repeticao()
        while not self.no_fim() and self.atual() not in "|)":
            no = concatenacao(no, self.repeticao())
        return no

    def repeticao(self):
        no = self.atomo()
        #Aceita mais de um operador seguido, como em a** (um fecho de um fecho).
        while not self.no_fim() and self.atual() in "*+?":
            operador = self.avancar()
            if operador == "*":
                no = fecho(no)
            elif operador == "+":
                no = concatenacao(no, fecho(no))     # x+ -> x x*
            else:
                no = alternancia(no, vazio())        # x? -> x | ε
        return no

    def atomo(self):
        inicio = self.pos
        caractere = self.atual()

        if caractere in "*+?":
            raise ErroDeLeitura("Repetição não tem elemento à esquerda para repetir", inicio + 1)

        if caractere == "(":
            self.avancar()
            interior = self.alternancia()
            if self.no_fim() or self.atual() != ")":
                raise ErroDeLeitura(f"Grupo aberto na posição {inicio + 1} não foi fechado antes do fim do padrão",
                                    self.pos + 1, origem=inicio + 1)
            self.avancar()
            return interior

        if caractere == "[":
            return self.classe()

        if caractere == ".":
            self.avancar()
            return qualquer()

        if caractere == "\\":
            self.avancar()
            if self.no_fim():
                raise ErroDeLeitura(f"Barra na posição {inicio + 1} está no fim do padrão, sem símbolo depois dela",
                                    self.pos + 1, origem=inicio + 1)
            return simbolo(self.avancar())

        return simbolo(self.avancar())

    def classe(self):
        inicio = self.pos
        self.avancar()   # o "["

        if not self.no_fim() and self.atual() == "^":
            raise ErroDeLeitura("Classe negada ([^...]) não é aceita", self.pos + 1, origem=inicio + 1)

        simbolos = []
        while not self.no_fim() and self.atual() != "]":
            inicio_da_faixa = self.pos
            primeiro = self._simbolo_da_classe()

            #Faixa: "a-c". O "-" só é faixa se houver um símbolo depois dele antes do "]".
            if (self.pos + 1 < len(self.texto) and self.atual() == "-"
                    and self.texto[self.pos + 1] != "]"):
                self.avancar()   # o "-"
                ultimo = self._simbolo_da_classe()
                if ord(ultimo) < ord(primeiro):
                    #Constatada no último símbolo da faixa; começa no primeiro.
                    raise ErroDeLeitura(f"Faixa invertida: {primeiro}-{ultimo}", self.pos,
                                        origem=inicio_da_faixa + 1)
                for codigo in range(ord(primeiro), ord(ultimo) + 1):
                    simbolos.append(chr(codigo))
            else:
                simbolos.append(primeiro)

        if self.no_fim():
            raise ErroDeLeitura(f"Classe aberta na posição {inicio + 1} não foi fechada com ]",
                                self.pos + 1, origem=inicio + 1)
        self.avancar()   # o "]"

        #Um símbolo repetido ([aa] ou [a-ca]) entra uma vez só.
        sem_repetir = list(dict.fromkeys(simbolos))
        if not sem_repetir:
            #Constatada no "]", que fecha a classe sem nada dentro.
            raise ErroDeLeitura("Classe vazia", self.pos, origem=inicio + 1)

        #[abc] -> alternancia(alternancia(a, b), c): aninhada pela esquerda
        no = simbolo(sem_repetir[0])
        for caractere in sem_repetir[1:]:
            no = alternancia(no, simbolo(caractere))
        return no

    def _simbolo_da_classe(self):
        #Dentro da classe, a barra também escapa: [\]] é o símbolo ].
        caractere = self.avancar()
        if caractere == "\\":
            if self.no_fim():
                raise ErroDeLeitura(f"Barra na posição {self.pos} está no fim do padrão, sem símbolo depois dela",
                                    self.pos + 1, origem=self.pos)
            caractere = self.avancar()
        return caractere