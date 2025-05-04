import math

def is_prime(n):
    """Проверка числа на простоту с использованием теста Миллера-Рабина"""
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in [2, 325, 9375, 28178, 450775, 9780504, 1795265022]:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def can_be_represented(d, k):
    """Проверяет, можно ли представить число d в виде u² + kv²"""
    if d == 1:
        return True  # 1 = 1² + k×0²

    if k == 3 and d == 2:
        return False  # Специальный исключенный случай

    max_u = int(math.isqrt(d)) + 1
    for u in range(max_u):
        remaining = d - u * u
        if remaining < 0:
            continue
        if remaining % k != 0:
            continue
        v_squared = remaining // k
        v = math.isqrt(v_squared)
        if v * v == v_squared:
            return True
    return False


def factorize(n):
    """Факторизация числа"""
    factors = {}
    if n == 1:
        return factors
    # Проверяем делимость на 2
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n = n // 2
    # Проверяем нечетные делители
    i = 3
    max_factor = math.isqrt(n) + 1
    while i <= max_factor:
        while n % i == 0:
            factors[i] = factors.get(i, 0) + 1
            n = n // i
            max_factor = math.isqrt(n) + 1
        i += 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def verify_theorem_4_21(N, x, y, k):
    """Проверка теоремы 4.21 для заданных N, x, y, k"""
    print(f"\nПример: N = {N} = {x}² + {k}×{y}²")

    # Проверка корректности входных данных
    if k not in {1, 2, 3}:
        print(f"Ошибка: k={k} должно быть 1, 2 или 3")
        return False

    if math.gcd(x, y) != 1:
        print(f"Ошибка: x={x} и y={y} не взаимно просты")
        return False

    if x * x + k * y * y != N:
        print(f"Ошибка: {x}² + {k}×{y}² = {x * x + k * y * y} ≠ {N}")
        return False

    # Получаем все делители N
    factors = factorize(N)
    divisors = [1]
    for p, exp in factors.items():
        temp = []
        for d in divisors:
            for e in range(exp + 1):
                temp.append(d * (p ** e))
        divisors = list(set(temp))
    divisors = sorted(divisors)

    theorem_holds = True
    for d in divisors:
        if d == 1:
            continue  # Тривиальный случай

        if not can_be_represented(d, k):
            print(f"Нарушение теоремы: делитель {d} нельзя представить в виде u² + {k}v²")
            theorem_holds = False

    if theorem_holds:
        print("Теорема выполняется для всех проверенных делителей")
    return theorem_holds


# Примеры использования
if __name__ == "__main__":
    print("Тестирование теоремы 4.21")
    print("=" * 40)

    # Пример 1: Некорректное k
    verify_theorem_4_21(13, 3, 1, 4)

    # Пример 2: Корректный случай
    verify_theorem_4_21(13, 3, 2, 1)

    # Пример 3
    verify_theorem_4_21(29, 5, 2, 1)

    # Пример 4
    verify_theorem_4_21(17, 4, 1, 1)

    # Пример 5
    verify_theorem_4_21(11, 3, 1, 2)

    # Пример 6: Специальный случай с k=3
    verify_theorem_4_21(7, 2, 1, 3)

    # Дополнительный тест с нарушением теоремы
    print("\nДополнительный тест с нарушением теоремы:")
    verify_theorem_4_21(91, 9, 1, 10)  # Намеренно неправильное k
