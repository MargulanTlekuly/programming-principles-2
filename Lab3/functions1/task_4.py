def prime(n):
    if n < 2:
        return False
    for i in range(2, int(n*0.5) +1):
        if n % i == 0:
            return False
    return True

def filter_prime(numbers):
    return [num for num in numbers if prime(num)]

input_numbers = input("Numbers by spaces:").split()
numbers = list(map(int, input_numbers))

prime_numbers = filter_prime(numbers)
print("Prime numbers:", prime_numbers)

