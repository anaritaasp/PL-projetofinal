import ply.yacc as yacc

from analiselexica import tokens


dicionario = {}

# normalword      no_hifen
#  - overheads            despesas (fpl) de administração     ->   fpl -> feminino plural
# m -> masculino singular
# f -> feminino singular
# mpl -> masculino plural

text = '''A
ADP (automatic data processing)   processamento (m) automático de
                                   dados
absenteeism                       absenteísmo (m)
absorption costing                custeio (f) de absorção
accountability                    responsabilidade (f) sujeita a
                                   prestação de contas
accountant:

chief                             chefe (m) de contabilidade
'''


"""TODO"""



def p_dict2(p):
    "Dict : Alphsection Dict"
    p[0] = dicionario

def p_dict1(p):
    "Dict : "
    p[0] = {}

def p_Alphsection1(p):
    "Alphsection : initial_letter translations"
    dicionario[p[1]] = p[2]

def p_translations1(p):
    "translations : normalword portugueseTranslation translations"
    p[3][p[1]] = p[2]
    p[0] = p[3]
    
def p_translations2(p):
    "translations : baseword portugueseTranslation translations"
    p[3][p[1]] = p[2]
    p[0] = p[3]

def p_translations3(p):
    "translations : "
    p[0] = {}

def p_error(p):
    print(f"Erro sintático: {p.value}")

parser = yacc.yacc()
print(parser.parse(text))

'''
a_parenteses + ptsearch_portugueseTranslation + f_parenteses + ptsearch_portugueseTranslation

LAFTA (Latin American Free      ALALC (Associação Latino-
           Trade Association)   Americana de Livre Comércio)
'''

'''
normal_word + ptsearch_portugueseTranslation + no_hifen + ptsearch_portugueseTranslation

Latin American Free Trade   Associação (f) Latino-Americana de
  Association (LAFTA)         Livre Comércio (ALALC)
'''

''' a_parenteses + ptsearch_portugueseTranslation + f_parenteses       ------>  Ver na análise sintática
CWM (clerical work              medição (f) de trabalho
                                   administrativo
measurement)


a_parenteses + ptsearch_portugueseTranslation + f_parenteses + ptsearch_portugueseTranslation

COINS (computerised information
 system)                        sistema (m) computadorizado de dados


'''


''' middle2_word_error + abreviattion + translation   ----> VER NA ANALISE SINTÁTICA
 management information -
  (MIS)                       sistema (m) de dados para gestão
'''