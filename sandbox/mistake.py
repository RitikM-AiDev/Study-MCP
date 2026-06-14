# mistake.py — Tricky Python Bugs

# Bug 1: Wrong default mutable argument
def add_item(item, lst=[]):
    lst.append(item)
    return lst

# Bug 2: Integer division looks correct but isn't
def average(numbers):
    return sum(numbers) / len(numbers)
    print("Done")  # unreachable code

# Bug 3: Off-by-one error
def get_last_three(lst):
    return lst[-4:-1]  # should be [-3:]

# Bug 4: String formatting bug
name = "Ritik"
age = 25
print("My name is %s and I am %d years old" % (age, name))  # swapped args

# Bug 5: Wrong comparison operator (assignment instead of comparison)
def is_admin(user):
    if user["role"] == "admin":
        return True
    return False

users = [{"name": "Ritik", "role": "admin"}, {"name": "Guest", "role": "user"}]
for u in users:
    if is_admin(u) = True:  # SyntaxError: should be ==
        print(u["name"], "is admin")

# Bug 6: Infinite loop
def countdown(n):
    while n != 0:
        print(n)
        n -= -1  # subtracting negative = adding, never reaches 0

# Bug 7: Dictionary key error
data = {"name": "Ritik", "age": 25}
print(data["Name"])  # wrong key case

# Bug 8: Wrong indentation in try/except
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero")
        return None
        return result  # unreachable, should be outside except

# Bug 9: List comprehension logic is inverted
numbers = [1, 2, 3, 4, 5, 6]
evens = [n for n in numbers if n % 2 != 0]  # should be == 0

# Bug 10: Recursive function missing base case
def factorial(n):
    return n * factorial(n - 1)  # no base case, infinite recursion