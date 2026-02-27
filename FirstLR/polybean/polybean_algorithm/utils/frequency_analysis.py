ENGLISH_FREQUENCY = {'a': 0.0817,
                     'b': 0.0149,
                     'c': 0.0278,
                     'd': 0.0425,
                     'e': 0.1270,
                     'f': 0.0223,
                     'g': 0.0202,
                     'h': 0.0609,
                     'i': 0.0697,
                     'j': 0.0015,
                     'k': 0.0077,
                     'l': 0.0403,
                     'm': 0.0241,
                     'n': 0.0675,
                     'o': 0.0751,
                     'p': 0.0193,
                     'q': 0.0010,
                     'r': 0.0599,
                     's': 0.0633,
                     't': 0.0906,
                     'u': 0.0276,
                     'v': 0.0098,
                     'w': 0.0236,
                     'x': 0.0015,
                     'y': 0.0197,
                     'z': 0.0007, }


class FrequencyAnalysis:
    def __init__(self, text: str):
        self._symbols = [first_letter + second_letter
                         for first_letter, second_letter in zip(text[::2], text[1::2])]
        counts_symbol = {}

        first_letters = text[::2]
        second_letters = text[1::2]

        self.first_freq = self._count(first_letters)
        self.second_freq = self._count(second_letters)
        self.full_freq = self._count(text)

        self.sorted_columns = sorted(self.first_freq, key=self.first_freq.get, reverse=True)
        self.sorted_rows = sorted(self.second_freq, key=self.second_freq.get, reverse=True)

        for symbol in self._symbols:
            counts_symbol.setdefault(symbol, 0)
            counts_symbol[symbol] += 1

        count_simbols = len(self._symbols)
        self._frequencies = {symbol: count / count_simbols for symbol, count in counts_symbol.items()}

        self._frequencies_table = '\n'.join(
            [f'   {symbol}   | {rate:4f} | {self.find_nearest_letter(rate)}' for symbol, rate in
             self._frequencies.items()])

        self._possible_key = {symbol: self.find_nearest_letter(rate) for symbol, rate in self._frequencies.items()}

    def print_table(self):
        print('Symbol  |   Rate   | Possible letter')
        print(self._frequencies_table)

    def print_possible_text(self):
        print('Possible text:')
        text = ''.join(self._possible_key[symbol] for symbol in self._symbols)
        print(text)

    def get_restored_key(self):
        print("\nRestored key (by frequency):\n")
        col_count = len(self.sorted_columns)
        row_count = len(self.sorted_rows)
        alphabet_iter = iter(ENGLISH_FREQUENCY)
        key_matrix = []
        key_matrix.append(["*"] + self.sorted_columns)
        for row_symbol in self.sorted_rows:
            row = [row_symbol]
            for _ in range(col_count):
                try:
                    row.append(next(alphabet_iter))
                except StopIteration:
                    row.append("*")
            key_matrix.append(row)
        return key_matrix

    @staticmethod
    def find_nearest_letter(frequency: float) -> str:
        letter = \
        min({letter: abs(frequency - rate) for letter, rate in ENGLISH_FREQUENCY.items()}.items(), key=lambda x: x[1])[
            0]
        return letter

    @staticmethod
    def _count(sequence):
        counts = {}
        for s in sequence:
            counts[s] = counts.get(s, 0) + 1
        total = len(sequence)
        return {k: v / total for k, v in counts.items()}
