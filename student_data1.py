import sqlite3
from tkinter import *
from tkinter import messagebox


class datas:
    def __init__(self):
        self.conn = sqlite3.connect("students.db")
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS student (id INTEGER PRIMARY KEY, name TEXT, college TEXT, rollno INTEGER)")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def view(self):
        self.cur.execute("SELECT * FROM student")
        rows = self.cur.fetchall()
        return rows

    def insert(self, name, college, rollno):
        self.cur.execute("INSERT INTO student VALUES (NULL,?,?,?)", (name, college, rollno))
        self.conn.commit()
        self.view()

    def update(self, id, name, college, rollno):
        self.cur.execute("UPDATE student SET name=?, college=?, rollno=? WHERE id=?", (name, college, rollno, id))
        self.view()

    def delete(self, id):
        self.cur.execute("DELETE FROM student WHERE id=?", (id,))
        self.conn.commit()
        self.view()

obj = datas()


def selected_row(event):
    global selected_tuple
    index = li1.curselection()[0]
    selected_tuple = li1.get(index)
    e1.delete(0, END)
    e1.insert(END, selected_tuple[1])
    e2.delete(0, END)
    e2.insert(END, selected_tuple[2])
    e3.delete(0, END)
    e3.insert(END, selected_tuple[3])


def viewall():
    li1.delete(0, END)
    for row in obj.view():
        li1.insert(END, row)


def add():
    obj.insert(name_text.get(), college_text.get(), rollno_text.get())
    li1.delete(0, END)
    li1.insert(END, (name_text.get(), college_text.get(), rollno_text.get()))
    e1.delete(0,END)
    e2.delete(0, END)
    e3.delete(0, END)


def delete():
    obj.delete(selected_tuple[0])
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    li1.delete(0,END)

def update():
    obj.update(selected_tuple[0], name_text.get(), college_text.get(), rollno_text.get())
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    li1.delete(0,END)


window = Tk()

window.title("Student Data")


def on_closing():
    dd = obj
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        del dd


window.protocol("WM_DELETE_WINDOW", on_closing)  # handle window closing

l1 = Label(window, text="name")
l1.grid(row=0, column=0)

l2 = Label(window, text="college")
l2.grid(row=0, column=2)

l3 = Label(window, text="rollno")
l3.grid(row=1, column=0)

name_text = StringVar()
e1 = Entry(window, textvariable=name_text)
e1.grid(row=0, column=1)

college_text = StringVar()
e2 = Entry(window, textvariable=college_text)
e2.grid(row=0, column=3)
rollno_text = StringVar()
e3 = Entry(window, textvariable=rollno_text)
e3.grid(row=1, column=1)

li1 = Listbox(window, height=6, width=35)
li1.grid(row=2, column=0, rowspan=6, columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=2, column=2, rowspan=6)

li1.configure(yscrollcommand=sb1.set)
sb1.configure(command=li1.yview)

li1.bind('<<ListboxSelect>>', selected_row)

b1 = Button(window, text="View all", width=12, command=viewall, relief=RAISED)
b1.grid(row=2, column=3)

b3 = Button(window, text="Add entry", width=12, command=add, relief=RAISED)
b3.grid(row=4, column=3)

b4 = Button(window, text="Update selected", width=12, command=update, relief=RAISED)
b4.grid(row=5, column=3)

b5 = Button(window, text="Delete selected", width=12, command=delete, relief=RAISED)
b5.grid(row=6, column=3)

b6 = Button(window, text="Close", width=12, command=window.destroy)
b6.grid(row=7, column=3)

window.mainloop()
