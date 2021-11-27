from math import log
from functools import reduce
from typing import List, Dict, Union, Tuple


def evaluate_trigrams(words_list: List[str]):

    overall_words = len(words_list)

    trigrams, bigrams, bigrams_with_word_inside, words = init_counts(
        words_list)

    result = []
    for trigram in trigrams.keys():
        contingency_table_values = calc_contingency_table_values(
            trigrams, bigrams, bigrams_with_word_inside, words, overall_words,
            trigram)

        expected_values = calc_expected_values(contingency_table_values)

        adder = 0
        for n, m in zip(contingency_table_values, expected_values):
            under_log = n / m
            if under_log == 0:
                log_part = 0
            else:
                log_part = log(under_log)
            adder += n * log_part
            w1_count = words[trigram[0]]
            w2_count = words[trigram[1]]
            w3_count = words[trigram[2]]
            result.append((trigram, 2 * adder, (w1_count, w2_count, w3_count)))

    return sorted(result, key=lambda x: (x[1], x[0]), reverse=True)


def init_counts(
        words_list: List[str]) -> Tuple[Dict, Dict, Dict, Dict]:

    def add_new_one(target: Dict, key: Union[str, Tuple]) -> None:
        value = target.get(key)
        if value is None:
            target[key] = 1
        else:
            target[key] += 1

    trigrams = dict()
    bigrams = dict()
    words = dict()
    bigrams_with_word_inside = dict()

    for i in range(1, len(words_list) - 1):
        w1 = words_list[i - 1]
        w2 = words_list[i]
        w3 = words_list[i + 1]

        add_new_one(words, w1)
        add_new_one(bigrams, (w1, w2))
        add_new_one(bigrams_with_word_inside, (w1, w3))
        add_new_one(trigrams, (w1, w2, w3))

        if i == len(words_list) - 2:
            add_new_one(bigrams, (w2, w3))
            add_new_one(words, w2)
            add_new_one(words, w3)

    return trigrams, bigrams, bigrams_with_word_inside, words


def calc_contingency_table_values(
        trigrams: Dict,
        bigrams: Dict,
        bigrams_with_word_inside: Dict,
        words: Dict,
        overall_words: int,
        trigram: Tuple[str, str, str]
) -> Tuple[int, int, int, int, int, int, int, int]:
        w1, w2, w3 = trigram
        w1w2w3 = trigrams[(w1, w2, w3)]
        _w2w3 = bigrams[(w2, w3)] - w1w2w3
        w1_w3 = bigrams_with_word_inside[(w1, w3)] - w1w2w3
        w1w2_ = bigrams[(w1, w2)] - w1w2w3
        __w3 = words[w3] - w1w2w3 - w1_w3 - _w2w3
        w1__ = words[w1] - w1w2w3 - w1_w3 - w1w2_
        _w2_ = words[w2] - w1w2w3 - w1w2_ - _w2w3
        ___ = overall_words - w1w2w3 - w1w2_ - w1_w3 - w1__ - _w2w3 - _w2_ - __w3
        return w1w2w3, _w2w3, w1_w3, __w3, w1w2_, _w2_, w1__, ___


def calc_expected_values(
        cont_table_values: Tuple) -> List:
    result = []
    all_together = sum(cont_table_values)
    bit_masks = [1, 2, 4]
    for i in range(len(cont_table_values)):
        numerator = (sum(
            (
                cont_table_values[k]
                for k in range(len(cont_table_values))
                if (k & mask) == (i & mask)
             )
        )
            for mask in bit_masks)
        production = reduce(lambda x, y: x * y, numerator, 1)
        result.append(production / all_together ** 2)
    return result

