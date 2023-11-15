from tkinter.ttk import Scrollbar, Frame

from sqlalchemy import Column, Integer, String, Date, ForeignKey, text, create_engine
import psycopg2
import tkinter as tk
from tkinter import ttk
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import tkinter.messagebox as messagebox
from  tkinter import ttk

engine = create_engine('postgresql://localhost:5435/Smith')

# engine = create_engine ('postgresql://postgrespassword@localhost:5435/Smith')   

conn = psycopg2.connect(
    database="Smith",
    user="postgres",
    password="89296593912f",
    host="localhost",
    port="5435"
)

Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Blacksmith(Base):
    __tablename__ = 'Blacksmiths'
    __tableargs__ = {'schema': 'public'}

    id = Column (Integer, primary_key = True)
    name = Column (String)
    surname = Column (String)
    birthdate = Column (Integer)
    work_experience = Column (Integer)

class Provider (Base):
    __tablename__ = 'Provider'
    __tableargs__ = {'schema': 'public'}

    id = Column (Integer, primary_key = True)
    name = Column (String)
    surname = Column (String)
    work_experience = Column (Integer)
    price_per_kg = Column (Integer)

class Raw_material(Base):
     __tablename__ = 'Raw_material'
     __tableargs__ = {'schema': 'public'}

     id = Column (Integer, primary_key = True)
     material = (String)
     heat_capacity = (Integer)
     price = (Integer)

class Anvil(Base):
    __tablename__ = 'Anvil'
    __tableargs__ = {'schema': 'public'}

    id = Column (Integer, primary_key = True)
    genus = (Integer)
    durability = (Integer)

class Smelter(Base):
    __tablename__ = 'Smelter'
    __tableargs__ = {'shema': 'public'}

    id = Column(Integer, primary_key = True)
    dimension = (Integer)
    fabric = (String)
    time_last = (Integer)
    maximum_temperatrure = (Integer)

class Product(Base):
    __tablename__ = 'Product'
    __tableargs__ = {'schema': 'public'}

    id = Column (Integer, primary_key = True)
    type = (String)
    size = (Integer)
    appoitoment = (String)
    weight = (Integer)
    endurance = (Integer)

def show_error(message):
    messagebox.showerror("Ошибка", message)

window = tk.Tk
window.title("Кузня")
window.geometry("800x212")
window.resizable(0, 0)
tables = ['Blacksmiths'
          'Provider'
          'Raw_material'
          'Anvil'
          'Smelter'
          'Product']

def create_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        messagebox.showerror("Error", str(e))


def query1():
    result = session.execute(
        text("SELECT DISTINCT name FROM \"Blacksmiths\" WHERE name = 'Rickie' AND birthdate = '2000-01-25'")
        )
    display_table_query(result, ['Кузнец'])

def query2():
    result = session.execute(
        text("SELECT \"work_experience\" FROM \"Provider\" WHERE work_experience = '40' AND price_per_kg = '35320'"))
    display_table_query(result, ['Поставщик'])

def query3():
    result = session.execute(
        text("SELECT \"material\" FROM \"Raw_material\" WHERE material = 'Aluminum''AND heat_capacity = '2974' AND price = '37294'"))
    display_table_query(result, ['Материал'])

def query4():
    result = session.execute(
        text("SELECT \"durability FROM \"Anvil\" WHERE durability = '65'"))
    display_table_query(result, ['Наковальня'])

def query5():
    result = session.execute(
        text("SELECT \"fabric FROM \"Smelter\" WHERE fabric = 'Granite' AND dimension = '135' AND maximum_temperature = '3200'"))
    display_table_query(result, ['Печь'])

def query6():
    result = session.execute(
        text("SELECT \"type FROM \"Product\" WHERE type = 'sword' AND appointment = 'war' AND weight = '35' AND endurance = '87'"))
    display_table_query(result, ['Товар'])


