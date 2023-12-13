from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import psycopg2
from tkinter import Listbox

db_name = 'postgres'
db_user = 'postgres'
db_password = '5658'
db_host = 'localhost'
db_port = '5432'

def create_connection():
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        messagebox.showerror('Error', f'Database error: {str(e)}')
        return None, None

def close_connection(connection, cursor):
    if connection:
        connection.close()
    if cursor:
        cursor.close()

def execute_query(query, params=None):
    connection, cursor = create_connection()
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    except Exception as e:
        messagebox.showerror('Error', f'Database error: {str(e)}')
        return None
    finally:
        close_connection(connection, cursor)

root=Tk()
root.title('Login')
root.geometry('500x500+500+150')
root.configure(bg="#F8F8FF")
root.resizable(False,False)

def signup_command():
    window = Toplevel(root)
    window.title('SignUp')
    window.geometry('500x500+500+150')
    window.configure(bg='#2F3C7E')
    window.resizable(False, False)

    def sign_up():
        username = user.get()
        password = code.get()
        confirm_password = conform_code.get()

        if password == confirm_password:
            window.destroy()
            additional_info_window(username, password)
        else:
            messagebox.showerror('Error', 'Passwords do not match')

    def additional_info_window(username, password):
        additional_window = Toplevel(root)
        additional_window.title('Additional Information')
        additional_window.geometry('500x500+500+150')
        additional_window.configure(bg='#2F3C7E')
        additional_window.resizable(False, False)

        Label(additional_window, text='Fill the form', fg='white', bg='#2F3C7E',
              font=('Microsoft YaHei UI Light', 30, 'bold')).place(x=130, y=50)

        Label(additional_window, text='Enter Address:', fg='white', bg='#2F3C7E',font=('Microsoft YaHei UI Light', 11)).place(x=100, y=160)
        address_entry = Entry(additional_window, width=25, fg='black', border=0, bg='white',font=('Microsoft YaHei UI Light', 11))
        address_entry.place(x=220, y=160)

        Label(additional_window, text='Enter Phone Number:', fg='white', bg='#2F3C7E',font=('Microsoft YaHei UI Light', 11)).place(x=50, y=220)
        phone_entry = Entry(additional_window, width=25, fg='black', border=0, bg='white',font=('Microsoft YaHei UI Light', 11))
        phone_entry.place(x=220, y=220)

        def submit_additional_info():
            address = address_entry.get()
            phone_number = phone_entry.get()

            try:
                connection = psycopg2.connect(
                    dbname=db_name,
                    user=db_user,
                    password=db_password,
                    host=db_host,
                    port=db_port
                )
                cursor = connection.cursor()
                cursor.execute("INSERT INTO clients (username, address, phone_number, password) VALUES (%s, %s, %s, %s)", (username, address, phone_number, password))
                connection.commit()

                messagebox.showinfo('Sign up', 'Successfully signed up')
                cursor.close()
                connection.close()
                additional_window.destroy()
            except Exception as e:
                messagebox.showerror('Error', f'Database error: {str(e)}')

        Button(additional_window, width=39, pady=7, text='Submit', bg='white', fg='#2F3C7E', border=0, command=submit_additional_info).place(x=110, y=320)

    def sign():
        window.destroy()

    Label(window, border=0, bg='#2F3C7E').place(x=50, y=90)

    frame = Frame(window, width=350, height=390, bg='#2F3C7E')
    frame.place(x=75, y=50)

    heading = Label(frame, text='Sign up', fg='white', bg='#2F3C7E', font=('Microsoft YaHei UI Light', 30, 'bold'))
    heading.place(x=100, y=5)

    #############-------------------------------------------------------

    def on_enter(e):
        user.delete(0, 'end')

    def on_leave(e):
        name = user.get()
        if name == '':
            user.insert(0, 'Username')

    user = Entry(frame, width=25, fg='white', border=0, bg='#2F3C7E', font=('Microsoft YaHei UI Light', 11))
    user.place(x=30, y=80)
    user.insert(0, 'Username')
    user.bind('<FocusIn>', on_enter)
    user.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='white').place(x=25, y=107)

    #############-------------------------------------------------------

    def on_enter(e):
        code.delete(0, 'end')

    def on_leave(e):
        name = code.get()
        if name == '':
            code.insert(0, 'Password')

    code = Entry(frame, width=25, fg='white', border=0, bg='#2F3C7E', font=('Microsoft YaHei UI Light', 11))
    code.place(x=30, y=150)
    code.insert(0, 'Password')
    code.bind('<FocusIn>', on_enter)
    code.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='white').place(x=25, y=177)

    #############-------------------------------------------------------

    def on_enter(e):
        conform_code.delete(0, 'end')

    def on_leave(e):
        name = conform_code.get()
        if name == '':
            conform_code.insert(0, 'Password')

    conform_code = Entry(frame, width=25, fg='white', border=0, bg='#2F3C7E', font=('Microsoft YaHei UI Light', 11))
    conform_code.place(x=30, y=220)
    conform_code.insert(0, 'Conform Password')
    conform_code.bind('<FocusIn>', on_enter)
    conform_code.bind('<FocusOut>', on_leave)

    Frame(frame, width=295, height=2, bg='white').place(x=25, y=247)

    #############-------------------------------------------------------

    Button(frame, width=39, pady=7, text='Sign up', bg='white', fg='#2F3C7E', border=0, command=sign_up).place(x=35, y=280)

    label = Button(frame, width=20, text="Log in", border=0, fg='white', cursor='hand2', bg='#2F3C7E',font=('Microsoft YaHei UI Light', 9),command=sign)
    label.place(x=100, y=330)

    window.mainloop()

