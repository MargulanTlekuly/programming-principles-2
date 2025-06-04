#set
thisset = {"apple", "banana", "cherry"}
print(thisset)

#in
thisset = {"apple", "banana", "cherry"}

for x in thisset:
  print(x)

#add
thisset = {"apple", "banana", "cherry"}

thisset.add("orange")

print(thisset)

#update
thisset = {"apple", "banana", "cherry"}
tropical = {"pineapple", "mango", "papaya"}

thisset.update(tropical)

print(thisset)

#discard
thisset = {"apple", "banana", "cherry"}

thisset.discard("banana")

print(thisset)

#union
set1 = {"a", "b", "c"}
set2 = {1, 2, 3}

set3 = set1.union(set2)
print(set3)

#intersection
set1 = {"apple", "banana", "cherry"}
set2 = {"google", "microsoft", "apple"}

set3 = set1.intersection(set2)
print(set3)