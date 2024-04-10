class Transliterator:

    @staticmethod
    def transliterate_ru_to_en(word):
        ru_en = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
                 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
                 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
                 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
                 'ш': 'sh', 'щ': 'shch', 'ь': '`', 'ы': 'y', 'ъ': '`', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

        return "".join(map(lambda x: ru_en[x] if ru_en.get(x, '') else x, word.lower()))
