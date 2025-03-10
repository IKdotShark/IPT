# LZFG

import math
# 17 нельзя нужно по правильному
# Костарев посмотреть
# Из учебника сравнить
uniq_sym = {}  # Словарь для хранения символов и их индексов
info = []  # Результирующая таблица
# message = "early_to_bed_and_early_to_rise_makes_a_man_wise"
message = "IF_WE_CANNOT_DO_AS_WE_WOULD_WE_SHOULD_DO_AS_WE_CAN"
in_proc = ""  # Накопленные необработанные символы
max_word = 16  # Максимальная длина слова


def dictionary_add(key, index):
    """Добавляет символ в словарь и возвращает True, если символ новый"""
    if key not in uniq_sym:
        uniq_sym[key] = []
        uniq_sym[key].append(index)
        return True
    else:
        uniq_sym[key].append(index)
        return False


def check_letter(symbol):
    """Проверяет, есть ли совпадение следующего символа в предыдущих вхождениях"""
    indexes = uniq_sym.get(symbol, [])
    if not indexes:
        return False
    if indexes[-1] == len(message) - 1:
        return False
    next_char = message[indexes[-1] + 1]
    for idx in indexes[:-1]:
        if idx + 1 < len(message) and message[idx + 1] == next_char:
            return True
    return False


def index_of_end(basic, substr):
    """Возвращает последний индекс вхождения подстроки"""
    pos = basic.rfind(substr)
    return pos if pos != -1 else -2


def find_word(now):
    """Ищет максимальное совпадение подстроки в предыдущих данных"""
    basic = message[:now]
    substr = message[now:now + 3]
    if len(substr) < 3:
        return (-1, 0)
    idx = index_of_end(basic, substr)
    if idx == -2:
        return (-1, 0)
    length = 3
    while True:
        if now + length >= len(message):
            break
        next_sub = substr + message[now + length]
        new_idx = index_of_end(basic, next_sub)
        if new_idx >= 0:
            idx = new_idx
            substr = next_sub
            dictionary_add(message[now + length], now + length)
            length += 1
        else:
            break
    return (idx, length)


def str_to_binary(input_str):
    """Преобразует строку в бинарное представление"""
    return ''.join([bin(ord(c))[2:].zfill(8) for c in input_str])


def fill_row_unique():
    """Формирует строку таблицы для уникальных символов"""
    global in_proc
    row = [""] * 8
    row[0] = str(len(info) + 1)
    row[1] = in_proc
    row[2] = "-"
    row[3] = "-"
    row[4] = str(len(in_proc))
    if not info:
        row[5] = row[4]
    else:
        row[5] = str(int(info[-1][5]) + int(row[4]))
    # Формируем кодовую строку
    prefix = '0000' + bin(len(in_proc) - 1)[2:].zfill(4)
    bin_str = prefix + str_to_binary(in_proc)
    row[6] = bin_str
    row[7] = str(len(bin_str))
    in_proc = ""
    return row


def main():
    global in_proc
    i = 0
    while i < len(message):
        if len(in_proc) == max_word:
            info.append(fill_row_unique())

        added = dictionary_add(message[i], i)
        if added:
            in_proc += message[i]
        else:
            if check_letter(message[i]):
                if i + 1 >= len(message):
                    in_proc += message[i]
                    continue
                dictionary_add(message[i + 1], i + 1)
                if check_letter(message[i + 1]):
                    if i + 2 >= len(message):
                        in_proc += message[i] + message[i + 1]
                        i += 1
                        continue
                    dictionary_add(message[i + 2], i + 2)
                    if in_proc:
                        info.append(fill_row_unique())
                    idx, length = find_word(i)
                    if idx == -1:
                        in_proc += message[i:i + 3]
                        i += 2
                        continue
                    row = [""] * 8
                    row[0] = str(len(info) + 1)
                    row[1] = message[idx:idx + length]
                    row[2] = str(i - idx - 1)
                    row[3] = str(length)
                    row[4] = "-"
                    if not info:
                        row[5] = str(length)
                    else:
                        row[5] = str(int(info[-1][5]) + length)
                    order = math.ceil(math.log2(int(info[-1][5]))) if info else 1
                    code_len = bin(length - 2)[2:].zfill(4)
                    code_dist = bin(i - idx - 1)[2:].zfill(order)
                    row[6] = code_len + code_dist
                    row[7] = str(len(row[6]))
                    info.append(row)
                    i += length - 1
                else:
                    in_proc += message[i] + message[i + 1]
                    i += 1
            else:
                in_proc += message[i]
        i += 1

    if in_proc:
        info.append(fill_row_unique())

    # Вывод таблицы
    print(
        "\nШаг  Пер. бук.          Расст. до обр.   Длин. совп.   Чис. нов. бук.   Сум. всех бук. до   Кодов. симв.                Затр. бит.")
    for row in info:
        step, letters, dist, match_len, new_letters, total, code, bits = row
        code_disp = code if len(code) < 25 else "отдельно"
        print(f"{step:<5}{letters:<19}{dist:<17}{match_len:<14}{new_letters:<17}{total:<20}{code_disp:<28}{bits:<7}")

    print("\n")
    result = {}
    for row in info:
        result[row[1]] = row[6]
        print(f"{row[1]:<16} - {row[6]}")

    print("\n")
    for char in uniq_sym:
        print(f"{char} - {uniq_sym[char]}")


if __name__ == "__main__":
    main()