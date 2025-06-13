import os

path = r"C:\Users\user\OneDrive\Рабочий стол\PP2\Lab6\folder"

for i in range(65, 91):  # A-Z
    name = os.path.join(path, chr(i) + ".txt")
    f = open(name, "a")
    f.close()
