import unittest as ut

from FirstLR.polybean.polybean_algorithm.utils import PolybeanCipher, get_random_key, create_key_matrix_from_text, \
    FrequencyAnalysis


class PolybeanCipherTest(ut.TestCase):
    def test_adjacency_key_dict(self):
        key_matrix = [['*', 'a', 'b'],
                      ['c', 'k', 'm'],
                      ['d', 'p/q', 'n']]
        polybean_cipher = PolybeanCipher(key_matrix)

        expected_key_encryption = {'k': 'ac', 'm': 'bc', 'p': 'ad', 'q': 'ad', 'n': 'bd'}
        expected_key_decryption = {'ac': 'k', 'bc': 'm', 'ad': 'p/q', 'bd': 'n'}

        self.assertDictEqual(expected_key_encryption, polybean_cipher._key_encryption)
        self.assertDictEqual(expected_key_decryption, polybean_cipher._key_decryption)

    def test_empty_key_dict(self):
        key_matrix = [['*', 'a', 'b'],
                      ['c', 'k', 'm'],
                      ['d', 'p', '*']]
        polybean_cipher = PolybeanCipher(key_matrix)

        expected_key_encryption = {'k': 'ac', 'm': 'bc', 'p': 'ad'}
        expected_key_decryption = {'ac': 'k', 'bc': 'm', 'ad': 'p'}

        self.assertDictEqual(expected_key_encryption, polybean_cipher._key_encryption)
        self.assertDictEqual(expected_key_decryption, polybean_cipher._key_decryption)

    def test_encrypt(self):
        key_matrix = [['*', 'a', 'b'],
                      ['c', 'k', 'm'],
                      ['d', 'p/q', 'n']]
        polybean_cipher = PolybeanCipher(key_matrix)

        text = 'knp'
        expected_encrypted_text = 'acbdad'
        actual_encrypted_text = polybean_cipher.encrypt(text)

        self.assertEqual(expected_encrypted_text, actual_encrypted_text)

    def test_decrypt(self):
        key_matrix = [['*', 'a', 'b'],
                      ['c', 'k', 'm'],
                      ['d', 'p/q', 'n']]
        polybean_cipher = PolybeanCipher(key_matrix)

        text = 'acbdad'
        expected_decrypted_text = 'knp/q'
        actual_decrypted_text = polybean_cipher.decrypt(text)

        self.assertEqual(expected_decrypted_text, actual_decrypted_text)

    def test_random_key(self):
        key_matrix = get_random_key()
        pc = PolybeanCipher(key_matrix)

        text = pc.encrypt('test')
        text = pc.decrypt(text)
        self.assertEqual(text, 'test')

    def test_create_key_matrix_from_text(self):
        text = """* a b
                  c k m
                  d p/q n
                  f l *   """

        expected_key_matrix = [
            ['*', 'a', 'b'],
            ['c', 'k', 'm'],
            ['d', 'p/q', 'n'],
            ['f', 'l', '*']
        ]
        actual_key_matrix = create_key_matrix_from_text(text)

        self.assertEqual(expected_key_matrix, actual_key_matrix)

class FrequencyAnalysisTest(ut.TestCase):

    def test_find_nearest_letter(self):
        actual_nearest_letter = FrequencyAnalysis.find_nearest_letter(0.0202)
        self.assertEqual(actual_nearest_letter, 'g')