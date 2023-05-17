import ply.yacc as yacc

from analiselexica import tokens

precedence = (
    ('left', 'middle2_word'),
    ('left', 'abbreviation'),
)


dicionario = {}

# normalword      no_hifen
#  - overheads            despesas (fpl) de administração     ->   fpl -> feminino plural
# m -> masculino singular
# f -> feminino singular
# mpl -> masculino plural

text = '''
A
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

'''

"""TODO"""


def p_dict1(p):
    "Dict : Alphsection Dict"
    p[2].update(p[1])
    p[0] = p[2]


def p_dict2(p):
    "Dict : "
    p[0] = {}


def p_Alphsection(p):
    "Alphsection : initial_letter translations"
    p[0] = {p[1]:p[2]}


def p_translations1(p):
    "translations : normalword portugueseTranslation translations"
    p[3][p[1]] = p[2]
    p[0] = p[3] 

def p_translations2(p):
    '''
    translations : baseword portugueseTranslation multipleTranslations translations
                 | baseword_error multipleTranslations translations
    '''

    if len(p) == 5: # translations : baseword portugueseTranslation multipleTranslations translations
        p[4][p[1]] = (p[1], p[2], p[3])
        p[0] = p[4]
    else: # translations : baseword_error multipleTranslations translations
        # não existe string portugueseTranslation
        p[3][p[1]] = (p[1], p[2], p[3])
        p[0] = p[3]

#definimos um caso para o vazio      
def p_translations3(p): 
    "translations : "
    p[0] = {}

# LAFTA (Latin American Free      ALALC (Associação Latino-
#           Trade Association)   Americana de Livre Comércio)
def p_multipleTranslations1(p):
    "multipleTranslations : a_parenteses portugueseTranslation f_parenteses portugueseTranslation multipleTranslations"
    
    #string que guarda as portugueseTranslations
    portugueseTranslation = ""

    if p[2] == "": #se ptsearch_portugueseTranslation é empty
        pass 
    else:   #otherwise, p[2] = Portuguese translation
        portugueseTranslation += p[2]
        
    if p[4] == "": #verificar se a segunda PortugueseTranslation é empty
        pass 
    else:   
        portugueseTranslation += " " + p[4] 
        
    # o resto:
    total_parenteses = p[1] + p[3] #abre parenteses + fechar parenteses
    
    p[5][total_parenteses] = portugueseTranslation 
    p[0] = p[5]
    


#Latin American Free Trade   Associação (f) Latino-Americana de
#  Association (LAFTA)         Livre Comércio (ALALC)    
def p_multipleTranslations2(p):
    "multipleTranslations : normalword portugueseTranslation no_hifen portugueseTranslation multipleTranslations"
    #string que guarda as portugueseTranslations
    portugueseTranslation = ""
    
    if p[2] == "":
        pass
    else:
        portugueseTranslation += p[2]
    
    if p[4] == "": #verificar se a segunda PortugueseTranslation é empty
        pass 
    else:   
        portugueseTranslation += " " + p[4] 
    
    # o resto:
    final_word = p[1] + p[3] #juntamos a palavra em ingles com a linha de baixo que tem a sua continuação
    
    p[5][final_word] = portugueseTranslation 
    p[0] = p[5] #output




#  management information -
#  (MIS)                       sistema (m) de dados para gestão
# return on -
#   employed (ROCE)      rendimento (m) do capital investido
def p_multipleTranslations3(p):
    '''
    multipleTranslations : middle2_word_error abbreviation portugueseTranslation multipleTranslations
                         | middle2_word_error no_hifen portugueseTranslation multipleTranslations
    '''
    final_word = p[1] + " " + p[2]
    portugueseTranslation = p[3]
    p[4][final_word] = portugueseTranslation
    p[0] = p[4]
            



# planning-programming -       sistema (m) orçamentário de
#  budgeting- (PPBS)            planejamento e programação
# 
# predetermined motion time    sistema (m) de movimentos
#  (PMTS)                       pré-determinados
#
# computerised information -
#  (COINS)                     sistema (m) computadorizado de dados
'''
multipleTranslations : middle1_word portugueseTranslation suffix_error_word portugueseTranslation multipleTranslations
                    | no_hifen portugueseTranslation abbreviation portugueseTranslation multipleTranslations
                    | middle2_word portugueseTranslation abbreviation portugueseTranslation multipleTranslations
'''
'''
multipleTranslations : no_hifen portugueseTranslation abbreviation portugueseTranslation multipleTranslations
'''
def p_multipleTranslations4(p):
    '''
    multipleTranslations : middle1_word portugueseTranslation suffix_error_word portugueseTranslation multipleTranslations
                         | no_hifen portugueseTranslation abbreviation portugueseTranslation multipleTranslations
                         | middle2_word portugueseTranslation abbreviation portugueseTranslation multipleTranslations
    '''
    final_word = p[1] + " " + p[3]
    portugueseTranslation = p[2] + " " + p[4]
    p[5] [final_word] = portugueseTranslation
    p[0] = p[5]



# return on capital
#   employed (ROCE)          rendimento (m) de capital investido
def p_multipleTranslations5(p):
    "multipleTranslations : no_hifen_paragraph no_hifen portugueseTranslation multipleTranslations"
    
    final_word = p[1] + " " + p[2]

    p[4][final_word] = p[3]
    p[0] = p[4]
    


# - within industry (TWI)   treinamento (mj dentro da indústria

#  - volume ratio (P/V)
#                            movimento
def p_multipleTranslations6(p):
    '''
    multipleTranslations : prefix_word portugueseTranslation multipleTranslations
                         | prefix_word_error portugueseTranslation multipleTranslations
                         | prefix_word_error_2 portugueseTranslation multipleTranslations
                         | middle1_word portugueseTranslation multipleTranslations
                         | middle1_word_error portugueseTranslation multipleTranslations
                         | middle1_word_error_2 portugueseTranslation multipleTranslations
                         | middle2_word portugueseTranslation multipleTranslations
                         | middle_word_5 portugueseTranslation multipleTranslations
                         | suffix_word portugueseTranslation multipleTranslations
                         | suffix_error portugueseTranslation multipleTranslations
                         | double_word portugueseTranslation multipleTranslations
                         | prefix_error_word portugueseTranslation multipleTranslations
                         | middle_error_word portugueseTranslation multipleTranslations
                         | suffix_error_word portugueseTranslation multipleTranslations             
    '''
    p[3][p[1]] = p[2]
    p[0] = p[3]                   
    

def p_multipleTranslations7(p):
    "multipleTranslations : "
    p[0] = {}

def p_error(p):
    print(f"Erro sintático: " + p.value)



# Tentativa de resolução de conflitos 

# planning-programming -       sistema (m) orçamentário de
#  budgeting- (PPBS)            planejamento e programação    
# (suffix_word portugueseTranslation suffix_error_word portugueseTranslation)

# com

# shift -    (suffix_word portugueseTranslation)


parser = yacc.yacc()
print(parser.parse(text, debug=1))

