import random
from enum import Enum
from typing import Optional

from ThirdLR.util import RSA


class Command(Enum):
    EXIT = '0'

    DELETE_KEY = '1'

    GENERATE_RANDOM = '2'
    GENERATE_PASSWORD = '3'

    ENCRYPT = '4'
    DECRYPT = '5'
    SIGN = '6'
    VERIFY = '7'
    SHOW_PUBLIC = '8'

    NOTHING = '9'

    @classmethod
    def _missing_(cls, value):
        return cls.NOTHING


class MainRSA:
    def __init__(self):
        self.rsa: Optional[RSA] = None
        self.command = Command.NOTHING

    def draw_menu(self):
        print('\n--- RSA Menu ---')
        print('0 - exit')
        if self.rsa is not None:
            print('1 - delete key')
            print('4 - encrypt text')
            print('5 - decrypt text')
            print('6 - sign document')
            print('7 - verify signature')
            print('8 - show public key (n, e)')
        else:
            print('2 - generate random key (choose length)')
            print('3 - generate key from password')
        print('----------------')

    def delete_key(self):
        self.rsa = None
        print('Key deleted.')

    def generate_random_key(self):
        try:
            length = int(input('Enter key length in bits (e.g., 1024, 2048): '))
            if length < 128:
                print('Key length too small, using 128 bits minimum.')
                length = 128
            self.rsa = RSA(length)
            print('Random key generated successfully.')
            self._show_public()
        except Exception as e:
            print(f'Error generating key: {e}')

    def generate_key_from_password(self):
        try:
            password = input('Enter password: ')
            length = int(input('Enter key length in bits: '))
            if length < 128:
                length = 128
            state = random.getstate()
            random.seed(password)
            self.rsa = RSA(length)
            random.setstate(state)
            print('Key generated from password successfully.')
            self._show_public()
        except Exception as e:
            print(f'Error generating key: {e}')

    def encrypt(self):
        if self.rsa is None:
            print('No key loaded.')
            return
        try:
            text = input('Enter text to encrypt: ')
            encrypted_blocks = self.rsa.encode_text(text)
            output = ' '.join(str(b) for b in encrypted_blocks)
            print('Encrypted blocks (numbers):')
            print(output)
        except Exception as e:
            print(f'Encryption error: {e}')

    def decrypt(self):
        if self.rsa is None:
            print('No key loaded.')
            return
        try:
            data = input('Enter encrypted blocks (numbers separated by space): ')
            blocks = [int(x) for x in data.strip().split()]
            decrypted_text = self.rsa.decode_text(blocks)
            print('Decrypted text:')
            print(decrypted_text)
        except Exception as e:
            print(f'Decryption error: {e}')

    def sign(self):
        if self.rsa is None:
            print('No key loaded.')
            return
        try:
            document = input('Enter document text to sign: ')
            signature = self.rsa.sign(document)
            print(f'Signature (integer): {signature}')
        except Exception as e:
            print(f'Signing error: {e}')

    def verify(self):
        if self.rsa is None:
            print('No key loaded.')
            return
        try:
            document = input('Enter document text: ')
            signature = int(input('Enter signature (integer): '))
            valid = self.rsa.verify(document, signature)
            print('Signature is VALID.' if valid else 'Signature is INVALID.')
        except Exception as e:
            print(f'Verification error: {e}')

    def show_public(self):
        if self.rsa is None:
            print('No key loaded.')
            return
        self._show_public()

    def _show_public(self):
        print(f'Public key (n, e):')
        print(f'n = {self.rsa._n}')
        print(f'e = {self.rsa.E}')

    def run(self):
        while self.command != Command.EXIT:
            match self.command:
                case Command.DELETE_KEY:
                    self.delete_key()
                case Command.GENERATE_RANDOM:
                    self.generate_random_key()
                case Command.GENERATE_PASSWORD:
                    self.generate_key_from_password()
                case Command.ENCRYPT:
                    self.encrypt()
                case Command.DECRYPT:
                    self.decrypt()
                case Command.SIGN:
                    self.sign()
                case Command.VERIFY:
                    self.verify()
                case Command.SHOW_PUBLIC:
                    self.show_public()

            self.draw_menu()
            self.command = Command(input('Enter command: '))


if __name__ == '__main__':
    app = MainRSA()
    app.run()

# 96440716976316323632979360518003590884768343450050041307159659018425334750494324892148500935843017905675569073864651918219936332954902434369115477118003671741766668401138505428792606951686500224276700016726205737069548380018501822848066524399654387317036871643539046962416494491988946999925714841596512994947