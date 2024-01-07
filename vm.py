def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def CompiledFileHandler(file_name):
    variables = {}
    with open(file_name, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].split()
            match line[0]:
                case "ADD":

                    if is_number(line[1]):
                        expr1 = float(line[1])
                    else:
                        expr1 = variables[line[1]]

                    if is_number(line[2]):
                        expr2 = float(line[2])
                    else:
                        expr2 = variables[line[2]]

                    if not is_number(line[3]):
                        variables[line[3]] = expr1 + expr2
                        i += 1
                    else:
                        raise "Number cannot be a variable name"

                case "SUB":
                    if '#' in line[1]:
                        lst, index = line[1].split('#')
                        if index in variables:
                            index = variables[index]
                            if isinstance(index, float) and not index.is_integer():
                                raise "The index can only be an integer"
                        line[1] = lst + '#' + str(int(index))
                        if line[1] not in variables:
                            raise ValueError("Index is out of range")

                    if '#' in line[2]:
                        lst, index = line[2].split('#')
                        if index in variables:
                            index = variables[index]
                            if isinstance(index, float) and not index.is_integer():
                                raise "The index can only be an integer"
                        line[2] = lst + '#' + str(int(index))
                        if line[2] not in variables:
                            raise ValueError("Index is out of range")

                    if is_number(line[1]):
                        expr1 = float(line[1])
                    else:
                        expr1 = variables[line[1]]

                    if is_number(line[2]):
                        expr2 = float(line[2])
                    else:
                        expr2 = variables[line[2]]

                    if not is_number(line[3]):
                        variables[line[3]] = expr1 - expr2
                        i += 1
                    else:
                        raise "Number cannot be a variable name"

                case "MUL":
                    if '#' in line[1]:
                        lst, index = line[1].split('#')
                        if index in variables:
                            index = variables[index]
                            if isinstance(index, float) and not index.is_integer():
                                raise "The index can only be an integer"
                        line[1] = lst + '#' + str(int(index))
                        if line[1] not in variables:
                            raise ValueError("Index is out of range")

                    if '#' in line[2]:
                        lst, index = line[2].split('#')
                        if index in variables:
                            index = variables[index]
                            if isinstance(index, float) and not index.is_integer():
                                raise "The index can only be an integer"
                        line[2] = lst + '#' + str(int(index))
                        if line[2] not in variables:
                            raise ValueError("Index is out of range")

                    if is_number(line[1]):
                        expr1 = float(line[1])
                    else:
                        expr1 = variables[line[1]]

                    if is_number(line[2]):
                        expr2 = float(line[2])
                    else:
                        expr2 = variables[line[2]]

                    if not is_number(line[3]):
                        variables[line[3]] = expr1 * expr2
                        i += 1
                    else:
                        raise "Number cannot be a variable name"

                case "DIV":
                    if '#' in line[1]:
                        lst, index = line[1].split('#')
                        if index in variables:
                            index = variables[index]
                            if isinstance(index, float) and not index.is_integer():
                                raise "The index can only be an integer"
                        line[1] = lst + '#' + str(int(index))
                        if line[1] not in variables:
                            raise ValueError("Index is out of range")

                    if '#' in line[2]:
                        lst, index = line[2].split('#')
                        if index in variables:
                            index = variables[index]
                            if isinstance(index, float) and not index.is_integer():
                                raise "The index can only be an integer"
                        line[2] = lst + '#' + str(int(index))
                        if line[2] not in variables:
                            raise ValueError("Index is out of range")

                    if is_number(line[1]):
                        expr1 = float(line[1])
                    else:
                        expr1 = variables[line[1]]

                    if is_number(line[2]):
                        expr2 = float(line[2])
                    else:
                        expr2 = variables[line[2]]

                    if not is_number(line[3]):
                        variables[line[3]] = expr1 / expr2
                        i += 1
                    else:
                        raise "Number cannot be a variable name"

                case "READ":
                    if not is_number(line[1]):
                        if '#' in line[1]:
                            lst, index = line[1].split('#')
                            if index in variables:
                                index = variables[index]
                                if isinstance(index, float) and not index.is_integer():
                                    raise "The index can only be an integer"
                            line[1] = lst + '#' + str(int(index))
                        variables[line[1]] = float(input(f"Input variable {line[1]}:"))
                        i += 1
                    else:
                        raise "Number cannot be a variable name"

                case "WRITE":
                    if '#' in line[1]:
                        lst, index = line[1].split('#')
                        if index in variables:
                            index = variables[index]
                            if isinstance(index, float) and not index.is_integer():
                                raise "The index can only be an integer"
                        line[1] = lst + '#' + str(int(index))
                        if line[1] not in variables:
                            raise ValueError("Index is out of range")
                    
                    if not is_number(line[1]):
                        print(variables[line[1]])
                    else:
                        print(line[1])
                    i += 1

                case "GOTOIFNOT":
                    if '#' in line[1]:
                        lst, index = line[1].split('#')
                        if index in variables:
                            index = variables[index]
                            if isinstance(index, float) and not index.is_integer():
                                raise "The index can only be an integer"
                        line[1] = lst + '#' + str(int(index))
                        if line[1] not in variables:
                            raise ValueError("Index is out of range")
                    
                    if is_number(line[1]):
                        cond_expression = float(line[1])
                    else:
                        cond_expression = variables[line[1]]

                    i += 1

                    if cond_expression <= 0:
                        i = int(line[2])

                case "GOTOIF":
                    if '#' in line[1]:
                        lst, index = line[1].split('#')
                        if index in variables:
                            index = variables[index]
                            if isinstance(index, float) and not index.is_integer():
                                raise "The index can only be an integer"
                        line[1] = lst + '#' + str(int(index))
                        if line[1] not in variables:
                            raise ValueError("Index is out of range")
                
                    if is_number(line[1]):
                        cond_expression = float(line[1])
                    else:
                        cond_expression = variables[line[1]]

                    i += 1

                    if cond_expression > 0:
                        i = int(line[2])
                        

                case "GOTO":
                    i = int(line[1])

                case "COPY":
                    if '#' in line[1]:
                        lst, index = line[1].split('#')
                        if index in variables:
                            index = variables[index]
                            if isinstance(index, float) and not index.is_integer():
                                raise "The index can only be an integer"
                        line[1] = lst + '#' + str(int(index))
                        if line[1] not in variables:
                            raise ValueError("Index is out of range")

                    if '#' in line[2]:
                        lst, index = line[2].split('#')
                        if index in variables:
                            index = variables[index]
                            if isinstance(index, float) and not index.is_integer():
                                raise "The index can only be an integer"
                        line[2] = lst + '#' + str(int(index))
                        if line[2] not in variables:
                            raise ValueError("Index is out of range")

                    if is_number(line[1]):
                        expr = float(line[1])
                    else:
                        expr = variables[line[1]]

                    if not is_number(line[2]):
                        variables[line[2]] = expr
                        i += 1
                    else:
                        raise "Number cannot be a variable name"
                    
                case _:
                    raise "An unknown command"
                

CompiledFileHandler("CompiledFile.txt")