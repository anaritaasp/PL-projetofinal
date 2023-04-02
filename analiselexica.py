
import ply.lex as lex

# List of token names. 

tokens = (
    'word:', #is the +base word, always appears in the beggining of a new line followed by the character ':'
    '-word', #is the type of the base word, always appears in a new line if the line contains the character '-'
    'PT_SENTENCE', #the portuguese sentence appears after more than \t before the end of the current line  
)


def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)
    
lexer = lex.lex()

with open('dic-finance-en.pt.txt', 'r') as file:
    data = file.read()

lexer.input(data)

print (data)

#while tok := lexer.token():
#    print(tok)