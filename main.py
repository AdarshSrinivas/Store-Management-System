import datetime
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.ttk import Treeview

from PIL import Image
from PIL import ImageTk

date = datetime.datetime.now().date()
conn = sqlite3.connect("./store.db")
cursor = conn.cursor()


def rounded_rect(canvas, x, y, w, h, c):
    canvas.create_arc(x, y, x + 2 * c, y + 2 * c, start=90, extent=90, style="arc")
    canvas.create_arc(x + w - 2 * c, y + h - 2 * c, x + w, y + h, start=270, extent=90, style="arc")
    canvas.create_arc(x + w - 2 * c, y, x + w, y + 2 * c, start=0, extent=90, style="arc")
    canvas.create_arc(x, y + h - 2 * c, x + 2 * c, y + h, start=180, extent=90, style="arc")
    canvas.create_line(x + c, y, x + w - c, y)
    canvas.create_line(x + c, y + h, x + w - c, y + h)
    canvas.create_line(x, y + c, x, y + h - c)
    canvas.create_line(x + w, y + c, x + w, y + h - c)


class Home_Screen(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Open_Screen,Login_Screen, Main_Screen, Check_Screen, Add_Screen, Update_Screen, Information_Screen, Bill_Screen):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Open_Screen")

    def show_frame(self, page_name):
        # Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()


class Open_Screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f64A8A')
        self.controller = controller
        label_1 = tk.Label(self, text="Welcome To SMS", fg='#faf8f0', bg='#f64A8A', font='Helvetica 25 bold')
        label_1.pack(side='top', fill='x')

        def login():
            controller.show_frame('Login_Screen')

        bottom_frame = tk.Frame(self, bg='#dfcbdb')
        bottom_frame.pack(fill='both', expand=True)
        img2 = ImageTk.PhotoImage(Image.open("icons/login.png"))
        button6 = tk.Button(bottom_frame, image=img2, bd=0, highlightthickness=0, command=login)
        button6.photo = img2
        button6.place(x=690, y=240)

