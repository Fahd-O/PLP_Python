# Basic Calculator Program

# Ask user for input
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
operation = input("Enter an operation (+, -, *, /): ")

# Perform calculation
if operation == "+":
    result = num1 + num2
elif operation == "-":
    result = num1 - num2
elif operation == "*":
    result = num1 * num2
elif operation == "/":
    if num2 == 0:
        print("Error: Division by zero is not allowed.")
        exit()
    result = num1 / num2
else:
    print("Invalid operation.")                            
    exit()

# Display result
print(f"{num1} {operation} {num2} = {result}")
