def lzfg_compress(source, W, M):
    n = len(source)
    N = 0
    codeword = ""

    while N < n:
        # Находим максимальную длину l
        l_max = 0
        d = 0
        for l in range(3, 18):
            if N + l > n:
                break
            substring = source[N:N + l]
            window_start = max(0, N - W)
            window = source[window_start:N]

            pos = window.rfind(substring)
            if pos != -1:
                l_max = l
                d = N - (window_start + pos)

        if l_max >= 2:
            # Кодирование найденной подстроки
            codeword += "0000"  # Префикс для повторяющейся подстроки
            codeword += format(l_max - 3, '04b')  # Длина подстроки в 4 битах
            codeword += format(d, f'0{(M-1).bit_length()}b')  # Расстояние до начала повторения
            N += l_max
        else:
            # Кодирование одиночного символа
            codeword += "1"  # Префикс для одиночного символа
            codeword += format(ord(source[N]), '08b')  # Символ в 8 битах (ASCII код)
            N += 1

    return codeword

# Пример использования
source = "early_to_bed_and_early_to_rise_makes_a_man_wise"
W = 16  # Длина окна
M = 256  # Размер алфавита (для ASCII символов)

compressed = lzfg_compress(source, W, M)
print("Закодированное слово:", compressed)
