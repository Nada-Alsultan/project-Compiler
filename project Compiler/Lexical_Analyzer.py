import re # Import the regular expression module for pattern matching

# Define token types using constants
TOKEN_NUMBER = 'number'
TOKEN_IDENTIFIER = 'identifier'
TOKEN_OPERATOR = 'OPERATOR'
TOKEN_ASSIGN = '='
TOKEN_STOP = 'STOP'

# Regular expressions for token patterns, each tuple contains token type and corresponding regex pattern
patterns = [
    (TOKEN_NUMBER, r'\d+(\.\d+)?'),        # Matches real numbers (float or int)
    (TOKEN_IDENTIFIER, r'[a-zA-Z_]\w*'),   # Matches variable names
    (TOKEN_OPERATOR, r'[-+*/()^]'),         # Matches operators and parentheses
    (TOKEN_ASSIGN, r'='),                  # Matches assignment operator
    (TOKEN_STOP, r'\s+'),                  # Matches one or more whitespace characters as a stop token
]

# Operator mapping for special tokens, maps operator symbols to their corresponding special token names
operator_mapping = {
    '+': '+',
    '-': '-',
    '*': '*',
    '/': '/',
    '^': '^',
    '(': '(',
    ')': ')',
}

def lex(input_str):
    tokens = []  # Initialize an empty list to store tokens
    symbol_table = {}  # Dictionary to store variable names and their types/values
    pos = 0  # Initialize position tracker for parsing input string
    identifier_counter = 1  # Counter for identifiers
    symbol_table_indices = {}  # Dictionary to store identifier indices in the symbol table

    # Loop through input string
    while pos < len(input_str):
        match = None  # Initialize match variable to None
        # Try matching each pattern
        for token_type, pattern in patterns:
            regex = re.compile(pattern)  # Compile the regex pattern
            match = regex.match(input_str, pos)  # Attempt to match the pattern starting from the current position
            if match:  # If a match is found
                value = match.group(0)  # Get the matched value
                if token_type == TOKEN_OPERATOR:  # If the token is an operator
                    value = operator_mapping.get(value, value)  # Map operator to special token
                    tokens.append((value, match.group(0).strip()))  # Add the special token directly to tokens
                elif token_type == TOKEN_IDENTIFIER:  # If the token is an identifier
                    if value in symbol_table:  # Check if identifier is already in symbol table
                        tokens.append((TOKEN_IDENTIFIER, value))  # Add identifier token
                    else:  # If not in symbol table
                        if '.' in value:  # Determine type (float or int) based on presence of dot
                            type_ = 'float'
                        else:
                            type_ = 'int'
                        tokens.append((TOKEN_IDENTIFIER, value))  # Add identifier token
                        symbol_value = input(f"Enter the value for {value}: ")  # Prompt for variable value
                        if symbol_value == '':  # If input is empty
                            symbol_table[value] = (None, None)  # Set symbol value to None
                        elif '.' in symbol_value:  # If input contains dot, treat as float
                            try:
                                symbol_table[value] = ('float', float(symbol_value))  # Store as float
                            except ValueError:  # Handle invalid input
                                print("Error: Invalid input.")
                                symbol_table[value] = (None, None)  # Set symbol value to None
                        else:  # If input is an integer
                            try:
                                symbol_table[value] = ('int', int(symbol_value))  # Store as integer
                            except ValueError:  # Handle invalid input
                                print("Error: Invalid input.")
                                symbol_table[value] = (None, None)  # Set symbol value to None
                        # Assign index to identifier in symbol table and increment identifier counter
                        symbol_table_indices[value] = identifier_counter
                        identifier_counter += 1
                elif token_type == TOKEN_NUMBER:  # If the token is a number
                    if '.' in value:  # Determine type (float or int) based on presence of dot
                        type_ = 'float'
                        value = float(value)  # Convert value to float
                    else:
                        type_ = 'int'
                        value = int(value)  # Convert value to integer
                    # Update symbol table with the correct value for the identifier
                    if tokens and tokens[-1][0] == TOKEN_IDENTIFIER:  # Check if previous token was an identifier
                        symbol_table[tokens[-1][1]] = (type_, value)  # Update type and value in symbol table
                    tokens.append((TOKEN_NUMBER, str(value)))  # Add number token with type
                
                elif token_type != TOKEN_STOP:  # If the token is not a stop token
                    tokens.append((token_type, value.strip()))  # Strip spaces from tokens and add to list
                pos = match.end()  # Move position to the end of the matched token
                break  # Exit the loop after processing the token
        if not match:  # If no match is found
            # Report an error and return empty tokens and symbol table
            print(f"Error: Invalid token at position {pos}: '{input_str[pos:]}'")
            return [], {}

    # Add stop token at the end of input
    tokens.append((TOKEN_STOP, '$'))  # Add the stop token to signify the end of input
    return tokens, symbol_table, symbol_table_indices  # Return the tokens list, symbol table, and symbol table indices


def print_tokens_lexemes(tokens,symbol_table,symbol_table_indices):
        # Print Tokens and Lexems
    print()  # Print an empty line for readability
    print("Tokens and Lexems:")  # Print header for tokens and lexems
    print()  # Print an empty line for readability
    for index, token in enumerate(tokens):  # Iterate through tokens list with index
        lexem = token[1]  # Get the lexem (value) of the token
        token_str = f"<'{token[0]}'"  # Create a string representation of the token
        if token[0] in [TOKEN_IDENTIFIER]:  # If the token is an identifier
            token_str += f", {symbol_table_indices[token[1]]} >"  # Add identifier index to token string
        elif token[0] == TOKEN_NUMBER:  # If the token is a number
            token_str += f", '{lexem}' >"  # Add number value to token string
        else:  # For other token types
            token_str += ">"  # Close the token string
        print(f"lexem: '{lexem}' , tokens: {token_str}")  # Print token and lexem information

    print("\nSymbol Table:")  # Print header for symbol table
    for variable, (type_, value) in symbol_table.items():  # Iterate through symbol table items
        print(f"{symbol_table_indices[variable]} : {variable} : {type_}, {value}")  # Print symbol table information


    
