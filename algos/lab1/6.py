n, k = map(int, input().split())
a = [int(input()) for _ in range(n)]
lo = 0
hi = 10000001
while hi > lo + 1:
    mid = (lo + hi) // 2
    if sum(x // mid for x in a) < k:
        hi = mid
    else:
        lo = mid
print(lo)