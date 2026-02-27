from random import sample
from math import isqrt, ceil
from typing import Dict

from . import EMPTY_SIMBLE, ENGLISH_ALPHANET, SIMBLE_ADJACENCY, KEY_TYPE


def get_random_key(alphabet: str = ENGLISH_ALPHANET) -> KEY_TYPE:
    columns_count = isqrt(len(alphabet))
    raws_count = ceil(len(alphabet) / columns_count)
    empty_count = raws_count * columns_count - len(alphabet)

    first_simbols = sample(alphabet, columns_count)
    second_simbols = sample(alphabet, raws_count)

    full_alphabet = alphabet + EMPTY_SIMBLE * empty_count
    key_matrix = [['*'] + first_simbols] + [
        list(second_simbols[raw] + full_alphabet[columns_count * raw: columns_count * (raw + 1)])
        for raw in range(raws_count)]

    return key_matrix


def create_key_matrix_from_text(text: str) -> KEY_TYPE:
    key_matrix = list(map(str.split, text.splitlines()))
    return key_matrix


def print_key_matrix(key_matrix: KEY_TYPE):
    text = '\n'.join([' '.join(raw) for raw in key_matrix])
    print(text)


class PolybeanCipher:
    __slots__ = ('_key_encryption', '_key_decryption', '_key_matrix')

    def __init__(self, key_matrix: KEY_TYPE) -> None:
        self._key_matrix = key_matrix
        """
        Пример key_matrix:
        [
        ['*', 'A', 'B', 'C', 'D', 'E'],
        ['A', 'A', 'B', 'C', 'D', 'E'],
        ['B', 'F', 'G', 'H', 'I/J', 'K'],
        ['C', 'L', 'M', 'N', 'O', 'P'],
        ['D', 'Q', 'R', 'S', 'T', 'U'],
        ['E', 'V', 'W', 'X', 'Y', 'Z'],
        ]
        """
        first_simbols = key_matrix[0][1:]
        second_simbols = [line[0] for line in key_matrix[1:]]

        self._key_encryption: Dict[str, str] = {
            key_matrix[raw][column]: first_simbols[column - 1] + second_simbols[raw - 1]
            for raw in range(1, len(second_simbols) + 1)
            for column in range(1, len(first_simbols) + 1)
            if key_matrix[raw][column] is not EMPTY_SIMBLE
        }

        # разделение смежных букв на разные ключи
        adjacency_items = list(filter(lambda item: SIMBLE_ADJACENCY in item[0], self._key_encryption.items()))
        for key, value in adjacency_items:
            self._key_encryption.pop(key)
            first_letter, second_letter = key.split(SIMBLE_ADJACENCY)
            self._key_encryption[first_letter] = value
            self._key_encryption[second_letter] = value

        self._key_decryption: Dict[str, str] = {
            first_simbols[column - 1] + second_simbols[raw - 1]: key_matrix[raw][column]
            for raw in range(1, len(second_simbols) + 1)
            for column in range(1, len(first_simbols) + 1)
            if key_matrix[raw][column] is not EMPTY_SIMBLE
        }

    def encrypt(self, text: str) -> str:
        return ''.join(map(self._key_encryption.__getitem__, text))

    def decrypt(self, text: str) -> str:
        pairs = map(lambda pair: pair[0] + pair[1], zip(text[::2], text[1::2]))
        return ''.join(map(self._key_decryption.__getitem__, pairs))


"""
Aa	8,17 %
Bb	1,49 %
Cc	2,78 %
Dd	4,25 %
Ee	12,70 %
Ff	2,23 %
Gg	2,02 %
Hh	6,09 %
Ii	6,97 %
Jj	0,15 %
Kk	0,77 %
Ll	4,03 %
Mm	2,41 %
Nn	6,75 %
Oo	7,51 %
Pp	1,93 %
Qq	0,10 %
Rr	5,99 %
Ss	6,33 %
Tt	9,06 %
Uu	2,76 %
Vv	0,98 %
Ww	2,36 %
Xx	0,15 %
Yy	1,97 %
Zz	0,07 %
"""
