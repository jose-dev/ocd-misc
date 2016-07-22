import random_generators as rg


def random_string(length=8):
    return rg.random_lower_alphabetic_str(length)


def random_element(s):
    return rg.random_from_sequence(s)


def random_integer(n):
    return rg.random_integer_by_range(1, n+1)


def random_second(min=1, max=30):
    return rg.random_integer_by_range(min, max)

