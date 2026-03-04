"""
Вариант 3
Потоковая система шифрования на основе Генератора-мультиплексора Дженнингса

Запуск:
    python main.py
"""

from jennings import JenningsGenerator, encrypt, decrypt
from tests import run_all_tests


# ---------------------------------------------------------------------------
# Параметры генератора (полиномы над GF(2))
# ---------------------------------------------------------------------------
# РСЛОС A: степень 10, примитивный многочлен x^10 + x^7 + x^5 + x^2 + 1
TAPS_A = [10, 7, 5, 2]
STATE_A = [1, 0, 1, 1, 0, 0, 1, 0, 1, 0]

# РСЛОС B: степень 11, примитивный многочлен x^11 + x^2 + 1
TAPS_B = [11, 2]
STATE_B = [1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1]

# Человека определяют не заложенные в нём качества, а только его выбор. — Альбус Дамблдор
# Мы сильны настолько, насколько мы едины, и слабы настолько, насколько разъединены. — Альбус Дамблдор

"""
❝ — Чёрт возьми, Гарри, ты убиваешь драконов! Если уж ты не можешь пригласить девчонок... — Знаешь, убивать драконов проще. ❞
"""

def demo_cipher():
    """Демонстрация шифрования/дешифрования"""
    message = "Всё, что мы теряем, обязательно к нам вернётся, только не всегда так, как мы ожидаем — Луна Лавгуд"
    plaintext = message.encode("utf-8")

    print("=" * 60)
    print("  Демонстрация шифрования")
    print("=" * 60)
    print(f"  Открытый текст : {message}")

    ciphertext = encrypt(plaintext, TAPS_A, STATE_A, TAPS_B, STATE_B)
    print(f"  Шифртекст (hex): {ciphertext.hex()}")

    decrypted = decrypt(ciphertext, TAPS_A, STATE_A, TAPS_B, STATE_B)
    decoded = decrypted[: len(plaintext)].decode("utf-8")
    print(f"  Расшифровано   : {decoded}")

    ok = decoded == message
    print(f"  Совпадение     : {'ДА ' if ok else 'НЕТ '}")
    print()


def demo_statistics():
    """Генерация ключевого потока и запуск статистических тестов"""
    SEQ_LEN = 20000  # бит для тестирования

    gen = JenningsGenerator(TAPS_A, STATE_A, TAPS_B, STATE_B)
    keystream = gen.generate(SEQ_LEN)

    ones = sum(keystream)
    zeros = SEQ_LEN - ones
    print("=" * 60)
    print(f"  Ключевой поток: {SEQ_LEN} бит")
    print(f"  Единиц: {ones} ({100*ones/SEQ_LEN:.2f}%)")
    print(f"  Нулей : {zeros} ({100*zeros/SEQ_LEN:.2f}%)")

    run_all_tests(keystream)


if __name__ == "__main__":
    demo_cipher()
    demo_statistics()
