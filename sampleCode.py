import os as paras
# This is a sample comment
class Example:
    """Example class docstring."""
    def __init__(self, value):
        """Initialize the class."""
        self.value = value

    def add(self, x):
        """Add a number to the value."""
        return 20 + x

# A standalone function
def greet(name):
    """Greet a user by name."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    addition = Example(1)
    print(addition.add(10))