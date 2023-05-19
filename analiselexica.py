import re
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
    'prefix_word_error', # -, insurance and freight
    'prefix_word_error_2', #  - volume ratio (P/V)\n
    'middle1_word', #is the type of the base word, always appears in a new line if the line contains the character '-' in the middle the word
    'middle1_word_error', #example:  sales -\n
    'middle1_word_error_2', #example: down.the -
    'middle2_word', #is the type of the base word, always appears in a new line if the line contains the character '-' in the middle the word
    'middle2_word_error', # example:  management information -\n
    'middle_word_5', # source and - of funds
    'suffix_word', #is the type of the base word, always appears in a new line if the line contains the character '-' after the word
    'suffix_error', #automatic data (ADP)-
    'double_word', #example: - base -
    'prefix_error_word', # example: -structuring
    'middle_error_word', #exameple: semi-costs
    'suffix_error_word', # example: shift-
    'abbreviation', #sigla ex: (PMTS)
    'no_hifen', #example: engineering
    'no_hifen_paragraph', # return on capital\n
    'normalword', # an english word to be translated (doesn't have a type)
    'a_parenteses', # CWM (clerical work
    'a_parenteses_paragraph', # ROCE (return on capital\n
    'f_parenteses', # measurement)
    'portugueseTranslation', #the portuguese sentence appears after more than \t before the end of the current line  
    'portugueseTranslationError', # example: treinamento (mj dentro da indústria
    'paragraph', # token extra
)


def t_paragraph(t):
    r'\n'
    t.lexer.lineno += 1
    pass

def t_initial_letter(t): #example: A\n
    r'\w[ \r\t\f]*\n'
    t.lexer.lineno += 1
    t.value = t.value.strip()
    return t

def t_normalword(t):#example: yearly report      OU     I.O.U. (I owe you)      OU    buyers's market    OU    cost-volume-analysis
    r'\w[\w\'\-\.\']*([ \r\t\f]\w[\w\-]*)*([ \r\t\f]\([^\)\n]*\))?[ \r\t\f]{3}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    t.value = t.value.strip()
    t.lexer.word = t.value
    return t

def t_baseword(t): #example: automatic data: \n  OU  administration:   ( pode ter tradução a seguir: "administração (f)" )
    r'[ \r\t\f]*\w[ \r\t\f\w\-]*:'
    t.lexer.push_state('ptsearch')
    t.value = t.value.strip(':')
    t.lexer.word = t.value
    return t

# Falta os : no final
def t_baseword_error(t): #example: worth\n   
    r'[ \r\t\f]*\w\w+\n'
    t.lexer.lineno += 1
    t.value = t.value.strip()
    t.lexer.word = t.value
    return t

# The third word is facultative!!!!!
# Pode incluir outros casos como:    to-rule   (to -)

def t_prefix_word(t): #example:   - of responsibilities (ROF)   OR   - of responsibilities rof (ROFR)     OR     - to-rule (to -)
    r'[ \r\t\f]*-[ \r\t\f]+\w[\w\-\,]*([ \r\t\f]\w[\w\-\,]*)?([ \r\t\f]\w[\w\-\,]*)?([ \r\t\f]\w[\w\-\,]*)?([ \r\t\f]\([^\)]*\))?[ \r\t\f]{3}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    t.value = re.sub("[ \r\t\f]*\-[ \r\t\f]+", t.lexer.word + " ", t.value)
    t.value = re.sub("[ \r\t\f]\-", " " + t.lexer.word, t.value)
    t.value = t.value.strip()
    # print(t.value)
    return t

# ERRO de FORMATO
def t_prefix_word_error(t): # example: -, insurance and freight
    r'[ \r\t\f]*\-\,[ \r\t\f]\w[\w\-\,]*([ \r\t\f]\w[\w\-\,]*)?([ \r\t\f]\w[\w\-\,]*)?([ \r\t\f]\w[\w\-\,]*)?([ \r\t\f]\([^\)]*\))?[ \r\t\f]{3}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    t.value = re.sub("[ \r\t\f]*\-\,[ \r\t\f]+", t.lexer.word + " ", t.value).strip()
    return t

def t_prefix_word_error_2(t): #  - volume ratio (P/V)\n
    r'[ \r\t\f]*-[ \r\t\f]\w[\w\,]*([ \r\t\f]\w[\w\-\,]*)*([ \r\t\f]\([^\)]*\))?\n'
    t.lexer.lineno += 1
    t.value = re.sub("[ \r\t\f]*\-[ \r\t\f]+", t.lexer.word + " ", t.value)
    t.value = t.value.strip()
    return t 