Label(root,bg='#F8F8FF').place(x=50,y=50)

frame=Frame(root,width=350, height=350,bg='#F8F8FF')
frame.place(x=75,y=70)

heading=Label(frame,text='Welcome!',fg='#2F3C7E',bg='#F8F8FF',font=('Microsoft YaHei UI Light',25,'bold'))
heading.place(x=100,y=5)

#############-----------------------------------------------------

def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username')

user = Entry(frame,width=25,fg='black',border=0,bg='#F8F8FF',font=('Microsoft YaHei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

#############-------------------------------------------------------

def on_enter(e):
    code.delete(0, 'end')

def on_leave(e):
    name = code.get()
    if name == '':
        code.insert(0, 'Password')

code = Entry(frame,width=25,fg='black',border=0,bg='#F8F8FF',font=('Microsoft YaHei UI Light',11))
code.place(x=30,y=150)
code.insert(0,'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

#############-------------------------------------------------------

def login_command():
    username = user.get()
    password = code.get()

    query = "SELECT * FROM clients WHERE username = %s AND password = %s"
    params = (username, password)

    try:
        result = execute_query(query, params)

        if result:
            open_welcome_window()
        else:
            messagebox.showerror('Error', 'Wrong username or password. Try again.')

    except Exception as e:
        messagebox.showerror('Error', f'Database error: {str(e)}')


def open_welcome_window(username, address, phone_number, password):
    root.withdraw()
    welcome_window = Toplevel(root)
    welcome_window.title('MainPage')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    welcome_window.geometry(f'{screen_width}x{screen_height}+0+0')
    welcome_window.configure(bg='#2F3C7E')
    welcome_window.resizable(False, False)

    label = Label(welcome_window, text='Online Shop', fg='#FCE6C9', bg='#2F3C7E',font=('Times New Roman', 60, 'bold'))
    label.place(x=500, y=5)

    Frame(welcome_window, width=450, height=900, bg='#FCE6C9').place(x=0, y=0)
    Frame(welcome_window, width=600, height=5, bg='#FCE6C9').place(x=1000, y=60)

    settings = Label(welcome_window, text='Settings', fg='#2F3C7E', bg='#FCE6C9', font=('Times New Roman', 60, 'bold'))
    settings.place(x=50, y=5)

    profil = Button(welcome_window, width=6, text='Profil', border=0, bg='#FCE6C9', cursor='hand2', fg='#2F3C7E', font=('Times New Roman', 20, 'bold'), command=lambda: open_profil_window(username, address, phone_number, password))
    profil.place(x=50, y=200)

    Frame(welcome_window, width=300, height=2, bg='#2F3C7E').place(x=65, y=250)

    Frame(welcome_window, width=300, height=2, bg='#2F3C7E').place(x=65, y=350)

    leave = Button(welcome_window, width=6, text='Leave', border=0, bg='#FCE6C9', cursor='hand2', fg='#2F3C7E', font=('Times New Roman', 20, 'bold'),command=lambda: leave_and_open_login(root, welcome_window))
    leave.place(x=50, y=400)

    Frame(welcome_window, width=300, height=2, bg='#2F3C7E').place(x=65, y=450)

    faq = Label(welcome_window, text='FAQ', fg='#FCE6C9', bg='#2F3C7E',font=('Times New Roman', 20, 'bold'))
    faq.place(x=600, y=750)

    advertisement = Label(welcome_window, text='Advertisement', fg='#FCE6C9', bg='#2F3C7E', font=('Times New Roman', 20, 'bold'))
    advertisement.place(x=740, y=750)

    support_service = Label(welcome_window, text='Support service', fg='#FCE6C9', bg='#2F3C7E',font=('Times New Roman', 20, 'bold'))
    support_service.place(x=1000, y=750)

    privacy_policy = Label(welcome_window, text='Privacy policy', fg='#FCE6C9', bg='#2F3C7E',font=('Times New Roman', 20, 'bold'))
    privacy_policy.place(x=1280, y=750)

    contact = Label(welcome_window, text='Contact', fg='#2F3C7E', bg='#FCE6C9',font=('Times New Roman', 20, 'bold'))
    contact.place(x=50, y=750)

    about = Label(welcome_window, text='About Us', fg='#2F3C7E', bg='#FCE6C9', font=('Times New Roman', 20, 'bold'))
    about.place(x=50, y=700)

    brand_label = Label(welcome_window, text='Select brand:', fg='#FCE6C9', bg='#2F3C7E',font=('Times New Roman', 30, 'bold'))
    brand_label.place(x=600, y=200)
    category_label = Label(welcome_window, text='Select category:', fg='#FCE6C9', bg='#2F3C7E',font=('Times New Roman', 30, 'bold'))
    category_label.place(x=900, y=200)

    def get_unique_brands():
        query = "SELECT DISTINCT brand FROM my_database"
        return ['All Brands'] + [brand[0] for brand in execute_query(query)]

    def get_unique_categories():
        query = "SELECT DISTINCT category FROM my_database"
        return ['All Categories'] + [category[0] for category in execute_query(query)]

    brands = get_unique_brands()
    categories = get_unique_categories()

    brand_combobox = ttk.Combobox(welcome_window, values=brands, state='readonly')
    brand_combobox.place(x=650, y=270)
    brand_combobox.set('All Brands')

    category_combobox = ttk.Combobox(welcome_window, values=categories, state='readonly')
    category_combobox.place(x=950, y=270)
    category_combobox.set('All Categories')

    min_price_entry = Entry(welcome_window, width=10)
    min_price_entry.place(x=1280, y=270)
    max_price_entry = Entry(welcome_window, width=10)
    max_price_entry.place(x=1380, y=270)

    def apply_filters():
        selected_brand = brand_combobox.get()
        selected_category = category_combobox.get()
        min_price = min_price_entry.get()
        max_price = max_price_entry.get()

        query = "SELECT * FROM my_database WHERE brand = %s AND category = %s"
        params = [selected_brand, selected_category]

        if min_price:
            query += " AND price >= %s"
            params.append(float(min_price))

        if max_price:
            query += " AND price <= %s"
            params.append(float(max_price))

        results = execute_query(query, tuple(params))

    apply_filters_button = Button(welcome_window, text="Apply Filters", command=apply_filters)
    apply_filters_button.place(x=1325, y=300)

    prices = Label(welcome_window, text='Filter prices:', fg='#FCE6C9', bg='#2F3C7E',font=('Times New Roman', 30, 'bold'))
    prices.place(x=1250, y=200)

    result_listbox = Listbox(welcome_window, width=150, height=15, selectbackground="#2F3C7E", selectforeground="white")
    result_listbox.place(x=550, y=400)

    def perform_search():
        selected_brand = brand_combobox.get()
        selected_category = category_combobox.get()
        min_price = min_price_entry.get()
        max_price = max_price_entry.get()

        query = "SELECT prod_id, prod_name, brand, price, category FROM my_database WHERE (%s = 'All Brands' OR brand = %s) AND (%s = 'All Categories' OR category = %s)"
        params = [selected_brand, selected_brand, selected_category, selected_category]

        if min_price:
            query += " AND price >= %s"
            params.append(float(min_price))

        if max_price:
            query += " AND price <= %s"
            params.append(float(max_price))

        results = execute_query(query, tuple(params))

        result_treeview.delete(*result_treeview.get_children())

        for result in results:
            result_treeview.insert("", "end", values=result)

        print(results)

    result_treeview = ttk.Treeview(welcome_window, columns=('ID', "Name", "Brand", "Price", "Category"), show="headings")
    result_treeview.heading("ID", text="ID")
    result_treeview.heading("Name", text="Name")
    result_treeview.heading("Brand", text="Brand")
    result_treeview.heading("Price", text="Price")
    result_treeview.heading("Category", text="Category")
    result_treeview.column("ID", width=100)
    result_treeview.column("Name", width=220)
    result_treeview.column("Brand", width=200)
    result_treeview.column("Price", width=200)
    result_treeview.column("Category", width=180)
    result_treeview.place(x=550, y=400)

    search_button = Button(welcome_window, text="Search", command=perform_search)
    search_button.place(x=1450, y=300)

    shopping_cart = []

    def on_treeview_select(event):
        selected_item = result_treeview.selection()
        if selected_item:
            values = result_treeview.item(selected_item)['values']
            shopping_cart.append(values)

    result_treeview.bind("<ButtonRelease-1>", on_treeview_select)

    def open_cart_window():
        cart_window = Toplevel(root)
        cart_window.title('Shopping Cart')

        def remove_item(item):
            shopping_cart.remove(item)
            update_cart()

        def buy_items_to_cart():
            try:
                if not shopping_cart:
                    messagebox.showwarning('Warning', 'Shopping cart is empty. Add items to the cart first.')
                    return
                connection, cursor = create_connection()
                for item in shopping_cart:
                    prod_id, product_name = item[0], item[1]
                    user_name = user.get()
                    query = "INSERT INTO cart (prod_id, product_name, user_name) VALUES (%s, %s, %s)"
                    params = (prod_id, product_name, user_name)
                    cursor.execute(query, params)
                connection.commit()
                close_connection(connection, cursor)
                messagebox.showinfo('Success', 'All items bought successfully!')
                shopping_cart.clear()
                update_cart()

            except Exception as e:
                print(f'Error: {str(e)}')
                messagebox.showerror('Error', f'Failed to buy the item. Error: {str(e)}')
                if connection:
                    close_connection(connection, cursor)

        def update_cart():
            for widget in cart_window.winfo_children():
                widget.destroy()

            for item in shopping_cart:
                Label(cart_window, text=item, font=('Arial', 12)).pack()
                remove_button = Button(cart_window, text="Remove", command=lambda i=item: remove_item(i))
                remove_button.pack()

            buy_button = Button(cart_window, text="Buy All", command=buy_items_to_cart)
            buy_button.pack()

        update_cart()

    cart = Button(welcome_window, width=5, text='Cart', border=0, bg='#FCE6C9', cursor='hand2', fg='#2F3C7E',font=('Times New Roman', 20, 'bold'), command=open_cart_window)
    cart.place(x=50, y=300)


def leave_and_open_login(root, welcome_window):
    welcome_window.destroy()
    root.deiconify()

def leave_and_open_login(root, welcome_window):
    welcome_window.destroy()
    root.deiconify()

def login_command():
    username = user.get()
    password = code.get()

    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM clients WHERE username = %s AND password = %s", (username, password))
        user_data = cursor.fetchone()

        if user_data:
            username = user_data[0]
            address = user_data[2]
            phone_number = user_data[3]
            password = user_data[1]

            open_welcome_window(username, address, phone_number, password)
        else:
            messagebox.showerror('Error', 'Wrong username or password. Try again.')

    except Exception as e:
        messagebox.showerror('Error', f'Database error: {str(e)}')

    finally:
        if connection:
            connection.close()
            cursor.close()

def open_profil_window(username, address, phone_number, password):
    profil_window = Toplevel(root)
    profil_window.title('Profil')
    profil_window.geometry('500x500+500+150')

    framedk = Frame(profil_window, width=500, height=500, bg='#FCE6C9')
    framedk.place(x=0, y=0)

    heading_profil = Label(framedk, text='Profil', fg='#2F3C7E', bg='#FCE6C9', font=('Microsoft YaHei UI Light', 30, 'bold'))
    heading_profil.place(x=200, y=50)

    Label(framedk, text=f'Username: {username}', fg='#2F3C7E', bg='#FCE6C9',font=('Microsoft YaHei UI Light', 15, 'bold')).place(x=150, y=170)
    Label(framedk, text=f'Address: {address}', fg='#2F3C7E', bg='#FCE6C9', font=('Microsoft YaHei UI Light', 15, 'bold')).place(x=150, y=210)
    Label(framedk, text=f'Phone Number: {phone_number}', fg='#2F3C7E', bg='#FCE6C9',font=('Microsoft YaHei UI Light', 15, 'bold')).place(x=150, y=250)
    Label(framedk, text=f'Password: {password}', fg='#2F3C7E', bg='#FCE6C9',font=('Microsoft YaHei UI Light', 15, 'bold')).place(x=150, y=290)

Button(frame,width=39,pady=7,text='Log in',bg='#2F3C7E',fg='#F8F8FF',border=0,command=login_command).place(x=35,y=204)

label=Label(frame,text="Don't have an account?",fg='black',bg='#F8F8FF',font=('Microsoft YaHei UI Light',9))
label.place(x=75,y=270)

sign_up = Button(frame,width=6,text='Sign up',border=0,bg='#F8F8FF',cursor='hand2',fg='#2F3C7E',command=signup_command)
sign_up.place(x=215,y=270)

root.mainloop()