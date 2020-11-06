from tkinter import *
from tkinter import ttk
import database as db
import file_manager as fm
import main


db.connect_to_database("IR_database")
root = Tk()

style = ttk.Style()
style.theme_use()

ttk.Label(root, foreground='dark blue', text='IR system', font=('Arial', 20, 'bold')).grid(row=0, column=2)
ttk.Label(root, foreground='black', text='Enter the query', font=('Arial', 15)).grid(row=1, column=0, padx=15, pady=50)

entry1 = ttk.Entry(root, width=40)
entry1.grid(row=1, column=1, pady=50)

style.configure('Info.TButton', foreground='red')
style.configure('Info.TButton', background='black', font=('Arial', 10, 'bold'))

var = IntVar()
var.set(0)

style.configure("TRadiobutton", background="light blue", foreground="dark blue", font=("arial", 15))

rb1 = ttk.Radiobutton(root, text='phrase query', variable=var, value=1).grid(row=2, column=2, ipadx=40)
rb2 = ttk.Radiobutton(root, text='free text query', variable=var, value=2).grid(row=3, column=2, padx=10, ipadx=33)
rb3 = ttk.Radiobutton(root, text='phrase and free query', variable=var, value=3).grid(row=4, column=2)

m = 0


def buclick():
    fail = entry1.get()
    global m
    if m > 0:
        for label in root.grid_slaves():
            if int(label.grid_info()["row"]) >= 5 or int(label.grid_info()["column"] >= 4):
                label.grid_forget()

    if fail:
        if var.get() == 1:
            var1 = IntVar()
            result = main.phrase_query(entry1.get())
            if result:
                ttk.Label(root, foreground='dark red', text='Document Name', font=('Arial', 15)).grid(row=5, column=3)
                c = 6
                docs = []

                def open_d():
                    fm.open_doc(docs[var1.get()], "Collection/")

                for doc_id, rank in result:
                    doc_name = db.load_filename(doc_id)
                    docs.append(doc_name)
                    ttk.Label(root, foreground='dark blue', text=doc_name, font=('Arial', 15)).grid(row=c, column=3)
                    ttk.Radiobutton(root, text='choose it to open', variable=var1, value=c - 6).grid(row=c, column=4)
                    c += 1
                    m += 1
                button2 = ttk.Button(root, text='open file', command=open_d, style='Info.TButton').grid(row=c + 1,
                                                                                                        column=4)
            else:
                m += 1
                ttk.Label(root, foreground='red', text='No result !', font=('Arial', 15, 'bold')).grid(row=5, column=3)
        elif var.get() == 2:
            var2 = IntVar()
            result1 = main.free_text_query(entry1.get())
            if result1:

                ttk.Label(root, foreground='dark red', text='Document Name', font=('Arial', 15)).grid(row=5, column=3)
                ttk.Label(root, foreground='dark red', text='score', font=('Arial', 15)).grid(row=5, column=4)
                c1 = 6
                docs_name = []

                def open1():
                    fm.open_doc(docs_name[var2.get()], "Collection/")

                for doc_id, rank in result1:
                    doc_name = db.load_filename(doc_id)
                    docs_name.append(doc_name)
                    ttk.Label(root, foreground='dark blue', text=doc_name, font=('Arial', 15)).grid(row=c1, column=3)
                    ttk.Label(root, foreground='dark blue', text=round(rank, 4), font=('Arial', 15)).grid(row=c1, column=4)
                    ttk.Radiobutton(root, text='choose it to open', variable=var2, value=c1 - 6).grid(row=c1, column=5)
                    c1 += 1
                    m += 1
                button2 = ttk.Button(root, text='open file', command=open1, style='Info.TButton').grid(row=c1 + 1,
                                                                                                       column=5)
            else:
                m += 1
                ttk.Label(root, foreground='red', text='No result !', font=('Arial', 15, 'bold')).grid(row=5, column=3)
        else:
            var1 = IntVar()
            c = 6
            docs = []

            def open_d():
                fm.open_doc(docs[var1.get()], "Collection/")

            result = main.phrase_query(entry1.get())
            if result:
                ttk.Label(root, foreground='dark red', text='phrase result:', font=('Arial', 15)).grid(row=5, column=0)
                ttk.Label(root, foreground='dark red', text='Document Name', font=('Arial', 15)).grid(row=5, column=1)
                for doc_id, rank in result:
                    doc_name = db.load_filename(doc_id)
                    docs.append(doc_name)
                    ttk.Label(root, foreground='dark blue', text=doc_name, font=('Arial', 12)).grid(row=c, column=1)
                    ttk.Radiobutton(root, text='choose it to open', variable=var1, value=c - 6).grid(row=c, column=2)
                    c += 1
                    m += 1
            else:
                m += 1
                c += 1
                ttk.Label(root, foreground='dark red', text='phrase result:', font=('Arial', 15)).grid(row=5, column=0)
                ttk.Label(root, foreground='red', text='No result !', font=('Arial', 15, 'bold')).grid(row=5, column=1)

            result1 = main.free_text_query(entry1.get())
            if result1:
                ttk.Label(root, foreground='dark red', text='free result:', font=('Arial', 15)).grid(row=c, column=0)

                ttk.Label(root, foreground='dark red', text='Document Name', font=('Arial', 15)).grid(row=c, column=1)
                ttk.Label(root, foreground='dark red', text='score', font=('Arial', 15)).grid(row=c, column=2)
                cc = 1

                def open1():
                    fm.open_doc(docs[var1.get()], "Collection/")

                for doc_id, rank in result1:
                    doc_name = db.load_filename(doc_id)
                    docs.append(doc_name)
                    if c <= 20:
                        ttk.Label(root, foreground='dark blue', text=doc_name, font=('Arial', 12)).grid(row=c + 1,
                                                                                                        column=1)
                        ttk.Label(root, foreground='dark blue', text=round(rank, 4), font=('Arial', 12)).grid(row=c + 1,
                                                                                                              column=2)
                        ttk.Radiobutton(root, text='choose it to open', variable=var1, value=c - 6).grid(row=c + 1,
                                                                                                         column=3)
                    else:
                        ttk.Label(root, foreground='dark blue', text=doc_name, font=('Arial', 12)).grid(row=cc,
                                                                                                        column=4)
                        ttk.Label(root, foreground='dark blue', text=round(rank, 4), font=('Arial', 12)).grid(row=cc,
                                                                                                              column=5)
                        ttk.Radiobutton(root, text='choose it to open', variable=var1, value=c - 6).grid(row=cc,
                                                                                                         column=6)
                        cc += 1
                    c += 1
                    m += 1
            else:
                m += 1
                ttk.Label(root, foreground='dark red', text='free result:', font=('Arial', 15)).grid(row=c, column=0)
                ttk.Label(root, foreground='red', text='No result !', font=('Arial', 15, 'bold')).grid(row=c, column=1)
            if result or result1:
                button2 = ttk.Button(root, text='open file', command=open_d, style='Info.TButton').grid(row=c + 1,
                                                                                                        column=3)
        entry1.delete(0, END)
    else:
        m += 1
        ttk.Label(root, foreground='red', text='please write query!', font=('Arial', 15, 'bold')).grid(row=5, column=1)


button1 = ttk.Button(root, text='Get query', command=buclick, style='Info.TButton').grid(row=1, column=2, pady=50,
                                                                                         padx=100)

root.mainloop()
