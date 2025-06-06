def has_33(nums):
    for i in range(len(nums) - 1):
        if nums[i] == 3 and nums[i+1] == 3:
            return True
    return False

input_numbers = input("Numbers of array:").split()
numbers = list(map(int, input_numbers))

print(has_33(numbers))