def spy_game(nums):
    code = [0, 0, 7]
    for num in nums:
        if code and num == code[0]:
            code.pop(0)
    return len(code) == 0

input_numbers = input("Numbers:").split()

numbers = list(map(int, input_numbers))

result = spy_game(numbers)
print(result)
