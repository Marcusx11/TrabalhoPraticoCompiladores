# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from lexico import token
from lexico import tipo_token, analisador_lexico
from antlr4 import *
import sys



if __name__ == '__main__':
    lexico = analisador_lexico.AnalisadorLexico("programa")
    lexico.inicializa_buffer()


    while True:
        t = lexico.proximo_token()

        if t:
            print(t.to_string())

            if t.tipo_token == tipo_token.TipoToken.FIM_DE_ARQUIVO:
                break


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
