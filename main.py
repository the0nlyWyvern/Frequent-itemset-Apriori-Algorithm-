from Frequent_itemset import *

files_name = ("./data/foodmart.txt", "./data/retail.txt",
              "./data/mushrooms.txt", "./data/chess.txt", "./data/simple_text.txt")

if __name__ == "__main__":
    ds = Frequent_itemset(files_name[4], minSup_percentage=0.5)
    # ds.debug(debug=True)
    freq_set = ds.get_freq_itemset()
    print(freq_set)

    print("Closed pattern: ")
    print(ds.get_closed_pattern())

    print("Max pattern: ")
    print(ds.get_max_pattern())
