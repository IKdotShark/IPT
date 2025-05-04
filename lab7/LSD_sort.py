import pygame
import sys
import random
from pygame.locals import *


class RadixSortVisualizer:
    def __init__(self, width=1200, height=700):
        self.width = width
        self.height = height
        self.bg_color = (30, 30, 30)
        self.colors = {
            'default': (100, 200, 255),
            'active': (255, 100, 100),
            'sorted': (100, 255, 100),
            'text': (255, 255, 200)
        }

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Radix Sort LSD - Corrected Implementation")
        self.font = pygame.font.Font(None, 20)
        self.value_font = pygame.font.Font(None, 14)

        # Генерация данных и инициализация
        self.arr = [random.randint(100, 9999) for _ in range(100)]  # 4-значные числа
        self.stats = {
            'accesses': 0,
            'comparisons': 0,
            'delay': 10,
            'max_value': max(self.arr)
        }
        self.bar_width = (self.width // len(self.arr)) - 1
        self.running = True

    def draw_bars(self, active_idx=None):
        self.screen.fill(self.bg_color)

        # Отрисовка столбцов
        max_bar_height = self.height - 150
        for i, num in enumerate(self.arr):
            color = self.colors['active'] if i == active_idx else self.colors['default']
            bar_height = int((num / self.stats['max_value']) * max_bar_height)
            x = i * (self.bar_width + 1)
            y = self.height - bar_height - 50

            pygame.draw.rect(self.screen, color, (x, y, self.bar_width, bar_height))

            # Подписи значений
            if self.bar_width > 20:
                text = self.value_font.render(str(num), True, self.colors['text'])
                text_rect = text.get_rect(center=(x + self.bar_width // 2, self.height - 30))
                self.screen.blit(text, text_rect)

        # Статистика
        stats = [
            f"Elements: {len(self.arr)}",
            f"Array Accesses: {self.stats['accesses']}",
            f"Delay: {self.stats['delay']} ms",
            f"Max Value: {self.stats['max_value']}"
        ]

        for i, text in enumerate(stats):
            surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(surface, (10, 10 + i * 25))

        pygame.display.flip()

    def lsd_sort(self):
        max_num = max(self.arr)
        exp = 1
        n = len(self.arr)

        while max_num // exp > 0:
            output = [0] * n
            count = [0] * 10

            # Фаза подсчёта (2N accesses)
            for num in self.arr:
                self.stats['accesses'] += 1
                digit = (num // exp) % 10
                count[digit] += 1
                self._update_display()

            # Накопительная сумма (10 accesses)
            for i in range(1, 10):
                count[i] += count[i - 1]
                self._update_display()

            # Распределение элементов (2N accesses)
            for i in reversed(range(n)):
                num = self.arr[i]
                self.stats['accesses'] += 1
                digit = (num // exp) % 10
                output[count[digit] - 1] = num
                count[digit] -= 1
                self._update_display(i)

            self.arr = output
            exp *= 10
            self._update_display()

        # Финальная проверка
        self._validate_sort()
        self._show_final_message()

    def _show_final_message(self):
        text = [
            "Сортировка завершена!",
            "Нажмите ESC для выхода",
            "",
            "Как работает Radix Sort LSD:",
            "1. Обработка чисел по разрядам, начиная с младшего",
            "2. Распределение элементов в 'корзины' по цифрам",
            "3. Повтор процесса для каждого разряда",
            "4. Сбор элементов после обработки всех разрядов"
        ]

        while True:
            self.screen.fill(self.bg_color)
            self.draw_bars()

            # Отрисовка пояснения
            y_pos = 50
            for line in text:
                surface = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(surface, (self.width // 2 - 200, y_pos))
                y_pos += 30

            pygame.display.flip()

            # Обработка событий
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def _update_display(self, active_idx=None):
        self.handle_events()
        self.draw_bars(active_idx)
        pygame.time.wait(self.stats['delay'])

    def _validate_sort(self):
        if self.arr == sorted(self.arr):
            print("✓ Сортировка выполнена корректно")
        else:
            print("⚠ Ошибка в сортировке!")
        self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    visualizer = RadixSortVisualizer()
    visualizer.lsd_sort()

    while visualizer.running:
        visualizer.handle_events()