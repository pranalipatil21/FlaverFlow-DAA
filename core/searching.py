import time

def linear_search(menu, target):
    steps = 0
    for item in menu:
        steps += 1
        if item['name'].lower() == target.lower(): return item, steps
    return None, steps

def binary_search(menu, target):
    sorted_menu = sorted(menu, key=lambda x: x['name'].lower())
    low, high, steps = 0, len(sorted_menu) - 1, 0
    while low <= high:
        steps += 1
        mid = (low + high) // 2
        if sorted_menu[mid]['name'].lower() == target.lower(): return sorted_menu[mid], steps
        elif sorted_menu[mid]['name'].lower() < target.lower(): low = mid + 1
        else: high = mid - 1
    return None, steps

# NEW: Karatsuba for Bulk Calculations
def karatsuba_multiplication(x, y):
    if x < 10 or y < 10: return x * y
    n = max(len(str(x)), len(str(y)))
    m = n // 2
    high1, low1 = divmod(x, 10**m)
    high2, low2 = divmod(y, 10**m)
    z0 = karatsuba_multiplication(low1, low2)
    z1 = karatsuba_multiplication((low1 + high1), (low2 + high2))
    z2 = karatsuba_multiplication(high1, high2)
    return (z2 * 10**(2*m)) + ((z1 - z2 - z0) * 10**m) + z0