def t_middle1_word(t): #example:  value - tax (VAT)         OR        value - (VA)   OR    value - Tax tax (VATT)      OR       buyers'
    r'[ \r\t\f]*\w[\w\-\,\']*[ \r\t\f]-([ \r\t\f]\w[\w\-\,]*)?([ \r\t\f]\w[\w\-\,]*)?([ \r\t\f]\([^\)]*\))?[ \r\t\f]{3}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    t.value = re.sub("[ \r\t\f]*\-[ \r\t\f]+", " " + t.lexer.word + " ", t.value).strip()
    return t

def t_middle1_word_error(t): #example:  sales -\n
    r'[ \r\t\f]*\w[\w\-\,]*[ \r\t\f]-([ \r\t\f]\w[\w\-\,]*)?([ \r\t\f]\w[\w\-\,]*)?([ \r\t\f]\([^\)]*\))?\n'
    t.lexer.lineno += 1
    t.value = re.sub("[ \r\t\f]*\-", t.lexer.word, t.value).strip()
    return t

def t_middle1_word_error_2(t): # down.the -
    r'[ \r\t\f]*\w[\w\-\,\.]*[ \r\t\f]-([ \r\t\f]\w[\w\-\,]*)?([ \r\t\f]\w[\w\-\,]*)?([ \r\t\f]\([^\)]*\))?[ \r\t\f]{3}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    t.value = re.sub("[ \r\t\f]*\-", t.lexer.word, t.value)
    t.value = re.sub("\.", " ", t.value).strip()
    return t

def t_middle2_word(t): #example:  value tax - (VAT)         OR    value Tax - tax (VTAT)    OU    quality (QC) -
    r'[ \r\t\f]*\w[\w\-\,]*[ \r\t\f][\w\(\)][\w\-\,\)]*[ \r\t\f]-([ \r\t\f]\w[\w\-\,]*)?([ \r\t\f]\([^\)]*\))?[ \r\t\f]{3}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    t.value = re.sub("[ \r\t\f]*\-[ \r\t\f]+", " " + t.lexer.word + " ", t.value).strip()
    return t

def t_middle2_word_error(t): # example:  management information -\n    OU     #  return on -\n
    r'[ \r\t\f]*\w[\w\-\,]*[ \r\t\f]\w[\w\-\,]*[ \r\t\f]-([ \r\t\f]\w[\w\-\,]*)?([ \r\t\f]\([^\)]*\))?\n'
    t.lexer.lineno += 1
    t.value = re.sub("[ \r\t\f]*\-", " " + t.lexer.word + " ", t.value).strip()
    return t

def t_middle_word_5(t): # source and - of funds
    r'[ \r\t\f]*\w[\w\-\,]*[ \r\t\f]\w[\w\-\,]*[ \r\t\f]-[ \r\t\f]\w[\w\-\,]*[ \r\t\f]\w[\w\-\,]*[ \r\t\f]{3}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    t.value = re.sub("[ \r\t\f]*\-", " " + t.lexer.word + " ", t.value).strip()
    return t

def t_suffix_word(t): #example:  value tax final - (VTFA)
    r'[ \r\t\f]*\w[\w\-\,]*[ \r\t\f]\w[\w\-\,]*[ \r\t\f]\w[\w\-\,]*[ \r\t\f]-([ \r\t\f]\([^\)]*\))?[ \r\t\f]{3}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    t.value = re.sub("[ \r\t\f]*\-[ \r\t\f]*", " " + t.lexer.word + " ", t.value).strip()
    return t

# ERRO de FORMATO
def t_suffix_error(t): #automatic data (ADP)-
    r'[ \r\t\f]*\w[\w\-\,]*[ \r\t\f]\w[\w\-\,]*[ \r\t\f]\(\w[\w\-\,]*\)-([ \r\t\f]\([^\)]*\))?[ \r\t\f]{3}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    t.value = re.sub("\-[ \r\t\f]", t.lexer.word + " ", t.value).strip()
    return t

def t_double_word(t): #example: - base -     OU           price - earnings - (PIE)
    r'[ \r\t\f]*(\w[\w\-\,]*[ \r\t\f])?\-[ \r\t\f]\w[\w\-\,]*[ \r\t\f]\-([ \r\t\f]\([^\)]*\))?[ \r\t\f]{3}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    t.value = re.sub("\-[ \r\t\f]", t.lexer.word + " ", t.value)
    t.value = re.sub("[ \r\t\f]\-[ \r\t\f]", " " + t.lexer.word + " ", t.value).strip()
    return t

# ERRO DE FORMATO
def t_prefix_error_word(t) : # example: -structuring
    r'[ \r\t\f]*\-\w[\w\,]*([ \r\t\f]\w[\w\-\,]*)*([ \r\t\f]\([^\)]*\))?[ \r\t\f]{3}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    t.value = re.sub("[ \r\t\f]*\-", t.lexer.word + " ", t.value).strip()
    return t

