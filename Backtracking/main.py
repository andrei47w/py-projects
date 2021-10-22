def rec_subs(arr):
    res = []
    rec_backtrack(res, [], arr, 0)
    return res


def rec_backtrack(res, temp, arr, start):
    sum = 0
    for elem in temp:
        sum += elem

    if not sum % len(arr) and temp:
        res.append(temp)

    for i in range(start, len(arr)):
        rec_backtrack(res, temp + [arr[i]], arr, i + 1)


def iter_subs(arr):
    res = [[]]
    new_res = []

    for i in arr:
        for j in res:
            res = res + [[i] + j]

    for list in res:
        sum = 0
        for elem in list:
            sum += elem
        if not sum % len(arr) and list:
            new_res.append(list)

    return new_res

"""
5. The sequence a = a1, ..., an with distinct integer numbers is given. Determine all subsets of elements having the sum divisible by a given n.
"""

arr = [1, 3, 6, 9]

print('\nrecursive implementation: ', rec_subs(arr))

print('\niterative implementation: ', iter_subs(arr))
