def solve():
    n = int(input())
    A = list(map(int, input().split())) 

    total_sum = 0
    for i in range(n):
        # Количество отрезков, в которых участвует элемент A[i]
        count = (i + 1) * (n - i)
        total_sum += A[i] * count

    print(total_sum)

solve()
