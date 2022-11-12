from copy import deepcopy
from math import ceil
import utility as util


class Frequent_itemset:
    def __init__(self, file_name: str, minSup: int = None, minSup_percentage: float = None):
        self.dataset = []
        try:
            f = open(file_name, "r")
            for line in f:
                transaction = []
                words = line.split(" ")
                for word in words:
                    try:
                        transaction.append(int(word))
                    except:
                        print("Found 1 value is not 'INT'.")

                self.dataset.append(transaction)
        except FileNotFoundError:
            print("Your file name might be wrong!")

        if minSup_percentage and minSup_percentage <= 1 and minSup_percentage >= 0:
            self.minSup = ceil(minSup_percentage *
                               self.cal_number_of_transactions())
        else:
            if minSup and minSup > 0:
                self.minSup = minSup
            else:
                raise Exception('''Invalid minimum support. 
                Type: minSup -> int (... > 0)
                or    minSup_percentage -> float (0 <= ... <= 1)
                Please type: _ = Apriori("files_name", minSup=3)
                or         : _ = Apriori("files_name", minSup_percentage=0.5)''')

        self.convert_to_Tidset()

    def cal_number_of_transactions(self):
        return len(self.dataset)

    def convert_to_Tidset(self):
        self.tidset = [[]
                       for _ in range(util.find_largest_value(self.dataset) + 1)]
        for idx, transaction in enumerate(self.dataset, start=1):
            for i in transaction:
                self.tidset[i].append(idx)

    def get_freq_itemset(self):
        self.freq_itemset = []
        freq_set1 = util.generate_freq_set_1(self.tidset, self.minSup)
        if freq_set1:
            self.freq_itemset = util.concat(self.freq_itemset, freq_set1)
        else:
            return self.freq_itemset

        freq_set2 = util.generate_freq_set_2(
            freq_set1, self.tidset, self.minSup)
        if freq_set2:
            self.freq_itemset = util.concat(self.freq_itemset, freq_set2)
        else:
            return self.freq_itemset

        s = deepcopy(freq_set2)
        while True:
            _s = util.generate_freq_set_n(s, self.tidset, self.minSup)
            if _s:
                self.freq_itemset = util.concat(self.freq_itemset, _s)
                s = deepcopy(_s)
            else:
                return self.freq_itemset

    def transaction_contains(self, items: tuple) -> list:
        check = util.check_minSup(items, self.tidset, self.minSup)
        if not check:
            raise Exception('These items is not in frequent set')
        return check

    def is_closed_pattern(self, items: tuple) -> bool:
        transactions = self.transaction_contains(items)
        result = []
        combine = []
        l = len(transactions)
        for i in transactions:
            combine += self.dataset[i-1]

        freq = util.count_frequency(combine)
        for key, value in freq.items():
            if value == l:
                result.append(key)
        try:
            if len(result) != len(items):
                return False
        except TypeError:
            if len(result) != 1:
                return False
        return True

    def get_closed_pattern(self):
        try:
            self.freq_itemset
        except AttributeError:
            self.get_freq_itemset()

        if not self.freq_itemset:
            return []

        self.closed_pattern = []
        for i in self.freq_itemset:
            if self.is_closed_pattern(i):
                self.closed_pattern.append(i)
        return self.closed_pattern

    def get_max_pattern(self) -> list:
        try:
            self.closed_pattern
        except AttributeError:
            self.get_closed_pattern()

        if not self.closed_pattern:
            return []

        self.max_pattern = []
        if len(self.closed_pattern) == 1:
            self.max_pattern = deepcopy(self.closed_pattern)
            return self.max_pattern

        for i in range(len(self.closed_pattern)):
            flag = False
            for j in range(i + 1, len(self.closed_pattern)):
                if util.is_subset(self.closed_pattern[i], self.closed_pattern[j]):
                    flag = True
                    break
            if not flag:
                self.max_pattern.append(self.closed_pattern[i])
        return self.max_pattern

    def debug(self, debug: bool = False):
        freq_set1 = util.generate_freq_set_1(self.tidset, self.minSup)
        freq_set2 = util.generate_freq_set_2(
            freq_set1, self.tidset, self.minSup, debug)
        freq_set3 = util.generate_freq_set_n(
            freq_set2, self.tidset, self.minSup, debug)
        freq_set4 = util.generate_freq_set_n(
            freq_set3, self.tidset, self.minSup, debug)

        print(f"freq_set1:\n{freq_set1}")
        print(f"freq_set2:\n{freq_set2}")
        print(f"freq_set3:\n{freq_set3}")
        print(f"freq_set4:\n{freq_set4}")
