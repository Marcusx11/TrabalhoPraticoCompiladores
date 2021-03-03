from .token import Token
from .tipo_token import TipoToken

# Constante do tamanho do Buffer
TAM_BUFFER = 5


class AnalisadorLexico:

    def __init__(self, file_path):
        self.file_path = file_path
        self.token_list = list()
        self.read_buffer = [""] * (TAM_BUFFER * 2)  # Buffer de tamanho 10
        self.pointer = 0

        # Abrindo-se o arquivo programa de entrada
        try:
            self.f = open(file_path)
        except FileNotFoundError:
            print("Arquivo não encontrado")
        except IOError:
            print("Não foi possível abrir o arquivo")
        except EOFError:
            print("Não foi possível ler o arquivo")

    # Recarrega o buffer da esquerda com a entrada, lendo byte por byte
    def recarregar_buffer_1(self):
        try:
            for i in range(TAM_BUFFER):
                self.read_buffer[i] = self.f.read(1)
                if self.read_buffer[i] == "":  # Fim de arquivo
                    break

        except FileNotFoundError:
            print("Arquivo não encontrado")
        except IOError:
            print("Não foi possível abrir o arquivo")
        except EOFError:
            print("Não foi possível ler o arquivo")

    # Recarrega o buffer da direita com a entrada, lendo byte por byte
    def recarregar_buffer_2(self):
        try:
            for i in range(TAM_BUFFER, TAM_BUFFER * 2):
                self.read_buffer[i] = self.f.read(1)
                if self.read_buffer[i] == "":  # Fim de arquivo
                    break

        except FileNotFoundError:
            print("Arquivo não encontrado")
        except IOError:
            print("Não foi possível abrir o arquivo")
        except EOFError:
            print("Não foi possível ler o arquivo")

    # Incrementa o ponteiro realizando a lógica circular de 2 buffers
    def incrementar_ponteiro(self):
        self.pointer += 1
        # Ponteiro com lógica circular
        if self.pointer == TAM_BUFFER:  # Cheguei na metade do Buffer(Fim do buffer da esquerda)
            self.recarregar_buffer_2()
        elif self.pointer == TAM_BUFFER * 2:  # Cheguei no final do Buffer(Fim do buffer da direita)
            self.recarregar_buffer_1()
            self.pointer = 0

    # Retrocede o ponteiro realizando também a lógica circular de 2 buffers
    def retroceder_ponteiro(self):
        self.pointer -= 1

        if self.pointer < 0:  # Cheguei no final do Buffer da esquerda
            self.pointer = TAM_BUFFER * 2 - 1  # Vai pro final do Buffer da direita

    # Inicializa o Buffer da esquerda com os caracteres do programa de entrada
    def inicializa_buffer(self):
        self.recarregar_buffer_1()

    # Lendo os caracteres do Buffer de entrada
    def ler_char_do_buffer(self) -> str:
        char_atual = self.read_buffer[self.pointer]
        self.incrementar_ponteiro()

        return char_atual

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
        # Vendo se o char lido é igual a menor ou menor ou igual
        elif char_lido == "<":
            new_char = self.ler_char_do_buffer()
            if new_char == "=":
                return Token(TipoToken.OP_COMP_MENOR_OU_IGUAL, "<=")
            else:
                self.retroceder_ponteiro()
                return Token(TipoToken.OP_MENOR, "<")

        # Vendo se o char lido é igual ao de diferença entre expressões
        elif char_lido == "~":
            new_char = self.ler_char_do_buffer()
            if new_char == "=":
                return Token(TipoToken.OP_COMP_DIF, "~=")

        # Vendo se o char lido é igual a maior ou maior ou igual
        elif char_lido == ">":
S            new_char = self.ler_char_do_buffer()
            if new_char == "=":
                return Token(TipoToken.OP_COMP_MAIOR_OU_IGUAL, ">=")
            else:
                self.retroceder_ponteiro()
                return Token(TipoToken.OP_MAIOR, ">")

        return None

    def ler_arquivo(self):
        self.inicializa_buffer()

        while True:
            # Lendo caractére por caractére
            caracter = self.ler_char_do_buffer()

            print(caracter, end="")

            # Fim de arquivo
            if not caracter:
                break

            token = self.proximo_token(caracter)

            if token:
                self.token_list.append(token)

        self.f.close()
        for i in self.token_list:
            print(i.to_string())
