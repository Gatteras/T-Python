def search_vowels(phrase: str) -> list:
    """Выводит гласные, найденные в строке word"""
    vowels = set('aeiouy')
    return sorted(list(vowels.intersection(set(phrase))))


def search_letters(phrase: str = '', letters: str = 'aeiouy') -> list:
    """Возвращает упорядоченный список букв из letters, содержащихся в prase"""
    return sorted(list(set(letters).intersection(set(phrase))))
