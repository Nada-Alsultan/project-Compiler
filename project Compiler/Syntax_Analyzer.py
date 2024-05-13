import re

# Grammar
grammar = {
    "PROGRAM": ["STMTS"],
    "STMTS": ["STMT STMTS'"],
    "STMTS'": ["; STMT STMTS'", 'ε'],
    "STMT": ['identifier ASSIGN EXPR'],
    "ASSIGN": ['='],
    "EXPR": ["TERM EXPRSI"],
    "EXPRSI": ["+ TERM EXPRSI", "- TERM EXPRSI", "ε"],
    "TERM": ["POWER TERMPO"],
    "TERMPO": ["* POWER TERMPO", "/ POWER TERMPO", "ε"],
    "POWER": ["FACTOR POWERUP"],
    "POWERUP": ["^ FACTOR POWERUP", "ε"],
    "FACTOR": ["UNARY UNIT"],
    "UNARY": ["-", "ε"],
    "UNIT": ["( EXPR )", "identifier", "number"]
}

def get_grammar():
    return grammar

# Compute FIRST sets
def first(symbol, grammar, first_sets, computed_sets):
    if symbol in computed_sets:
        return first_sets[symbol]

    first_set = set()
    for rule in grammar[symbol]:
        symbols = rule.split()
        for s in symbols:
            if not s.isupper():  # terminal symbol
                first_set.add(s)
                break
            else:  # non-terminal symbol
                next_symbol = first(s, grammar, first_sets, computed_sets)
                first_set.update(next_symbol - {'ε'})
                if 'ε' not in next_symbol:
                    break
        else:  # If we did not break, all symbols can produce ε
            first_set.add('ε')

    first_sets[symbol] = first_set
    computed_sets.add(symbol)
    return first_set

# Compute FOLLOW sets
def follow(symbol, grammar, first_sets, follow_sets, computed_sets):
    if symbol in computed_sets:
        return follow_sets[symbol]

    follow_sets[symbol] = set()

    if symbol == 'PROGRAM':
        follow_sets[symbol].add('$')

    for non_terminal in grammar:
        for production in grammar[non_terminal]:
            tokens = production.split()
            for i, token in enumerate(tokens):
                if token == symbol:
                    if i + 1 < len(tokens):
                        next_symbol = tokens[i + 1]
                        if next_symbol.isupper():
                            follow_sets[symbol].update(first_sets[next_symbol] - {'ε'})
                            if 'ε' in first_sets[next_symbol]:
                                if non_terminal not in computed_sets:
                                    follow(non_terminal, grammar, first_sets, follow_sets, computed_sets)
                                follow_sets[symbol].update(follow_sets[non_terminal])
                        else:
                            follow_sets[symbol].add(next_symbol)
                    else:
                        if non_terminal != symbol:
                            if non_terminal not in computed_sets:
                                follow(non_terminal, grammar, first_sets, follow_sets, computed_sets)
                            follow_sets[symbol].update(follow_sets[non_terminal])

    computed_sets.add(symbol)
    return follow_sets[symbol]

# Construct parsing table
def parsing_table(grammar):
    first_sets = {}
    follow_sets = {}
    computed_sets_first = set()
    computed_sets_follow = set()
    table = {}

    # Compute FIRST sets
    for non_terminal in grammar:
        first(non_terminal, grammar, first_sets, computed_sets_first)

    print("\nFirst Sets:")
    for non_t, t in first_sets.items():
        print(f"First({non_t}) = {t}")

    # Compute FOLLOW sets
    for non_terminal in grammar:
        follow(non_terminal, grammar, first_sets, follow_sets, computed_sets_follow)

    print("\nFollow Sets:")
    for non_t, t in follow_sets.items():
        print(f"Follow({non_t}) = {t}")

    # Construct parsing table
    for non_term, productions in grammar.items():
        table[non_term] = {}
        for production in productions:
            prod_first = set()
            items = production.split()
            for item in items:
                if item in grammar:  # Check if the item is a non-terminal
                    prod_first.update(first_sets[item] - {'ε'})
                    if 'ε' not in first_sets[item]:
                        break
                else:
                    prod_first.add(item)
                    break
            else:
                prod_first.add('ε')
            for terminal in prod_first - {'ε'}:
                table[non_term][terminal] = production
            if 'ε' in prod_first:
                for terminal in follow_sets[non_term]:
                    table[non_term][terminal] = production

    return table


def parse_input(input_str, parsing_table):
    stack = ['$']
    parse_tree = Node('PROGRAM')
    current_node = parse_tree
    stack.append('PROGRAM')
    current_token = 0

    while stack and current_token < len(input_str):  # Check for end of input string tokens
        top_of_stack = stack.pop()

        if top_of_stack in parsing_table:
            try:
                production = parsing_table[top_of_stack][input_str[current_token]]
                for symbol in reversed(production.split()):
                    if symbol != 'ε':
                        new_node = Node(symbol)
                        new_node.parent = current_node
                        current_node.children.append(new_node)
                        stack.append(symbol)
                        current_node = new_node
            except KeyError:
                 print("Syntax Error: Error in parsing. Unexpected token.")
        else:
            if top_of_stack == input_str[current_token]:
                current_token += 1
                current_node = current_node.parent
            else:
                raise ValueError("Error in parsing. Unexpected token.")

    if current_token != len(input_str):  # Check if the input string tokens are fully consumed
        raise ValueError("Syntax Error: Error in parsing. Unexpected end of input.")
    
    print("Input Accepted.")
    return parse_tree
def print_parsing_table(parsing_table):
    print("\nParsing Table:")
    for non_terminal, rules in parsing_table.items():
        print(f"Non-terminal: {non_terminal}")
        for terminal, production in rules.items():
            print(f"  On input {terminal}, use -> {production}")
        print()

# Print parse tree
def print_parse_tree(node, depth=0):
    if depth == 0:
        print(node.value)
    else:
        print(' ' * (depth - 2) + '|__ ' + node.value)

    for i, child in enumerate(node.children):
        if i == len(node.children) - 1:
            print_parse_tree(child, depth + 4)
        else:
            print_parse_tree(child, depth + 4)
            print(' ' * (depth + 2) + '|')


# Define Node class
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

