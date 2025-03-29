import datetime
from tkinter import *
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk

# Clear the frame
def clear_frame():
    for widget in frame.winfo_children():
        widget.destroy()
    bg_image()

# Login frame
def login_frame():
    def login():
        if username_entry.get() == "admin" and password_entry.get() == "password":
            main_frame()
            menubar()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    clear_frame()
    login_frame = Frame(frame, bg="#272220", width=400, height=300)
    login_frame.place(relx=0.5, rely=0.3, anchor="center")
    Label(login_frame, text="Admin Login", font=("Arial", 18, "bold"), bg="#272220", fg="white").place(relx=0.5, rely=0.1, anchor="center")

    Label(login_frame, text="Username", font=("Arial", 14, "bold"), bg="#272220", fg="white").place(relx=0.5, rely=0.3, anchor="center")
    username_entry = Entry(login_frame, font=("Arial", 15), justify="center")
    username_entry.place(relx=0.5, rely=0.38, anchor="center")

    Label(login_frame, text="Password", font=("Arial", 14, "bold"), bg="#272220", fg="white").place(relx=0.5, rely=0.5, anchor="center")
    password_entry = Entry(login_frame, show="*", font=("Arial", 15), justify="center")
    password_entry.place(relx=0.5, rely=0.58, anchor="center")

    forgot_pass = Label(login_frame, text="Forgot Password", font=("Arial", 10, "bold"), bg="#272220", fg="white")
    forgot_pass.place(relx=0.36, rely=0.67, anchor="center")

    login_button = Button(login_frame, text="Login", font=("Arial", 13, "bold"), width=10, bg="#272220", fg="white", command=login)
    login_button.place(relx=0.5, rely=0.85, anchor="center")

    def on_hover(event):
        login_button.config(bg="#3e3733")

    def on_leave(event):
        login_button.config(bg="#272220")

    login_button.bind("<Enter>", on_hover)
    login_button.bind("<Leave>", on_leave)

# Main application
root = Tk()
root.title("Snack BAR")
root.geometry("600x400")
root.config(bg="#272220")
root.resizable(False, False) # width and height not resizable
root.protocol("WM_DELETE_WINDOW", lambda: None)  # Disables the close button
root.state("zoomed")  # Maximizes the window

# Create a frame
frame = Frame(root, bg="#272220")
frame.place(relheight=1, relwidth=1, x=0, y=0)

def bg_image():
    # Set a background image that cannot be cleared or deleted
    background_image = Image.open("C:/Users/mcyor/Documents/Mycodes/pythonProject/snackbar_system/coffeeshop_bg.png")
    resized = background_image.resize((1530, 820))
    background_photo = ImageTk.PhotoImage(resized)

    background_label = Label(frame, image=background_photo)
    background_label.image = background_photo
    background_label.place(x=0, y=0)

    # Lower the background label to ensure it stays behind all other widgets
    background_label.lower()

def menubar():
    # Add a menu bar
    menu_bar = Menu(root)

    # Add a "Menu" cascade
    menu = Menu(menu_bar, tearoff=0)
    menu.add_command(label="Log Out", command=login_frame)
    menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="Menu", menu=menu)

    # Configure the menu bar
    root.config(menu=menu_bar)

# Sample data structure for products
products = []

# Receipt history
receipt_history = []

# login_frame()

