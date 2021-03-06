from .token import Token
from .tipo_token import TipoToken

# Constante do tamanho do Buffer
TAM_BUFFER = 20


class AnalisadorLexico:

    def __init__(self, file_path):
        self.file_path = file_path
        self.token_list = list()
        self.read_buffer = [""] * (TAM_BUFFER * 2)  # Buffer de tamanho 10
        self.pointer = 0
        # Variável de controle para evitar a reescrita do Buffer 2 vezes
        self.buffer_atual = 1

        # Ponteiro para o início do lexema que estou tentando encontrar para reconhecê-lo
        self.inicio_lexema = 0
        self.lexema = ""  # Lexema completo reconhecido

        # Abrindo-se o arquivo programa de entrada
        try:
            self.f = open(file_path)
        except FileNotFoundError:
            print("Arquivo não encontrado")
        except IOError:
            print("Não foi possível abrir o arquivo")
        except EOFError:
            print("Não foi possível ler o arquivo")

    def ler_proximo_caractere(self) -> str:
        c = self.f.read(1)
        self.lexema += c
        return c

    # Recarrega o buffer da esquerda com a entrada, lendo byte por byte
    def recarregar_buffer_1(self):

        if self.buffer_atual == 2:
            self.buffer_atual = 1

            try:
                for i in range(TAM_BUFFER):
                    self.read_buffer[i] = self.ler_proximo_caractere()
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

        if self.buffer_atual == 1:
            self.buffer_atual = 2

            try:
                for i in range(TAM_BUFFER, TAM_BUFFER * 2):
                    self.read_buffer[i] = self.ler_proximo_caractere()
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

        self.lexema = self.lexema[:-1]  # Tirando-se o último caracter do lexema

        if self.pointer < 0:  # Cheguei no final do Buffer da esquerda
            self.pointer = TAM_BUFFER * 2 - 1  # Vai pro final do Buffer da direita

    # Inicializa o Buffer da esquerda com os caracteres do programa de entrada
    def inicializa_buffer(self):
        self.buffer_atual = 2

        self.recarregar_buffer_1()

    # Lendo os caracteres do Buffer de entrada
    def ler_char_do_buffer(self) -> str:
        char_atual = self.read_buffer[self.pointer]

        print(self.to_string())

        self.incrementar_ponteiro()

        return char_atual

    # Método para zerar o ponteiro de leitura toda vez que não foi possível reconhecer um padrão
    def zerar_ponteiro(self):
        self.pointer = self.inicio_lexema
        self.lexema = ""

    # Confirma um lexema que foi devidamente reconhecido
    def confirmar_lexema(self):
        self.inicio_lexema = self.pointer
        self.lexema = ""

    # Método para recuperar o lexema quando ele for lido
    def get_lexema(self) -> str:
        return self.lexema

    # Vai fazer a leitura do arquivo texto de entrada até reconhecer um padrão e retornar este token
    def proximo_token(self, char_lido: str) -> Token or None:

        # Ignorando espaços em brancos:
        if char_lido == " " or char_lido == "\n" or char_lido == "\t":
            return None



        # TODO Lembrar de tratar tokens que precisam ver mais de 1 token para ver seu resultado real
        # Vendo se o char lido é igual a menor ou menor ou igual

        return None

    def to_string(self):
        ret = "Buffer:["
        for i in self.read_buffer:
            if i == " " or i == "\n" or i == "\t":
                ret += " "
            else:
                ret += i

        ret += "]\n"
        ret += "        "

        for i in range(0, TAM_BUFFER * 2):
            if i == self.inicio_lexema and i == self.pointer:
                ret += "%"
            elif i == self.inicio_lexema:
                ret += "^"
            elif i == self.pointer:
                ret += "*"
            else:
                ret += " "

        return ret

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


    ## --- MÉTODOS PARA RECONHECER PADRÕES DE TOKENS -- ##


    def get_token_operador_aritmetico(self) -> Token or None:

        char_lido = self.ler_proximo_caractere()

        if char_lido == "*":
            return Token(TipoToken.OP_ARIT_MULTIPLICACAO, "*")
        elif char_lido == "+":
            return Token(TipoToken.OP_ARIT_SOMA, "+")
        elif char_lido == "/":
            return Token(TipoToken.OP_ARIT_DIVISAO, "/")
        elif char_lido == "-":
            return Token(TipoToken.OP_ARIT_SUBTRACAO, "-")
        else:
            return None

    def get_token_delimitador(self) -> Token or None:

        char_lido = self.ler_proximo_caractere()

        # TODO lembrar de fazer a lógica pra ver se é tipo de dado ou ternary-if
        # TODO fazer dos outros tokens delimitadores
        if char_lido == ":":
            return Token(TipoToken.DELIM_TIPO_DAD, ":")
        else:
            return None

    def get_token_operador_comparacao(self) -> Token or None:

        char_lido = self.ler_proximo_caractere()

        if char_lido == "<":
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
            new_char = self.ler_char_do_buffer()
            if new_char == "=":
                return Token(TipoToken.OP_COMP_MAIOR_OU_IGUAL, ">=")
            else:
                self.retroceder_ponteiro()
                return Token(TipoToken.OP_MAIOR, ">")

        elif char_lido == "=":
            new_char = self.ler_char_do_buffer()
            if new_char == "=":
                return Token(TipoToken.OP_COMP_IGUAL, "==")
            else:
                return None

        else:
            return None


    def get_token_parenteses(self) -> Token or None:
        char_lido = self.ler_proximo_caractere()

        if char_lido == "(":
            return Token(TipoToken.DELIM_ABRE_PARENTESES, "(")
        elif char_lido == ")":
            return Token(TipoToken.DELIM_FECHA_PARENTESES, ")")
        else:
            return None


    def get_token_numero(self) -> Token or None:
        estado = 1

        while True:
            c = self.ler_proximo_caractere()
            if estado == 1:
                if c.isdigit():
                    estado = 2
                else:
                    return None

            elif estado == 2:
                if c == ".":
                    c = self.ler_proximo_caractere()
                    if c.isdigit():
                        estado = 3
                    else:
                        return None
                elif not c.isdigit():
                    self.retroceder_ponteiro()
                    return Token(TipoToken.NUM_INT_CONST, self.get_lexema())

            elif estado == 3:
                if not c.isdigit():
                    self.retroceder_ponteiro()
                    return Token(TipoToken.NUM_FLAOT_CONST, self.get_lexema())


    def get_variavel_id(self) -> Token or None:
        # TODO se necessário, implementar a tipagem da variável
        # Lembrar que em Monga, as variáveis válidas tem até 32 caracteres
        estado = 1
        while True:
            c = self.ler_proximo_caractere()
            if estado == 1:
                if c.isalpha():
                    estado = 2
                else:
                    return None

            elif estado == 2:
                if not c.isalnum():
                    self.retroceder_ponteiro()
                    return Token(TipoToken.VAR_ID, self.get_lexema())


    def pular_espacos_e_comentarios(self) -> None:
        estado = 1
        while True:
            c = self.ler_proximo_caractere()
            if estado == 1:
                if c.isspace() or c == ' ':
                    estado = 2

                elif c == "#":
                    estado = 3

                else:
                    self.retroceder_ponteiro()
                    return None

            elif estado == 2:
                if c == "#":
                    estado = 3

                elif not c.isspace() or c == ' ':
                    self.retroceder_ponteiro()
                    return None

            elif estado == 3:
                if c == "\n":
                    return None
