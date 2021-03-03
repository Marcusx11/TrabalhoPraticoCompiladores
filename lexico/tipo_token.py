# Adicionando enumerações ao Python
from enum import Enum


# Referencia da construção desta classe: https://www.youtube.com/watch?v=36MOhcBz7p0&t=2312s

class TipoToken(Enum):
    # Classes de Tokens para as palavras-chave da linguagem
    PAL_CHAVE_AS = 1
    PAL_CHAVE_ELSE = 2
    PAL_CHAVE_FUNCTION = 3
    PAL_CHAVE_IF = 4
    PAL_CHAVE_NEW = 5
    PAL_CHAVE_RETURN = 6
    PAL_CHAVE_TYPE = 7
    PAL_CHAVE_VAR = 8
    PAL_CHAVE_WHILE = 9

    # Classes de Tokens para os operadores aritméticos
    OP_ARIT_SOMA = 10
    OP_ARIT_SUBTRACAO = 11
    OP_ARIT_MULTIPLICACAO = 12
    OP_ARIT_DIVISAO = 13

    # Classes de Tokens para operadores booleanos
    OP_BOOL_AND = 14
    OP_BOOL_OR = 15
    OP_BOOL_NOT = 16

    # Classes de Tokens para delimitadores
    DELIM_TIPO_DADO = 17
    DELIM_ABRE_PARENTESES = 18
    DELIM_FECHA_PARENTESES = 19
    DELIM_ABRE_CHAVES = 20
    DELIM_FECHA_CHAVES = 21
    DELIM_PONTO = 22
    DELIM_VIRGULA = 23
    DELIM_PONTO_E_VIRGULA = 24
    DELIM_ATRIBUICAO = 25

    # Classes de Tokens para as palavras-chaves dos tipos de dados
    PAL_CHAVE_TIPO_INT = 26
    PAL_CHAVE_TIPO_FLOAT = 27
    PAL_CHAVE_TIPO_RECORD = 28

    # Classes de Tokens para os operadores de comparação
    OP_COMP_IGUAL = 29
    OP_COMP_DIF = 30
    OP_COMP_MENOR_OU_IGUAL = 31
    OP_COMP_MAIOR_OU_IGUAL = 32
    OP_MENOR = 33
    OP_MAIOR = 34
    OP_COND_TERNARIO_TRUE = 35
    OP_COND_TERNARIO_FALSE = 41

    # Classes de Tokens para identificadores
    ID = 36

    # Classes de Tokens para constantes
    NUM_INT_CONST = 37
    NUM_FLAOT_CONST = 38

    # Classes de Tokens para Arrays
    ARRAY_ABRE_COLCHETES = 39
    ARRAY_FECHA_COLCHETES = 40

    # Operador para imprimir o valor de uma expressão
    OP_IMPRIME_VALOR = 42


