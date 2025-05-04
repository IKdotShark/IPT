import math


def continued_fraction_sqrt(D, u, v):
    if math.isqrt(D) ** 2 == D: # Проверочка
        raise ValueError("D must not be a perfect square")

    # Хр. в виде переменных от многократного пересчета
    sqrt_D = math.sqrt(D)
    sqrt_D_floor = math.isqrt(D)

    # Отдельно обрабатываем A_0
    A_0 = math.floor((sqrt_D - u) / v)
    u_curr = u + A_0 * v
    v_curr = v

    yield A_0, u_curr, v_curr

    # Inf cycle
    while True:
        v_next = (D - u_curr ** 2) // v_curr
        if v_next == 0:
            break

        if v_next > 0: # Замечание из теоремы
            A = (sqrt_D_floor + u_curr) // v_next
        else:
            A = (sqrt_D_floor + 1 + u_curr) // v_next

        # Обночление переменных
        u_next = A * v_next - u_curr

        yield A, u_next, v_next

        u_curr, v_curr = u_next, v_next


def find_period(D, u=0, v=1):
    seen = {}
    cf = continued_fraction_sqrt(D, u, v)
    elements = []
    # Перебор элементов цепной дроби
    for i, (a, u_n, v_n) in enumerate(cf):
        key = (u_n, v_n, a)  # Добавляем a в ключ для надежности
        if key in seen:
            idx = seen[key]
            return elements[:idx], elements[idx:]
        seen[key] = i
        elements.append(a)


# Пример для √23
D = 25
pre, period = find_period(D)
print(f"Предпериод: {pre}")
print(f"Период: {period}")
print(f"Полное представление: {pre}({period})")
