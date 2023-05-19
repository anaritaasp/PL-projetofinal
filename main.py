from collections import OrderedDict
import sys
import os

from analisesintatica import dicionario


def buildFile():
    for letter in dicionario:
        bases = dicionario[letter]
        for base in bases:
            (base_word, base_translation, dict_base) = bases[base]
            string_base = "+base " + base_word
            if base_translation != "":
                string_base = string_base + " " + base_translation
            dict_base = OrderedDict(reversed(list(dict_base.items())))
            for english in dict_base:
                portuguese = dict_base[english]
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