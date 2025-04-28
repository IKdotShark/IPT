import os
from typing import List


class TapeEmulator:
    """Эмулятор ленты (файла) для внешней сортировки"""

    def __init__(self, filename: str):
        self.filename = filename
        if not os.path.exists(self.filename):
            open(self.filename, 'w').close()
        self.length = 0

    def write(self, data: List[int]):
        with open(self.filename, 'w') as f:
            f.write(','.join(map(str, data)))
        self.length = len(data)

    def read(self) -> List[int]:
        try:
            with open(self.filename, 'r') as f:
                content = f.read().strip()
                return list(map(int, content.split(','))) if content else []
        except FileNotFoundError:
            return []

    def clean(self):
        open(self.filename, 'w').close()
        self.length = 0


def external_radix_sort(input_data: List[int], num_tapes: int = 4) -> List[int]:
    if not input_data:
        return []

    max_key = max(input_data)
    num_bits = max(max_key.bit_length(), 1)
    passes = (num_bits + 1) // 2  # Обрабатываем по 2 бита за проход

    tapes = [TapeEmulator(f'tape_{i}.txt') for i in range(num_tapes)]
    tapes[0].write(input_data)

    for pass_num in range(passes):
        # Очищаем вспомогательные ленты
        for tape in tapes[1:]:
            tape.clean()

        current_data = tapes[0].read()
        tapes[0].clean()

        # Распределение данных по лентам
        for num in current_data:
            # Извлекаем 2 бита, начиная с младших
            bits = (num >> (2 * pass_num)) & 0b11
            tape_num = bits  # Используем ленты 0-3
            tapes[tape_num].write(tapes[tape_num].read() + [num])

        # Сборка данных на первую ленту в порядке возрастания битов
        merged = []
        for tape in tapes:
            merged.extend(tape.read())
        tapes[0].write(merged)

    sorted_data = tapes[0].read()

    # Очистка временных файлов
    for tape in tapes:
        tape.clean()

    return sorted_data


# Пример использования
if __name__ == "__main__":
    # Тест 1: базовый пример
    data = [7, 6, 5, 4, 3, 2, 1, 0]
    print("Исходные данные:", data)
    print("Отсортированные данные:", external_radix_sort(data))

    # Тест 2: случайные данные
    import random

    data = [random.randint(0, 99) for _ in range(20)]
    print("\nСлучайные данные:", data)
    print("Отсортировано:", external_radix_sort(data))