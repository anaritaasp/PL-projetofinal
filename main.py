from collections import OrderedDict

from analisesintatica import dicionario


def buildFile():
    file = open("final.txt", "w")
    for letter in dicionario:
        bases = dicionario[letter]
        for base in bases:
            (base_word, base_translation, dict_base) = bases[base]
            string_base = "+base " + base_word + "\n"
            if base_translation != "":
                string_long_base = "EN " + base_word + "\nPT " + base_translation + "\n\n"
                file.write(string_long_base)
            dict_base = OrderedDict(reversed(list(dict_base.items())))
            for english in dict_base:
                file.write("EN " + english + "\n" + string_base)
                portuguese = dict_base[english]
                file.write("PT " + portuguese + "\n\n")
def main():
    print()
    print("########################################################")
    print("# PL 2023 - 2.4 - Reverse Engineering de um dicionário #")
    print("########################################################")

    buildFile()

    print()
    print("O resultado final foi colocado no ficheiro final.txt!\n")

if __name__ == '__main__':
    main()