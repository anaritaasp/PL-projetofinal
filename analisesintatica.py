from collections import OrderedDict
import re
import ply.yacc as yacc

from analiselexica import tokens


#  - overheads            despesas (fpl) de administração     ->   fpl -> feminino plural
# m -> masculino singular
# f -> feminino singular
# mpl -> masculino plural


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
    "translations : normalword traducao translations"
    portugueseTranslations = [p[2]]
    if re.search(r'[,;]', p[2]):
        portugueseTranslations = re.split(r'[,;]\s*', p[2])
    p[3][p[1]] = (p[1], portugueseTranslations, {})
    p[0] = p[3] 


#Latin American Free Trade   Associação (f) Latino-Americana de
#  Association (LAFTA)         Livre Comércio (ALALC)    
#
# clerical work measurement   medição (f) de trabalho administrativo
# (CWM)
def p_translations2(p):
    '''
    translations : normalword traducao no_hifen traducao translations
                 | normalword traducao abbreviation traducao translations
    '''
    #string que guarda as portugueseTranslations
    portugueseTranslation = p[2]
    
    if p[4] == "": #verificar se a segunda PortugueseTranslation é empty
        pass 
    else:   
        portugueseTranslation += " " + p[4] 
    
    portugueseTranslations = [portugueseTranslation]
    if re.search(r'[,;]', portugueseTranslation):
        portugueseTranslations = re.split(r'[,;]\s*', portugueseTranslation)

    # o resto:
    final_word = p[1] + p[3] #juntamos a palavra em ingles com a linha de baixo que tem a sua continuação
    
    p[5][final_word] = (final_word, portugueseTranslations, {}) 
    p[0] = p[5] #output



# copyright                     direitos (mpl) reservados, direito
#                                (m) autoral 
#  - advertising              publicidade (f) empresarial
#

def p_translations3(p):
    '''
    translations : normalword traducao multipleTranslations translations
    '''
    
    portugueseTranslations = [p[2]]
    if re.search(r'[,;]', p[2]):
        portugueseTranslations = re.split(r'[,;]\s*', p[2])

    p[4][p[1]] = (p[1], portugueseTranslations, p[3])
    p[0] = p[4]

    
def p_translations4(p):
    '''
    translations : baseword traducao multipleTranslations translations
                 | baseword_error traducao multipleTranslations translations
                 | baseword_error multipleTranslations translations
    '''

    if len(p) == 5: # translations : baseword traducao multipleTranslations translations
        portugueseTranslations = [p[2]]
        if re.search(r'[,;]', p[2]):
            portugueseTranslations = re.split(r'[,;]\s*', p[2])
        p[4][p[1]] = (p[1], portugueseTranslations, p[3])
        p[0] = p[4]
    else: # translations : baseword_error multipleTranslations translations
        # não existe string traducao
        p[3][p[1]] = (p[1], [], p[2])
        p[0] = p[3]



# LAFTA (Latin American Free      ALALC (Associação Latino-
#           Trade Association)   Americana de Livre Comércio)
#
# ROCE (return on capital
#  employed)                       rendimento (m) do capital investido
def p_translations5(p):
    '''
    translations : a_parenteses traducao f_parenteses traducao translations
                 | a_parenteses_paragraph f_parenteses traducao translations
    '''
    
    if len(p) == 6:
        #string que guarda as portugueseTranslations
        portugueseTranslation = p[2]
        if p[2] != "": 
            portugueseTranslation += " "
        portugueseTranslation += p[4] 

        portugueseTranslations = [portugueseTranslation]
        if re.search(r'[,;]', portugueseTranslation):
            portugueseTranslations = re.split(r'[,;]\s*', portugueseTranslation)
            
        # o resto:
        total_parenteses = p[1] + " " + p[3] #abre parenteses + fechar parenteses
        
        p[5][total_parenteses] = (total_parenteses, portugueseTranslations, {}) 
        p[0] = p[5]
    
    else:
        #string que guarda as portugueseTranslations
        portugueseTranslation = p[3] 

        portugueseTranslations = [portugueseTranslation]
        if re.search(r'[,;]', portugueseTranslation):
            portugueseTranslations = re.split(r'[,;]\s*', portugueseTranslation)
            
        # o resto:
        total_parenteses = p[1] + " " + p[2]  #abre parenteses + fechar parenteses
        
        p[4][total_parenteses] = (total_parenteses, portugueseTranslations, {}) 
        p[0] = p[4]



#R and D (research and            pesquisa (f) e desenvolvimento (m)
# development\n
def p_translations6(p):
    '''
    translations : a_parenteses traducao baseword_error translations
    '''

    #string que guarda as portugueseTranslations
    portugueseTranslation = p[2]

    portugueseTranslations = [portugueseTranslation]
    if re.search(r'[,;]', portugueseTranslation):
        portugueseTranslations = re.split(r'[,;]\s*', portugueseTranslation)
        
    # o resto:
    total_parenteses = p[1] + p[3] + ")" #abre parenteses + fechar parenteses
    
    p[4][total_parenteses] = (total_parenteses, portugueseTranslations, {}) 
    p[0] = p[4]


