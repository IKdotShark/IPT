import random

def is_prime(n, k=5):
    """Тест Миллера-Рабина на простоту"""
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0:
        return False

    # Записываем n-1 в виде (2^s)*d
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # Проводим k тестов
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_large_prime(bits):
    """Генерация большого простого числа заданной битности"""
    while True:
        # Генерируем нечетное число нужного размера
        num = random.getrandbits(bits)
        num |= (1 << bits - 1) | 1  # Устанавливаем старший и младший биты

        if is_prime(num):
            return num


def gcd(a, b):
    """Алгоритм Евклида для НОД"""
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    """Расширенный алгоритм Евклида"""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def modinv(a, m):
    """Модульная инверсия с использованием расширенного алгоритма Евклида"""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        return None  # Обратного элемента не существует
    else:
        return x % m


def generate_keys(bits=2048):
    """Генерация ключей RSA заданной битности"""
    # Генерируем два больших простых числа
    p = generate_large_prime(bits // 2)
    q = generate_large_prime(bits // 2)
    while q == p:
        q = generate_large_prime(bits // 2)

    n = p * q
    phi = (p - 1) * (q - 1)

    # Выбираем открытую экспоненту (обычно 65537)
    e = 65537
    while gcd(e, phi) != 1:
        e = generate_large_prime(16)  # Если 65537 не подошла, берем другое простое

    # Находим секретную экспоненту d
    d = modinv(e, phi)

    return ((e, n), (d, n))


def bytes_to_int(bytes_data):
    """Преобразование байтов в большое целое число"""
    return int.from_bytes(bytes_data, byteorder='big', signed=False)


def int_to_bytes(number, fill_size=None):
    """Преобразование большого целого числа в байты"""
    bytes_data = number.to_bytes((number.bit_length() + 7) // 8, byteorder='big')

    if fill_size:
        if len(bytes_data) < fill_size:
            bytes_data = b'\x00' * (fill_size - len(bytes_data)) + bytes_data

    return bytes_data


def encrypt(public_key, plaintext):
    """Шифрование сообщения"""
    e, n = public_key
    # Преобразуем текст в байты
    plain_bytes = plaintext.encode('utf-8')

    # Определяем размер блока (меньше, чем битность n)
    block_size = (n.bit_length() - 1) // 8
    blocks = [plain_bytes[i:i + block_size] for i in range(0, len(plain_bytes), block_size)]

    # Шифруем каждый блок
    cipher_blocks = []
    for block in blocks:
        m = bytes_to_int(block)
        if m >= n:
            raise ValueError("Слишком большой блок для шифрования")
        c = pow(m, e, n)
        cipher_blocks.append(int_to_bytes(c, (n.bit_length() + 7) // 8))

    # Объединяем все блоки
    return b''.join(cipher_blocks)


def decrypt(private_key, ciphertext):
    """Дешифрование сообщения"""
    d, n = private_key
    # Определяем размер блока
    block_size = (n.bit_length() + 7) // 8
    blocks = [ciphertext[i:i + block_size] for i in range(0, len(ciphertext), block_size)]

    # Дешифруем каждый блок
    plain_blocks = []
    for block in blocks:
        c = bytes_to_int(block)
        m = pow(c, d, n)
        plain_blocks.append(int_to_bytes(m))

    # Объединяем все блоки и декодируем
    plain_bytes = b''.join(plain_blocks)
    return plain_bytes.decode('utf-8', errors='replace')


if __name__ == "__main__":
    print("Генерация 2048-битных ключей RSA...")
    public_key, private_key = generate_keys(2048)
    print(f"Публичный ключ (e, n): e={public_key[0]}\nn={public_key[1]}")
    print(f"Приватный ключ (d, n): d={private_key[0]}\nn={private_key[1]}")

    message = input("Введите сообщение для шифрования: ")

    try:
        # Шифрование
        encrypted_msg = encrypt(public_key, message)
        print(f"Зашифрованное сообщение (hex): {encrypted_msg.hex()}")

        # Дешифрование
        decrypted_msg = decrypt(private_key, encrypted_msg)
        print(f"Расшифрованное сообщение: {decrypted_msg}")
    except ValueError as e:
        print(f"Ошибка: {e}")