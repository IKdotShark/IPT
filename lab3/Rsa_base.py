import random

def is_prime(n):
    """Проверка числа на простоту"""
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    w = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += w
        w = 6 - w
    return True


def generate_prime(min_val, max_val):
    """Генерация простого числа в заданном диапазоне"""
    while True:
        p = random.randint(min_val, max_val)
        if is_prime(p):
            return p


def gcd(a, b):
    """Нахождение наибольшего общего делителя (НОД)"""
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    """Расширенный алгоритм Евклида"""
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    """Нахождение модульного обратного числа"""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        return None  # Обратного элемента не существует
    else:
        return x % m


def generate_keys():
    """Генерация ключей для RSA"""
    # Выбираем два различных простых числа
    p = generate_prime(100, 1000)
    q = generate_prime(100, 1000)
    while q == p:
        q = generate_prime(100, 1000)

    n = p * q
    phi = (p - 1) * (q - 1)

    # Выбираем открытую экспоненту e
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    # Находим секретную экспоненту d
    d = modinv(e, phi)

    return ((e, n), (d, n))


def encrypt(public_key, plaintext):
    """Шифрование сообщения"""
    e, n = public_key
    # Преобразуем каждый символ в его ASCII код и шифруем
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher


def decrypt(private_key, ciphertext):
    """Дешифрование сообщения"""
    d, n = private_key
    # Дешифруем каждый блок и преобразуем обратно в символ
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)


# Пример использования
if __name__ == "__main__":
    print("Генерация ключей RSA...")
    public_key, private_key = generate_keys()
    print(f"Публичный ключ (e, n): {public_key}")
    print(f"Приватный ключ (d, n): {private_key}")

    message = input("Введите сообщение для шифрования: ")

    # Шифрование
    encrypted_msg = encrypt(public_key, message)
    print(f"Зашифрованное сообщение: {encrypted_msg}")

    # Дешифрование
    decrypted_msg = decrypt(private_key, encrypted_msg)
    print(f"Расшифрованное сообщение: {decrypted_msg}")