import unittest as ut

from ThirdLR.util import RSA


class RsaTest(ut.TestCase):
    def test_generate_pq(self):
        key_lengths = [128, 256, 512, 1024, 2048]
        num_trials = [10000, 1000, 100, 10, 5]

        for length, trials in zip(key_lengths, num_trials):
            with self.subTest(length=length):
                for _ in range(trials):
                    p, q = RSA.generate_pq(length, RSA.E)
                    self.assertEqual((p * q).bit_length(), length)

    def test_key_properties(self):
        rsa = RSA(256)
        message = 12345
        cipher = rsa.encode(message)
        self.assertEqual(rsa.decode(cipher), message)

    def test_encrypt_decrypt_int(self):
        rsa = RSA(128)
        test_messages = [0, 1, 42, 123456, rsa._n - 1]
        for msg in test_messages:
            with self.subTest(msg=msg):
                cipher = rsa.encode(msg)
                decrypted = rsa.decode(cipher)
                self.assertEqual(decrypted, msg)

    def test_encrypt_decrypt_text(self):
        rsa = RSA(256)
        original = 'Hello, RSA! Привет, мир! 123'
        encrypted_blocks = rsa.encode_text(original)
        decrypted = rsa.decode_text(encrypted_blocks)
        self.assertEqual(original, decrypted)

    def test_sign_verify(self):
        rsa = RSA(256)
        document = 'Важный документ №42'
        signature = rsa.sign(document)

        self.assertTrue(rsa.verify(document, signature))

        fake_doc = document + 'x'
        self.assertFalse(rsa.verify(fake_doc, signature))

        fake_signature = signature + 1
        self.assertFalse(rsa.verify(document, fake_signature))

    def test_various_key_lengths(self):
        for length in (128, 256, 512, 1024):
            with self.subTest(length=length):
                rsa = RSA(length)
                text = 'Тестовое сообщение для длины ключа ' + str(length)
                encrypted = rsa.encode_text(text)
                decrypted = rsa.decode_text(encrypted)
                self.assertEqual(text, decrypted)