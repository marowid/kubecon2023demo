import string

import pandas as pd


class Tokenizer:
    def __init__(self, key):
        self.key = key.lower()
        self.substitution_table = self._generate_substitution_table(self.key)

    def _generate_substitution_table(self, key):
        available_chars = list(string.ascii_lowercase)
        used_chars = set()
        substitution_table = {}

        for k in key:
            if not available_chars:
                break
            if k not in used_chars:
                substitution_table[available_chars.pop(0)] = k
                used_chars.add(k)
                if k in available_chars:
                    available_chars.remove(k)

        for c in available_chars:
            substitution_table[c] = c

        return substitution_table

    def mask_value(self, value):
        return "".join(
            [
                self.substitution_table[c] if c in self.substitution_table else c
                for c in value.lower()
            ]
        )

    def mask_series(self, series: pd.Series) -> pd.Series:
        return series.apply(lambda val: self.mask_value(val))
