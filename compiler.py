import re

class Token:
    def __init__(self, lexem: str, line):
        self.lex = lexem
        self.line = line

    def __str__(self):
        return self.lex
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Token):
            return self.lex == other.lex
        return False
    
    def is_variable(self):
        pattern = "^[a-zA-Z]+$"
        if len(self.lex) == 1 and bool(re.match(pattern, self.lex)):
            return True
        elif '#' in self.lex and bool(re.match(pattern, self.lex.split('#')[0])) and (bool(re.match(pattern, self.lex.split('#')[1])) or self.lex.split('#')[1].isnumeric()):
            return True
        else:
            return False
        
    def is_number(self):
        try:
            float(self.lex)
            return True
        except ValueError:
            return False
        
    def is_operator(self):
        pattern = r"[\*/\+\-\(\)]"
        if len(self.lex) == 1 and bool(re.match(pattern, self.lex)):
            return True
        else:
            return False
        
    def is_block_operator(self):
        pattern = ['while', 'whilenot', 'if', 'ifnot']
        if self.lex in pattern:
            return True
        else:
            return False
        
    def is_command(self):
        pattern = ['read', 'write']
        if self.lex in pattern:
            return True
        else:
            return False
    
    def priority(self):
        match self.lex:
            case ')':
                return 0
            case '(':
                return 0
            case '+':
                return 1
            case '-':
                return 1
            case '*':
                return 2
            case '/':
                return 2
            case _:
                return -1


def handleExpression(tokens: list, res_var: str, list_of_commands: list, temp_count: int):
    ARG = []
    OP = []
    def generateCommand(temp_count: int):
        op = OP.pop()
        rhs = ARG.pop()
        lhs = ARG.pop()
        
        match op.lex:
            case "+":
                name = "ADD"
            case "-":
                name = "SUB"
            case "*":
                name = "MUL"
            case "/":
                name = "DIV"

        temp_count += 1
        res = "t" + str(temp_count)
        list_of_commands.append(f"{name} {lhs} {rhs} {res}")
        ARG.append(res)
        

        return temp_count

    if len(tokens) == 1 and res_var != '':
        list_of_commands.append(f"COPY {tokens[0].lex} {res_var}")
    else:
        while tokens:
            token = tokens.pop(0)
            if token.is_number() or token.is_variable():
                ARG.append(token)
            elif token.lex == ")":
                while OP[-1].lex != "(":
                    temp_count = generateCommand(temp_count)
                if OP[-1].lex != "(":
                    raise "Syntax error1"
                OP.pop()
            elif token.lex == "(":
                OP.append(token)
            elif token.is_operator():
                while OP and OP[-1].is_operator() and OP[-1].priority() >= token.priority():
                    temp_count = generateCommand(temp_count)
                OP.append(token)
            else:
                raise SyntaxError("Incorrect expression")
        
        while OP:
            if OP[-1].lex == "(" or OP[-1].lex == ")":
               raise "Syntax error2"
            temp_count = generateCommand(temp_count)
        
        if res_var != '':
            last_command = list_of_commands.pop()
            last_command = last_command.replace("t" + str(temp_count), res_var)
            list_of_commands.append(last_command)
            temp_count -= 1
            
    return list_of_commands, temp_count




def handleCommand(tokens: list, list_of_commands: list, temp_count: int):
    if (tokens[0].lex == 'read' or tokens[0].lex == 'write') and tokens[1].lex != '>':
        raise SyntaxError(f"Except '>' symbol in line {tokens[0].line}")
    elif tokens[0].is_variable() and tokens[1].lex != '=':
        raise SyntaxError(f"Except '=' symbol in line {tokens[0].line}")
    elif not (tokens[0].lex == 'read' or tokens[0].lex == 'write' or tokens[0].is_variable()):
        raise SyntaxError(f"An unknown command in line {tokens[0].line}")
    
    if tokens[0].line != tokens[-1].line:
        raise SyntaxError(f"Expect ';' in the end of a command in line {tokens[0].line}")

    match tokens[0].lex:
        case 'read':
            list_of_commands.append(f"READ {tokens[2].lex}")
        case 'write':
            list_of_commands.append(f"WRITE {tokens[2].lex}")
        case _:
            list_of_commands, temp_count = handleExpression(tokens[2:-1], tokens[0].lex, list_of_commands, temp_count)

    return list_of_commands, temp_count


