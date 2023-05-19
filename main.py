from collections import OrderedDict

from analisesintatica import dicionario


def buildFile():

    file = open("final.txt", "w")
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
            
def main():
    print()
    print("##########################################################")
    print("#                                                        #")
    print("#  PL 2023 - 2.4 - Reverse Engineering de um dicionário  #")
    print("#                                                        #")
    print("#                  Grupo 7.5 - RevEng                    #")
    print("#                                                        #")
    print("##########################################################")

    buildFile()

    print()
    print("O resultado final foi colocado no ficheiro 'final.txt'!\n")

if __name__ == '__main__':
    main()