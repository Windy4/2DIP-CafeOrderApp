import os
from datetime import datetime

#Version with user input, some bugs


# Sample menu items and prices
menu_items = {
    'Ice Chocolate': 5,
    'Jucie': 1.5,
    'Nachos': 5,
    'Pie': 5,
    'Steam Bun': 4.50,
    'Donut': 2.50,
    'Brownie': 4.50
}

class ClickAndCollectApp:
    def __init__(self):
        self.username_var = ''
        self.age_var = ''
        self.password_var = ''
        self.items_var = ''
        self.quantities_var = ''

    def get_user_input(self):
        self.username_var = input("Enter your username: ")
        self.age_var = input("Enter your age: ")
        self.password_var = input("Enter your password: ")
        self.items_var = input("Enter items to order (comma-separated): ")
        self.quantities_var = input("Enter quantities for each item (comma-separated): ")

    def login_register(self):
        if not (12 <= int(self.age_var) <= 19):
            print('You must be between 12 and 19 years old to register.')
            return

        if not self.check_password():
            print('Invalid username or password.')
            return

        print(f'Logged in as {self.username_var}')
        self.create_order_frame()

    def check_password(self):
        script_dir = os.path.dirname(__file__)
        file_name = os.path.join(script_dir, f'passwords.txt')
        with open(file_name, 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    user, pwd = parts
                    if user == self.username_var:
                        if pwd == self.password_var:
                            return True
                        else:
                            print('Wrong password. Please try again.')
                            return False
            print('Username not found, registering account')
            self.add_user()
            return True

    def add_user(self):
        script_dir = os.path.dirname(__file__)
        file_name = os.path.join(script_dir, f'passwords.txt')
        with open(file_name, 'a') as file:
            file.write(f'{self.username_var}:{self.password_var}\n')

    def create_order_frame(self):
        order_details = ''
        items_list = self.items_var.split(',')
        quantities_list = self.quantities_var.split(',')
        for item, quantity in zip(items_list, quantities_list):
            if quantity.isdigit() and int(quantity) > 0:
                price = menu_items.get(item, 0)
                if price > 0:
                    order_details += f'{item}: {quantity} x ${price:.2f}\n'
                else:
                    print(f'Item "{item}" not found in the menu.')
            else:
                print(f'Invalid quantity for item "{item}". Please enter a positive number.')

        total_price = sum(int(qty) * menu_items.get(item, 0) for item, qty in zip(items_list, quantities_list))
        order_summary = f'Order Details:\n\n{order_details}\nTotal Price: ${total_price:.2f}'

        script_dir = os.path.dirname(__file__)
        today_date = datetime.now().strftime('%Y-%m-%d')
        file_name = os.path.join(script_dir, f'{today_date}_order_details.txt')
        with open(file_name, 'a') as file:
            file.write(order_summary)

        print(order_summary)
        print('Thank you for ordering!')

# Example usage:
app = ClickAndCollectApp()
app.get_user_input()
app.login_register()