class Login_Screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f64A8A')
        self.controller = controller
        label_1 = tk.Label(self, text="User Authentication", fg='#faf8f0', bg='#f64A8A', font='Helvetica 25 bold')
        label_1.pack(side='top', fill='x')

        def login():
            cursor.execute("Select * from Login where username=?",(self.entry_1.get(),))
            r=cursor.fetchall()

            if self.entry_2.get() == r[0][1]:
                controller.show_frame('Main_Screen')
            else:
                tk.messagebox.showerror('Login Error', 'Invalid')
                self.entry_1.delete(0,END)
                self.entry_2.delete(0, END)


        bottom_frame = tk.Frame(self, bg='#dfcbdb')
        bottom_frame.pack(fill='both', expand=True)
        img2 = ImageTk.PhotoImage(Image.open("icons/login.png"))
        label_2 = tk.Label(bottom_frame, image=img2, bd=0, highlightthickness=0)
        label_2.photo = img2
        label_2.place(x=687, y=75)
        canvas = tk.Canvas(bottom_frame, width=550, height=450, bg='#f64A8A', relief='solid', highlightthickness=0,
                           bd=0)
        canvas.create_rectangle(520, 410, 25, 20, fill='#faf8f0', outline='#23eb66')
        rounded_rect(canvas, 25, 20, 495, 390, 5)
        canvas.place(x=480, y=200)
        img3 = ImageTk.PhotoImage(Image.open("icons/user.png"))
        label_3 = tk.Label(canvas, image=img3, bd=0, highlightthickness=0)
        label_3.photo = img3
        label_3.place(x=100, y=90)
        label_username = tk.Label(canvas, text='Username', bg='#faf8f0', fg='#f64A8A', font='Helvetica 12 bold')
        label_username.place(x=197, y=95)
        self.entry_1 = tk.Entry(canvas, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_1.place(x=200, y=120)
        img4 = ImageTk.PhotoImage(Image.open("icons/pass.png"))
        label_4 = tk.Label(canvas, image=img4, bd=0, highlightthickness=0)
        label_4.photo = img4
        label_4.place(x=100, y=200)
        label_password = tk.Label(canvas, text='Password', bg='#faf8f0', fg='#f64A8A', font='Helvetica 12 bold')
        label_password.place(x=197, y=205)
        self.entry_2 = tk.Entry(canvas, bg="white", show='*', bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_2.place(x=200, y=230)
        button2 = tk.Button(canvas, text='Login', font="Helvetica 14 bold", fg='#faf8f0', bg='#f64A8A', bd=1,
                            relief='solid', command=login)
        button2.place(x=255, y=300)


class Main_Screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f64A8A')
        self.controller = controller
        self.controller.title("Store Management System")
        self.controller.state('zoomed')

        def check():
            controller.show_frame("Check_Screen")

        def add():
            controller.show_frame("Add_Screen")

        def update():
            controller.show_frame("Update_Screen")

        def info():
            controller.show_frame("Information_Screen")

        def bill():
            controller.show_frame("Bill_Screen")

        def exit():
            if messagebox.askyesno("Confirm", "Are you sure?"):
                sys.exit()

        label1 = tk.Label(self, text="Store Management System", fg='#faf8f0', bg='#f64A8A', font='Helvetica 25 bold')
        label1.pack()
        bottom_frame = tk.Frame(self, bg='#dfcbdb')
        bottom_frame.pack(side='bottom', fill='both', expand=True)
        img1 = ImageTk.PhotoImage(Image.open("icons/check.png"))
        button1 = tk.Button(self, image=img1, bd=0, highlightthickness=0, command=check)
        button1.photo = img1
        button1.place(x=700, y=70)
        label_1 = tk.Label(self, text='Check', fg='#f64A8A', bg='#dfcbdb', font='Helvetica 16 bold')
        label_1.place(x=720, y=210)
        img2 = ImageTk.PhotoImage(Image.open("icons/add.png"))
        button2 = tk.Button(self, image=img2, bd=0, highlightthickness=0, command=add)
        button2.photo = img2
        button2.place(x=1000, y=200)
        label_2 = tk.Label(self, text='Add', fg='#f64A8A', bg='#dfcbdb', font='Helvetica 16 bold')
        label_2.place(x=1020, y=340)
        img3 = ImageTk.PhotoImage(Image.open("icons/updateinv.png"))
        button3 = tk.Button(self, image=img3, bd=0, highlightthickness=0, command=update)
        button3.photo = img3
        button3.place(x=400, y=200)
        label_3 = tk.Label(self, text='Update', fg='#f64A8A', bg='#dfcbdb', font='Helvetica 16 bold')
        label_3.place(x=420, y=340)
        img4 = ImageTk.PhotoImage(Image.open("icons/information.png"))
        button4 = tk.Button(self, image=img4, bd=0, highlightthickness=0, command=info)
        button4.photo = img4
        button4.place(x=400, y=440)
        label_4 = tk.Label(self, text='Info', fg='#f64A8A', bg='#dfcbdb', font='Helvetica 16 bold')
        label_4.place(x=440, y=585)
        img5 = ImageTk.PhotoImage(Image.open("icons/bill.png"))
        button5 = tk.Button(self, image=img5, bd=0, highlightthickness=0, command=bill)
        button5.photo = img5
        button5.place(x=1000, y=440)
        label_6 = tk.Label(self, text='Bill', fg='#f64A8A', bg='#dfcbdb', font='Helvetica 16 bold')
        label_6.place(x=1040, y=585)
        img6 = ImageTk.PhotoImage(Image.open("icons/exit.png"))
        button6 = tk.Button(self, image=img6, bd=0, highlightthickness=0, command=exit)
        button6.photo = img6
        button6.place(x=700, y=570)
        label_6 = tk.Label(self, text='Exit', fg='#f64A8A', bg='#dfcbdb', font='Helvetica 16 bold')
        label_6.place(x=720, y=710)


class Check_Screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f64A8A')
        self.controller = controller
        self.controller.title("Store Management System")
        self.controller.state('zoomed')
        id = []
        product = []
        stock = []
        price = []
        self.count = 0

        def home():
            controller.show_frame('Main_Screen')

        def remove_one():
            x=tree.selection()[0]
            y=tree.item(x,'values')
            cursor.execute(("Delete from Products where product="+"'"+y[1]+"'"),)
            conn.commit()
            tree.delete(x)

        label1 = tk.Label(self, text="Store Management System", fg='#faf8f0', bg='#f64A8A', font='Helvetica 25 bold')
        label1.pack()
        bottom_frame = tk.Frame(self, bg='#dfcbdb')
        bottom_frame.pack(side='bottom', fill='both', expand=True)
        img2 = ImageTk.PhotoImage(Image.open("icons/back.png"))
        button_back = tk.Button(bottom_frame, image=img2, bd=0, highlightthickness=0, command=home)
        button_back.photo = img2
        button_back.place(x=90, y=5)
        tree = ttk.Treeview(bottom_frame)
        tree['columns'] = ("ID", "PRODUCT", "IN STOCK", "PRICE")
        tree.column("#0", width=0, stretch='no')
        tree.column("ID", anchor='center', width=120, minwidth=25)
        tree.column("PRODUCT", anchor='center', width=250, minwidth=170)
        tree.column("IN STOCK", anchor='center', width=120, minwidth=25)
        tree.column("PRICE", anchor='center', width=120, minwidth=25)
        tree.heading("ID", text='ID', anchor='center')
        tree.heading("PRODUCT", text='PRODUCT', anchor='center')
        tree.heading("IN STOCK", text='IN STOCK', anchor='center')
        tree.heading("PRICE", text='PRICE', anchor='center')
        tree.pack(pady=200)
        cursor.execute("SELECT * FROM Products")
        row = cursor.fetchall()
        for r in row:
            id.append(str(r[0]))
            product.append(str(r[1]))
            stock.append(str(r[2]))
            price.append(str(r[3]))
        for i in range(0, len(id)):
            if self.count % 2 == 0:
                tree.insert(parent='', index='end', iid=i, text='', values=(id[i], product[i], stock[i], price[i]),
                            tags=['evenrow',])
            else:
                tree.insert(parent='', index='end', iid=i, text='', values=(id[i], product[i], stock[i], price[i]),
                            tags=['oddrow',])
            self.count += 1
        tree.tag_configure('oddrow', background='#faf8f0')
        tree.tag_configure('evenrow', background='#dfcbdb')
        self.count = 0
        button2 = tk.Button(bottom_frame, text='Delete Selected', font="Helvetica 14 bold", fg='#faf8f0', bg='#f64A8A', bd=1,
                            relief='solid', command=remove_one)
        button2.place(x=655,y=450)
        conn.commit()


class Add_Screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f64A8A')
        self.controller = controller
        self.controller.title("Store Management System")
        self.controller.state('zoomed')

        def home():
            controller.show_frame('Main_Screen')

        def add():
            cursor.execute("Select * from Products")
            row = cursor.fetchall()
            if self.entry_1.get() == "" or self.entry_2.get() == "" or self.entry_3.get() == "":
                messagebox.showerror("Error", "Please Fill All")
            else:
                for t in row:
                    if self.entry_1.get() in t:
                        messagebox.showerror("Error", "Already exists")
                        break
                else:
                    cursor.execute("Insert into Products(product,instock,price) Values(?,?,?)",
                                   (self.entry_1.get(), self.entry_2.get(), self.entry_3.get(),))
                    conn.commit()
                    messagebox.showinfo("Successful", "Successfully Added")
                    self.entry_1.delete(0, END)
                    self.entry_2.delete(0, END)
                    self.entry_3.delete(0, END)

        label1 = tk.Label(self, text="Store Management System", fg='#faf8f0', bg='#f64A8A', font='Helvetica 25 bold')
        label1.pack()
        bottom_frame = tk.Frame(self, bg='#dfcbdb')
        bottom_frame.pack(side='bottom', fill='both', expand=True)
        img2 = ImageTk.PhotoImage(Image.open("icons/back.png"))
        button_back = tk.Button(bottom_frame, image=img2, bd=0, highlightthickness=0, command=home)
        button_back.photo = img2
        button_back.place(x=90, y=5)
        canvas = tk.Canvas(bottom_frame, width=550, height=450, bg='#f64A8A', relief='solid', highlightthickness=0,
                           bd=0)
        canvas.create_rectangle(520, 410, 25, 20, fill='#faf8f0', outline='#23eb66')
        rounded_rect(canvas, 25, 20, 495, 390, 5)
        canvas.place(x=480, y=200)
        label_3 = tk.Label(canvas, text='Product', bd=0, highlightthickness=0, fg='#f64A8A', bg='#faf8f0',
                           font='Helvetica 16 bold')
        label_3.place(x=80, y=70)
        self.entry_1 = tk.Entry(canvas, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_1.place(x=190, y=70)

        label_4 = tk.Label(canvas, text='In Stock', bd=0, highlightthickness=0, fg='#f64A8A', bg='#faf8f0',
                           font='Helvetica 16 bold')
        label_4.place(x=80, y=170)
        self.entry_2 = tk.Entry(canvas, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_2.place(x=190, y=170)
        label_5 = tk.Label(canvas, text='Price', bd=0, highlightthickness=0, fg='#f64A8A', bg='#faf8f0',
                           font='Helvetica 16 bold')
        label_5.place(x=80, y=270)
        self.entry_3 = tk.Entry(canvas, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_3.place(x=190, y=270)
        button2 = tk.Button(canvas, text='Add', font="Helvetica 14 bold", fg='#faf8f0', bg='#f64A8A', bd=1,
                            relief='solid', command=add)
        button2.place(x=255, y=360)


class Update_Screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f64A8A')
        self.controller = controller
        self.controller.title("Store Management System")
        self.controller.state('zoomed')

        def home():
            controller.show_frame('Main_Screen')

        def update():
            cursor.execute("Update Products SET product=?,instock=?,price=? where Id=?",
                           (self.entry_1.get(), self.entry_2.get(), self.entry_3.get(), self.entry_0.get(),))
            conn.commit()
            messagebox.showinfo("Successful", "Successfully Updated")
            self.entry_0.delete(0, END)
            self.entry_1.delete(0, END)
            self.entry_2.delete(0, END)
            self.entry_3.delete(0, END)

        def search():
            cursor.execute("Select * from Products where Id=?", (self.entry_0.get(),))
            row = cursor.fetchall()
            if len(row) == 0:
                messagebox.showerror("Error", "Item not Found")
            else:
                for r in row:
                    self.n1 = r[1]
                    self.n2 = r[2]
                    self.n3 = r[3]
                conn.commit()
                self.entry_1.delete(0, END)
                self.entry_1.insert(0, str(self.n1))
                self.entry_2.delete(0, END)
                self.entry_2.insert(0, str(self.n2))
                self.entry_3.delete(0, END)
                self.entry_3.insert(0, str(self.n3))

        label1 = tk.Label(self, text="Store Management System", fg='#faf8f0', bg='#f64A8A', font='Helvetica 25 bold')
        label1.pack()
        bottom_frame = tk.Frame(self, bg='#dfcbdb')
        bottom_frame.pack(side='bottom', fill='both', expand=True)
        img2 = ImageTk.PhotoImage(Image.open("icons/back.png"))
        button_back = tk.Button(bottom_frame, image=img2, bd=0, highlightthickness=0, command=home)
        button_back.photo = img2
        button_back.place(x=90, y=5)
        canvas = tk.Canvas(bottom_frame, width=550, height=510, bg='#f64A8A', relief='solid', highlightthickness=0,
                           bd=0)
        canvas.create_rectangle(520, 470, 25, 20, fill='#faf8f0', outline='#23eb66')
        rounded_rect(canvas, 25, 20, 495, 450, 5)
        canvas.place(x=480, y=140)

        label_2 = tk.Label(canvas, text='Enter ID', bd=0, highlightthickness=0, fg='#f64A8A', bg='#faf8f0',
                           font='Helvetica 16 bold')
        label_2.place(x=80, y=70)
        self.entry_0 = tk.Entry(canvas, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_0.place(x=190, y=70)
        button1 = tk.Button(canvas, text='Search', font="Helvetica 12 bold", fg='#faf8f0', bg='#f64A8A', bd=1,
                            relief='solid', command=search)
        button1.place(x=400, y=70)
        label_3 = tk.Label(canvas, text='Product', bd=0, highlightthickness=0, fg='#f64A8A', bg='#faf8f0',
                           font='Helvetica 16 bold')
        label_3.place(x=80, y=170)
        self.entry_1 = tk.Entry(canvas, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_1.place(x=190, y=170)
        label_4 = tk.Label(canvas, text='In Stock', bd=0, highlightthickness=0, fg='#f64A8A', bg='#faf8f0',
                           font='Helvetica 16 bold')
        label_4.place(x=80, y=270)
        self.entry_2 = tk.Entry(canvas, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_2.place(x=190, y=270)
        label_5 = tk.Label(canvas, text='Price', bd=0, highlightthickness=0, fg='#f64A8A', bg='#faf8f0',
                           font='Helvetica 16 bold')
        label_5.place(x=80, y=370)
        self.entry_3 = tk.Entry(canvas, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_3.place(x=190, y=370)
        button2 = tk.Button(canvas, text='Update', font="Helvetica 14 bold", fg='#faf8f0', bg='#f64A8A', bd=1,
                            relief='solid', command=update)
        button2.place(x=255, y=420)


class Information_Screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f64A8A')
        self.controller = controller
        self.controller.title("Store Management System")
        self.controller.state('zoomed')

        def home():
            controller.show_frame('Main_Screen')

        def search():
            cursor.execute("SELECT * From customer WHERE Billno=" + self.entry_no.get())
            row = cursor.fetchall()
            if len(row) == 0:
                messagebox.showerror("Error", "Customer doesn't exists")
            else:
                for r in row:
                    self.n=r[1]
                    self.n1 = r[2]
                    self.n2 = r[3]
                conn.commit()
                self.entry_0.delete(0, END)
                self.entry_0.insert(0, str(self.n))
                self.entry_1.delete(0, END)
                self.entry_1.insert(0, str(self.n1))
                self.entry_2.delete(0, END)
                self.entry_2.insert(0, str(self.n2))

        def reset():
            self.entry_no.delete(0, END)
            self.entry_0.delete(0, END)
            self.entry_1.delete(0, END)
            self.entry_2.delete(0, END)

        label1 = tk.Label(self, text="Store Management System", fg='#faf8f0', bg='#f64A8A', font='Helvetica 25 bold')
        label1.pack()
        bottom_frame = tk.Frame(self, bg='#dfcbdb')
        bottom_frame.pack(side='bottom', fill='both', expand=True)
        img2 = ImageTk.PhotoImage(Image.open("icons/back.png"))
        button_back = tk.Button(bottom_frame, image=img2, bd=0, highlightthickness=0, command=home)
        button_back.photo = img2
        button_back.place(x=90, y=5)
        canvas = tk.Canvas(bottom_frame, width=550, height=450, bg='#f64A8A', relief='solid', highlightthickness=0,
                           bd=0)
        canvas.create_rectangle(520, 410, 25, 20, fill='#faf8f0', outline='#23eb66')
        rounded_rect(canvas, 25, 20, 495, 390, 5)
        canvas.place(x=480, y=200)
        label_no = tk.Label(canvas, text='Bill No.', bd=0, highlightthickness=0, fg='#f64A8A', bg='#faf8f0',
                            font='Helvetica 16 bold')
        label_no.place(x=40, y=70)
        self.entry_no = tk.Entry(canvas, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_no.place(x=230, y=70)
        label_2 = tk.Label(canvas, text='Mobile No.', bd=0, highlightthickness=0, fg='#f64A8A', bg='#faf8f0',
                           font='Helvetica 16 bold')
        label_2.place(x=40, y=130)
        self.entry_0 = tk.Entry(canvas, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_0.place(x=230, y=130)
        button1 = tk.Button(canvas, text='Search', font="Helvetica 12 bold", fg='#faf8f0', bg='#f64A8A', bd=1,
                            relief='solid', command=search)
        button1.place(x=432, y=67)
        label_3 = tk.Label(canvas, text='Customer Name', bd=0, highlightthickness=0, fg='#f64A8A', bg='#faf8f0',
                           font='Helvetica 16 bold')
        label_3.place(x=40, y=180)
        self.entry_1 = tk.Entry(canvas, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_1.place(x=230, y=180)
        label_4 = tk.Label(canvas, text='Last Purchased', bd=0, highlightthickness=0, fg='#f64A8A', bg='#faf8f0',
                           font='Helvetica 16 bold')
        label_4.place(x=40, y=230)
        self.entry_2 = tk.Entry(canvas, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_2.place(x=230, y=230)
        button2 = tk.Button(canvas, text='Reset', font="Helvetica 14 bold", fg='#faf8f0', bg='#f64A8A', bd=1,
                            relief='solid', command=reset)
        button2.place(x=255, y=295)


class Bill_Screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#f64A8A')
        self.controller = controller
        self.controller.title("Store Management System")
        self.controller.state('zoomed')
        self.bill = 0
        self.count = 0
        self.items=[]
        self.s=","
        query=[]

        def home():
            controller.show_frame('Main_Screen')

        def search():
            sq = "Select * From Products WHERE Id=?"
            cursor.execute(sq, (self.entry_1.get(),))
            i = cursor.fetchall()
            if len(i) == 0:
                messagebox.showerror('Error', 'No item found')
                self.entry_1.delete(0, END)
                self.entry_2.delete(0, END)
                self.entry_3.delete(0, END)
            else:
                for ii in i:
                    self.i1 = ii[1]
                    self.i2 = ii[3]
                conn.commit()
                self.entry_1.delete(0, END)
                self.entry_2.delete(0, END)
                self.entry_2.insert(0, str(self.i1))
                self.entry_3.delete(0, END)
                self.entry_3.insert(0, str(self.i2))

        def remove_one():
            x=tree.selection()[0]
            y=tree.item(x,'values')
            self.items.remove(y[1])
            query.pop(int(x))
            self.bill-=int(y[3])
            tree.delete(x)

        def reset():
            for r in tree.get_children():
                tree.delete(r)
            self.entry_1.delete(0,END)
            self.entry_2.delete(0, END)
            self.entry_3.delete(0, END)
            self.entry_4.delete(0, END)
            self.entry_5.delete(0, END)
            self.entry_6.delete(0, END)
            label_bill.configure(text="")


        def add():
            if self.entry_2.get() == '' or self.entry_3.get() == '' or self.entry_4.get() == '':
                messagebox.showerror('Error', 'No entries available')
            else:
                self.items.append(str(self.entry_2.get()))
                query.append(str("Update Products set instock=instock - "+str(self.entry_4.get()) +" where product='"+self.entry_2.get()+"'"))
                amount = int(self.entry_3.get()) * int(self.entry_4.get())
                self.bill += amount
                if self.count % 2 == 0:
                    tree.insert(parent='', index='end', iid=self.count, text='',
                                values=(self.count + 1, self.entry_2.get(), self.entry_4.get(), amount),
                                tags=('evenrow',))
                    self.count += 1
                else:
                    tree.insert(parent='', index='end', iid=self.count, text='',
                                values=(self.count + 1, self.entry_2.get(), self.entry_4.get(), amount),
                                tags=('oddrow',))
                    self.count += 1

                self.entry_1.delete(0, END)
                self.entry_2.delete(0, END)
                self.entry_3.delete(0, END)
                self.entry_4.delete(0, END)

        def bill():
            if self.entry_5.get() == '' or self.entry_6.get() == '':
                messagebox.showerror("Error", "Please Fill Customer Details")
            else:
                self.s=self.s.join(self.items)
                for r in query:
                    cursor.execute(r)
                cursor.execute("Select * from customer")
                row = cursor.fetchall()
                cursor.execute("Insert into customer(Billno,mobile,name,lpurchase) values(?,?,?,?)",
                               (len(row) + 1, self.entry_5.get(), self.entry_6.get(), datetime.date.today(),))

                cursor.execute("Insert into orders values(?,?,?)",(len(row)+1,self.s,self.bill))
                conn.commit()
                label_bill.configure(text=str("Bill Amount: Rs "+str(self.bill)))

        label1 = tk.Label(self, text="Store Management System", fg='#faf8f0', bg='#f64A8A', font='Helvetica 25 bold')
        label1.pack()
        bottom_frame = tk.Frame(self, bg='#dfcbdb')
        bottom_frame.pack(side='bottom', fill='both', expand=True)
        img2 = ImageTk.PhotoImage(Image.open("icons/back.png"))
        button_back = tk.Button(bottom_frame, image=img2, bd=0, highlightthickness=0, command=home)
        button_back.photo = img2
        button_back.place(x=90, y=5)
        label2 = tk.Label(bottom_frame, text="Enter Product ID", fg='#faf8f0', bg='#dfcbdb', font='Helvetica 14 bold')
        label2.place(x=250, y=95)
        self.entry_1 = tk.Entry(bottom_frame, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_1.place(x=450, y=95)

        label3 = tk.Label(bottom_frame, text="Product", fg='#faf8f0', bg='#dfcbdb', font='Helvetica 14 bold')
        label3.place(x=250, y=145)
        self.entry_2 = tk.Entry(bottom_frame, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_2.place(x=450, y=145)

        label4 = tk.Label(bottom_frame, text="Price", fg='#faf8f0', bg='#dfcbdb', font='Helvetica 14 bold')
        label4.place(x=250, y=195)
        self.entry_3 = tk.Entry(bottom_frame, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_3.place(x=450, y=195)

        label5 = tk.Label(bottom_frame, text="Quantity", fg='#faf8f0', bg='#dfcbdb', font='Helvetica 14 bold')
        label5.place(x=250, y=245)
        self.entry_4 = tk.Entry(bottom_frame, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_4.place(x=450, y=245)

        label6 = tk.Label(bottom_frame, text="Customer Name", fg='#faf8f0', bg='#dfcbdb', font='Helvetica 14 bold')
        label6.place(x=700, y=145)
        self.entry_5 = tk.Entry(bottom_frame, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_5.place(x=900, y=145)

        label7 = tk.Label(bottom_frame, text="Mobile No.", fg='#faf8f0', bg='#dfcbdb', font='Helvetica 14 bold')
        label7.place(x=700, y=195)
        self.entry_6 = tk.Entry(bottom_frame, bg="white", bd=1, relief='solid', font="Helvetica 14", width=17)
        self.entry_6.place(x=900, y=195)

        button1 = tk.Button(bottom_frame, text='Search', font="Helvetica 13 bold", fg='#faf8f0', bg='#f64A8A', bd=1,
                            relief='solid', command=search)
        button1.place(x=700, y=95)

        button2 = tk.Button(bottom_frame, text='Add', font="Helvetica 13 bold", fg='#faf8f0', bg='#f64A8A', bd=1,
                            relief='solid', command=add)
        button2.place(x=600, y=325)
        tree: Treeview = ttk.Treeview(bottom_frame)
        tree['columns'] = ("ID", "PRODUCT", "QUANTITY", "PRICE")
        tree.column("#0", width=0, stretch='no')
        tree.column("ID", anchor='center', width=120, minwidth=25)
        tree.column("PRODUCT", anchor='center', width=250, minwidth=170)
        tree.column("QUANTITY", anchor='center', width=120, minwidth=25)
        tree.column("PRICE", anchor='center', width=120, minwidth=25)
        tree.heading("ID", text='ID', anchor='center')
        tree.heading("PRODUCT", text='PRODUCT', anchor='center')
        tree.heading("QUANTITY", text='QUANTITY', anchor='center')
        tree.heading("PRICE", text='PRICE', anchor='center')
        tree.tag_configure("oddrow", background='#faf8f0')
        tree.tag_configure("evenrow", background='#dfcbdb')
        tree.place(x=250, y=400)

        img2 = ImageTk.PhotoImage(Image.open("icons/generate.png"))
        button2 = tk.Button(bottom_frame, image=img2, bd=0, highlightthickness=0, command=bill)
        button2.photo = img2
        button2.place(x=1000, y=450)
        label_bill = tk.Label(bottom_frame, text="", fg='#faf8f0', bg='#dfcbdb', font='Helvetica 14 bold')
        label_bill.place(x=1000, y=620)
        button = tk.Button(bottom_frame, text='Delete Selected', font="Helvetica 14 bold", fg='#faf8f0', bg='#f64A8A',bd=1,relief='solid', command=remove_one)
        button.place(x=440, y=630)
        button0 = tk.Button(bottom_frame, text='Reset', font="Helvetica 14 bold", fg='#faf8f0', bg='#f64A8A',bd=1, relief='solid', command=reset)
        button0.place(x=630, y=630)

def main():
    app = Home_Screen()
    app.mainloop()


if __name__ == "__main__":
    main()
