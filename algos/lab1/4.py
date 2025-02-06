MOD = 987654323

# (a**b) mod m = ((a mod m)**b) mod m

def mod_exp(a, b, m):
    result = 1
    a = a % m
    while b > 0:
        if b % 2 == 1:
            result = (result * a) % m
        a = (a * a) % m
        b //= 2
    return result

a, b = map(int, input().split())

print(mod_exp(a, b, MOD))
