from random import randint
import math
from numba import jit

def generate_random_number(number_length: int = 9):
    result: list = []
    for _ in range(0, number_length):
        result.append(f"{randint(0, 9)}")
        if result[0] == '0':
            result[0] = f"{randint(0, 9)}"
    return int(''.join(result))

@jit
def check_trial_divisions(number):
    prime = True
    i = 2
    while i <= math.sqrt(number):
        if number % i == 0:
            prime = False
            break
        i += 1
    return prime

def check_ferma(number, n):
    if number ** (n - 1) % n == 1:
        return True
    else:
        return False

def generate_prime(length):
    while True:
        random_number = generate_random_number(length)
        if check_trial_divisions(random_number) and check_ferma(random_number, 11):
            print(random_number, '- prime number')
            break

generate_prime(10)
