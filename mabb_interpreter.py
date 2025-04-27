class Token:
    def __init__(self):
        self.keywords = ["_PRINT", "_EXECUTE", "_IF", "_ENDIF", "_VAR", "_NUMBER", "_TEXT", "_INPUT", "_END", "_OPERATION"]
        self.operations = ["-", "+", "/", "*"]
        self.comparison_op = ["<", ">", "_IN"]  
        self.count = 0
        self.tokens = []

    def string(self):
        """Метод для добавления текста"""
        start = self.count
        self.count += 1
        while self.count < self.len_code and self.code[self.count] != "'":
            self.count += 1
        self.tokens.append(('STRING', self.code[start+1:self.count]))
        self.count += 1

    def number(self):
        """Метод для добавления числа"""
        start = self.count
        while self.count < self.len_code and self.code[self.count].isdigit():
            self.count += 1
        self.tokens.append(('NUMBER', int(self.code[start:self.count])))

    def assign(self):
        """Метод для добавления присваивания"""
        self.tokens.append(('ASSIGN', self.code[self.count]))
        self.count += 1

    def id(self):
        """Метод для добавления названия переменной"""
        start = self.count
        while self.count < self.len_code and (self.code[self.count].isalpha() or self.code[self.count].isdigit() or self.code[self.count] == '_'):
            self.count += 1
        identifier = self.code[start:self.count]
        self.tokens.append(('ID', identifier))

    def command(self):
        """Метод для добавления команды или же ключевых слов"""
        start = self.count
        while self.count < self.len_code and self.code[self.count] != " " and self.code[self.count] != "\n":
            self.count += 1
        word = self.code[start:self.count]
        if word in self.keywords:
            self.tokens.append(("KEYWORD", word))
        else:
            self.count = start
            self.id()

    def operation(self):
        """Метод для добавления арифметической операции"""
        self.tokens.append(("OP", self.code[self.count]))
        self.count += 1

    def new_line(self):
        """Метод для добавления новой строки"""
        self.tokens.append(("NEWLINE", "\n"))
        self.count += 1

    def skip_whitespace(self):
        while self.count < self.len_code and self.code[self.count] == " ":
            self.count += 1

    def compare(self):
        """Метод для добавления операции сравнения"""
        self.tokens.append(("COMPARE", self.code[self.count]))
        self.count += 1

    def token(self, code: str):
        """Метод для добавления в список токены токены"""
        self.code = code
        self.len_code = len(self.code)

        while self.count < self.len_code:
            symbol = self.code[self.count]

            if self.count + 1 < self.len_code:
                two_char = self.code[self.count] + self.code[self.count + 1]
                if two_char in ('==', '!='):
                    self.tokens.append(('COMPARE', two_char))
                    self.count += 2
                    continue
                if two_char in ('//'):
                    self.tokens.append(('//', two_char))
                    self.count += 2
                    continue
            
            if symbol == "'":
                self.string()
            elif symbol == "\n":
                self.new_line()
            elif symbol in self.comparison_op:
                self.tokens.append(('COMPARE', symbol))
                self.count += 1
            elif symbol == "=":
                self.assign()
            elif symbol.isdigit():
                self.number()
            elif symbol == "_" or symbol.isalpha():
                self.command()
            elif symbol in self.operations:
                self.operation()
            elif symbol == " ":
                self.skip_whitespace()
            else:
                self.count += 1  

        return self.tokens



