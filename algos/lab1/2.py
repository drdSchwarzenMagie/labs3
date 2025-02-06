n = int(input())  # Количество чисел в массиве
arr = list(map(int, input().split()))  # Массив чисел
q = int(input())  # Количество запросов

# Создаем массив префиксных сумм
prefix_sum = [0] * (n + 1)
for i in range(1, n + 1):
    prefix_sum[i] = prefix_sum[i - 1] + arr[i - 1]

# Обработка запросов
for _ in range(q):
    l, r = map(int, input().split())
    # Ответ на запрос — разница префиксных сумм
    print(prefix_sum[r] - prefix_sum[l - 1])
