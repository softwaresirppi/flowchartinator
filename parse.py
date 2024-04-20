# AST nodes
class Sequence:
    def __init__(self, sequence):
        self.sequence = sequence
    def __str__(self):
        return '{\n' + indent('\n'.join(map(str, self.sequence)), 2) + '\n}'

class Condition:
    def __init__(self, condition, true_action, false_action):
        self.condition = condition
        self.true_action = true_action
        self.false_action = false_action
    def __str__(self):
        return f'IF {self.condition}\n{indent(str(self.true_action), 0)}\nELSE\n{indent(str(self.false_action), 0)}'

class Iteration:
    def __init__(self, condition, iteration):
        self.condition = condition
        self.iteration = iteration
    def __str__(self):
        return f'WHILE {self.condition}\n{str(self.iteration)}'

def indent(text, n = 2):
    return '\n'.join(map(lambda line: ' ' * n + line, text.split('\n')))

# Parsers
def parseSpaces(source, i):
    spaces = ''
    while i < len(source) and source[i].isspace():
        spaces += source[i]
        i += 1
    return (spaces, i)

def parseText(source, i):
    start = i
    spaces, i = parseSpaces(source, i)
    while i < len(source) and (source[i].isalpha() or source[i].isspace()):
        i += 1
    end = i
    return (source[start:end].strip(), end)

def parseLiteral(literal, source, i):
    if not literal.isspace():
        spaces, i = parseSpaces(source, i)
    if source[i:].startswith(literal):
        return (literal, i + len(literal))
    return (None, i)

def parseStep(source, i):
    start = i
    spaces, i = parseSpaces(source, i)
    text, i = parseText(source, i)
    literal, i = parseLiteral(';', source, i)
    if not literal:
        return (None, start)
    return (Sequence([text]), i)

def parseBlock(source, i):
    start = i
    spaces, i = parseSpaces(source, i)
    literal, i = parseLiteral('{', source, i)
    if not literal:
        return (None, start)
    actions = []
    while True:
        action, i = parseAction(source, i)
        if not action:
            break
        actions.append(action)
    literal, i = parseLiteral('}', source, i)
    if not literal:
        return (None, start)
    return (Sequence(actions), i)

def parseIf(source, i):
    start = i
    spaces, i = parseSpaces(source, i)
    literal, i = parseLiteral('if', source, i)
    if not literal:
        return (None, start)

    literal, i = parseLiteral('(', source, i)
    if not literal:
        return (None, start)

    condition, i = parseText(source, i)
    if not condition:
        return (None, start)

    literal, i = parseLiteral(')', source, i)
    if not literal:
        return (None, start)

    true, i = parseAction(source, i)
    if not true:
        return (None, start)

    start = i
    literal, i = parseLiteral('else', source, i)
    if not literal:
        return (Condition(condition, true, Sequence([])), start)

    literal, i = parseLiteral(' ', source, i)
    if not literal:
        return (Condition(condition, true, Sequence([])), start)

    false, i = parseAction(source, i)
    if not false:
        return (Condition(condition, true, Sequence([])), start)
    return (Condition(condition, true, false), i)

def parseWhile(source, i):
    start = i
    spaces, i = parseSpaces(source, i)
    literal, i = parseLiteral('while', source, i)
    if not literal:
        return (None, start)

    literal, i = parseLiteral('(', source, i)
    if not literal:
        return (None, start)

    condition, i = parseText(source, i)
    if not condition:
        return (None, start)

    literal, i = parseLiteral(')', source, i)
    if not literal:
        return (None, start)

    action, i = parseAction(source, i)
    if not action:
        return (None, start)
    return (Iteration(condition, action), i)

def parseFor(source, i):
    start = i
    spaces, i = parseSpaces(source, i)
    literal, i = parseLiteral('for', source, i)
    if not literal:
        return (None, start)

    literal, i = parseLiteral('(', source, i)
    if not literal:
        return (None, start)

    initializer, i = parseText(source, i)
    if not initializer:
        return (None, start)

    literal, i = parseLiteral(';', source, i)
    if not literal:
        return (None, start)

    condition, i = parseText(source, i)
    if not condition:
        return (None, start)

    literal, i = parseLiteral(';', source, i)
    if not literal:
        return (None, start)

    increment, i = parseText(source, i)
    if not increment:
        return (None, start)

    literal, i = parseLiteral(')', source, i)
    if not literal:
        return (None, start)

    iteration, i = parseAction(source, i)
    if not iteration:
        return (None, start)
    return (Sequence([initializer, Iteration(condition, Sequence([iteration, increment]))]), i)

def parseAction(source, i):
    start = i
    action, i = parseIf(source, i)
    if action:
        return (action, i)
    action, i = parseWhile(source, i)
    if action:
        return (action, i)
    action, i = parseFor(source, i)
    if action:
        return (action, i)
    action, i = parseBlock(source, i)
    if action:
        return (action, i)
    return parseStep(source, i)


source = 'if(at home) while (hungry) {eat;eat;eat;} else starve to death;'
action, i = parseAction(source, 0)
print(action)
