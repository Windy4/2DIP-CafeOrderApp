import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime
from PIL import Image, ImageTk
from ctypes import windll, byref, sizeof, c_int

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
    def __init__(self, root):
        self.root = root
        self.root.title('Click and Collect App')
        # Load the PNG image file
        script_dir = os.path.dirname(__file__)
        file_name = os.path.join(script_dir, f'icon.png')
        icon_image = Image.open(file_name)
        # Resize the image if needed
        icon_image = icon_image.resize((32, 32), Image.LANCZOS)  # Adjust size as needed

        # Convert the image to a format that Tkinter can use
        icon_photo = ImageTk.PhotoImage(icon_image)

        # Set the window icon
        self.root.iconphoto(True, icon_photo)

        # Sets the color of the entire window to #6b003e
        self.root.configure(bg='#6b003e')

        # Variables to store user input
        self.username_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.items_var = tk.StringVar(value='')
        self.quantities_var = tk.StringVar(value='')

        # Create login/register frame
        self.login_frame = tk.Frame(self.root, bg='#6b003e')
        self.login_frame.pack(padx=20, pady=20)

        tk.Label(self.login_frame, text='Username:', bg='#6b003e', fg='white').grid(row=0, column=0)
        tk.Entry(self.login_frame, textvariable=self.username_var, bg='#50002e', fg='white').grid(row=0, column=1)
        tk.Label(self.login_frame, text='Age:', bg='#6b003e', fg='white').grid(row=1, column=0)
        tk.Entry(self.login_frame, textvariable=self.age_var, bg='#50002e', fg='white').grid(row=1, column=1)
        tk.Label(self.login_frame, text='Password:', bg='#6b003e', fg='white').grid(row=2, column=0)
        tk.Entry(self.login_frame, textvariable=self.password_var, show='*', bg='#50002e', fg='white').grid(row=2, column=1)
        tk.Button(self.login_frame, text='Login/Register', bg='#50002e', fg='white', command=self.login_register).grid(row=3, columnspan=2)

        # Hide the order details frame initially
        self.order_details_frame = None

    def login_register(self):
        username = self.username_var.get()
        age = self.age_var.get()
        password = self.password_var.get()

        if not (12 <= int(age) <= 19):
            messagebox.showerror('Error', 'You must be between 12 and 19 years old to register.')
            return

        if not self.check_password(username, password):
            messagebox.showerror('Error', 'Invalid username or password.')
            return

        # Check if username is valid and implement login/register logic
        messagebox.showinfo('Info', f'Logged in as {username}')
        # Destroy the login frame
        self.login_frame.destroy()
        # Show the order frame
        self.create_order_frame()

    def check_password(self, username, password):
        script_dir = os.path.dirname(__file__)
        file_name = os.path.join(script_dir, f'passwords.txt')
        with open(file_name, 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                if len(parts) == 2:
                    user, pwd = parts
                    if user == username:
                        if pwd == password:
                            return True
                        else:
                            messagebox.showerror('Error', 'Wrong password. Please try again.')
                            return False
            messagebox.showinfo('Info', 'Username not found, registering account')
            self.add_user(username, password)
            return True


    def add_user(self, username, password):
        # Find what directory CafeOrder.py is in and look for passwords.txt (will be used alot)
        script_dir = os.path.dirname(__file__)
        file_name = os.path.join(script_dir, f'passwords.txt')
        with open(file_name, 'a') as file:
            file.write(f'{username}:{password}\n')

    def create_order_frame(self):
        self.order_frame = tk.Frame(self.root, bg='#6b003e')
        self.order_frame.pack(padx=20, pady=20)

        tk.Label(self.order_frame, text='Select Item:', bg='#6b003e', fg='white').grid(row=0, column=0)
        tk.OptionMenu(self.order_frame, self.items_var, *menu_items.keys()).grid(row=0, column=1)
        tk.Label(self.order_frame, text='Quantity:', bg='#6b003e', fg='white').grid(row=1, column=0)
        tk.Entry(self.order_frame, textvariable=self.quantities_var, bg='#50002e', fg='white').grid(row=1, column=1)
        tk.Button(self.order_frame, text='Add Item', command=self.add_item).grid(row=2, columnspan=2)
        tk.Button(self.order_frame, text='Place Order', command=self.place_order).grid(row=3, columnspan=2)

        # Create order details frame
        self.order_details_frame = tk.Frame(self.root)
        self.order_details_frame.pack(padx=20, pady=20)

        tk.Label(self.order_details_frame, text='Order Details:').grid(row=0, columnspan=2)
        self.order_details_text = tk.Text(self.order_details_frame, height=10, width=50)
        self.order_details_text.grid(row=1, columnspan=2)
    # Adds item to order details
    def add_item(self):
        item = self.items_var.get()
        quantity = self.quantities_var.get()
        if quantity.isdigit() and int(quantity) > 0:
            price = menu_items.get(item, 0)
            if price > 0:
                order_details = self.order_details_text.get('1.0', tk.END)
                order_details += f'{item}: {quantity} x ${price:.2f}\n'
                self.order_details_text.delete('1.0', tk.END)
                self.order_details_text.insert(tk.END, order_details)
        else:
            # If quantity is not a positive integer, show error.
            messagebox.showerror('Error', 'Invalid quantity. Please enter a positive number.')

    def place_order(self):
        items_list = self.order_details_text.get('1.0', tk.END).split('\n')
        items_list = [item.strip() for item in items_list if item.strip()]
        username = self.username_var.get()
        if not username:
            messagebox.showerror('Error', 'Please enter your username first.')
            return
        # Calculate total price
        total_price = 0
        order_summary = f'Order Details for {username}:\n\n'
        for item in items_list:
            if ':' in item:
                item_name, quantity_price = item.split(':')
                quantity, price = quantity_price.split('x')
                total_price += int(quantity) * float(price.strip().replace('$', ''))
                order_summary += f'{item_name}: {quantity} x {price}\n'
        order_summary += f'\nTotal Price: ${total_price:.2f}'

        # Save order details to file
        script_dir = os.path.dirname(__file__)
        today_date = datetime.now().strftime('%Y-%m-%d')
        file_name = os.path.join(script_dir, f'{today_date}_order_details.txt')
        with open(file_name, 'a') as file:
            file.write(order_summary)

        messagebox.showinfo('Order Placed', order_summary)
        self.close_program()
    # Close program function
    def close_program(self):
        messagebox.showinfo('Thank You', 'Thank you for ordering!')
        self.root.destroy()

# Create main window
root = tk.Tk()
app = ClickAndCollectApp(root)
root.mainloop()
