import time as ti
import datetime as dt
import json
import os
import sys
import platform

global d    # To store JSON-data of all users
d: dict = dict()
global acno     # To store the AccNo of current user throughout the program
acno: int = 0

def checkexist() -> None:                               #To check the existence of the file(s-bank.json)
    f: str = 's-bank.json'
    if os.path.exists(f):
        fp = open(f, 'r')
        global d
        d = json.load(fp)
        fp.close()
        return
    else:
        fp = open(f, 'w')
        x: dict = dict()
        json.dump(x, fp, indent=4)
        fp.close()


class bank:
    def __init__(self: object, accno: int) -> None:
        self.accno = accno
        
    def createacc() -> None:            # To create a new Account
        times = dt.datetime.now()
        lr: int = 0
        age: int = 0
        print()
        na: str = input("Enter your name : ").upper()
        while 1:                                # Validating new-user's Age
            age = int(input("Enter your age : "))
            lr += 1
            if age < 18:
                print(f"Your Age {age} is below '18', Please try with correct Age(>18).")
            else:
                break
        clearsc_lines(2*lr)
        print("Please Wait...\nYour new account is creating.....")
        k: list = list(d.keys())
        acc: int = 0
        j: int = 1
        while 1:                    # Validating the ACC number {ACC no is unique to everyone}
            acc = int(input("Enter new account number (4-digit) : "))
            for i in k:
                if i == str(acc):
                    j = 0
                    break
            if j == 1:
                break
            else:
                continue
        clearsc_lines(1)
        sacno: str = str(acc)
        s: dict = {               # Schema of customer JSON data.
            'name':na,
            'age':age,
            'bal':0.0,
            'transhistory':[]
            }
        d[sacno] = s
        f = open('s-bank.json','w')
        json.dump(d, f, indent=4)
        f.close()
        load()
        clearsc_lines(2)
        print(f"Your account has been created successfully with Account number    {acc}\n\t{times}")
        print("Thank you for creating your account in \'S-Bank\'!!!")
        print(f"\nNOTE : Kindly Remember your account number as {acc} ( ' You cannot be logged in anymore IF you forget your account number. ' ).")
        te=input("Press Enter to continue...")
        clearsc_lines(11)
        head(2)     # To re-start(resume) the new user program/operations

    def test(self: object) -> None:                   # To check & validate the customer
        if self.accno >= 1000 and self.accno <= 9999:
            global d
            global acno
            for x in d:
                if x == str(self.accno):
                    print(f"Details of the customer : --->\nUserName       : {d[str(x)]['name']}\nAccount Number : {x}\n")
                    acno = x
                    break
            if acno != 0:
                pass
            else:
                print(f'There is no account with AccNo : {self.accno}\nPlease create a new account to do transactions...')
                clearsc_lines(2)
                bank.createacc()
        else:
            print("Invalid account number !\nPlease enter a valid one.")
            clearsc_lines(2)
            head(2)


