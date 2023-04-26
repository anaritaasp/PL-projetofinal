import ply.yacc as yacc

from analiselexica import tokens


dicionario = {}



text = '''A
ADP (automatic data processing)   processamento (m) automático de
                                   dados
absenteeism                       absenteísmo (m)
absorption costing                custeio (f) de absorção
abandonment:
 product -                        retirada (f) de um produto
above par                         com ágio; acima da paridade
acceleration clause               cláusula (f) de aceleração
acceptance:                       aceitação (f)
 brand -                          aceitação (f) de uma marca
 consumer -                       aceitação (f) por parte do consumidor
access:
 multi -                          acesso (m) múltiplo
 random -                         acesso (m) casual
account:
 bank -                           conta (f) bancária
 joint -                          conta (f) conjunta
accountability                    responsabilidade (f) sujeita a
                                   prestação de contas
accountant:

chief                             chefe (m) de contabilidade
'''


"""TODO"""



def p_dict2(p):
    "Dict : Alphsection Dict"
    p[0] = p[1] + p[2]

def p_dict1(p):
    "Dict : "
    p[0] = ""

def p_Alphsection1(p):
    "Alphsection : initial_letter translations"
    p[0] = f"initial_letter: {p[1]} - translations[{p[2]}] "

def p_translations1(p):
    "translations : normalword portugueseTranslation translations"
    p[0] = f"normalword: {p[1]} - PT: {p[2]} - translations[{p[3]}]"
    
def p_translations2(p):
    "translations : baseword portugueseTranslation translations"
    p[0] = f"baseword: {p[1]} - translations[{p[2]}] "

def p_translations3(p):
    "translations : "
    p[0] = ""

def p_error(p):
    print(f"Erro sintático: {p.value}")

parser = yacc.yacc()
parser.parse(text)

