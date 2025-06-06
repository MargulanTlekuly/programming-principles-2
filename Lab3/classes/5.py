class Account():
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def deposite(self, money):
        self.balance += money

    def withdraw(self, money):
        self.balance -= money
        if(self.balance < 0):
            print("Not money")
        else:
            print(self.balance)
    
w = Account("Madi", 10000)
w.deposite(5000)
w.withdraw(8000)