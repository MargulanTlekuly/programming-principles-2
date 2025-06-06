def unique_elements(lst):
    unique_lst = []
    for item in lst:
        if item not in unique_lst:
            unique_lst.append(item)
    return unique_lst

input_list = input("Numbers:").split()

input_list = list(map(int, input_list))

result = unique_elements(input_list)
print("Unique elements:", result)
