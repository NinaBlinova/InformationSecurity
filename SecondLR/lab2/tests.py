"""
Статистические тесты
1. Частотный тест
 Проверяет, примерно ли одинаковое количество нулей и единиц во всей последовательности.
2. Последовательный тест
Проверяет равномерность распределения всех возможных комбинаций бит длины m
(тут, вероятно, m=2: 00, 01, 10, 11). В случайной строке все пары бит встречаются примерно с одинаковой частотой.
3. Тест серий
Проверяет, соответствует ли длина "серий" (последовательно идущих единиц или нулей) тому, что ожидается в случайной
последовательности. Например, в случайном потоке половина серий должна быть длиной 1, четверть — длиной 2 и т.д.
4. Автокорреляционный тест
Проверяет, есть ли зависимость между битами и их соседями (со сдвигом 1).
Если последовательность случайна, такой зависимости быть не должно.
5. Универсальный тест Маурера
Более сложный тест, который ищет сжимаемость последовательности. Если последовательность можно значительно сжать,
значит, в ней есть закономерности, и она не случайна. Этот тест хорошо обнаруживает "настоящие" случайные потоки
от псевдослучайных.
"""

import math
from typing import List, Tuple


# ---------------------------------------------------------------------------
# 1. Частотный тест (Monobit)
# ---------------------------------------------------------------------------

def frequency_test(bits: List[int]) -> Tuple[float, bool]:
    """
    Проверяет равновероятность 0 и 1 в последовательности

    Возвращает (p_value, passed)
    H0 принимается при p_value >= 0.01
    """
    n = len(bits)
    s = sum(1 if b == 1 else -1 for b in bits)
    s_obs = abs(s) / math.sqrt(n)
    # p-value = erfc(s_obs / sqrt(2))
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value, p_value >= 0.01


# ---------------------------------------------------------------------------
# 2. Последовательный тест
# ---------------------------------------------------------------------------

def serial_test(bits: List[int]) -> Tuple[float, bool]:
    """
    Частотный тест для всех 2-битных подпоследовательностей

    Считает частоты пар (00, 01, 10, 11) и вычисляет x^2.
    p_value считается через chi2 sf с df=3 (аппроксимация)
    """
    n = len(bits)
    counts = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0}
    for i in range(n - 1):
        pair = (bits[i], bits[i + 1])
        counts[pair] += 1
    total = sum(counts.values())
    expected = total / 4.0
    chi2 = sum((c - expected) ** 2 / expected for c in counts.values())
    # Приближённый p-value через regularized incomplete gamma
    p_value = _chi2_sf(chi2, df=3)
    return p_value, p_value >= 0.01


# ---------------------------------------------------------------------------
# 3. Тест серий
# ---------------------------------------------------------------------------

