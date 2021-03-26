from lexico import analisador_lexico, token, tipo_token

TAM_BUFFER = 10


class Parser:
    def __init__(self, lexico: analisador_lexico.AnalisadorLexico):
        self.buffer_tokens = list()
        self.lexico = lexico
        self.chegou_no_fim = False

        # Leitura de um token
        self.ler_token()

    # Vai procurar o token no léxico e preencher o buffer de Tokens
    def ler_token(self):
        if len(self.buffer_tokens) > 0:
            remove = self.buffer_tokens[0]
            self.buffer_tokens.remove(remove)

        # Carregando o Buffer
        while len(self.buffer_tokens) < TAM_BUFFER and not self.chegou_no_fim:
            proximo = self.lexico.proximo_token()
            self.buffer_tokens.append(proximo)

            if proximo:
                if proximo.tipo_token == tipo_token.TipoToken.FIM_DE_ARQUIVO:
                    self.chegou_no_fim = True

        print("Lido: " + str(self.look_ahead(1).to_string()))

    # Vai olhar "k" símbolos a frente para tomar uma decisão
    def look_ahead(self, k) -> token.Token or None:

        if len(self.buffer_tokens) == 0:
            return token.Token(tipo_token.TipoToken.FIM_DE_ARQUIVO, "$")

        if k - 1 >= len(self.buffer_tokens):
            buffer_len = len(self.buffer_tokens)
            return self.buffer_tokens[buffer_len - 1]

        return self.buffer_tokens[k - 1]

    # Vai pegar os tipos dos Tokens que esteja esperando e compara-os com o tipo passado como parametro
    def match(self, tipo: tipo_token.TipoToken):
        if self.look_ahead(1).tipo_token == tipo:
            print("Match: " + str(self.look_ahead(1).to_string()))
            self.ler_token()  # Avança na leitura
        else:
            # Inserindo a lista como parâmetro
            lista_tipo_tokens = list()
            lista_tipo_tokens.append(tipo)

            self.erro_sintatico(lista_tipo_tokens)

    def erro_sintatico(self, tokens_esperados):
        mensagem = "Erro sintático! Esperando os demais tokens: ("

        for i in range(len(tokens_esperados)):
            mensagem += str(tokens_esperados[i])

            if i < len(tokens_esperados) - 1:
                mensagem += ", "

        mensagem += "), mas foi encontrado: " + str(self.look_ahead(1).tipo_token.name)

        # Levanta uma nova exceção
        raise Exception(mensagem)

    ################################################################################
    #
    # - CRIANDO-SE OS MÉTODOS PARA OS NÃO-TERMINAIS DA GRAMÁTICA
    #
    ################################################################################

    def program(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_VAR or\
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_FUNCTION or\
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_TYPE:
            self.__definition()
            self.program()
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.FIM_DE_ARQUIVO:
            self.match(tipo_token.TipoToken.FIM_DE_ARQUIVO)
        else:
            tokens = list()
            tokens.append("ID")
            tokens.append("EOF")
            self.erro_sintatico(tokens)

    def __definition(self):
        # Caso de uma definição de variável
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_VAR:
            self.__def_variable()
        # Caso de uma definição de função
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_FUNCTION:
            self.__def_function()
        # Caso de uma definição de tipo de dado
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_TYPE:
            self.__def_type()
        else:
            tokens = list()
            tokens.append("PAL_CHAVE_VAR")
            tokens.append("PAL_CHAVE_FUNCTION")
            tokens.append("PAL_CHAVE_TYPE")
            self.erro_sintatico(tokens)

    def __def_variable(self):
        self.match(tipo_token.TipoToken.PAL_CHAVE_VAR)
        self.match(tipo_token.TipoToken.ID)
        self.match(tipo_token.TipoToken.DELIM_DOIS_PONTOS)
        self.__type()
        self.match(tipo_token.TipoToken.DELIM_PONTO_E_VIRGULA)

    def __type(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID:
            self.match(tipo_token.TipoToken.ID)
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_TIPO_INT:
            self.match(tipo_token.TipoToken.PAL_CHAVE_TIPO_INT)
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_TIPO_FLOAT:
            self.match(tipo_token.TipoToken.PAL_CHAVE_TIPO_FLOAT)
        else:
            tokens = list()
            tokens.append("ID")
            tokens.append("PAL_CHAVE_TIPO_INT")
            tokens.append("PAL_CHAVE_TIPO_FLOAT")

            self.erro_sintatico(tokens)

    def __def_type(self):
        self.match(tipo_token.TipoToken.PAL_CHAVE_TYPE)
        self.match(tipo_token.TipoToken.ID)
        self.match(tipo_token.TipoToken.DELIM_ATRIBUICAO)
        self.__typedesc()
        self.match(tipo_token.TipoToken.DELIM_PONTO_E_VIRGULA)

    def __typedesc(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID:
            self.match(tipo_token.TipoToken.ID)
        # Caso de um array
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.ARRAY_ABRE_COLCHETES:
            self.match(tipo_token.TipoToken.ARRAY_ABRE_COLCHETES)
            self.__typedesc()
            self.match(tipo_token.TipoToken.ARRAY_FECHA_COLCHETES)

        # Caso de um record
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_CHAVES:
            self.match(tipo_token.TipoToken.DELIM_ABRE_CHAVES)
            self.__field2()
            self.match(tipo_token.TipoToken.DELIM_FECHA_CHAVES)
        else:
            tokens = list()
            tokens.append("ID")
            tokens.append("TOKEN_COLCHETES")
            tokens.append("TOKEN_CHAVES")
            self.erro_sintatico(tokens)

    def __field2(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID:
            self.__field()
            self.__field2()
        else:
            """tokens = list()
            tokens.append("CAMPOS_RECORD")
            self.erro_sintatico(tokens)"""
            # VAZIO
            pass

    def __field(self):
        self.match(tipo_token.TipoToken.ID)
        self.match(tipo_token.TipoToken.DELIM_DOIS_PONTOS)
        self.__type()
        self.match(tipo_token.TipoToken.DELIM_PONTO_E_VIRGULA)

    def __def_function(self):
        self.match(tipo_token.TipoToken.PAL_CHAVE_FUNCTION)
        self.match(tipo_token.TipoToken.ID)
        self.match(tipo_token.TipoToken.DELIM_ABRE_PARENTESES)
        self.__parameters()
        # self.match(tipo_token.TipoToken.DELIM_FECHA_PARENTESES)
        self.__type2()
        self.__block()

    def __type2(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_DOIS_PONTOS:
            self.match(tipo_token.TipoToken.DELIM_DOIS_PONTOS)
            self.__type()
        else:
            """tokens = list()
            tokens.append("TOKEN DOIS PONTOS")
            self.erro_sintatico(tokens)"""
            # VAZIO
            pass

    def __parameters(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID:
            self.__parameters()
            self.__parameters2()
            self.match(tipo_token.TipoToken.DELIM_FECHA_PARENTESES)
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_FECHA_PARENTESES:
            self.match(tipo_token.TipoToken.DELIM_FECHA_PARENTESES)

        else:
            tokens = list()
            tokens.append("ID")
            tokens.append("DELIM_FECHA_PARENTESES")
            self.erro_sintatico(tokens)

    def __parameters2(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_VIRGULA:
            self.match(tipo_token.TipoToken.DELIM_VIRGULA)
            self.__parameter()
            self.__parameters2()
        else:
            """tokens = list()
            tokens.append("DELIM_VIRGULA")
            self.erro_sintatico(tokens)"""
            # VAZIO
            pass

    def __parameter(self):
        self.match(tipo_token.TipoToken.ID)
        self.match(tipo_token.TipoToken.DELIM_DOIS_PONTOS)
        self.__type()

    def __block(self):
        self.match(tipo_token.TipoToken.DELIM_ABRE_CHAVES)

        self.__def_variable2()
        self.__statement2()

        self.match(tipo_token.TipoToken.DELIM_FECHA_CHAVES)

    def __def_variable2(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_VAR:
            self.__def_variable()
            self.__def_variable2()
        else:
            """tokens = list()
            tokens.append("TOKENS DAS VARIÁVEIS DO BLOCO DE FUNÇÃO")
            self.erro_sintatico(tokens)"""
            # VAZIO
            pass

    def __statement2(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_IF or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_WHILE or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_RETURN or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_IMPRIME_VALOR or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_CHAVES:
            self.__statement()
            self.__statement2()
        else:
            """tokens = list()
            tokens.append("PAL_CHAVE_IF")
            tokens.append("PAL_CHAVE_WHILE")
            tokens.append("ID")
            tokens.append("PAL_CHAVE_RETURN")
            tokens.append("OP_IMPRIME_VALOR")
            tokens.append("DELIM_ABRE_CHAVES")
            self.erro_sintatico(tokens)"""
            # VAZIO
            pass

    def __statement(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_IF:
            self.match(tipo_token.TipoToken.PAL_CHAVE_IF)
            self.__cond()
            self.__block()
            self.__else_cond()
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_WHILE:
            self.match(tipo_token.TipoToken.PAL_CHAVE_WHILE)
            self.__cond()
            self.__block()
        # ID de variáveis
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID:
            self.__var()
            self.match(tipo_token.TipoToken.DELIM_ATRIBUICAO)
            self.__exp()
            self.match(tipo_token.TipoToken.DELIM_PONTO_E_VIRGULA)
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_RETURN:
            self.match(tipo_token.TipoToken.PAL_CHAVE_RETURN)
            self.__return_exp()

        # Nome para chamar função
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID:
            self.__call()
            self.match(tipo_token.TipoToken.DELIM_PONTO_E_VIRGULA)
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_IMPRIME_VALOR:
            self.match(tipo_token.TipoToken.OP_IMPRIME_VALOR)
            self.__exp()
            self.match(tipo_token.TipoToken.DELIM_PONTO_E_VIRGULA)

        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_CHAVES:
            self.__block()

        else:
            tokens = list()
            tokens.append("TOKENS DE INSTRUÇÕES BÁSICAS")

            self.erro_sintatico(tokens)

    def __else_cond(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_ELSE:
            self.match(tipo_token.TipoToken.PAL_CHAVE_ELSE)
            self.__block()
        else:
            """tokens = list()
            tokens.append("PAL_CHAVE_ELSE")
            self.erro_sintatico(tokens)"""
            # VAZIO
            pass

    def __return_exp(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_INT_CONST or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_FLOAT_CONST or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_PARENTESES or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_NEW or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_ARIT_SUBTRACAO or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_PARENTESES or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_BOOL_NOT:
            self.__exp()
            self.match(tipo_token.TipoToken.DELIM_PONTO_E_VIRGULA)
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_PONTO_E_VIRGULA:
            self.match(tipo_token.TipoToken.DELIM_PONTO_E_VIRGULA)
        else:
            tokens = list()
            tokens.append("TOKENS POSSIVEIS COMO RETORNO DE MÉTODOS")

            self.erro_sintatico(tokens)

    def __var(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID:
            self.match(tipo_token.TipoToken.ID)
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_INT_CONST or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_FLOAT_CONST or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_PARENTESES or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_NEW or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_ARIT_SUBTRACAO or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_PARENTESES or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_BOOL_NOT:
            self.__exp()
            self.match(tipo_token.TipoToken.ARRAY_ABRE_COLCHETES)
            self.__exp()
            self.match(tipo_token.TipoToken.ARRAY_FECHA_COLCHETES)
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_INT_CONST or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_FLOAT_CONST or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_PARENTESES or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_NEW or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_ARIT_SUBTRACAO or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_PARENTESES or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_BOOL_NOT:
            self.__exp()
            self.match(tipo_token.TipoToken.DELIM_PONTO)
            self.match(tipo_token.TipoToken.ID)
        else:
            tokens = list()
            tokens.append("TOKENS DE VARIAVEIS")
            tokens.append("TOKENS DE ARRAYS")
            tokens.append("TOKENS DE ATRIBUTSO DE RECORDS")

            self.erro_sintatico(tokens)

    def __exp(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_PARENTESES or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_INT_CONST or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_FLOAT_CONST or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_NEW or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_ARIT_SUBTRACAO or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_BOOL_NOT:
            self.__cond()
            self.match(tipo_token.TipoToken.OP_COND_TERNARIO_TRUE)
            self.__exp()
            self.match(tipo_token.TipoToken.DELIM_DOIS_PONTOS)
            self.__exp()
            self.__exp_rec()
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_INT_CONST:
            self.match(tipo_token.TipoToken.NUM_INT_CONST)
            self.__exp_rec()
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_FLOAT_CONST:
            self.match(tipo_token.TipoToken.NUM_FLOAT_CONST)
            self.__exp_rec()

        # ID de Var.
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_PARENTESES or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_INT_CONST or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_FLOAT_CONST or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_NEW or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_ARIT_SUBTRACAO or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_BOOL_NOT:
            self.__var()
            self.__exp_rec()

        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_PARENTESES:
            self.match(tipo_token.TipoToken.DELIM_ABRE_PARENTESES)
            self.__exp()
            self.match(tipo_token.TipoToken.DELIM_FECHA_PARENTESES)
            self.__exp_rec()

        # Call de função
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID:
            self.__call()
            self.__exp_rec()

        # exp NEW
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_PARENTESES or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_INT_CONST or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_FLOAT_CONST or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_NEW or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_ARIT_SUBTRACAO or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_BOOL_NOT:
            self.__exp()
            self.match(tipo_token.TipoToken.PAL_CHAVE_AS)
            self.__type()
            self.__exp_rec()

        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_NEW:
            self.match(tipo_token.TipoToken.PAL_CHAVE_NEW)
            self.__type()
            self.__new2()
            self.__exp_rec()

        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_ARIT_SUBTRACAO:
            self.match(tipo_token.TipoToken.OP_ARIT_SUBTRACAO)
            self.__exp()
            self.__exp_rec()

    def __exp_rec(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_ARIT_SOMA:
            self.match(tipo_token.TipoToken.OP_ARIT_SOMA)
            self.__exp()
            self.__exp_rec()
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_ARIT_SUBTRACAO:
            self.match(tipo_token.TipoToken.OP_ARIT_SUBTRACAO)
            self.__exp()
            self.__exp_rec()

        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_ARIT_MULTIPLICACAO:
            self.match(tipo_token.TipoToken.OP_ARIT_MULTIPLICACAO)
            self.__exp()
            self.__exp_rec()

        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_ARIT_DIVISAO:
            self.match(tipo_token.TipoToken.OP_ARIT_DIVISAO)
            self.__exp()
            self.__exp_rec()

        else:
            # VAZIO
            pass


    def __new2(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.ARRAY_ABRE_COLCHETES:
            self.match(tipo_token.TipoToken.ARRAY_ABRE_COLCHETES)
            self.__exp()
            self.match(tipo_token.TipoToken.ARRAY_FECHA_COLCHETES)
        else:
            tokens = list()
            tokens.append("TOKENS DO ARRAY NAS EXPRESSÕES DE CRIAR UM NOVO ARRAY")

            self.erro_sintatico(tokens)

    def __cond(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_PARENTESES:
            self.match(tipo_token.TipoToken.DELIM_ABRE_PARENTESES)
            self.__cond()
            self.match(tipo_token.TipoToken.DELIM_FECHA_PARENTESES)
            self.__cond_rec()

        # Expressão condicional
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_INT_CONST or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_FLOAT_CONST or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_PARENTESES or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_NEW or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_ARIT_SUBTRACAO or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_PARENTESES or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_BOOL_NOT:
            self.__exp()
            self.__exp_esq()

        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_BOOL_NOT:
            self.match(tipo_token.TipoToken.OP_BOOL_NOT)
            self.__cond()
            self.__cond_rec()

        else:
            tokens = list()
            tokens.append("TOKENS DE EXPRESSÕES CONDICIONAIS")

            self.erro_sintatico(tokens)

    def __cond_rec(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_BOOL_AND or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_BOOL_OR:
            self.__cond()
            self.__cond_rec()
        else:
            """tokens = list()
            tokens.append("TOKENS DE OPERAÇÕES BOOLEANAS")

            self.erro_sintatico(tokens)"""
            # VAZIO
            pass



    def __exp_esq(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_COMP_IGUAL:
            self.match(tipo_token.TipoToken.OP_COMP_IGUAL)
            self.__exp()
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_COMP_DIF:
            self.match(tipo_token.TipoToken.OP_COMP_DIF)
            self.__exp()

        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_COMP_MENOR_OU_IGUAL:
            self.match(tipo_token.TipoToken.OP_COMP_MENOR_OU_IGUAL)
            self.__exp()

        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_COMP_MAIOR_OU_IGUAL:
            self.match(tipo_token.TipoToken.OP_COMP_MAIOR_OU_IGUAL)
            self.__exp()

        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_MENOR:
            self.match(tipo_token.TipoToken.OP_MENOR)
            self.__exp()

        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_MAIOR:
            self.match(tipo_token.TipoToken.OP_MAIOR)
            self.__exp()
        else:
            tokens = list()
            tokens.append("TOKENS DE OPERADORES RELACIONAIS")

            self.erro_sintatico(tokens)


    def __call(self):
        self.match(tipo_token.TipoToken.ID)
        self.match(tipo_token.TipoToken.DELIM_ABRE_PARENTESES)
        self.__explist()

    def __explist(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_INT_CONST or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.NUM_FLOAT_CONST or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_PARENTESES or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.ID or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.PAL_CHAVE_NEW or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_ARIT_SUBTRACAO or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_ABRE_PARENTESES or \
                self.look_ahead(1).tipo_token == tipo_token.TipoToken.OP_BOOL_NOT:
            self.__exp()
            self.__explist2()
            self.match(tipo_token.TipoToken.DELIM_FECHA_PARENTESES)
        elif self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_FECHA_PARENTESES:
            self.match(tipo_token.TipoToken.DELIM_FECHA_PARENTESES)
        else:
            tokens = list()
            tokens.append("TOKENS PARA PARAMETROS NA CHAMADA DE UMA FUNÇÃO")

            self.erro_sintatico(tokens)


    def __explist2(self):
        if self.look_ahead(1).tipo_token == tipo_token.TipoToken.DELIM_VIRGULA:
            self.match(tipo_token.TipoToken.DELIM_VIRGULA)
            self.__exp()
            self.__explist2()
        else:
            """tokens = list()
            tokens.append("TOKENS PARA LISTA PARAMETROS NA CHAMADA DE UMA FUNÇÃO - PART 2")

            self.erro_sintatico(tokens)"""
            # VAZIO
            pass