def main_call():
    add_window = tk.Toplevel (window)
    add_window.title ("Найти")
    add_window.geometry ("250x110")
    window.resizable (0, 0)
    entry_vars = []
    column_names = ['Атрибут', 'В таблице', 'Где атрибут,', 'Должен быть']
    for col in column_names:
        label = tk.Label (add_window, text=col)
        label.grid(row=column_names.index(col), column=0, sticky=tk.W)
        entry_var = tk.StringVar()
        entry = tk.Entry(add_window, textvariable=entry_var)
        entry.grid(row=column_names.index(col), column=1, sticky=tk.W)
        entry_vars.append(entry_var)

    def save_row():
        new_values = [var.get() for var in entry_vars]

        print(new_values)
        til = []
        if (new_values[0].find(", ") != -1):
            til = new_values[0].split(", ")
            new_values[0] = new_values[0].split(", ")
            l = new_values[0][0]
            for i in new_values[0]:
                if i!=l:
                    l += "\", \"" + i
            new_values[0] = l
        else:
            til.append(new_values[0])
        if (new_values[0] == "все" or new_values[0] == "*") and new_values[2]=="":
            tex = "SELECT * FROM public.\"" + new_values[1] + "\""
            table = Base.metadata.tables["public." + new_values[1]]
            til = table.columns.keys()
        else:
            if (new_values[0] == "все" or new_values[0] == "*"):
                tex = "SELECT * FROM public.\"" + new_values[1] + "\" WHERE \"" + new_values[2] + "\"" + new_values[3]
            else:
                tex = "SELECT \"" +new_values[0] +"\" FROM public.\"" + new_values[1] +"\" WHERE \"" + new_values[2] +"\"" + new_values[3]
        result = session.execute(
            text(tex)
        )
        display_table_query(result, til)

    save_button = tk.Button(add_window, width=4, text="ОК", command=save_row)
    save_button.grid(row=len(column_names), columnspan=2)

query0_button = tk.Button(window, width=1000, height=1, text="Расширенный режим поиска", command=main_call)
query0_button.pack(side='bottom')

query1_button = tk.Button(window, width=1000, height=1, text="Определить кузнеца по имени Rickie и его дату рождения ", command=query1)
query1_button.pack(side='bottom')

query2_button = tk.Button(window,width=1000, height=1, text="Определить поставщика с определенным опытом работы и конкретной ценой", command=query2)
query2_button.pack(side='bottom')

query3_button = tk.Button(window, width=1000, height=1, text="Определить аллюминевый материал", command=query3)
query3_button.pack(side='bottom')

query4_button = tk.Button(window, width=1000, height=1, text="Выяснить пригодность наковальни", command=query4)
query4_button.pack(side='bottom')

query5_button = tk.Button(window, width=1000, height=1, text="Узнать характеристку печи", command=query5)
query5_button.pack(side='bottom')

query6_button = tk.Button(window, width=1000, height=1, text="Что это за товар", command=query6)
query6_button.pack(side='bottom')

def display_table_query(result, table):

    rows = result
    table_window = tk.Toplevel(window)
    table_window.title(table[0])
    column_names = table
    treeview = ttk.Treeview(table_window)

    treeview["columns"] = column_names
    treeview.column("#0", width=0, stretch="no")
    for col in column_names:
        treeview.heading(col, text=col)
        treeview.column(col, anchor="center", width=100)

    for row in rows:
        values = [i for i in row]
        treeview.insert(parent='', index='end', text='', values=values)

        treeview.pack(fill="both",  expand=True)


