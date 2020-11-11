import math
import random
import sympy

def prim_roots(modulo):
    coprime_set = {num for num in range(1, modulo) if math.gcd(num, modulo) == 1}
    return [g for g in range(1, modulo) if coprime_set == {pow(g, powers, modulo)
            for powers in range(1, modulo)}]

def generate_public_g(public_p):
  primitive_primes = prim_roots(public_p)
  index = random.randint(0, len(primitive_primes) - 1)
  return primitive_primes[index]

def generate_public_keys(min_val, max_val):
  public_p = sympy.randprime(min_val, max_val)
  public_g = generate_public_g(public_p)
  return public_p, public_g

def generate_private(min_val, max_val):
  return random.randint(min_val, max_val)

def calculate_key(public_g, public_p, private):
  return public_g ** private % public_p
