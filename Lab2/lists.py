#1
thislist = ["apple", "banana", "cherry"]
print(thislist)

#len
thislist = ["apple", "banana", "cherry"]
print(len(thislist))

#index
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[2:5])

#index
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[:4])

#index
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[2:])

#index
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
print(thislist[-4:-1])

#in
thislist = ["apple", "banana", "cherry"]
if "apple" in thislist:
  print("Yes, 'apple' is in the fruits list")

#change
thislist = ["apple", "banana", "cherry"]
thislist[1] = "blackcurrant"
print(thislist)

#insert
thislist = ["apple", "banana", "cherry"]
thislist.insert(2, "watermelon")
print(thislist)

#append
thislist = ["apple", "banana", "cherry"]
thislist.append("orange")
print(thislist)

#extend
thislist = ["apple", "banana", "cherry"]
tropical = ["mango", "pineapple", "papaya"]
thislist.extend(tropical)
print(thislist)

#remove
thislist = ["apple", "banana", "cherry"]
thislist.remove("banana")
print(thislist)

#pop
thislist = ["apple", "banana", "cherry"]
thislist.pop(1)
print(thislist)

#del
thislist = ["apple", "banana", "cherry"]
del thislist[0]
print(thislist)

#clear
thislist = ["apple", "banana", "cherry"]
thislist.clear()
print(thislist)

#for loop
thislist = ["apple", "banana", "cherry"]
for x in thislist:
  print(x)

#range
thislist = ["apple", "banana", "cherry"]
for i in range(len(thislist)):
  print(thislist[i])

#while loop
thislist = ["apple", "banana", "cherry"]
i = 0
while i < len(thislist):
  print(thislist[i])
  i = i + 1

#sort ascending
thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort()
print(thislist)

#sort descending
thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort(reverse = True)
print(thislist)

#copy
thislist = ["apple", "banana", "cherry"]
mylist = thislist.copy()
print(mylist)

#list(copy)
thislist = ["apple", "banana", "cherry"]
mylist = list(thislist)
print(mylist)

#:(copy)
thislist = ["apple", "banana", "cherry"]
mylist = thislist[:]
print(mylist)