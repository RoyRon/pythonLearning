def b_search(l, value):
    print("里面")
    left_index, right_index = 0, len(l) - 1
    while left_index <= right_index :
        middle_index = (left_index + right_index) // 2
        if value < l[middle_index]:
            right_index = middle_index-1
        elif value > l[middle_index]:
            left_index = middle_index+1
        else:
            return middle_index
    return -1

l2=[-1,0,1,2,3,4,5,6]
print("外面")
print(b_search(l2,6))


