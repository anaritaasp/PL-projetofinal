


def buildFile(result):
    for letter in result:

        for base in letter:

            for (base_word, base_translation, dict_base) in base:

                for (english, portuguese) in dict_base:
                    