#definimos um caso para o vazio      
def p_translations7(p): 
    "translations : "
    p[0] = {}


# Lidar com as multiplas traduções:    capital (m) circulante, capital (m) de giro


#  management information -
#  (MIS)                       sistema (m) de dados para gestão
#
# return on -
#   employed (ROCE)      rendimento (m) do capital investido
def p_multipleTranslations3(p):
    '''
    multipleTranslations : middle2_word_error abbreviation traducao multipleTranslations
                         | middle2_word_error no_hifen traducao multipleTranslations
    '''
    final_word = p[1] + " " + p[2]
    portugueseTranslations = [p[3]]
    if re.search(r'[,;]', p[3]):
        portugueseTranslations = re.split(r'[,;]\s*', p[3])
    p[4][final_word] = portugueseTranslations
    p[0] = p[4]
            



# planning-programming -       sistema (m) orçamentário de
#  budgeting- (PPBS)            planejamento e programação
# 
# predetermined motion time    sistema (m) de movimentos
#  (PMTS)                       pré-determinados
#
# computerised information -
#  (COINS)                     sistema (m) computadorizado de dados
#
# planning programming - system   sistema (m) orçamentário de
# (PPBS)                           programação e planejamento 
#
#
#  predetermined - time system   sistema (m) de movimentos
# (PMTS)                         pré-determinados

def p_multipleTranslations4(p):
    '''
    multipleTranslations : middle1_word traducao suffix_error_word traducao multipleTranslations
                         | no_hifen traducao abbreviation traducao multipleTranslations
                         | middle2_word traducao abbreviation traducao multipleTranslations
                         | middle1_word traducao abbreviation traducao multipleTranslations
    '''
    final_word = p[1] + " " + p[3]
    portugueseTranslation = (p[2] + " " + p[4])
    portugueseTranslations = [portugueseTranslation]
    if re.search(r'[,;]', portugueseTranslation):
        portugueseTranslations = re.split(r'[,;]\s*', portugueseTranslation)
    p[5] [final_word] = portugueseTranslations
    p[0] = p[5]



# return on capital
#   employed (ROCE)          rendimento (m) de capital investido
#
#   organisation and methods
#   (O and M)                  organização (f) e métodos (mpl)
def p_multipleTranslations5(p):
    '''
    multipleTranslations : no_hifen_paragraph no_hifen traducao multipleTranslations
                         | no_hifen_paragraph abbreviation traducao multipleTranslations
    '''
    
    final_word = p[1] + " " + p[2]

    portugueseTranslations = [p[3]]
    if re.search(r'[,;]', p[3]):
         portugueseTranslations = re.split(r'[,;]\s*', p[3])
    p[4][final_word] = portugueseTranslations
    p[0] = p[4]
    


# - within industry (TWI)   treinamento (mj dentro da indústria

#  - volume ratio (P/V)
#                            movimento

#  (of personnel)                promoção (f) (de cargo)
def p_multipleTranslations6(p):
    '''
    multipleTranslations : prefix_word traducao multipleTranslations
                         | prefix_word_error traducao multipleTranslations
                         | prefix_word_error_2 traducao multipleTranslations
                         | prefix_word_error_2 baseword_error multipleTranslations
                         | middle1_word traducao multipleTranslations
                         | middle1_word_error_2 traducao multipleTranslations
                         | middle_word_5 traducao multipleTranslations
                         | middle2_word traducao multipleTranslations
                         | suffix_word traducao multipleTranslations
                         | suffix_error traducao multipleTranslations
                         | double_word traducao multipleTranslations
                         | prefix_error_word traducao multipleTranslations
                         | middle_error_word traducao multipleTranslations
                         | suffix_error_word traducao multipleTranslations  
                         | no_hifen traducao multipleTranslations   
                         | abbreviation traducao multipleTranslations
    '''

    portugueseTranslations = [p[2]]
    if re.search(r'[,;]', p[2]):
        portugueseTranslations = re.split(r'[,;]\s*', p[2])
    
    p[3][p[1]] = portugueseTranslations
    p[0] = p[3]                   
    
# middle2_word_error ->  salary progression -
def p_multipleTranslations9(p):
    '''
    multipleTranslations : middle1_word_error multipleTranslations
                         | middle2_word_error multipleTranslations
    '''
    p[2][p[1]] = []
    p[0] = p[2] 

def p_multipleTranslations8(p):
    "multipleTranslations : "
    p[0] = {}

def p_traducao(p):
    '''
    traducao : portugueseTranslationError
             | portugueseTranslation
    '''
    p[0] = p[1]


def p_error(p):
    print(f"Erro sintático: " + p.value)



with open('dic-finance-en.pt.txt', 'r') as file:
    data = file.read()

parser = yacc.yacc()
#print(parser.parse(data)) #print(parser.parse(text, debug=1)) #print(parser.parse(text))
dicionario = parser.parse(data)

dicionario = OrderedDict(reversed(list(dicionario.items())))

#print(dicionario)