def reverse():
    string = input("sentence:")
    words = string.split()
    reversed_words = words[::-1]
    reversed_string = ' '.join(reversed_words)
    print(reversed_string)

reverse()