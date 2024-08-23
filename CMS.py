import email
import random
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import webbrowser
import pymysql

class CustomerManagementSystem:
    def __init__(self):
        self.customers = []
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='1234',
            db='d1'
        )
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):

            create_table_query = """
            CREATE TABLE IF NOT EXISTS customers (
                id INT PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                gender ENUM('Male', 'Female', 'Other'),
                age INT,
                phone BIGINT,
                email VARCHAR(100),
                country VARCHAR(50),
                city VARCHAR(50),
                pincode VARCHAR(20),
                occupation VARCHAR(50)
            )
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()

    def close_connection(self):
            self.cursor.close()
            self.connection.close()

    def get_id(self):
        existing_ids = {customer[0] for customer in self.customers}
        while True:
            customer_id = random.randint(1000000, 9999999)
            if customer_id not in existing_ids:
                return customer_id

    def get_phone(self, prompt="Phone Number: "):
        while True:
            try:
                number = simpledialog.askstring("Input", prompt)
                if number and number.isdigit() and len(number) == 10:
                    return int(number)
                else:
                    messagebox.showerror("Invalid Input", "Please enter a valid 10-digit phone number.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Invalid input. Please enter a numeric phone number.")

    def get_age(self):
        while True:
            try:
                age = simpledialog.askstring("Input", "Age: ")
                if age and age.isdigit():
                    return int(age)
                else:
                    messagebox.showerror("Invalid Input", "Please enter a valid age.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid age.")

    def get_gender(self):
        while True:
            gender = simpledialog.askstring("Input", "Gender (Male, Female, Other): ")
            if gender in ["Male", "Female", "Other"]:
                return gender
            else:
                messagebox.showerror("Invalid Input", "Please enter a valid gender (Male, Female, Other).")

    def add_customer(self):
        add_cus = tk.Toplevel()
        add_cus.title("Add Customer")
        add_cus.geometry("350x800")

        # Frame for the form
        form_frame = ttk.Frame(add_cus, padding=20)
        form_frame.pack(expand=True, fill='both')

        # Labels and Entry fields for each customer attribute
        ttk.Label(form_frame, text="First Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        first_name_entry = ttk.Entry(form_frame)
        first_name_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(form_frame, text="Last Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        last_name_entry = ttk.Entry(form_frame)
        last_name_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(form_frame, text="Gender:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        gender_var = tk.StringVar()
        gender_menu = ttk.OptionMenu(form_frame, gender_var, "Male", "Male", "Female", "Other")
        gender_menu.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(form_frame, text="Age:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        age_entry = ttk.Entry(form_frame)
        age_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(form_frame, text="Phone:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        phone_entry = ttk.Entry(form_frame)
        phone_entry.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(form_frame, text="Email:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        email_entry = ttk.Entry(form_frame)
        email_entry.grid(row=5, column=1, padx=10, pady=5)

        ttk.Label(form_frame, text="Country:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        country_entry = ttk.Entry(form_frame)
        country_entry.grid(row=6, column=1, padx=10, pady=5)

        ttk.Label(form_frame, text="City:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
        city_entry = ttk.Entry(form_frame)
        city_entry.grid(row=7, column=1, padx=10, pady=5)

        ttk.Label(form_frame, text="Pincode:").grid(row=8, column=0, padx=10, pady=5, sticky="w")
        pincode_entry = ttk.Entry(form_frame)
        pincode_entry.grid(row=8, column=1, padx=10, pady=5)

        ttk.Label(form_frame, text="Occupation:").grid(row=9, column=0, padx=10, pady=5, sticky="w")
        occupation_entry = ttk.Entry(form_frame)
        occupation_entry.grid(row=9, column=1, padx=10, pady=5)

        # Function to save customer
        def save_customer():
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            gender = gender_var.get()
            age = int(age_entry.get()) if age_entry.get().isdigit() else 0
            phone = int(phone_entry.get()) if phone_entry.get().isdigit() and len(phone_entry.get()) == 10 else 0
            email = email_entry.get()
            country = country_entry.get()
            city = city_entry.get()
            pincode = pincode_entry.get()
            occupation = occupation_entry.get()

            if not all([first_name, last_name, gender, age, phone, email, country, city, pincode, occupation]):
                messagebox.showerror("Input Error", "All fields must be filled out.")
                return

            customer = [
                self.get_id(),
                first_name,
                last_name,
                gender,
                age,
                phone,
                email,
                country,
                city,
                pincode,
                occupation
            ]

            self.customers.append(customer)

            query = "INSERT INTO customers (id, first_name, last_name, gender, age, phone, email, country, city, pincode, occupation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, customer)
            self.connection.commit()

            messagebox.showinfo("Success", f"{first_name} {last_name} added successfully.")
            add_cus.destroy()

        # Save Button
        save_button = ttk.Button(form_frame, text="Save Customer", command=save_customer)
        save_button.grid(row=10, column=0, columnspan=2, pady=20)

    def search_customer(self):
        phone = self.get_phone()
        for customer in self.customers:
            if phone == customer[5]:
                messagebox.showinfo("Customer Found", str(customer))
                return
        messagebox.showerror("Not Found", "Customer Not Found. Try again.")

    def delete_customer(self):
        phone = self.get_phone()
        for customer in self.customers:
            if phone == customer[5]:
                query = "DELETE FROM customers WHERE phone = %s"
                self.cursor.execute(query, phone)
                self.connection.commit()
                self.customers.remove(customer)
                messagebox.showinfo("Success", f"Customer removed successfully: {customer}")
                return
        messagebox.showerror("Not Found", "Customer Not Found. Try again.")

    def modify_customer(self):
        phone = self.get_phone()

        mod_cus = tk.Toplevel()
        mod_cus.title("Modify Customer")
        mod_cus.geometry("350x800")

        # Frame for the form
        form_frame = ttk.Frame(mod_cus, padding=20)
        form_frame.pack(expand=True, fill='both')

        for customer in self.customers:
            if phone == customer[5]:
                messagebox.showinfo("Modify", "Modify the customer details and click 'Save'.")

                # Labels and Entry fields for each customer attribute, pre-filled with current details
                ttk.Label(form_frame, text="First Name:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
                first_name_entry = ttk.Entry(form_frame)
                first_name_entry.insert(0, customer[1])
                first_name_entry.grid(row=0, column=1, padx=10, pady=5)

                ttk.Label(form_frame, text="Last Name:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
                last_name_entry = ttk.Entry(form_frame)
                last_name_entry.insert(0, customer[2])
                last_name_entry.grid(row=1, column=1, padx=10, pady=5)

                ttk.Label(form_frame, text="Gender:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
                gender_var = tk.StringVar(value=customer[3])
                gender_menu = ttk.OptionMenu(form_frame, gender_var, customer[3], "Male", "Female", "Other")
                gender_menu.grid(row=2, column=1, padx=10, pady=5)

                ttk.Label(form_frame, text="Age:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
                age_entry = ttk.Entry(form_frame)
                age_entry.insert(0, customer[4])
                age_entry.grid(row=3, column=1, padx=10, pady=5)

                ttk.Label(form_frame, text="Phone:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
                phone_entry = ttk.Entry(form_frame)
                phone_entry.insert(0, customer[5])
                phone_entry.grid(row=4, column=1, padx=10, pady=5)

                ttk.Label(form_frame, text="Email:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
                email_entry = ttk.Entry(form_frame)
                email_entry.insert(0, customer[6])
                email_entry.grid(row=5, column=1, padx=10, pady=5)

                ttk.Label(form_frame, text="Country:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
                country_entry = ttk.Entry(form_frame)
                country_entry.insert(0, customer[7])
                country_entry.grid(row=6, column=1, padx=10, pady=5)

                ttk.Label(form_frame, text="City:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
                city_entry = ttk.Entry(form_frame)
                city_entry.insert(0, customer[8])
                city_entry.grid(row=7, column=1, padx=10, pady=5)

                ttk.Label(form_frame, text="Pincode:").grid(row=8, column=0, padx=10, pady=5, sticky="w")
                pincode_entry = ttk.Entry(form_frame)
                pincode_entry.insert(0, customer[9])
                pincode_entry.grid(row=8, column=1, padx=10, pady=5)

                ttk.Label(form_frame, text="Occupation:").grid(row=9, column=0, padx=10, pady=5, sticky="w")
                occupation_entry = ttk.Entry(form_frame)
                occupation_entry.insert(0, customer[10])
                occupation_entry.grid(row=9, column=1, padx=10, pady=5)

                # Function to save modifications
                def save_modifications(first_name=None, last_name=None, gender=None, age=None, new_phone=None,
                                       country=None, city=None, pincode=None, occupation=None):
                    customer[1] = first_name_entry.get()
                    customer[2] = last_name_entry.get()
                    customer[3] = gender_var.get()
                    customer[4] = int(age_entry.get()) if age_entry.get().isdigit() else customer[4]
                    customer[5] = int(phone_entry.get()) if phone_entry.get().isdigit() and len(
                        phone_entry.get()) == 10 else customer[5]
                    customer[6] = email_entry.get()
                    customer[7] = country_entry.get()
                    customer[8] = city_entry.get()
                    customer[9] = pincode_entry.get()
                    customer[10] = occupation_entry.get()
                    query = "UPDATE customers SET first_name = %s, last_name = %s, gender = %s, age = %s, phone = %s, email = %s, country = %s, city = %s, pincode = %s, occupation = %s WHERE id = %s"
                    self.cursor.execute(query, (first_name, last_name, gender, age, new_phone, email, country, city, pincode, occupation,customer[0]))
                    self.connection.commit()
                    messagebox.showinfo("Success", "Customer Modified Successfully.")
                    mod_cus.destroy()

                # Save Button
                save_button = ttk.Button(form_frame, text="Save Changes", command=save_modifications)
                save_button.grid(row=10, column=0, columnspan=2, pady=20)

                return
            

        messagebox.showerror("Not Found", "Customer Not Found. Try again.")
        mod_cus.destroy()

    def display_all_customers(self):
        if not self.customers:
            messagebox.showinfo("No Customers", "No customers found.")
        else:
            dis_cus = tk.Toplevel()
            dis_cus.title("All Customer Information")
            dis_cus.geometry("1920x1080")

            columns = ("First Name", "Last Name", "Gender", "Age", "Phone", "Email", "Country", "City", "Pincode", "Occupation")
            tree = ttk.Treeview(dis_cus, columns=columns, show="headings")
            tree.pack(fill=tk.BOTH, expand=True)
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150, anchor='center')

                # Insert customer data into the tree
            for customer in self.customers:
                tree.insert('', tk.END, values=customer)

                # Add a scrollbar
            scrollbar = ttk.Scrollbar(dis_cus, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    def play_music(self, song_query):
        try:
            # Using webbrowser to open in Chrome
            chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
            webbrowser.get(chrome_path).open(f"https://www.youtube.com/results?search_query={song_query}")
            print(f"Playing {song_query} on YouTube.")
        except Exception as e:
            print(e)
            print("There was an error while trying to search for the song.")

class Calculator:
    def __init__(self, root):
        self.expression = ""
        self.input_text = tk.StringVar()
        self.create_widgets(root)

    def create_widgets(self, root):
        input_frame = ttk.Frame(root)
        input_frame.pack()

        input_field = tk.Entry(input_frame, textvariable=self.input_text, font=('Helvetica', 18), width=50, borderwidth=5)
        input_field.grid(row=0, column=0, columnspan=4)

        btns_frame = ttk.Frame(root)
        btns_frame.pack()

        buttons = [
            '7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        row_val = 1
        col_val = 0
        for button in buttons:
            ttk.Button(btns_frame, text=button, command=lambda x=button: self.click(x)).grid(row=row_val, column=col_val, padx=5, pady=5)
            col_val += 1
            if col_val == 4:
                col_val = 0
                row_val += 1

        ttk.Button(btns_frame, text='C', command=self.clear).grid(row=row_val, column=0, padx=5, pady=5, columnspan=4, sticky="ew")

    def click(self, item):
        if item == "=":
            self.calculate()
        else:
            self.expression += str(item)
            self.input_text.set(self.expression)

    def calculate(self):
        try:
            result = str(eval(self.expression))
            self.input_text.set(result)
            self.expression = result
        except Exception as e:
            self.input_text.set("Error")
            self.expression = ""

    def clear(self):
        self.expression = ""
        self.input_text.set("")

def main():
    cms = CustomerManagementSystem()

    def add_customer():
        cms.add_customer()

    def search_customer():
        cms.search_customer()

    def delete_customer():
        cms.delete_customer()

    def modify_customer():
        cms.modify_customer()

    def display_all_customers():
        cms.display_all_customers()

    def play_music():
        song_query = simpledialog.askstring("Input", "Enter song query: ")
        if song_query:
            cms.play_music(song_query)

    def open_calculator():
        calc_window = tk.Toplevel()
        calc_window.title("Scientific Calculator")
        calc_window.geometry("400x600")
        calculator = Calculator(calc_window)

    root = tk.Tk()
    root.title("Customer Management System")
    root.geometry("700x500")

    style = ttk.Style()
    style.configure('TLabel', font=('Helvetica', 14, 'italic'), padding=10)
    style.configure('TButton', font=('Helvetica', 12), padding=5)
    style.configure('TFrame', background='#f0f0f0')

    # Main Frame
    main_frame = ttk.Frame(root, padding=20, style='TFrame')
    main_frame.pack(expand=True, fill='both')

    # Title Section
    title_label = ttk.Label(main_frame, text="Customer Management System", font=("Helvetica", 24, 'bold'))
    title_label.pack(pady=20)

    # Customer Operations Section
    operations_frame = ttk.Frame(main_frame, padding=20, style='TFrame')
    operations_frame.pack(pady=10)

    ttk.Button(operations_frame, text="Add Customer", command=add_customer).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    ttk.Button(operations_frame, text="Search Customer", command=search_customer).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    ttk.Button(operations_frame, text="Modify Customer", command=modify_customer).grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    ttk.Button(operations_frame, text="Delete Customer", command=delete_customer).grid(row=1, column=1, padx=10, pady=10, sticky="ew")
    ttk.Button(operations_frame, text="Display All Customers", command=display_all_customers).grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # Additional Features Section
    features_frame = ttk.Frame(main_frame, padding=20, style='TFrame')
    features_frame.pack(pady=10)

    ttk.Button(features_frame, text="Play Music", command=play_music).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    ttk.Button(features_frame, text="Open Calculator", command=open_calculator).grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    # Exit Button Section
    exit_frame = ttk.Frame(main_frame, padding=10, style='TFrame')
    exit_frame.pack(pady=10)

    ttk.Button(exit_frame, text="Exit", command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
