import math

def sphere_volume(radius):
    volume = (4/3) * math.pi * radius**3
    return volume

r = float(input("Radius "))
print("Volume", sphere_volume(r))
