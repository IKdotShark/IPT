import math


def continued_fraction_sqrt(D, u=0, v=1):
    sqrt_D_floor = math.isqrt(D)

    if sqrt_D_floor ** 2 == D:
        yield sqrt_D_floor, sqrt_D_floor, 0  # Для полных квадратов
        return

    # Хр. в виде переменных от многократного пересчета
    sqrt_D = math.sqrt(D)
    A_0 = math.floor((sqrt_D - u) / v)
    u_curr = u + A_0 * v
    v_curr = v

    yield A_0, u_curr, v_curr

    while True:
        v_next = (D - u_curr ** 2) // v_curr
        if v_next == 0:
            break

        if v_next > 0:
            A = (sqrt_D_floor + u_curr) // v_next
        else:
            A = (sqrt_D_floor + 1 + u_curr) // v_next

        u_next = A * v_next - u_curr
        yield A, u_next, v_next
        u_curr, v_curr = u_next, v_next


def find_period(D, u=0, v=1):
    sqrt_D_floor = math.isqrt(D)
    if sqrt_D_floor ** 2 == D:
        return [sqrt_D_floor], []  # Полный квадрат: предпериод [k], период []

    seen = {}
    cf = continued_fraction_sqrt(D, u, v)
    elements = []

    for i, (a, u_n, v_n) in enumerate(cf):
        key = (u_n, v_n, a)
        if key in seen:
            idx = seen[key]
            return elements[:idx], elements[idx:]
        seen[key] = i
        elements.append(a)


print(find_period(16))  # ([4], [])
print(find_period(23))  # ([4], [1, 3, 1, 8])
print(find_period(25))  # ([5], [])
