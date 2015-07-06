from functools import reduce
import random
from string import ascii_letters, digits

def _d(n, k):
    return reduce(lambda x, y: x*y, range(n-k+1, n+1), 1)

def generateToken(list_of_tokens=None, lenght=7, alphabet=ascii_letters+digits):
    if not list_of_tokens:
        list_of_tokens = dict()

    #anti endless loop math ahead!
    if len(list_of_tokens) == _d(len(alphabet), lenght):
      raise ValueError("it's not possible to generate a new token!")

    is_ok, new_token = False, None
    while not is_ok :
        new_token = "".join(random.sample(alphabet, lenght))
        is_ok = new_token not in list_of_tokens

    return new_token
