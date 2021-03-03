from .token import Token
from .tipo_token import TipoToken


class AnalisadorLexico:

    def __init__(self, file_path):
        self.file_path = file_path
        self.token_list = list()

    # Vai fazer a leitura do arquivo texto de entrada até reconhecer um padrão e retornar este token
    def proximo_token(self, char_lido: str) -> Token or None:

        # Ignorando espaços em brancos:
        if char_lido == " " or char_lido == "\n" or char_lido == "\t":
            return None

        # Tokens de 1 caracter
        if char_lido == "(":
            return Token(TipoToken.DELIM_ABRE_PARENTESES, "(")
        elif char_lido == ")":
            return Token(TipoToken.DELIM_FECHA_PARENTESES, ")")
        elif char_lido == "*":
            return Token(TipoToken.OP_ARIT_MULTIPLICACAO, "*")
        elif char_lido == "+":
            return Token(TipoToken.OP_ARIT_SOMA, "+")
        elif char_lido == "/":
            return Token(TipoToken.OP_ARIT_DIVISAO, "/")
        elif char_lido == "-":
            return Token(TipoToken.OP_ARIT_SUBTRACAO, "-")
        elif char_lido == "?":
            return Token(TipoToken.OP_COND_TERNARIO_TRUE, "?")
        elif char_lido == ";":
            return Token(TipoToken.DELIM_PONTO_E_VIRGULA, ";")
        elif char_lido == "{":
            return Token(TipoToken.DELIM_ABRE_CHAVES, "{")
        elif char_lido == "}":
            return Token(TipoToken.DELIM_FECHA_CHAVES, "}")
        elif char_lido == "[":
            return Token(TipoToken.ARRAY_ABRE_COLCHETES, "[")
        elif char_lido == "]":
            return Token(TipoToken.ARRAY_FECHA_COLCHETES, "]")
        elif char_lido == "!":
            return Token(TipoToken.OP_BOOL_NOT, "!")
        elif char_lido == ",":
            return Token(TipoToken.DELIM_VIRGULA, ",")
        elif char_lido == "@":
            return Token(TipoToken.OP_IMPRIME_VALOR, "@")
        elif char_lido == ".":
            return Token(TipoToken.DELIM_PONTO, ".")

        # TODO Lembrar de tratar tokens que precisam ver mais de 1 token para ver seu resultado real

    def ler_arquivo(self):

        try:
            # Abrindo-se o caminho do arquivo passado como parâmetro à classe
            with open(self.file_path) as f:

                while True:
                    # Lendo caractére por caractére
                    caracter = f.read(1)

                    # Fim de arquivo
                    if not caracter:
                        break

                    token = self.proximo_token(caracter)

                    if token:
                        self.token_list.append(token)

        except FileNotFoundError:
            print("Arquivo não encontrado")
        except IOError:
            print("Não foi possível abrir o arquivo")
        finally:
            f.close()
            for i in self.token_list:
                print(i.to_string())
