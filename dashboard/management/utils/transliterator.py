class Transliterator:

    @staticmethod
    def transliterate_ru_to_en(word):
        ru_en = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
                 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
                 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
                 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
                 'ш': 'sh', 'щ': 'shch', 'ь': 'blank', 'ы': 'y', 'ъ': 'blank', 'э': 'e', 'ю': 'yu', 'я': 'ya'}

        return "".join(
            map(lambda x: '' if ru_en.get(x, False) == 'blank' else ru_en[x] if ru_en.get(x, False) else x,
                word.lower()))
