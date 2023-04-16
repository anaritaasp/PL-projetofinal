
import ply.lex as lex

states = (
    ('ptsearch','exclusive'),
)

# List of token names. 

tokens = (
    'initial_letter', #is when we have a letter wihch finishes with '\n', example: A
    'baseword', #is the +base word, always appears in the beggining of a new line followed by the character ':'
    'prefix_word', #is the type of the base word, always appears in a new line if the line contains the character '-' before the word
    'middle_word', #is the type of the base word, always appears in a new line if the line contains the character '-' in the middle the word
    'suffix_word', #is the type of the base word, always appears in a new line if the line contains the character '-' after the word
    'final_word', # example: shift-
    'normalword', # an english word to be translated (doesn't have a type)
    'portugueseTranslation', #the portuguese sentence appears after more than \t before the end of the current line  
)

def t_initial_letter(t): #example: A\n
    r'\w\s*\n'
    return t

def t_normalword(t):#example: dole (do ot lex example)     OU    yearly report
    r'\w[\w-]*(\s\w[\w-]*)*(\s\([^\)]*\))?\s{2}\s*'
    t.lexer.push_state('ptsearch')
    return t

def t_baseword(t): #example: automatic data: \n  OU  administration:         administração (f)
    r'\w[\s\w-]*:'
    t.lexer.push_state('ptsearch')
    return t

# The third word is facultative!!!!!
# Pode incluir outros casos como:    to-rule   (to -)

def t_prefix_word(t): #example:   - of responsibilities (ROF)
    r'(\s)+-\s\w[\w-]+(\s\w[\w-]+)?(\s\([^\)]*\))?\s{2}\s*'
    t.lexer.push_state('ptsearch')
    return t

def t_middle_word(t): #example:  value - tax (VAT)         OR        value - (VA)   
    r'(\s)+\w[\w-]+\s-(\s\w[\w-]+)?(\s\([^\)]*\))?\s{2}\s*'
    t.lexer.push_state('ptsearch')
    return t

def t_suffix_word(t): #example:  value tax - (VTA)
    r'(\s)+\w[\w-]+\s\w[\w-]+\s-(\s\([^\)]*\))?\s{2}\s*'
    t.lexer.push_state('ptsearch')
    return t

def t_final_word(t): #example:  shift-
    r'(\s)+\w[\w-]+\s{2}\s*'
    t.lexer.push_state('ptsearch')
    return t

def t_ptsearch_portugueseTranslation(t): # includes () í ,
    r'[^\n]*\n(\s{10}[^\n]*\n)*'
    t.lexer.pop_state()
    return t
    
t_ANY_ignore = ""

def t_ANY_error(t):
    print(f"Caracter ilegal {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

with open('dic-finance-en.pt.txt', 'r') as file:
    data = file.read()

lexer.input(data)

#print(lexer.token())

#'''
while tok := lexer.token():
    print(tok)
#'''