def handleBlock(tokens: list, list_of_commands = [], temp_count = 0, inserts = 0):
    command = []
    operator_block = []
    brace_counter = 0

    for token in tokens:
        if token.is_block_operator():
            operator_block.append(token)
            brace_counter += 1
            
        elif operator_block:
            operator_block.append(token)
            if token.lex == '}':
                brace_counter -= 1
                if not brace_counter:
                    list_of_commands, temp_count = handleOperatorBlock(operator_block, list_of_commands, temp_count, inserts)
                    operator_block = []
        
        elif command:
            command.append(token)
            if token.lex in [';', 'while', 'whilenot', 'read', 'write', 'if', 'ifnot', '}']:
                list_of_commands, temp_count = handleCommand(command, list_of_commands, temp_count)
                command = []
        elif token.is_command() or token.is_variable():
            command.append(token)
        else:
            raise SyntaxError(f'An unknown command {token.lex} in line {token.line}')

    if command:
        raise SyntaxError(f"Excepts a ';' in the end of a command in line {tokens[-1].line}")
    if operator_block:
        raise SyntaxError("Excepts a '}' at the end of a block" + f"in line {tokens[-1].line}")

    return list_of_commands, temp_count

        

def handleOperatorBlock(tokens: list, list_of_commands: list, temp_count: int, inserts: int):
    index_of_start_expr = 1
    if tokens[index_of_start_expr].lex != '[':
        raise SyntaxError(f"Expect a '[' symbol as the start of the condition in line {tokens[index_of_start_expr-1].line}")
    index_of_end_expr = None
    for i, token in enumerate(tokens):
        if token.lex == '{' or i == len(tokens) - 1:
            raise SyntaxError(f"Expect a ']' symbol as the end of the condition in line {tokens[index_of_start_expr].line}")
        if token.lex == ']':
            index_of_end_expr = i
            break
    expr_tokens = tokens[index_of_start_expr+1:index_of_end_expr]
    go_to = len(list_of_commands) + inserts
    list_of_commands, temp_count = handleExpression(expr_tokens, '', list_of_commands, temp_count)
    index_to_insert_go = len(list_of_commands)
    

    if tokens[index_of_start_expr+2].lex == ']':
        go_if_what = tokens[index_of_start_expr+1].lex
    else:
        go_if_what = 't' + str(temp_count)
        
    index_of_start_block = index_of_end_expr + 1
    if tokens[index_of_start_block].lex != '{':
        raise SyntaxError("Expect a '{' after the condition in line " + str(tokens[index_of_start_block-1].line))
    index_of_start_block += 1
    index_of_end_block = len(tokens) - 1
    block_tokens = tokens[index_of_start_block:index_of_end_block]
    list_of_commands, temp_count = handleBlock(block_tokens, list_of_commands, temp_count, inserts+1)
    

    match tokens[0].lex:
        case 'while':
            list_of_commands.append(f"GOTO {go_to}")
            list_of_commands.insert(index_to_insert_go, f"GOTOIFNOT {go_if_what} {len(list_of_commands)+1+inserts}")

        case 'whilenot':
            list_of_commands.append(f"GOTO {go_to}")
            list_of_commands.insert(index_to_insert_go, f"GOTOIF {go_if_what} {len(list_of_commands)+1+inserts}")

        case 'if':
            list_of_commands.insert(index_to_insert_go, f"GOTOIFNOT {go_if_what} {len(list_of_commands)+1+inserts}")

        case 'ifnot':
            list_of_commands.insert(index_to_insert_go, f"GOTOIF {go_if_what} {len(list_of_commands)+1+inserts}")

    return list_of_commands, temp_count

def fileHandler(input_file_name, output_file_name):
    text = ""
    with open(input_file_name, 'r') as file:
        text = file.read()
        
    file.close()

    list_of_Tokens = []

    matches = re.finditer(r"[>;=\*/\+\-\(\){}\[\]\n\t ]", text)
    previous_index = 0
    line = 1
    for match in matches:
        lexem = text[previous_index:match.start()]
        if lexem:
            list_of_Tokens.append(Token(lexem, line))
        if match.group() == '\n':
            line += 1
        elif match.group() == ' ':
            pass
        elif match.group() == '\t':
            pass
        else:
            list_of_Tokens.append(Token(match.group(), line))
        previous_index = match.start() + 1

    list_to_output = handleBlock(list_of_Tokens)[0]

    with open(output_file_name, 'w') as file:
        for command in list_to_output:
            print(command, file=file)