# Main frame
def main_frame():
    menubar()
    def show_product_list():
        clear_frame()

        list_main_frame = Frame(frame, bg="#3e3733")
        list_main_frame.place(relx=0.5, rely=0.5, anchor="center", height=600, width=1300) 

        Label(frame, text="Product List", font=("Arial", 20), bg="#272220", fg="white", width=100, height=2).place(relx=0.5, rely=0.03, anchor="center")

        # canvas and a vertical scrollbar for scrolling
        canvas = Canvas(list_main_frame, bg='#3e3733', highlightthickness=0)
        v_scrollbar = Scrollbar(list_main_frame, orient=VERTICAL, command=canvas.yview)
        scrollable_frame = Frame(canvas, bg='#3e3733')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Bind mouse wheel scrolling to the canvas
        def on_mouse_wheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

        # Bind mouse wheel scrolling to the canvas and its children
        def bind_mouse_wheel_to_children(widget):
            widget.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mouse_wheel))
            widget.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
            for child in widget.winfo_children():
                bind_mouse_wheel_to_children(child)

        bind_mouse_wheel_to_children(scrollable_frame)

        canvas.create_window((0, 0), window=scrollable_frame, anchor="center")
        canvas.configure(yscrollcommand=v_scrollbar.set)

        canvas.pack(side=RIGHT, fill=BOTH, expand=True)  # Adjusted to fill both directions
        v_scrollbar.pack(side=RIGHT, fill=Y)

        def refresh_product_list():
            row = 0
            col = 0
            for product in products:
                item_image = Image.open(product['image'])
                item_image = item_image.resize((200, 150))
                item_photo = ImageTk.PhotoImage(item_image)

                list_frame = Frame(scrollable_frame, bd=1, width=5, height=5, bg="#272220")
                list_frame.grid(row=row, column=col, pady=5, padx=15, sticky="nsew")

                product_info = f"{product['name']} - ${product['price']['small']}/{product['price']['medium']}/{product['price']['large']} - {'Available' if product['available'] else 'Unavailable'}"
                image_label = Label(list_frame, image=item_photo, bg="#272220")
                image_label.image = item_photo
                image_label.grid(row=0, column=0, pady=10, padx=5, sticky="nsew")

                Label(list_frame, text=product_info, bg="#3e3733", fg="white", font=("Arial", 12, "bold"), justify="center", anchor="center").grid(row=1, column=0, pady=5, padx=5, sticky="nsew")

                list_frame.grid_columnconfigure(0, weight=1)  # Center content horizontally

                col += 1
                if col == 4:  # Wrap to the next row after 4 columns
                    col = 0
                    row += 1
        
        refresh_product_list()

        back_btn = Button(frame, text="Back", width=15, font=("Arial", 14, "bold"), bg="#3e3733", fg="white", command=main_frame)
        back_btn.place(relx=0.5, rely=0.9, anchor="center")

        def back_btn_enter(event):
            back_btn.config(bg="#272220")
        def back_btn_leave(event):
            back_btn.config(bg="#3e3733")
        
        back_btn.bind("<Enter>", back_btn_enter)
        back_btn.bind("<Leave>", back_btn_leave)
        bind_mouse_wheel_to_children(scrollable_frame)

    def add_product():
        def browse_image():
            file_path = filedialog.askopenfilename(
                title="Select Product Image",
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
            )
            if file_path:
                image_path_var.set(file_path)

        def save_product():
            name = name_entry.get()
            small_price = small_price_entry.get()
            medium_price = medium_price_entry.get()
            large_price = large_price_entry.get()
            image_path = image_path_var.get()

            # Check if all fields are filled
            if not name or not small_price or not medium_price or not large_price or not image_path:
                messagebox.showerror("Error", "All fields must be filled")
                return

            # Confirm before adding the product
            confirm = messagebox.askyesno("Confirm Add", f"Are you sure you want to add the product '{name}'?")
            if not confirm:
                return

            # Add the product
            products.append({
            "name": name,
            "price": {"small": float(small_price), "medium": float(medium_price), "large": float(large_price)},
            "available": True,
            "image": image_path
            })
            messagebox.showinfo("Success", "Product added successfully")
            main_frame()

        clear_frame()

        Label(frame, text="Add Product", font=("Arial", 21), width=100, height=2, bg="#272220", fg="white").place(relx=0.5, rely=0.03, anchor="center")

        add_product_frame = Frame(frame, bd=1, width=500, height=400, bg="#3e3733")
        add_product_frame.place(relx=0.5, rely=0.52, anchor="center")
        
        Label(add_product_frame, text="Name", bg="#3e3733", fg="white", font=("Arial", 15, "bold")).place(relx=0.5, rely=0.09, anchor="center")
        name_entry = Entry(add_product_frame, font=("Arial", 15, "bold"))
        name_entry.place(relx=0.5, rely=0.15, anchor="center")
        
        Label(add_product_frame, text="Small Cup Price", bg="#3e3733", fg="white", font=("Arial", 15, "bold")).place(relx=0.5, rely=0.23, anchor="center")
        small_price_entry = Entry(add_product_frame, font=("Arial", 15, "bold"))
        small_price_entry.place(relx=0.5, rely=0.29, anchor="center")
        
        Label(add_product_frame, text="Medium Cup Price", bg="#3e3733", fg="white", font=("Arial", 15, "bold")).place(relx=0.5, rely=0.37, anchor="center")
        medium_price_entry = Entry(add_product_frame, font=("Arial", 15, "bold"))
        medium_price_entry.place(relx=0.5, rely=0.43, anchor="center")
        
        Label(add_product_frame, text="Large Cup Price", bg="#3e3733", fg="white", font=("Arial", 15, "bold")).place(relx=0.5, rely=0.51, anchor="center")
        large_price_entry = Entry(add_product_frame, font=("Arial", 15, "bold"))
        large_price_entry.place(relx=0.5, rely=0.57, anchor="center")
        
        Label(add_product_frame, text="Image", bg="#3e3733", fg="white", font=("Arial", 15, "bold")).place(relx=0.5, rely=0.65, anchor="center")
        image_path_var = StringVar()
        Entry(add_product_frame, textvariable=image_path_var, state="readonly", font=("Arial", 15, "bold")).place(relx=0.5, rely=0.71, anchor="center")
        browse_button = Button(add_product_frame, text="Browse", font=("Arial", 12, "bold"), bg="#3e3733", fg="white", command=browse_image)
        browse_button.place(relx=0.8, rely=0.71, anchor="center")

        def on_hover(event):
            browse_button.config(bg="#272220")

        def on_leave(event):
            browse_button.config(bg="#3e3733")

        browse_button.bind("<Enter>", on_hover)
        browse_button.bind("<Leave>", on_leave)

        def on_hover(event, button, hover_color="#272220", default_color="#3e3733"):
            button.config(bg=hover_color, fg="white", cursor="hand2")

        def on_leave(event, button, default_color="#3e3733"):
            button.config(bg=default_color, fg="white")

        save_button = Button(add_product_frame, text="Save", width=10, font=("Arial", 12, "bold"), bg="#3e3733", fg="white", command=save_product)
        save_button.place(relx=0.35, rely=0.85, anchor="center")
        save_button.bind("<Enter>", lambda e: on_hover(e, save_button))
        save_button.bind("<Leave>", lambda e: on_leave(e, save_button))

        back_button = Button(add_product_frame, text="Back", width=10, font=("Arial", 12, "bold"), bg="#3e3733", fg="white", command=main_frame)
        back_button.place(relx=0.65, rely=0.85, anchor="center")
        back_button.bind("<Enter>", lambda e: on_hover(e, back_button))
        back_button.bind("<Leave>", lambda e: on_leave(e, back_button))

    def remove_product():
        def delete_product():
            selected_product = product_var.get()
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {selected_product}?")
            if confirm:
                for product in products:
                    if product["name"] == selected_product:
                        products.remove(product)
                        messagebox.showinfo("Success", "Product removed successfully")
                        main_frame()
                        return

        clear_frame()
        remove_product_frame = Frame(frame, bd=1, width=500, height=300, bg="#3e3733")
        remove_product_frame.place(relx=0.5, rely=0.52, anchor="center")

        Label(frame, text="Remove Product", font=("Arial", 21), width=100, height=2, bg="#272220", fg="white").place(relx=0.5, rely=0.03, anchor="center")
        
        Label(remove_product_frame, text="Select Product", bg="#272220", fg="white", font=("Arial", 18, "bold")).place(relx=0.5, rely=0.05, anchor="center",relwidth=1)
        product_var = StringVar()
        product_var.set(products[0]["name"])
        selecting = OptionMenu(remove_product_frame, product_var, *[product["name"] for product in products])
        selecting.config(font=("Arial", 12, "bold"), bg="#3e3733", fg="white")
        selecting.place(relx=0.5, rely=0.2, anchor="center")

        def on_hover(event, button, hover_color="#272220", default_color="#3e3733"):
            button.config(bg=hover_color, fg="white", cursor="hand2")

        def on_leave(event, button, default_color="#3e3733"):
            button.config(bg=default_color, fg="white")

        delete_button = Button(remove_product_frame, text="Delete", width=10, font=("Arial", 12, "bold"), bg="#3e3733", fg="white", command=delete_product)
        delete_button.place(relx=0.35, rely=0.4, anchor="center")
        delete_button.bind("<Enter>", lambda e: on_hover(e, delete_button))
        delete_button.bind("<Leave>", lambda e: on_leave(e, delete_button))

        back_button = Button(remove_product_frame, text="Back", width=10, font=("Arial", 12, "bold"), bg="#3e3733", fg="white", command=main_frame)
        back_button.place(relx=0.65, rely=0.4, anchor="center")
        back_button.bind("<Enter>", lambda e: on_hover(e, back_button))
        back_button.bind("<Leave>", lambda e: on_leave(e, back_button))

    def purchase_products():
        def add_to_cart():
            selected_product = product_var.get()
            quantity = int(quantity_entry.get())
            size = size_var.get()
            for product in products:
                if product["name"] == selected_product:
                    if not product["available"]:
                        messagebox.showerror("Error", "Product is unavailable")
                        return
                    cart.append({"name": selected_product, "size": size, "quantity": quantity, "price": product["price"][size] * quantity})
                    update_cart()
                    return

        def update_cart():
            cart_list.delete(0, END)
            for item in cart:
                cart_list.insert(END, f"{item['name']} ({item['size']}) x{item['quantity']} - ${item['price']:.2f}")

        def remove_from_cart():
            selected_index = cart_list.curselection()
            if selected_index:
                cart.pop(selected_index[0])
                update_cart()
            else:
                messagebox.showerror("Error", "No item selected to remove")

        def checkout():
            total = sum(item["price"] for item in cart)
            receipt = f"Receipt - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            receipt += "\n".join([f"{item['name']} ({item['size']}) x{item['quantity']} - ${item['price']:.2f}" for item in cart])
            receipt += f"\n\nTotal: ${total:.2f}"
            receipt_history.append(receipt)
            messagebox.showinfo("Receipt", receipt)
            cart.clear()
            update_cart()

        clear_frame()
        purchase_product_frame = Frame(frame, bd=1, width=500, height=550, bg="#3e3733")
        purchase_product_frame.place(relx=0.5, rely=0.52, anchor="center")

        Label(frame, text="Purchase Product", font=("Arial", 21), width=100, height=2, bg="#272220", fg="white").place(relx=0.5, rely=0.03, anchor="center")
        
        product_var = StringVar()
        available_products = [product["name"] for product in products if product["available"]]
        if available_products:
            product_var.set(available_products[0])
        Label(purchase_product_frame, text="Select Product", bg="#272220", fg="white", font=("Arial", 16, "bold"), width=100, height=2).place(relx=0.5, rely=0.05, anchor="center")
        selecting = OptionMenu(purchase_product_frame, product_var, *available_products)
        selecting.config(font=("Arial", 12, "bold"), bg="#3e3733", fg="white")
        selecting.place(relx=0.5, rely=0.15, anchor="center")

        Label(purchase_product_frame, text="Quantity", bg="#3e3733", fg="white", font=("Arial", 15, "bold")).place(relx=0.5, rely=0.25, anchor="center")
        quantity_entry = Entry(purchase_product_frame, font=("Arial", 14))
        quantity_entry.place(relx=0.5, rely=0.3, anchor="center")
        
        Label(purchase_product_frame, text="Size", bg="#3e3733", fg="white", font=("Arial", 15, "bold")).place(relx=0.5, rely=0.35, anchor="center")
        size_var = StringVar(value="small")
        OptionMenu(purchase_product_frame, size_var, "small", "medium", "large").place(relx=0.5, rely=0.4, anchor="center")
        
        add_to_cart_button = Button(purchase_product_frame, text="Add to Cart", font=("Arial", 12, "bold"), bg="#3e3733", fg="white", command=add_to_cart)
        add_to_cart_button.place(relx=0.5, rely=0.48, anchor="center")

        def on_hover(event):
            add_to_cart_button.config(bg="#272220")

        def on_leave(event):
            add_to_cart_button.config(bg="#3e3733")

        add_to_cart_button.bind("<Enter>", on_hover)
        add_to_cart_button.bind("<Leave>", on_leave)
        cart = []
        Label(purchase_product_frame, text="Cart", bg="#3e3733", fg="white", font=("Arial", 15, "bold")).place(relx=0.5, rely=0.6, anchor="center")
        cart_list = Listbox(purchase_product_frame, font=("Arial", 18), width=35, height=5, justify="center")
        cart_list.place(relx=0.5, rely=0.66, anchor="center")
        
        def on_hover(event, button, hover_color="#272220", default_color="#3e3733"):
            button.config(bg=hover_color, fg="white", cursor="hand2")

        def on_leave(event, button, default_color="#3e3733"):
            button.config(bg=default_color, fg="white")

        remove_button = Button(purchase_product_frame, text="Remove Selected", font=("Arial", 12, "bold"), bg="#3e3733", fg="white", command=remove_from_cart)
        remove_button.place(relx=0.5, rely=0.86, anchor="center")
        remove_button.bind("<Enter>", lambda e: on_hover(e, remove_button))
        remove_button.bind("<Leave>", lambda e: on_leave(e, remove_button))

        checkout_button = Button(purchase_product_frame, text="Checkout", font=("Arial", 12, "bold"), width=10, bg="#3e3733", fg="white", command=checkout)
        checkout_button.place(relx=0.35, rely=0.95, anchor="center")
        checkout_button.bind("<Enter>", lambda e: on_hover(e, checkout_button))
        checkout_button.bind("<Leave>", lambda e: on_leave(e, checkout_button))

        back_button = Button(purchase_product_frame, text="Back", font=("Arial", 12, "bold"), width=10, bg="#3e3733", fg="white", command=main_frame)
        back_button.place(relx=0.65, rely=0.95, anchor="center")
        back_button.bind("<Enter>", lambda e: on_hover(e, back_button))
        back_button.bind("<Leave>", lambda e: on_leave(e, back_button))

    def edit_product():
        def save_changes():
            selected_product = product_var.get()
            for product in products:
                if product["name"] == selected_product:
                    product["price"]["small"] = float(small_price_entry.get())
                    product["price"]["medium"] = float(medium_price_entry.get())
                    product["price"]["large"] = float(large_price_entry.get())
                    product["available"] = available_var.get()
                    messagebox.showinfo("Success", "Product updated successfully")
                    main_frame()
                    return

        clear_frame()
        edit_product_frame = Frame(frame, bd=1, width=500, height=400, bg="#3e3733")
        edit_product_frame.place(relx=0.5, rely=0.52, anchor="center")

        Label(frame, text="Remove Product", font=("Arial", 21), width=100, height=2, bg="#272220", fg="white").place(relx=0.5, rely=0.03, anchor="center")
        
        Label(edit_product_frame, text="Select Product", bg="#272220", fg="white", font=("Arial", 18, "bold")).place(relx=0.5, rely=0.04, anchor="center",relwidth=1)
        product_var = StringVar()
        product_var.set(products[0]["name"])
        selecting = OptionMenu(edit_product_frame, product_var, *[product["name"] for product in products])
        selecting.config(font=("Arial", 12, "bold"), bg="#3e3733", fg="white")
        selecting.place(relx=0.5, rely=0.15, anchor="center")

        Label(edit_product_frame, text="Small Cup Price", bg="#3e3733", fg="white", font=("Arial", 15, "bold")).place(relx=0.5, rely=0.3, anchor="center")
        small_price_entry = Entry(edit_product_frame, font=("Arial", 15, "bold"))
        small_price_entry.place(relx=0.5, rely=0.36, anchor="center")

        Label(edit_product_frame, text="Medium Cup Price", bg="#3e3733", fg="white", font=("Arial", 15, "bold")).place(relx=0.5, rely=0.44, anchor="center")
        medium_price_entry = Entry(edit_product_frame, font=("Arial", 15, "bold"))
        medium_price_entry.place(relx=0.5, rely=0.5, anchor="center")

        Label(edit_product_frame, text="Large Cup Price", bg="#3e3733", fg="white", font=("Arial", 15, "bold")).place(relx=0.5, rely=0.58, anchor="center")
        large_price_entry = Entry(edit_product_frame, font=("Arial", 15, "bold"))
        large_price_entry.place(relx=0.5, rely=0.65, anchor="center")

        available_var = BooleanVar(value=True)
        Checkbutton(edit_product_frame, text="Available", bg="grey", fg="black", font=("Arial", 15, "bold"), variable=available_var).place(relx=0.5, rely=0.75, anchor="center")

        def populate_fields(*args):
            selected_product = product_var.get()
            for product in products:
                if product["name"] == selected_product:
                    small_price_entry.delete(0, END)
                    small_price_entry.insert(0, product["price"]["small"])
                    medium_price_entry.delete(0, END)
                    medium_price_entry.insert(0, product["price"]["medium"])
                    large_price_entry.delete(0, END)
                    large_price_entry.insert(0, product["price"]["large"])
                    available_var.set(product["available"])
                    return

        product_var.trace("w", populate_fields)
        populate_fields()

        save_button = Button(edit_product_frame, text="Save", width=10, font=("Arial", 12, "bold"), bg="#3e3733", fg="white", command=save_changes)
        save_button.place(relx=0.35, rely=0.9, anchor="center")
        back_button = Button(edit_product_frame, text="Back", width=10, font=("Arial", 12, "bold"), bg="#3e3733", fg="white", command=main_frame)
        back_button.place(relx=0.65, rely=0.9, anchor="center")

        def on_hover(event, button, hover_color="#272220", default_color="#3e3733"):
            button.config(bg=hover_color, fg="white", cursor="hand2")

        def on_leave(event, button, default_color="#3e3733"):
            button.config(bg=default_color, fg="white")

        save_button.bind("<Enter>", lambda e: on_hover(e, save_button))
        save_button.bind("<Leave>", lambda e: on_leave(e, save_button))
        back_button.bind("<Enter>", lambda e: on_hover(e, back_button))
        back_button.bind("<Leave>", lambda e: on_leave(e, back_button))

    def view_receipt_history():
        clear_frame()
        receipt_product_frame = Frame(frame, bd=1, bg="#3e3733")
        receipt_product_frame.place(relx=0.5, rely=0.45, anchor="center", width=500, height=500)

        Label(frame, text="Receipt History", font=("Arial", 21), width=100, height=2, bg="#272220", fg="white").place(relx=0.5, rely=0.03, anchor="center")
        
        rcpt_row = 0
        for receipt in receipt_history:
            frame_rc = Frame(receipt_product_frame)
            frame_rc.grid(row=rcpt_row, column=0)

            Label(frame_rc, text=receipt, anchor="w", justify="left", font=("Arial", 14)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
            rcpt_row += 1

        back_button = Button(frame, text="Back", width=10, font=("Arial", 12, "bold"), bg="#3e3733", fg="white", command=main_frame)
        back_button.place(relx=0.5, rely=0.8, anchor="center")

        def on_hover(event):
            back_button.config(bg="#272220")

        def on_leave(event):
            back_button.config(bg="#3e3733")

        back_button.bind("<Enter>", on_hover)
        back_button.bind("<Leave>", on_leave)

    clear_frame()
    Label(frame, text="Snack BAR", font=("Arial", 22), bg="#272220", fg="white", width=100, height=2).place(relx=0.5, rely=0.03, anchor="center")
    
    navigator_frame = Frame(frame, bg="#aa7b56")
    navigator_frame.place(relx=0.5, rely=0.5, anchor="center", width=500)

    product_list_btn = Button(navigator_frame, text="Product List", font=("Arial", 18), bg="#3e3733", fg="white", command=show_product_list)
    product_list_btn.pack(pady=(0,15), fill=X)
    add_product_btn = Button(navigator_frame, text="Add Product", font=("Arial", 18), bg="#3e3733", fg="white", command=add_product)
    add_product_btn.pack(pady=15, fill=X)
    remove_product_btn = Button(navigator_frame, text="Remove Product", font=("Arial", 18), bg="#3e3733", fg="white", command=remove_product)
    remove_product_btn.pack(pady=15, fill=X)
    edit_product_btn = Button(navigator_frame, text="Edit Product", font=("Arial", 18), bg="#3e3733", fg="white", command=edit_product)
    edit_product_btn.pack(pady=15, fill=X)
    purchase_product_btn = Button(navigator_frame, text="Purchase Products", font=("Arial", 18), bg="#3e3733", fg="white", command=purchase_products)
    purchase_product_btn.pack(pady=15, fill=X)
    rpt_history_btn = Button(navigator_frame, text="Receipt History", font=("Arial", 18), bg="#3e3733", fg="white", command=view_receipt_history)
    rpt_history_btn.pack(pady=(15,0), fill=X)

    def on_hover(event, button, hover_color="#272220", default_color="#3e3733"):
        button.config(bg=hover_color, fg="white", cursor="hand2")

    def on_leave(event, button, default_color="#3e3733"):
        button.config(bg=default_color, fg="white")

    for button in navigator_frame.winfo_children():
        button.bind("<Enter>", lambda e, btn=button: on_hover(e, btn))
        button.bind("<Leave>", lambda e, btn=button: on_leave(e, btn))

    menubar()

login_frame()

root.mainloop()