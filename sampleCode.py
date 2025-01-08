import math


# Define a class for Arithmetic operations
class ArithmeticOperations:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    # Method for addition
    def add(self):
        return self.num1 + self.num2

    # Method for subtraction
    def subtract(self):
        return self.num1 - self.num2

    # Method for multiplication
    def multiply(self):
        return self.num1 * self.num2

    # Method for division
    def divide(self):
        if self.num2 != 0:
            return self.num1 / self.num2
        else:
            return "Error: Division by zero"

    # Method for modulus
    def modulus(self):
        if self.num2 != 0:
            return self.num1 % self.num2
        else:
            return "Error: Division by zero"

    # Method for power
    def power(self):
        return self.num1 ** self.num2

    # Method for square root
    def square_root(self):
        if self.num1 >= 0:
            return math.sqrt(self.num1)
        else:
            return "Error: Negative number for square root"


# Function for a simple menu system
def menu():
    print("Select the operation you would like to perform:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Modulus")
    print("6. Power")
    print("7. Square Root")
    print("8. Exit")

    choice = input("Enter choice (1/2/3/4/5/6/7/8): ")
    return choice


# Function to get user input
def get_input():
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number (if applicable): "))
        return num1, num2
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return None, None


# Function to handle operations based on user input
def perform_operation(choice, num1, num2):
    arithmetic = ArithmeticOperations(num1, num2)

    if choice == '1':
        print(f"Result of addition: {arithmetic.add()}")
    elif choice == '2':
        print(f"Result of subtraction: {arithmetic.subtract()}")
    elif choice == '3':
        print(f"Result of multiplication: {arithmetic.multiply()}")
    elif choice == '4':
        print(f"Result of division: {arithmetic.divide()}")
    elif choice == '5':
        print(f"Result of modulus: {arithmetic.modulus()}")
    elif choice == '6':
        print(f"Result of power: {arithmetic.power()}")
    elif choice == '7':
        print(f"Result of square root of {num1}: {arithmetic.square_root()}")
    elif choice == '8':
        print("Exiting the program.")
    else:
        print("Invalid choice. Please choose a valid operation.")


# Main driver function
def main():
    print("Welcome to the basic Arithmetic Operations Program!")
    while True:
        choice = menu()

        if choice == '8':
            break

        num1, num2 = get_input()

        if num1 is None or (choice != '7' and num2 is None):
            continue

        perform_operation(choice, num1, num2)
        print("\n")


# Checking if the script is the main module
if __name__ == "__main__":
    main()


# Additional classes for extended functionality
class AdvancedArithmeticOperations:
    def __init__(self, num1, num2=None):
        self.num1 = num1
        self.num2 = num2

    def factorial(self):
        if self.num1 < 0:
            return "Error: Factorial not defined for negative numbers."
        return math.factorial(int(self.num1))

    def log(self):
        if self.num1 <= 0:
            return "Error: Logarithm defined for positive numbers only."
        return math.log(self.num1)

    def exp(self):
        return math.exp(self.num1)

    def sin(self):
        return math.sin(math.radians(self.num1))

    def cos(self):
        return math.cos(math.radians(self.num1))


# Function to handle additional advanced operations
def advanced_menu():
    print("Select an advanced operation:")
    print("1. Factorial")
    print("2. Logarithm (base e)")
    print("3. Exponentiation")
    print("4. Sine (in degrees)")
    print("5. Cosine (in degrees)")
    print("6. Exit")

    choice = input("Enter choice (1/2/3/4/5/6): ")
    return choice


# Function to get user input for advanced operations
def get_advanced_input():
    try:
        num1 = float(input("Enter a number: "))
        return num1
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
        return None


# Function to handle advanced operations
def perform_advanced_operation(choice, num1):
    adv_arithmetic = AdvancedArithmeticOperations(num1)

    if choice == '1':
        print(f"Factorial of {num1}: {adv_arithmetic.factorial()}")
    elif choice == '2':
        print(f"Logarithm of {num1}: {adv_arithmetic.log()}")
    elif choice == '3':
        print(f"Exponentiation of {num1}: {adv_arithmetic.exp()}")
    elif choice == '4':
        print(f"Sine of {num1}: {adv_arithmetic.sin()}")
    elif choice == '5':
        print(f"Cosine of {num1}: {adv_arithmetic.cos()}")
    elif choice == '6':
        print("Exiting the advanced operations menu.")
    else:
        print("Invalid choice. Please choose a valid operation.")


# Main driver for advanced operations
def advanced_operations():
    print("\nAdvanced Arithmetic Operations")
    while True:
        choice = advanced_menu()

        if choice == '6':
            break

        num1 = get_advanced_input()

        if num1 is None:
            continue

        perform_advanced_operation(choice, num1)
        print("\n")


# Additional program flow to enter advanced operations mode
def extended_program():
    while True:
        print("\nMain Menu:")
        print("1. Basic Arithmetic Operations")
        print("2. Advanced Arithmetic Operations")
        print("3. Exit")

        user_choice = input("Choose an option (1/2/3): ")

        if user_choice == '1':
            main()  # Call the basic arithmetic operations
        elif user_choice == '2':
            advanced_operations()  # Call the advanced arithmetic operations
        elif user_choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please choose again.")


# Run the extended program
if __name__ == "__main__":
    extended_program()
