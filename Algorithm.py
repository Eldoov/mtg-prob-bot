import math


def getCombos(n, nums):
    total = sum(nums)  # total numbers of desired cards
    leftover = n - total  # total cards - desired cards

    if leftover < 0:
        # error
        return []
    elif leftover == 0:
        # return self
        return [nums]

    res = []
    length = len(nums)

    def recursion(i, current_sum, allocated):
        if i == length:
            if current_sum == leftover:
                new_combination = [nums[j] + allocated[j] for j in range(length)]
                res.append(new_combination)
            return

        can_allocate = leftover - current_sum

        for x in range(can_allocate + 1):
            allocated[i] = x
            recursion(i + 1, current_sum + x, allocated)

        allocated[i] = 0

    recursion(0, 0, [0] * length)
    return res


def factCalc(k, n):
    # k!/n!*(k-n)!
    # x/y*z
    x = math.factorial(k)
    y = math.factorial(n)
    # print(k, "-", n, '=', k-n)
    z = math.factorial((k - n))
    return x / (y * z)
