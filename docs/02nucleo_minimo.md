# O núcle mínimo de operadores e as redações:

O critério de inclusão é apenas um:
1. A impossibilidade de redução/simplificação
    > Um operador que se exprime pela composição de outros é conveniência de quem escreve o pattern, não capacidade do sistema.


|Construção   |Papel                                 |
|-------------|--------------------------------------|
|Adição       |núcleo - soma entre um número e outro |
|Subtração    |núcleo - retirada de um valor x de y  |
|Multiplicação|folha - repetição da adição, mas existem reursos de hardware para executala|
|Divisão      |folha - repetição da subtração, além de contar QUANTAS iterações foram necessária, também possui recursos de hardware| 

Tudo mais que o usuário pode escrever é reduzido a isto durante a leitura.

# As reduções, em pares:
|Usuário escreve|Árvore recebe     |
|---------------|------------------|
|x+y            | som(x, y)        |
|y-x            | sub(x,y)         |
|x*3            | mult(x,y)        |
|x/2            | div(x,y)         |

## Descartado
**multiplicação e divisão como repetições da adição e subtração** respectivamente.
O próprio harware pode lidar com essas operações de forma muito mais eficiente (registradores MUL/IMUL, DIV/IDIV em x86).