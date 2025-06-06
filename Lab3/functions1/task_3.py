def solve(numheads, numlegs):
    for chickens in range(numheads + 1):
        rabbits = numheads - chickens
        if(chickens*2 + rabbits*4) == numlegs:
            print("Chickens:", chickens)
            print("Rabbits:", rabbits)
            return
    else:
        print("No solution")

h = int(input("heads:"))
l = int(input("legs:"))

solve(h,l)