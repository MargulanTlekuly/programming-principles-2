def histogram(inputList):
    for i in inputList:
        print("*" * i)

input_numbers = input("Numbers:").split()
myList = list(map(int, input_numbers))
result = histogram(myList)
