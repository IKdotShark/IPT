import math

def jacobi_symbol(a, n):
    """Вычисление символа Якоби (a/n)"""
    if n <= 0 or n % 2 == 0:
        return 0
    a = a % n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a = a // 2
            mod = n % 8
            if mod == 3 or mod == 5:
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a = a % n
    if n == 1:
        return result
    else:
        return 0


def solovay_strassen_deterministic(N):
    """Детерминированный тест Соловея-Штрассена на простоту"""
    if N < 2:
        return False
    if N == 2:
        return True
    if N % 2 == 0:
        return False

    # Проверяем все числа от 1 до N-1
    for a in range(1, N):
        # Шаг 1: Проверяем НОД(a, N)
        d = math.gcd(a, N)
        if d > 1 and d < N:
            return False

        # Шаг 2: Проверяем условие теста
        if d == 1:
            # Вычисляем a^((N-1)/2) mod N
            exponent = (N - 1) // 2
            mod_exp = pow(a, exponent, N)

            # Вычисляем символ Якоби (a/N)
            jacobi = jacobi_symbol(a, N)
            if jacobi == -1:
                jacobi_mod = N - 1  # так как -1 mod N = N-1
            else:
                jacobi_mod = jacobi

            # Проверяем сравнение
            if mod_exp != jacobi_mod % N:
                return False

    # Если все проверки пройдены
    return True


# Тестирование функции
test_numbers = [2, 3, 5, 7, 11, 13, 15, 17, 19, 21, 23, 29, 31, 33, 37, 41, 43, 47, 51, 53]
for num in test_numbers:
    print(f"{num}: {'Простое' if solovay_strassen_deterministic(num) else 'Составное'}")
