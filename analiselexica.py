
import ply.lex as lex

# List of token names. 

tokens = (
    'baseword', #is the +base word, always appears in the beggining of a new line followed by the character ':'
    'prefix_word', #is the type of the base word, always appears in a new line if the line contains the character '-' before the word
    'suffix_word', #is the type of the base word, always appears in a new line if the line contains the character '-' after the word
    'normalword', # an english word to be translated (doesn't have a type)
    'portugueseTranslation', #the portuguese sentence appears after more than \t before the end of the current line  
)

def t_baseword(t): #example: dividends:
    r'\w+:'
    return t

def t_prefix_word(t): #example:   - policy 
    r'^(\s)+-+(\s)+(\w)+'
    return t

def t_suffix_word(t): #example:  operating -
    r'^[\t ]+(\w)+[\t ]+-'
    return t

def t_normalword(t):#example: dole 
    r'^(\w)+[\t ]'
    return t

#def t_portugueseTranslation(t):
#    r'\w+ +-'
#    return t

def t_error(t):
    print(f"Carácter ilegal {t.value[0]}")
    t.lexer.skip(1)
    
lexer = lex.lex()

with open('dic-finance-en.pt.txt', 'r') as file:
    data = file.read()

lexer.input(data)


while tok := lexer.token():
   print(tok)