import random

def guess_the_number():
    print("Hello! What is your name?")
    name = input()

    number = random.randint(1, 20)
    print(f"\nWell, {name}, I am thinking of a number between 1 and 20.")
    
    guesses = 0

    while True:
        print("Take a guess.")
        guess = int(input())
        guesses += 1

        if guess < number:
            print("\nYour guess is too low.")
        elif guess > number:
            print("\nYour guess is too high.")
        else:
            print(f"\nGood job, {name}! You guessed my number in {guesses} guesses!")
            break

guess_the_number()
