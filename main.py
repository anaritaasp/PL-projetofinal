import sys
import os

from analisesintatica import dicionario


def buildFile():
    for letter in dicionario:

        for base in letter:

            for (base_word, base_translation, dict_base) in base:

                for (english, portuguese) in dict_base:
                    print()

def main():
    print()

if __name__ == '__main__':
    main()