for table in tables:
    button = tk.Button(window, width=15, height=3, text=table, command=lambda name=table: display_table(name))
    button.pack(expand=1, side='left', anchor='w')

    def display_table(table_name):

        table = Base.metadata.tables["public." + table_name]
        rows = session.query(table).all()
        column_names = table.columns.keys()

        table_window = tk.Toplevel(window)
        table_window.title(table_name)

        treeview = ttk.Treeview(table_window)

        treeview["columns"] = column_names
        treeview.column("#0", width=0, stretch="no")
        for col in column_names:
            treeview.heading(col, text=col)
            treeview.column(col, anchor="center", width=100)

        for row in rows:
            values = [getattr(row, col) for col in column_names]
            treeview.insert("", "end", values=values)

            treeview.pack(fill="both", expand=True)
            
        def edit_row():
                    selected_item = treeview.selection()
                    if not selected_item:
                        messagebox.showinfo("Ошибка", "Укажите какую запись редактировать")
                        return

                    values = treeview.item(selected_item)["values"]

                    edit_window = tk.Toplevel(table_window)
                    edit_window.title("Изменить запись")

                    entry_vars = []
                    for col, value in zip(column_names, values):
                        label = tk.Label(edit_window, text=col)
                        label.grid(row=column_names.index(col), column=0, sticky=tk.W)

                        entry_var = tk.StringVar(value=str(value))
                        entry = tk.Entry(edit_window, textvariable=entry_var)
                        entry.grid(row=column_names.index(col), column=1, sticky=tk.W)

                        entry_vars.append(entry_var)

                    def save_changes():
                            new_values = [var.get() for var in entry_vars]
                            session.query(table).filter_by(**{column_names[i]: values[i] for i in range(len(column_names))}). \
                                update({column_names[i]: new_values[i] for i in range(len(column_names))})
                            session.commit()
                            messagebox.showinfo("Успешно", "Запись отредактирована.")
                            edit_window.destroy()
                            table_window.destroy()
                            display_table(table_name)

                            save_button = tk.Button(edit_window, text="Сохранить", command=save_changes)
                            save_button.grid(row=len(column_names), columnspan=2)

        def add_row():

                    add_window = tk.Toplevel(table_window)
                    add_window.title("Добавить запись")

                    entry_vars = []
                    for col in column_names:
                        label = tk.Label(add_window, text=col)
                        label.grid(row=column_names.index(col), column=0, sticky=tk.W)

                        entry_var = tk.StringVar()
                        entry = tk.Entry(add_window, textvariable=entry_var)
                        entry.grid(row=column_names.index(col), column=1, sticky=tk.W)

                        entry_vars.append(entry_var)


                    def save_row():
                        new_values = [var.get() for var in entry_vars]

                        new_row = table.insert().values({column_names[i]: new_values[i] for i in range(len(column_names))})
                        session.execute(new_row)
                        session.commit()

                        messagebox.showinfo("Успешно", "Строка добавленна успешно")
                        add_window.destroy()
                        table_window.destroy()
                        display_table(table_name)

                    save_button = tk.Button(add_window, text="Сохранить", command=save_row)
                    save_button.grid(row=len(column_names), columnspan=2)

        def delete_row():
                    selected_item = treeview.selection()
                    if not selected_item:
                        messagebox.showinfo("Ошибка", "Выберете строку для удаления")
                        return

                    confirmation = messagebox.askyesno("Подтвердите удаление", "Вы уверенны, что хотите удалить строку?")
                    if confirmation:
                        values = treeview.item(selected_item)["values"]

                        session.query(table).filter_by(
                            **{column_names[i]: values[i] for i in range(len(column_names))}).delete()
                        session.commit()

                        messagebox.showinfo("Успешно", "Строка удалена успешно")
                        table_window.destroy()
                        display_table(table_name)

        add_button = tk.Button(table_window, width=30, text="Добавить запись", command=add_row)
        add_button.pack(side='right')

        delete_button = tk.Button(table_window, width=30, text="Удалить запись", command=delete_row)
        delete_button.pack(side='right')

        edit_button = tk.Button(table_window, width=30, text="Изменить запись", command=edit_row)
        edit_button.pack(side='right')


window.mainloop()

session.close()