def runs_test(bits: List[int]) -> Tuple[float, bool]:
    """
    Тест серий (одинаковых подряд идущих битов)

    Сначала проверяет частотный тест (предусловие по NIST)
    Затем считает число серий и вычисляет p_value
    """
    n = len(bits)
    pi = sum(bits) / n

    # Предусловие: |pi - 0.5| < 2/sqrt(n)
    if abs(pi - 0.5) >= 2.0 / math.sqrt(n):
        return 0.0, False

    vn = 1 + sum(1 for i in range(n - 1) if bits[i] != bits[i + 1])
    numerator = abs(vn - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    if denominator == 0:
        return 0.0, False
    p_value = math.erfc(numerator / denominator)
    return p_value, p_value >= 0.01


# ---------------------------------------------------------------------------
# 4. Автокорреляционный тест
# ---------------------------------------------------------------------------

def autocorrelation_test(bits: List[int], lag: int = 1) -> Tuple[float, bool]:
    """
    Тест автокорреляции с заданным сдвигом (lag)

    Считает число несовпадений между bits[i] и bits[i+lag],
    нормирует и вычисляет p_value через erfc
    """
    n = len(bits)
    if lag >= n:
        raise ValueError("lag должен быть меньше длины последовательности")
    m = n - lag
    a = sum(bits[i] ^ bits[i + lag] for i in range(m))
    # Стандартизованная статистика
    s = (a - m / 2.0) / math.sqrt(m / 4.0)
    p_value = math.erfc(abs(s) / math.sqrt(2))
    return p_value, p_value >= 0.01


# ---------------------------------------------------------------------------
# 5. Универсальный тест Маурера
# ---------------------------------------------------------------------------

def maurer_universal_test(bits: List[int], L: int = 7, Q: int = 1280) -> Tuple[float, bool]:
    """
    Универсальный статистический тест Маурера

    L  — длина блока (рекомендовано 6–16)
    Q  — число инициализирующих блоков (рекомендовано >= 10*2^L)

    Если последовательность слишком короткая, возвращает (0.0, False)
    """
    n = len(bits)
    num_blocks = n // L
    if num_blocks < Q + 2:
        return 0.0, False

    K = num_blocks - Q  # число тестовых блоков

    # Таблица ожидаемых значений и дисперсий (по NIST SP 800-22)
    # для L = 6..16
    expected_value = {
        6: 5.2177052, 7: 6.1962507, 8: 7.1836656,
        9: 8.1764248, 10: 9.1723243, 11: 10.170032,
        12: 11.168765, 13: 12.168070, 14: 13.167693,
        15: 14.167488, 16: 15.167379,
    }
    variance = {
        6: 2.954, 7: 3.125, 8: 3.238,
        9: 3.311, 10: 3.356, 11: 3.384,
        12: 3.401, 13: 3.410, 14: 3.416,
        15: 3.419, 16: 3.421,
    }

    if L not in expected_value:
        return 0.0, False

    # Инициализация таблицы последнего вхождения
    table = {}
    for i in range(Q):
        block = _bits_to_int(bits, i * L, L)
        table[block] = i + 1  # 1-indexed

    # Накопление суммы log2(расстояний)
    total = 0.0
    for i in range(Q, Q + K):
        block = _bits_to_int(bits, i * L, L)
        dist = (i + 1) - table.get(block, 0)
        table[block] = i + 1
        if dist > 0:
            total += math.log2(dist)

    fn = total / K
    c = 0.7 - 0.8 / L + (4 + 32 / L) * (K ** (-3 / L)) / 15
    sigma = c * math.sqrt(variance[L] / K)

    if sigma == 0:
        return 0.0, False

    p_value = math.erfc(abs(fn - expected_value[L]) / (math.sqrt(2) * sigma))
    return p_value, p_value >= 0.01


# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------

def _bits_to_int(bits: List[int], start: int, length: int) -> int:
    val = 0
    for i in range(length):
        val = (val << 1) | bits[start + i]
    return val


def _chi2_sf(x: float, df: int) -> float:
    """Приближённая функция выживания X^2 распределения через regularized gamma"""
    return _regularized_upper_gamma(df / 2.0, x / 2.0)


def _regularized_upper_gamma(a: float, x: float, iterations: int = 200) -> float:
    """Регуляризованная неполная гамма-функция Γ(a, x) / Γ(a) (верхняя)"""
    if x < 0:
        return 1.0
    if x == 0:
        return 1.0
    # Используем разложение в ряд для нижней неполной гамма-функции
    # P(a, x) = lower / Γ(a), Q = 1 - P
    if x < a + 1:
        # ряд
        term = math.exp(-x + a * math.log(x) - _log_gamma(a))
        result = term
        running = term
        for n in range(1, iterations):
            running *= x / (a + n)
            result += running
            if abs(running) < 1e-12 * abs(result):
                break
        lower = result / a
        return max(0.0, 1.0 - lower)
    else:
        # непрерывная дробь (метод Ленца)
        fpmin = 1e-300
        b = x + 1.0 - a
        c = 1.0 / fpmin
        d = 1.0 / b
        h = d
        for i in range(1, iterations):
            an = -i * (i - a)
            b += 2.0
            d = an * d + b
            if abs(d) < fpmin:
                d = fpmin
            c = b + an / c
            if abs(c) < fpmin:
                c = fpmin
            d = 1.0 / d
            delta = d * c
            h *= delta
            if abs(delta - 1.0) < 1e-12:
                break
        return math.exp(-x + a * math.log(x) - _log_gamma(a)) * h


def _log_gamma(x: float) -> float:
    """Логарифм гамма-функции (аппроксимация Ланцоша)"""
    g = 7
    c = [
        0.99999999999980993,
        676.5203681218851,
        -1259.1392167224028,
        771.32342877765313,
        -176.61502916214059,
        12.507343278686905,
        -0.13857109526572012,
        9.9843695780195716e-6,
        1.5056327351493116e-7,
    ]
    if x < 0.5:
        return math.log(math.pi / math.sin(math.pi * x)) - _log_gamma(1 - x)
    x -= 1
    a = c[0]
    t = x + g + 0.5
    for i in range(1, g + 2):
        a += c[i] / (x + i)
    return math.log(math.sqrt(2 * math.pi)) + math.log(a) - t + math.log(t) * (x + 0.5)


# ---------------------------------------------------------------------------
# Запуск всех тестов
# ---------------------------------------------------------------------------

def run_all_tests(bits: List[int], verbose: bool = True) -> dict:
    """Запускает все 5 тестов и возвращает результаты"""
    results = {}

    tests = [
        ("1. Частотный тест (Monobit)", lambda: frequency_test(bits)),
        ("2. Последовательный тест (Serial)", lambda: serial_test(bits)),
        ("3. Тест серий (Runs)", lambda: runs_test(bits)),
        ("4. Автокорреляционный тест (lag=1)", lambda: autocorrelation_test(bits, lag=1)),
        ("5. Универсальный тест Маурера", lambda: maurer_universal_test(bits)),
    ]

    if verbose:
        print(f"\n{'=' * 60}")
        print(f"  Статистические тесты (n={len(bits)} бит)")
        print(f"{'=' * 60}")

    for name, fn in tests:
        try:
            p_value, passed = fn()
        except Exception as e:
            p_value, passed = 0.0, False
            if verbose:
                print(f"  {name}: ОШИБКА — {e}")
            results[name] = {"p_value": p_value, "passed": passed}
            continue

        results[name] = {"p_value": p_value, "passed": passed}
        if verbose:
            status = "ПРОЙДЕН " if passed else "ПРОВАЛЕН"
            print(f"  {name}")
            print(f"    p-value = {p_value:.6f}  ->  {status}")

    if verbose:
        passed_count = sum(1 for v in results.values() if v["passed"])
        print(f"{'=' * 60}")
        print(f"  Итог: {passed_count}/{len(results)} тестов пройдено")
        print(f"{'=' * 60}\n")

    return results
