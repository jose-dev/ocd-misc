from random import choice, random
import string



def random_alphabetic_str(length):
    return ''.join(choice(string.ascii_letters) for x in range(length))

def random_lower_alphabetic_str(length):
    return random_alphabetic_str(length).lower()
