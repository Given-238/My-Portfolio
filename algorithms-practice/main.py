from searching.linear_search import linear_search
from searching.binary_search import binary_search

from sorting.bubble_sort import bubble_sort
from sorting.selection_sort import selection_sort
from sorting.insertion_sort import insertion_sort
from sorting.merge_sort import merge_sort

def main():
    print("\n=== Algorithms Practice ===")
    print("1. Linear Search")
    print("2. Binary Search")
    print("3. Bubble Sort")
    print("4. Selection Sort")
    print("5. Insertion Sort")
    print("6. Merge Sort")
    print("0. Exit")

    arr = [42, 17, 23, 99, 8, 4, 50]

    while True:
        choice = input("\nChoose an option: ")

        if choice == "1":
            print("Index:", linear_search(arr, 23))

        elif choice == "2":
            sorted_arr = sorted(arr)
            print("Sorted:", sorted_arr)
            print("Index:", binary_search(sorted_arr, 23))

        elif choice == "3":
            print("Sorted:", bubble_sort(arr.copy()))

        elif choice == "4":
            print("Sorted:", selection_sort(arr.copy()))

        elif choice == "5":
            print("Sorted:", insertion_sort(arr.copy()))

        elif choice == "6":
            print("Sorted:", merge_sort(arr.copy()))

        elif choice == "0":
            print("Goodbye")
            break

        else:
            print("Invalid option")

if __name__ == "__main__":
    main()