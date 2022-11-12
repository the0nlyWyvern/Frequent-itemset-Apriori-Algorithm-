from numpy import sort
from copy import deepcopy


def count_frequency(lst: list) -> dict:
    freq = {}
    for item in lst:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    return freq


def find_largest_value(dataset: list) -> int:
    largest = 0
    for i in dataset:
        if largest < max(i):
            largest = max(i)
    return largest


def check_minSup(set, tidset, minSup: int):
    if type(set) is int:
        if len(tidset[set]) >= minSup:
            return tidset[set]

    result = []
    trans = []
    for i in set:
        trans += tidset[i]

    freq = count_frequency(trans)
    for key, value in freq.items():
        if value == len(set):
            result.append(key)

    if len(result) >= minSup:
        return result
    return None  # if check is None, means the transaction minSup(i_j) < minSup


def itemset_names_isValid(names: list):
    combine = list(names[0] + names[1])
    freq = count_frequency(combine)

    sum = 0
    for key, value in freq.items():
        assert value <= 2, "Error: Invalid names! "
        if value == 1:
            sum += 1
    if sum == 2:
        combine = [key for key, _ in freq.items()]
        combine.sort()
        combine = tuple(combine)
        return combine
    return None


def is_exist(name: list, names: list, debug: bool = False):
    """Only check for n itemset"""
    if debug:
        for i in names:
            if name == i[0]:
                return True
    else:
        for i in names:
            if name == i:
                return True
    return False


def generate_freq_set_1(tidset: list, minSup: int) -> list:
    set = []
    for i, t in enumerate(tidset):
        if i == 0:
            continue
        if len(t) >= minSup:
            set.append(i)
    return set


def generate_freq_set_2(base_set: list, tidset: list, minSup: int, debug: bool = False) -> list:
    """create a set of 2 items only
    can return empty set"""
    set = []
    length = len(base_set)
    for i in range(length):
        for j in range(i+1, length):
            check = check_minSup((base_set[i], base_set[j]), tidset, minSup)
            if check:
                if debug:
                    set.append([(base_set[i], base_set[j]), check])
                else:
                    #print(f"i: {base_set[i]}, j: {base_set[j]}")
                    set.append((base_set[i], base_set[j]))
    return set


def generate_freq_set_n(base_set: list, tidset: list, minSup: int, debug: bool = False) -> list:
    """Input: set of n old items
    Output: set of n + 1 items | >= minSup"""
    try:
        n = len(base_set[0][0])
    except:
        if debug:
            raise Exception("Error: base_set has 1 items")
    set = []
    length = len(base_set)

    if debug:
        for i in range(length):
            for j in range(i+1, length):
                check_name = itemset_names_isValid(
                    (base_set[i][0], base_set[j][0]))
                if check_name is None or is_exist(check_name, set, debug):
                    continue
                check = check_minSup(check_name, tidset, minSup)
                if check:
                    set.append([check_name, check])
    else:
        for i in range(length):
            for j in range(i+1, length):
                check_name = itemset_names_isValid(
                    (base_set[i], base_set[j]))
                if check_name is None or is_exist(check_name, set):
                    continue
                check = check_minSup(check_name, tidset, minSup)
                if check:
                    set.append(check_name)
    return set


def concat(set1: list, set2: list):
    result = deepcopy(set1)
    for i in set2:
        result.append(i)
    return result


def is_subset(items1, items2) -> bool:
    '''Check whether items1 is a subset of items 2
    Eg: items1 = (1,4); items2 = (1,3,4,6) -> True'''
    if type(items1) is not int:
        i1 = {i for i in items1}
    else:
        i1 = {items1}
    if type(items2) is not int:
        i2 = {i for i in items2}
    else:
        i2 = {items2}
    return i1.issubset(i2)


if __name__ == "__main__":
    # tidset = [[], [1, 3, 4, 5], [1, 2, 3, 4, 5, 6],
    #           [2, 4, 5, 6], [1, 3, 5, 6], [1, 2, 3, 4, 5]]
    # minSup = 4
    # g = generate_freq_set_2([1, 2, 3, 4, 5], tidset, minSup)
    # print(f"set 2 items:\n{g}")

    # g_n = generate_freq_set_n(g, tidset, minSup)
    # print(f"set n items:\n{g_n}")
    print(is_subset(2, (1, 2, 3)))
