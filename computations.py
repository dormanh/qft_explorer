import numpy as np
import math


def exp2int(n: int) -> int:
    """Returns 2^n as an integer."""
    return int(np.exp2(n))


def compute_factors(n: int) -> list[int]:
    """Computes all factors of the given integer."""
    return [k for k in range(2, n) if n % k == 0]


def is_semiprime(n: int) -> bool:
    """Decides, whether the given integer is a semiprime,
    meaning it can be expressed as the product of two prime numbers."""
    factors = compute_factors(n)
    return (len(factors) == 2) & (not any((len(compute_factors(f)) for f in factors)))


def compute_valid_Ns(n_states: int) -> list[int]:
    """Given the number of qubits, returns all semiprimes that can be represented by them."""
    return [k for k in range(3, n_states) if is_semiprime(k)]


def compute_valid_as(N: int) -> list[int]:
    """Given N, computes the valid `a` parameters for the period-finding problem."""
    return [k for k in range(2, N) if math.gcd(k, N) == 1]


def modulo_func(N: int, a: int, n: int) -> int:
    """Computes the module function value for the given parameters."""
    return (a**n) % N


def compute_remainders(N: int, a: int) -> list[int]:
    """Computes the array a^n mod N, where n = 1, ..., N - 1."""
    return [modulo_func(N, a, n) for n in range(N)]


def compute_consistent_exponents(N: int, a: int, remainder: int) -> list[int]:
    """Given a remainder, returns all exponents consistent with it up to N."""
    return [n for n in range(1, N) if modulo_func(N, a, n) == remainder]
