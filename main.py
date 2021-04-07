# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from lexico import token
from lexico import tipo_token, analisador_lexico
from sintatico import parser
from sys import argv



if __name__ == '__main__':
    lexico = analisador_lexico.AnalisadorLexico(argv[1])
    lexico.inicializa_buffer()

    while True:
        t = lexico.proximo_token()

        if t:
            print(t.to_string())

            if t.tipo_token == tipo_token.TipoToken.FIM_DE_ARQUIVO:
                break