class Interpreter:
    def __init__(self):
        self.pc = 0 # Program counter
        self.variables = {}
        self.call_stack = []
        self.len_tokens = 0
        self.tokens = []

    def _print(self):
        """Метод для вывода переменных, текста или чисел в консоль"""
        output = []
        self.pc += 1
        while self.pc < self.len_tokens and self.tokens[self.pc][0] != 'NEWLINE':
            token_type, token_value = self.tokens[self.pc]
            if token_type == 'ID':
                if token_value in self.variables:
                    output.append(str(self.variables[token_value]))
            elif token_type in ('STRING', 'NUMBER'):
                output.append(token_value)
            self.pc += 1
        print(' '.join(output))
        self.pc += 1

    def _var(self):
        """Метод для создания переменной"""
        self.pc += 1
        var_type = self.tokens[self.pc][1]
        self.pc += 1
        var_name = self.tokens[self.pc][1]
        self.pc += 1

        if self.tokens[self.pc][0] == 'ASSIGN':
            self.pc += 1

            token_type, token_value = self.tokens[self.pc]
            if var_type == '_TEXT':
                value = token_value
            elif var_type == '_NUMBER':
                value = int(token_value)
            elif var_type == '_INPUT':
                value = input(token_value)
            elif token_type == 'ID':
                if token_value in self.variables:
                    value = self.variables[token_value]
            else:
                value = None

            self.variables[var_name] = value
            self.pc += 1

        self.pc += 1

    def _execute(self):        
        """Метод для выполнения программы с заданной строки"""
        self.pc += 1
        token, number = self.tokens[self.pc]
        count = 0
        if token == "ID":
            number = self.variables[number]
        number = int(number) - 2

        self.pc = 0
        while self.pc < self.len_tokens:
            token, word = self.tokens[self.pc]
            if count > number:
                break
            elif token == 'NEWLINE':
                count += 1
            self.pc += 1

    def _operation(self):
        """Метод для выполнения арифметических операций"""
        self.pc += 1
        token, variable = self.tokens[self.pc]
        self.pc += 2
        token1, arg1 = self.tokens[self.pc]
        self.pc += 1
        token2, operation = self.tokens[self.pc]
        self.pc += 1
        token3, arg2 = self.tokens[self.pc]
        if token1 == "ID":
            arg1 = int(self.variables[arg1])
        if token2 == "ID":
            operation = self.variables[operation]
        if token3 == "ID":
            arg2 = int(self.variables[arg2])

        if operation == "+":
            self.variables[variable] = arg1 + arg2
        if operation == "-":
            self.variables[variable] = arg1 - arg2
        if operation == "*":
            self.variables[variable] = arg1 * arg2
        if operation == "/":
            self.variables[variable] = arg1 /  arg2

    def _if(self):
        """Метод для проверки условия"""
        self.pc += 1
        token_type1, arg1 = self.tokens[self.pc]

        if token_type1 == 'ID':
            left_value = self.variables[arg1]
        else:
            left_value = arg1

        self.pc += 1
        token_type2, compare_op = self.tokens[self.pc]
        self.pc += 1
        token_type3, arg2 = self.tokens[self.pc]

        if token_type3 == 'ID':
            right_value = self.variables[arg2]
        else:
            right_value = arg2

        if compare_op in ('<', '>'):
            left_value = float(left_value)
            right_value = float(right_value)

        condition_met = False
        if compare_op == "==":
            condition_met = str(left_value) == str(right_value)
        elif compare_op == "!=":
            condition_met = str(left_value) != str(right_value)
        elif compare_op == "<":
            condition_met = left_value < right_value
        elif compare_op == ">":
            condition_met = left_value > right_value
        elif compare_op == "_IN":
            condition_met = str(left_value) in str(right_value)

        if not condition_met:
            nesting_level = 1
            while self.pc < self.len_tokens:
                self.pc += 1

                token_type, token_value = self.tokens[self.pc]
                if token_type == 'KEYWORD':
                    if token_value == '_IF':
                        nesting_level += 1
                    elif token_value == '_ENDIF':
                        nesting_level -= 1
                        if nesting_level == 0:
                            break
        self.pc += 1

    def run(self, tokens: list):
        """Метод для проверки и выполнения команд"""
        self.len_tokens = len(tokens)
        self.tokens = tokens
        while self.pc < self.len_tokens: 
            try:
                token_type, token_value = self.tokens[self.pc]

                if token_type == 'NEWLINE':
                    self.pc += 1 
                    continue

                elif token_type == 'KEYWORD':
                    if token_value == '_PRINT': # Команда вывода в консоль
                        self._print()
                    elif token_value == '_VAR': # Команда создания переменной
                        self._var()
                    elif token_value == '_EXECUTE': # Команда для выполнения программы с заданной строки
                        self._execute()
                    elif token_value == '_OPERATION': # Команда для сложения двух чисел/переменных и записи ответа в указанную переменную
                        self._operation()
                    elif token_value == '_END': # Команда для прекращения выполнения кода
                        break
                    elif token_value == '_IF': # Команда для проверки, выполненно ли условие
                        self._if()
                    else:
                        self.pc += 1
                else:
                    self.pc += 1
            except Exception as e:
                print(f"\033[31m{e}. pc: {self.pc}\033[0m")
                return


if __name__ == "__main__":
    code = """
_VAR _NUMBER count = 0
_VAR _NUMBER range = 100

_IF count != range
    _OPERATION count = count + 1
    _PRINT 'Count:' count
    _EXECUTE 4
_ENDIF
"""

    tokenizer = Token()
    interpreter = Interpreter()
    interpreter.run(tokenizer.token(code))