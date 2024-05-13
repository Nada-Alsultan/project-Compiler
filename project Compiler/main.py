import Syntax_Analyzer as parser ,Lexical_Analyzer as lexer ,re

input_str = input("Enter a string to tokenize: ")  # Prompt user to enter a string
tokens, symbol_table, symbol_table_indices = lexer.lex(input_str)  # Tokenize the input string
lexer.print_tokens_lexemes(tokens,symbol_table,symbol_table_indices)

input_tokens=""
for j  in tokens:
    if(j[0] != 'STOP'):
        input_tokens += j[0]
        input_tokens += " "

input_tokens = re.findall(r'\w+|[^\w\s]', input_tokens)

grammar = parser.get_grammar()

parse_table = parser.parsing_table(grammar)

parser.print_parsing_table(parse_table)

parse_tree = parser.parse_input(input_tokens,parse_table)

parser.print_parse_tree(parse_tree)