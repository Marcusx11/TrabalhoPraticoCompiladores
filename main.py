# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from lexico import token
from lexico import tipo_token, analisador_lexico


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    a = token.Token(tipo_token.TipoToken.ID, "variavel1")
    print(a.to_string())

    lexico = analisador_lexico.AnalisadorLexico("programa")
    lexico.ler_arquivo()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
