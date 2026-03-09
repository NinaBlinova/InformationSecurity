import hashlib
from math import ceil

from sympy import randprime, igcd


class RSA:
    E: int = 65537  # открытая экспонента

    def __init__(self, length: int):
        self._length = length

        p, q = self.generate_pq(length, self.E)
        self._n = q * p

        euler_func = (p - 1) * (q - 1)
        self._d = pow(self.E, -1, euler_func) #  закрытый ключ

    def encode_text(self, text: str) -> list:
        """
        Шифрует строку, разбивая её на блоки
        """
        message_bytes = text.encode('utf-8')

        block_size = (self._length // 8) - 1

        encrypted_blocks = []
        for i in range(0, len(message_bytes), block_size):
            block = message_bytes[i:i + block_size]
            block_int = int.from_bytes(block, byteorder='big')
            encrypted_block = self.encode(block_int)
            encrypted_blocks.append(encrypted_block)

        return encrypted_blocks

    def decode_text(self, encrypted_blocks: list) -> str:
        """
        Дешифрует список зашифрованных блоков обратно в строку
        """
        message_bytes = bytearray()

        for block_int in encrypted_blocks:
            decrypted_int = self.decode(block_int)
            byte_length = (decrypted_int.bit_length() + 7) // 8
            block_bytes = decrypted_int.to_bytes(byte_length, byteorder='big')
            message_bytes.extend(block_bytes)

        return message_bytes.decode('utf-8')

    def encode(self, message: int) -> int:
        """
        Шифрование сообщения (числа) открытым ключом (n, E)
        """
        if message >= self._n:
            raise ValueError(f'Сообщение {message} слишком большое для модуля {self._n}')

        return pow(message, self.E, self._n)

    def decode(self, cipher: int) -> int:
        """
        Расшифровка сообщения (числа) закрытым ключом (n, d)
        """
        if cipher >= self._n:
            raise ValueError(f'Шифротекст {cipher} слишком большой для модуля {self._n}')

        return pow(cipher, self._d, self._n)

    def sign(self, document: str) -> int:
        """
        Создание подписи документа с использованием SHA-1
        """
        hash_bytes = hashlib.sha1(document.encode('utf-8')).digest()
        hash_int = int.from_bytes(hash_bytes, byteorder='big')

        signature = pow(hash_int, self._d, self._n)
        return signature

    def verify(self, document: str, signature: int) -> bool:
        """
        Проверка подписи документа с использованием SHA-1
        """
        hash_bytes = hashlib.sha1(document.encode('utf-8')).digest()
        hash_int = int.from_bytes(hash_bytes, byteorder='big')

        extracted_hash = pow(signature, self.E, self._n)
        return hash_int == extracted_hash


    @staticmethod
    def generate_pq(length_key: int, e: int):
        """Генерирует p и q такими, чтобы p * q в битах имело длину length_key"""

        try:
            low_p = 2 ** (length_key // 2 - 1)
            high_p = 2 ** (length_key // 2) - 1
            p = randprime(low_p, high_p)

            q_min = ceil(2 ** (length_key - 1) / p)
            q_max = (2 ** length_key - 1) // p
            q = randprime(q_min, q_max)

            if igcd((p - 1) * (q - 1), e) == 1:
                return p, q
            else:
                return RSA.generate_pq(length_key, e)

        except ValueError:
            """При случайном совпадении, что нет простых чисел в заданном диапазоне, заново вызываем функцию"""
            return RSA.generate_pq(length_key, e)