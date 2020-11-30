from numpy.random import randint
from sympy import randprime
from sympy.abc import a, b, c
from sympy.parsing.sympy_parser import parse_expr
import math

def prim_roots(modulo):
    coprime_set = {num for num in range(1, modulo) if math.gcd(num, modulo) == 1}
    return [g for g in range(1, modulo) if coprime_set == {pow(g, powers, modulo)
            for powers in range(1, modulo)}]

def generate_public_g(public_p):
  primitive_primes = prim_roots(public_p)
  index = randint(0, high=len(primitive_primes) - 1)
  return primitive_primes[index]

def generate_public_keys(min_val, max_val):
  public_p = randprime(min_val, max_val)
  public_g = generate_public_g(public_p)
  return public_p, public_g

def generate_private(min_val, max_val):
  return randint(min_val, high=max_val)

def calculate_key(public_g, public_p, private):
  sympy_exp = parse_expr('(a ** b) % c')
  return int(sympy_exp.evalf(subs={a:public_g, b:private, c:public_p}))
