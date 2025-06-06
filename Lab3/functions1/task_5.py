import itertools

def print_permutations():
    user_input = input("string: ")
    perms = itertools.permutations(user_input)
    
    for p in perms:
        print(''.join(p))

print_permutations()
