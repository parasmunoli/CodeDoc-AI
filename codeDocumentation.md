


Arithmetic Operations Program Documentation


Arithmetic Operations Program Documentation
===========================================

---

Overview
--------

This program provides a simple command-line interface for performing basic and advanced arithmetic operations. It includes two classes, `ArithmeticOperations` and `AdvancedArithmeticOperations`, which encapsulate the arithmetic operations. The program's main flow is controlled by the `extended_program` function.

---

Variables
---------

The program uses the following variables:

* `num1` and `num2`: used to store the input numbers for arithmetic operations.
* `choice`: used to store the user's choice of arithmetic operation.

---

Functions
---------

### Menu Functions

The following functions are used to display menus and get user input:

* `menu()`: displays a simple menu for basic arithmetic operations and returns the user's choice (1-8).
* `advanced_menu()`: displays a menu for advanced arithmetic operations and returns the user's choice (1-6).
* `get_input()`: gets user input for basic arithmetic operations and returns two numbers (`num1`, `num2`).
* `get_advanced_input()`: gets user input for advanced arithmetic operations and returns one number (`num1`).

### Operation Functions

The following functions are used to perform arithmetic operations:

* `perform_operation(choice, num1, num2)`: performs the chosen basic arithmetic operation.
* `perform_advanced_operation(choice, num1)`: performs the chosen advanced arithmetic operation.

### Main Functions

The following functions are used to control the program's main flow:

* `main()`: the main driver function for basic arithmetic operations.
* `advanced_operations()`: the main driver function for advanced arithmetic operations.
* `extended_program()`: the main driver function for the entire program.

---

Classes
-------

### ArithmeticOperations Class

The `ArithmeticOperations` class encapsulates the basic arithmetic operations:

* `add(num1, num2)`: returns the sum of `num1` and `num2`.
* `subtract(num1, num2)`: returns the difference of `num1` and `num2`.
* `multiply(num1, num2)`: returns the product of `num1` and `num2`.
* `divide(num1, num2)`: returns the quotient of `num1` and `num2`.
* `modulus(num1, num2)`: returns the remainder of `num1` divided by `num2`.
* `power(num1, num2)`: returns `num1` raised to the power of `num2`.
* `square_root(num1)`: returns the square root of `num1`.

### AdvancedArithmeticOperations Class

<p