# ERRO DE FORMATO
def t_middle_error_word(t): #exameple: semi-costs
    r'[ \r\t\f]*\w[\w\,]*\-\w[\w\,]*([ \r\t\f]\w[\w\-\,]*)*([ \r\t\f]\([^\)]*\))?[ \r\t\f]{3}[ \r\t\f]*'
    t.lexer.push_state('ptsearch')
    t.value = re.sub("\-", " " + t.lexer.word + " ", t.value).strip()
    return t

# ERRO DE FORMATO
def t_suffix_error_word(t): #example:  shift-       OU     resale price-(RPM)
    r'[ \r\t\f]*(\w[\w\,]*[ \r\t\f])?\w[\w\,]*-([ \r\t\f]\w[\w\-,]*)*(\(\w*\))*([ \r\t\f]\([^\)]*\))?[ \r\t\f]{3}[ \r\t\f]*'
    t.value = re.sub("\-", " " + t.lexer.word + " ", t.value).strip()
    t.lexer.push_state('ptsearch')
    return t

# Sigla - Acronim
def t_abbreviation(t): # (PMTS)    OU    (O and M)    OU    (PPBS)
    r'[ \r\t\f]*\(\w[\w, \r\t\f]*\)[ \r\t\f]*'
    t.value = t.value.strip()
    t.lexer.push_state('ptsearch')
    return t


# abrir parenteses
def t_a_parenteses(t): # CWM (clerical work     OU     EEC (European Economic Com-            OU    R and D (research and
    r'[ \r\t\f]*(\w+[ \r\t\f])+\((\w[\w\,]*([ \r\t\f\-])?)+[ \r\t\f]{3}[ \r\t\f]*'
    t.value = t.value.strip()
    t.lexer.push_state('ptsearch')
    return t

# com paragrafo no final
def t_a_parenteses_paragraph(t): # ROCE (return on capital\n
    r'[ \r\t\f]*(\w+[ \r\t\f])+\((\w[\w\,]*([ \r\t\f\-])?)+\n'
    t.value = t.value.strip()
    return t

# fechar parenteses
def t_f_parenteses(t): # measurement)
    r'[ \r\t\f]*\w+(([ \r\t\f]\w+)*)?\)[ \r\t\f]*'
    t.value = t.value.strip()
    t.lexer.push_state('ptsearch')
    return t

# às vezes pode n
def t_no_hifen(t): # diferença em relação ao normalword: contém espaço no início
    r'[ \r\t\f]+\(?\w[\w\,\-]*([ \r\t\f]\w[\w\-\,]*)*([ \r\t\f]\([^\)]*\))?\)?[ \r\t\f]{3}[ \r\t\f]*'
    t.value = t.value.strip()
    t.lexer.push_state('ptsearch')
    return t

def t_no_hifen_paragraph(t): # return on capital\n
    r'[ \r\t\f]*\w[\w\,]*([ \r\t\f]\w[\w\-\,]*)*([ \r\t\f]\([^\)]*\))?\n'
    t.value = t.value.strip()
    t.lexer.lineno += 1
    return t

'''
 - measurement                medição (f) de trabalho
 clerical-measurement (CWM)   medição (f) de trabalho administrativo
'''

'''
 performance -                   controle (m) orçamentário de rendimen-
                                 to
'''
def t_ptsearch_portugueseTranslation(t): # includes () í ,
    r'[^\n]*\n([ \r\t\f]{12}[^\n]*\n)*'
    t.lexer.pop_state()
    t.lexer.lineno += str(t.value).count('\n')
    list = t.value.split()
    t.value = ""
    for l in list:
        if l[len(l) - 1] == '-':
            l = l[:-1]
        elif t.value != "": # empty string 
            t.value += " "
        t.value += l.strip()
    return t

# ERRO DE FORMATO
def t_ptsearch_portugueseTranslationError(t): # example: treinamento (mj dentro da indústria
    r'[^\n]*\n([ \r\t\f]{12}[^\)\n]*\n)*'
    t.lexer.pop_state()
    t.lexer.lineno += str(t.value).count('\n')
    t.value = re.sub
    t.value = t.value.strip()
    return t
    
t_ANY_ignore = ""

def t_ANY_error(t):
    print(f"Carácter ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.lineno += str(t.value).count('\n')
    t.lexer.skip(1)



lexer = lex.lex()
lexer.word = None # por agora, não tem palavra para substituição

'''
with open('dic-finance-en.pt.txt', 'r') as file:
    data = file.read()


lexer.input(data)

while tok := lexer.token():
    print(tok)
'''