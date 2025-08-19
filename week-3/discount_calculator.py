# Week Three Assignment

# 1. Function to calculate discount
def calculate_discount(price, discount_percent):
    """
    Calculate the final price after applying a discount.
    Discount is only applied if discount_percent >= 20.
    """
    if discount_percent >= 20:
        discount_amount = (discount_percent / 100) * price
        final_price = price - discount_amount
        return final_price
    else:
        return price


# 2. Prompt user for inputs
try:
    price = float(input("Enter the original price of the item: "))
    discount_percent = float(input("Enter the discount percentage: "))

    final_price = calculate_discount(price, discount_percent)

    # Output result
    if discount_percent >= 20:
        print(f"Final Price after {discount_percent}% discount: {final_price}")
    else:
        print(f"No discount applied. Final Price: {final_price}")

except ValueError:
    print("Invalid input. Please enter numbers only.")
