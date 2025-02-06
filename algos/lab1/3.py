import bisect

N, K = map(int, input().split())
first_array = list(map(int, input().split()))
second_array = list(map(int, input().split()))

for num in second_array:
    idx = bisect.bisect_left(first_array, num)
    if idx < N and first_array[idx] == num:
        print("YES")
    else:
        print("NO")
