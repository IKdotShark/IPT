def merge(left, right):
    """Алгоритм M: двухпутевое слияние двух отсортированных массивов."""
    merged = []
    i = j = 0  # Индексы для left и right

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Добавляем оставшиеся элементы (шаги M4 и M6)
    merged += left[i:]
    merged += right[j:]

    return merged

def merge_sort(arr):
    """Сортировка слиянием с использованием алгоритма двухпутевого слияния."""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

# Пример использования
arr = [503, 87, 512, 61, 908, 170, 897, 275, 653, 426, 154, 509, 612, 677, 765, 703]
sorted_arr = merge_sort(arr)
print("Отсортированный массив:", sorted_arr)