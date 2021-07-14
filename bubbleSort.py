def bubble_sort(lis):
    for right in range(len(lis) - 1, 0, -1):
        for index in range(right):
            if lis[index] > lis[index + 1]:
                lis[index], lis[index + 1] = lis[index + 1], lis[index]


list2 = [2, 3, 1, 5, 4]
bubble_sort(list2)
print(list2)


