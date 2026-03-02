"""
Вариант 3
Потоковая система шифрования на основе Генератора-мультиплексора Дженнингса (Jennings Generator)

Генератор Дженнингса состоит из двух РСЛОС (регистров сдвига с линейной обратной связью):
  - РСЛОС A (управляющий) — выход управляет выбором разряда РСЛОС B
  - РСЛОС B (данных) — из него считывается либо текущий бит, либо следующий,
    в зависимости от выхода РСЛОС A

Ключевой поток: если bit_A == 0 -> берётся bit_B[0], иначе -> bit_B[1]
затем РСЛОС B тактируется один или два раза (irregular clocking)
"""

from typing import List


class LFSR:
    """Регистр сдвига с линейной обратной связью (РСЛОС / LFSR)"""

    def __init__(self, taps: List[int], state: List[int]):
        """
        taps  — список позиций (1-индексация) для XOR обратной связи
        state — начальное состояние (список битов, LSB first)
        """
        if not state or all(b == 0 for b in state):
            raise ValueError("Начальное состояние РСЛОС не может быть нулевым")
        self.taps = taps
        self.state = list(state)
        self.length = len(state)

    def clock(self) -> int:
        """Один такт: возвращает выходной бит (state[0]), сдвигает регистр"""
        output = self.state[0]
        feedback = 0
        for t in self.taps:
            feedback ^= self.state[t - 1]
        self.state = self.state[1:] + [feedback]
        return output

    def peek(self) -> int:
        """Возвращает текущий выходной бит без тактирования"""
        return self.state[0]


class JenningsGenerator:
    """
    Генератор-мультиплексор Дженнингса

    РСЛОС A управляет тактированием РСЛОС B:
      - output_A == 0 -> берём текущий бит B, тактируем B один раз
      - output_A == 1 -> тактируем B, берём новый бит B, тактируем B ещё раз
    РСЛОС A тактируется на каждом шаге
    """

    def __init__(
        self,
        taps_a: List[int],
        state_a: List[int],
        taps_b: List[int],
        state_b: List[int],
    ):
        self.lfsr_a = LFSR(taps_a, state_a)
        self.lfsr_b = LFSR(taps_b, state_b)

    def next_bit(self) -> int:
        """
        Генерирует один бит ключевого потока   

        Схема Дженнингса (нерегулярное тактирование):
          1. Считываем текущий выходной бит РСЛОС B (без тактирования)
          2. Тактируем РСЛОС A — получаем управляющий бит
          3. Если управляющий бит == 1 -> тактируем РСЛОС B дважды,
             иначе -> тактируем РСЛОС B один раз
        """
        keybit = self.lfsr_b.peek()
        bit_a = self.lfsr_a.clock()
        self.lfsr_b.clock()
        if bit_a == 1:
            self.lfsr_b.clock()   # дополнительный такт
        return keybit

    def generate(self, length: int) -> List[int]:
        """Генерирует последовательность битов заданной длины"""
        return [self.next_bit() for _ in range(length)]


def bytes_to_bits(data: bytes) -> List[int]:
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits


def bits_to_bytes(bits: List[int]) -> bytes:
    result = []
    for i in range(0, len(bits), 8):
        chunk = bits[i:i + 8]
        # дополняем до 8 бит если нужно
        while len(chunk) < 8:
            chunk.append(0)
        byte = 0
        for b in chunk:
            byte = (byte << 1) | b
        result.append(byte)
    return bytes(result)


def xor_bits(data: List[int], keystream: List[int]) -> List[int]:
    return [d ^ k for d, k in zip(data, keystream)]


def encrypt(
    plaintext: bytes,
    taps_a: List[int],
    state_a: List[int],
    taps_b: List[int],
    state_b: List[int],
) -> bytes:
    """Шифрование открытого текста"""
    gen = JenningsGenerator(taps_a, state_a, taps_b, state_b)
    plain_bits = bytes_to_bits(plaintext)
    key_bits = gen.generate(len(plain_bits))
    cipher_bits = xor_bits(plain_bits, key_bits)
    return bits_to_bytes(cipher_bits)


def decrypt(
    ciphertext: bytes,
    taps_a: List[int],
    state_a: List[int],
    taps_b: List[int],
    state_b: List[int],
) -> bytes:
    """Дешифрование (симметрично шифрованию - XOR)"""
    return encrypt(ciphertext, taps_a, state_a, taps_b, state_b)
