
import ply.lex as lex

states = (
    ('ptsearch','exclusive'),
)

# List of token names. 

tokens = (
    'initial_letter', #is when we have a letter wihch finishes with '\n', example: A
    'baseword', #is the +base word, always appears in the beggining of a new line followed by the character ':'
    'baseword_error', #example: worth
    'prefix_word', #is the type of the base word, always appears in a new line if the line contains the character '-' before the word
    'middle1_word', #is the type of the base word, always appears in a new line if the line contains the character '-' in the middle the word
    'middle1_word_error', #example:  sales -\n
    'middle2_word', #is the type of the base word, always appears in a new line if the line contains the character '-' in the middle the word
    'suffix_word', #is the type of the base word, always appears in a new line if the line contains the character '-' after the word
    'double_word', #example: - base -
    'no_word', #example: engineering
    'prefix_error_word', # example: -structuring
    'middle_error_word', #exameple: semi-costs
    'suffix_error_word', # example: shift-
    'normalword', # an english word to be translated (doesn't have a type)
    'portugueseTranslation', #the portuguese sentence appears after more than \t before the end of the current line  
    'portugueseTranslationError', # example: treinamento (mj dentro da indústria
    'paragraph',
)

def t_paragraph(t):
    r'\n'
    pass

def t_initial_letter(t): #example: A\n
    r'\w[ \r\t\f]*\n'
    return t

def t_normalword(t):#example: dole (do ot lex example)     OU    yearly report
    r'\w[\w\'-]*([ \r\t\f]\w[\w\-]*)*([ \r\t\f]\([^\)]*\))?[ \r\t\f]{2}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    return t

def t_baseword(t): #example: automatic data: \n  OU  administration:         administração (f)
    r'\w[ \r\t\f\w-]*:'
    t.lexer.push_state('ptsearch')
    return t

# Falta os : no final
def t_baseword_error(t): #example: worth\n
    r'\w+\n'
    t.lexer.push_state('ptsearch')
    return t

# The third word is facultative!!!!!
# Pode incluir outros casos como:    to-rule   (to -)

def t_prefix_word(t): #example:   - of responsibilities (ROF)   OR   - of responsibilities rof (ROFR)
    r'[ \r\t\f]+-[ \r\t\f]\w[\w-]*([ \r\t\f]\w[\w-]*)?([ \r\t\f]\w[\w-]*)?([ \r\t\f]\w[\w-]*)?([ \r\t\f]\([^\)]*\))?[ \r\t\f]{2}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    return t

def t_middle1_word(t): #example:  value - tax (VAT)         OR        value - (VA)   OR    value - Tax tax (VATT)
    r'[ \r\t\f]+\w[\w-]*[ \r\t\f]-([ \r\t\f]\w[\w-]*)?([ \r\t\f]\w[\w-]*)?([ \r\t\f]\([^\)]*\))?[ \r\t\f]{2}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    return t

def t_middle1_word_error(t): #example:  sales -\n
    r'[ \r\t\f]+\w[\w-]*[ \r\t\f]-([ \r\t\f]\w[\w-]*)?([ \r\t\f]\w[\w-]*)?([ \r\t\f]\([^\)]*\))?\n'
    t.lexer.push_state('ptsearch')
    return t

def t_middle2_word(t): #example:  value tax - (VAT)         OR    value Tax - tax (VTAT)
    r'[ \r\t\f]+\w[\w-]*[ \r\t\f]\w[\w-]*[ \r\t\f]-([ \r\t\f]\w[\w-]*)?([ \r\t\f]\([^\)]*\))?[ \r\t\f]{2}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    return t

def t_suffix_word(t): #example:  value tax final - (VTFA)
    r'[ \r\t\f]+\w[\w-]*[ \r\t\f]\w[\w-]*[ \r\t\f]\w[\w-]*[ \r\t\f]-([ \r\t\f]\([^\)]*\))?[ \r\t\f]{2}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    return t

def t_double_word(t): #example: - base -
    r'[ \r\t\f]+\-[ \r\t\f]\w[\w-]*[ \r\t\f]\-'
    t.lexer.push_state('ptsearch')
    return t

# às vezes pode n
def t_no_word(t): # diferença em relação ao normalword: contém espaço no início
    r'[ \r\t\f]+\w+([ \r\t\f]\w[\w-]*)*([ \r\t\f]\([^\)]*\))?[ \r\t\f]{2}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    return t

'''
 - measurement                medição (f) de trabalho
 clerical-measurement (CWM)   medição (f) de trabalho administrativo
'''
'''
def t_continue_word(t):
    r''
    t.lexer.push_state('ptsearch')
    return t
'''

# ERRO DE FORMATO
def t_prefix_error_word(t) : # example: -structuring
    # r'[ \r\t\f]+-\w[\w-]*([ \r\t\f]\w[\w-]*)?([ \r\t\f]\([^\)]*\))?[ \r\t\f]{2}[ \r\t\f]*'
    r'[ \r\t\f]+\-\w+([ \r\t\f]\w[\w-]*)*([ \r\t\f]\([^\)]*\))?[ \r\t\f]{2}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    return t

# ERRO DE FORMATO
def t_middle_error_word(t): #exameple: semi-costs
    r'[ \r\t\f]+\w+\-\w+([ \r\t\f]\w[\w-]*)*([ \r\t\f]\([^\)]*\))?[ \r\t\f]{2}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    return t

# ERRO DE FORMATO
def t_suffix_error_word(t): #example:  shift-
    r'[ \r\t\f]+\w+-([ \r\t\f]\w[\w-]*)*([ \r\t\f]\([^\)]*\))?[ \r\t\f]{2}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    return t

def t_ptsearch_portugueseTranslation(t): # includes () í ,
    r'[^\n]*\n([ \r\t\f]{10}[^\n]*\n)*'
    t.lexer.pop_state()
    return t

# ERRO DE FORMATO
def t_ptsearch_portugueseTranslationError(t): # example: treinamento (mj dentro da indústria
    r'[^\n]*\n([ \r\t\f]{10}[^\)\n]*\n)*'
    t.lexer.pop_state()
    return t
    
t_ANY_ignore = ""

def t_ANY_error(t):
    print(f"Carácter ilegal '{t.value[0]}' na linha {t.lineno}")
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