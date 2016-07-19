from random import choice, random, randrange
import string



def random_alphabetic_str(length):
    return ''.join(choice(string.ascii_letters) for x in range(length))

def random_lower_alphabetic_str(length):
    return random_alphabetic_str(length).lower()

def random_integer_by_range(a, b):
    return randrange(a, b)


def random_from_sequence(s):
    return choice(s)

