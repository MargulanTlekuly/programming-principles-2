import os

path = r'C:\Users\user\OneDrive\Рабочий стол\PP2\Lab6\dir-and-files\text.txt'

with open (path, 'r') as f:
	lines = len(f.readlines())
	print(lines)