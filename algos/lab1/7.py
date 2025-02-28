def max_rope_length(n, k, ropes):
    if n == 0:
        return 0

    left, right = 1, min(ropes)  # Верхняя граница — минимальная веревка
    result = 0

    while left <= right:
        mid = (left + right) // 2
        count = sum(rope // mid for rope in ropes)

        if count >= k:
            result = mid
            left = mid + 1  # Пробуем большее значение
        else:
            right = mid - 1  # Пробуем меньшее значение

    return result

# Чтение входных данных
n, k = map(int, input().split())
ropes = [int(input()) for _ in range(n)]

# Вывод результата
print(max_rope_length(n, k, ropes))
