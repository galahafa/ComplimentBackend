import random
import string

from apps.common_utils.constant import RARITY_CHANCE


def get_rarity():
    chance = random.random()
    compare_value = 0
    now_rarity = 1
    for key, value in RARITY_CHANCE.items():
        compare_value += value
        if chance <= compare_value:
            now_rarity = key
            break
        else:
            pass
    return now_rarity


def get_random_integer(number):
    return ''.join(random.choices(string.digits, k=number))