class customer:
    def __init__(self: object, choice: int) -> None:
        self.choice=choice
        
    def trans(c: str, amou: float, times) -> None:         # To update the transaction history in JSON-file
        s: str = c + str(amou) + " *//* " + str(times)
        global d
        global acno
        r: list = list(d[str(acno)]['transhistory'])
        r.append(s)
        d[str(acno)]['transhistory'] = r
        
    def option(self: object) -> None:
        times = dt.datetime.now()
        global d
        global acno
        if self.choice == 1 :             # Withdraw
            amount: float = float(input("Enter amount to withdraw : "))
            clearsc_lines(1)
            if amount <= d[str(acno)]['bal']:
                print("Please Wait...")
                d[str(acno)]['bal'] = d[str(acno)]['bal'] - amount
                load()
                customer.trans('-', amount, times)
                print(f"Transaction done\t -{amount}\nAvailable Balance : {d[str(acno)]['bal']}\t{times}")
                te=input("Press Enter to continue...")
                clearsc_lines(4)
            else:
                print(f"Insufficient Balance\nYour Available Balance is only {d[str(acno)]['bal']}\nPlease try again with correct amount based on your balance")
                te=input("Press Enter to continue...")
                clearsc_lines(3)
                
        elif self.choice == 2 :           # Deposit
            amount:float = float(input("Enter amount to deposit : "))
            clearsc_lines(1)
            print("Please Wait...")
            d[str(acno)]['bal'] = d[str(acno)]['bal'] + amount
            load()
            customer.trans('+', amount, times)
            print(f"Transaction done\t +{amount}\nAvailable Balance : {d[str(acno)]['bal']}\t{times}")
            te=input("Press Enter to continue...")
            clearsc_lines(4)
            
        elif self.choice == 3 :           # Balance check
            print("Please Wait...")
            load()
            print(f"Your Available Balance : {d[str(acno)]['bal']}\t{times}")
            te=input("Press Enter to continue...")
            clearsc_lines(3)
            
        elif self.choice == 4 :           # Transaction history
            print("please Wait...")
            load()
            trans_history: list = d[str(acno)]['transhistory']
            l: int = len(trans_history)
            print("Your Transaction History :--> ")
            for i in trans_history:
                print(i)
            te=input("Press Enter to continue...")
            clearsc_lines(l+3)
            
        else:                           # Catch (error) block
            print("Invalid choice\nPlease Enter a valid one next time...")
            clearsc_lines(2)

        f = open('s-bank.json','w')       # To update the changes made to account
        json.dump(d, f, indent=4)
        f.close()


def clearsc_lines(n: int) -> None:                   # To clear the given n.o of lines on console
    ti.sleep(0.65)
    for _ in range(n):
        sys.stdout.write('\033[F')      # Move the cursor up one line
        sys.stdout.write('\033[2K')     # Clear the line
    sys.stdout.flush()


def load() -> None:                 # Loader for all positions
    for i in range(8):
        print("\033[31m🌐 \033[0m"*(i+1), end="\r")
        ti.sleep(0.1)
    ti.sleep(0.1)
    clearsc_lines(1)
    ti.sleep(0.1)
    print("\033[31m        ✅\033[0m")
    ti.sleep(0.35)
    clearsc_lines(1)


def clear_console() -> None:            # To clear the whole console
    ti.sleep(0.5)
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def head(g: int) -> None:                # Main-program execution starter
    if g == 1:
        bank.createacc()
    else:
        x: int = int(input("Enter your (4-digit) Account Number : "))
        clearsc_lines(1)
        cus1=bank(x)
        cus1.test()


def hor() -> None:                  # S-letter animation-methods
        print(" * "*(6))
        ti.sleep(0.2)
def ver(n: int) -> None:
    for i in range(3):
        if n == 1:
            print(" "*(17),end="")
        print("*")
        ti.sleep(0.2)




def start1() -> None:               #1 Execution start line
    checkexist()
    hor()
    ver(0)              # ' S ' animation
    hor()
    ver(1)        
    hor()
    clear_console()

    print("Welcome to")
    a: list = [' _ ', ' S ', ' _ ']
    for i in a:
        print(i, end="\r")
        ti.sleep(0.5)

    print(" _S_ "+"\033[31m🏦\033[0m"+" Bank\n\n")
    x=input("Press Enter to continue...")
    clearsc_lines(2)
    

def start2() -> None:                       #2 Start - End Project Runner (Main)method of whole program
    g: int = int(input("1. Create new account.\n2. LogIn to existing account.\nEnter your choice : "))
    clearsc_lines(3)
    head(g)

    while 1:
        checkexist()        # To update the values repeatedly in json-file
        print("1. Withdraw\n2. Deposit\n3. Check Balance\n4. Transaction History\n5. Exit")
        ch: int = int(input("Enter choice to continue : "))
        clearsc_lines(6)
        if ch == 5:
            break
        else:
            b1=customer(ch)
            b1.option()

    clear_console()
    print("Thank you for choosing  _S_ \033[31m🏦\033[0m bank!\n\nVisit again for fast and secure payments...\n\n\n")         # Execution end line
