from collections import OrderedDict

from analisesintatica import parser


def buildFile(namefile):

    with open(namefile, 'r') as file:
        data = file.read()

    #print(parser.parse(data)) #print(parser.parse(text, debug=1)) #print(parser.parse(text))
    dicionario = parser.parse(data)

    dicionario = OrderedDict(reversed(list(dicionario.items())))

    file = open("final_" + namefile, "w")
    for letter in dicionario:
        bases = dicionario[letter]
        bases = OrderedDict(reversed(list(bases.items())))
        for base in bases:
            (base_word, base_translations, dict_base) = bases[base]
            string_base = "+base " + base_word + ":\n"

            base_translations = [x for x in base_translations if x != ""] # tiramos as strings vazias
            if len(base_translations) > 0:
                file.write("EN " + base_word + "\n")
                for base_translation in base_translations:
                    string_long_base = "PT " + base_translation + "\n"
                    file.write(string_long_base)
                file.write("\n")

            dict_base = OrderedDict(reversed(list(dict_base.items())))
            for english in dict_base:
                file.write("EN " + english + "\n" + string_base)
                portuguese_translations = dict_base[english]
                for portuguese in portuguese_translations:
                    if portuguese != "":
                        file.write("PT " + portuguese + "\n")
                file.write("\n")

    print()
    print("O resultado final foi colocado no ficheiro '" + "final_" + namefile + "'!\n")

            
def main():
    opcao = -1

    print()
    print("##########################################################")
    print("#                                                        #")
    print("#  PL 2023 - 2.4 - Reverse Engineering de um dicionário  #")
    print("#                                                        #")
    print("#                  Grupo 7.5 - RevEng                    #")
    print("#                                                        #")
    print("##########################################################")
    
    while opcao == -1:
        print()
        print(" Escolha o ficheiro que quer aplicar: ")
        print(" ------------------------------------")
        print(" 1) dic-finance-en.pt.txt")
        print(" 2) teste.txt")
        print(" 0) SAIR")
        print()
        print("Escreva aqui a opção: ", end ="")
        x = int(input())

        if x == 1:
            buildFile("dic-finance-en.pt.txt")
        elif x == 2:
            buildFile("teste.txt")
        elif x == 0:
            opcao = 0

    print()

if __name__ == '__main__':
    main()