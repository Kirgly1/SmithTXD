import random
import sqlite3
import tkinter
from tkinter import messagebox, ttk
import tkinter as tk
import datetime
import time

with sqlite3.connect('blacksmith.db') as conn:
    cursor = conn.cursor()

# Создаем таблицу Blacksmith
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Blacksmith (
        Human_ID INTEGER PRIMARY KEY,
        name TEXT,
        surname TEXT,
        birthdate DATE,
        work_experience INTEGER
    )
''')

# Создаем таблицу Provider
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Provider (
        Human_ID INTEGER PRIMARY KEY,
        Material_ID INTEGER,
        name TEXT,
        surname TEXT,
        work_experience INTEGER,
        price_per_kg INTEGER,
        FOREIGN KEY (Human_ID) REFERENCES Blacksmith(Human_ID),
        FOREIGN KEY (Material_ID) REFERENCES RawMaterial(Material_ID)
    )
''')

# Создаем таблицу RawMaterial
cursor.execute('''
    CREATE TABLE IF NOT EXISTS RawMaterial (
        Material_ID INTEGER PRIMARY KEY,
        Provider_ID INTEGER,
        material TEXT,
        heat_capacity INTEGER,
        price INTEGER,
        FOREIGN KEY (Provider_ID) REFERENCES Provider(Human_ID)
    )
''')

# Создаем таблицу Anvil
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Anvil (
        Human_ID INTEGER PRIMARY KEY,
        genus TEXT,
        durability INTEGER,
        FOREIGN KEY (Human_ID) REFERENCES Blacksmith(Human_ID)
    )
''')

# Создаем таблицу Product
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Product (
        Human_ID INTEGER PRIMARY KEY,
        type TEXT,
        size INTEGER,
        appointment TEXT,
        weight INTEGER,
        endurance INTEGER,
        FOREIGN KEY (Human_ID) REFERENCES Blacksmith(Human_ID)
    )
''')

# Создаем таблицу Smelter
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Smelter (
        Material_ID INTEGER PRIMARY KEY,
        Product_ID INTEGER,
        dimension TEXT,
        fabric TEXT,
        time_last INTEGER,
        maximum_temperature INTEGER,
        FOREIGN KEY (Material_ID) REFERENCES RawMaterial(Material_ID),
        FOREIGN KEY (Product_ID) REFERENCES Product(Human_ID)
    )
''')

conn.commit()

conn = sqlite3.connect('blacksmith.db')
cursor = conn.cursor()


class DatabaseApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Database App")
        self.master.geometry("1000x800")

        self.conn = sqlite3.connect('blacksmith.db')
        self.cursor = self.conn.cursor()

        # self.populate_tables()
        self.create_widgets()

        # Завершение программы
        master.protocol("WM_DELETE_WINDOW", self.close_connection)

    def close_connection(self):
        # Закрытие соединения при выходе из программы
        self.conn.close()
        self.master.destroy()

    def populate_tables(self):
        # Проверяем наличие данных в таблицах,
        existing_data = self.cursor.execute('SELECT COUNT(*) FROM Blacksmith').fetchone()[0]

        if existing_data == 0:
            # Заполняем таблицу Blacksmith
            for _ in range(10):
                name = f"Name{_}"
                surname = f"Surname{_}"
                birthdate = datetime.datetime(2000, 1, 1)
                work_experience = random.randint(1, 10)
                self.cursor.execute('''
                    INSERT INTO Blacksmith (name, surname, birthdate, work_experience)
                    VALUES (?, ?, ?, ?)
                ''', (name, surname, birthdate, work_experience))

        # Заполняем таблицу RawMaterial
        materials = ["Steel", "Iron", "Aluminum", "Copper", "Gold"]
        used_provider_ids = set()
        for provider_id in range(1, 11):
            while provider_id in used_provider_ids:
                provider_id = random.randint(1, 50)

            material = random.choice(materials)
            heat_capacity = random.randint(200, 1000)
            price = random.randint(100, 500)
            used_provider_ids.add(provider_id)

            self.cursor.execute('''
                INSERT INTO RawMaterial (Provider_ID, material, heat_capacity, price)
                VALUES (?, ?, ?, ?)
            ''', (provider_id, material, heat_capacity, price))

        # Заполняем таблицу Provider
        for _ in range(10):
            name = f"ProviderName{_}"
            surname = f"ProviderSurname{_}"
            work_experience = random.randint(1, 10)
            price_per_kg = random.randint(50, 200)

            existing_human_ids = [row[0] for row in self.cursor.execute('SELECT Human_ID FROM Provider').fetchall()]
            human_id = random.randint(1, 50)
            while human_id in existing_human_ids:
                human_id = random.randint(1, 50)

            material_id = random.randint(1, 50)

            self.cursor.execute('''
                INSERT INTO Provider (Human_ID, Material_ID, name, surname, work_experience, price_per_kg)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (human_id, material_id, name, surname, work_experience, price_per_kg))

        # Заполняем таблицу Anvil
        for _ in range(10):
            genus = f"Genus{_}"
            durability = random.randint(50, 200)
            existing_human_ids = [row[0] for row in self.cursor.execute('SELECT Human_ID FROM Anvil').fetchall()]

            human_id = random.randint(1, 50)
            while human_id in existing_human_ids:
                human_id = random.randint(1, 50)

            self.cursor.execute('''
                INSERT INTO Anvil (Human_ID, genus, durability)
                VALUES (?, ?, ?)
            ''', (human_id, genus, durability))

        # Заполняем таблицу Product
        for _ in range(10):
            type_ = f"Type{_}"
            size = random.randint(1, 10)
            appointment = f"Appointment{_}"
            weight = random.randint(5, 50)
            endurance = random.randint(1, 10)

            existing_human_ids = [row[0] for row in self.cursor.execute('SELECT Human_ID FROM Product').fetchall()]
            human_id = random.randint(1, 50)
            while human_id in existing_human_ids:
                human_id = random.randint(1, 50)

            self.cursor.execute('''
                INSERT INTO Product (Human_ID, type, size, appointment, weight, endurance)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (human_id, type_, size, appointment, weight, endurance))

        # Заполняем таблицу Smelter
        for product_id in range(1, 11):
            dimension = f"Dimension{product_id}"
            fabric = f"Fabric{product_id}"
            time_last = random.randint(1, 10)
            maximum_temperature = random.randint(500, 2000)
            time.sleep(0.1)
            self.cursor.execute('''
                INSERT INTO Smelter (Product_ID, dimension, fabric, time_last, maximum_temperature)
                VALUES (?, ?, ?, ?, ?)
            ''', (product_id, dimension, fabric, time_last, maximum_temperature))

        self.conn.commit()

    def create_widgets(self):
        self.treeview = ttk.Treeview(self.master)
        self.treeview.pack(expand="yes", fill="both")

        self.custom_query_button = tk.Button(self.master, text="Поиск по именам и фамилиям кузнецов, "
                                                               "типам, размерам и весу продуктов, "
                                                               "а также виды и прочность наковален",
                                             command=self.execute_custom_query_custom)
        self.custom_query_button.pack()

        self.new_query_button = tk.Button(self.master, text="Определить поставщика, работающего 5 лет с "
                                                            "ценой за килограмм материала в 140",
                                          command=self.execute_new_query)
        self.new_query_button.pack()

        # Кнопки для открытия каждой таблицы
        table_buttons = tk.Frame(self.master)
        table_buttons.pack()

        tables = ["Blacksmith", "Provider", "RawMaterial", "Anvil", "Product", "Smelter"]
        for table_name in tables:
            button = tk.Button(table_buttons, text=f"Show {table_name}",
                               command=lambda name=table_name: self.display_table(name))
            button.pack(side="left")

    def execute_new_query(self):

        query_text = "SELECT * FROM Provider WHERE work_experience = '5' AND price_per_kg = 140"

        try:
            # Результаты запроса
            result = self.cursor.execute(query_text).fetchall()

            result_window = tk.Toplevel(self.master)
            result_window.title("New Query Results")

            result_window.geometry("400x200")

            result_listbox = tk.Listbox(result_window, selectmode=tk.SINGLE)
            result_listbox.pack(expand=True, fill="both")

            for i, row in enumerate(result, 1):
                result_listbox.insert(tk.END, f"{i}: {row}")

        except Exception as e:
            messagebox.showerror("Error", f"Query execution error: {str(e)}")

    def execute_custom_query_custom(self):

        query_text = """
        SELECT Blacksmith.name AS BlacksmithName, Blacksmith.surname AS BlacksmithSurname,
               Product.type AS ProductType, Product.size AS ProductSize, Product.weight AS ProductWeight,
               Anvil.genus AS AnvilGenus, Anvil.durability AS AnvilDurability
        FROM Blacksmith
        JOIN Product ON Blacksmith.Human_ID = Product.Human_ID
        JOIN Anvil ON Blacksmith.Human_ID = Anvil.Human_ID
        WHERE Blacksmith.work_experience > 5 AND Product.weight > 10 AND Anvil.durability > 100
        """

        try:

            result = self.cursor.execute(query_text).fetchall()

            result_window = tk.Toplevel(self.master)
            result_window.title("Custom Query Results")

            result_window.geometry("400x200")

            result_listbox = tk.Listbox(result_window, selectmode=tk.SINGLE)
            result_listbox.pack(expand=True, fill="both")

            for i, row in enumerate(result, 1):
                result_listbox.insert(tk.END, f"{i}: {row}")

        except Exception as e:
            messagebox.showerror("Error", f"Query execution error: {str(e)}")

        for item in self.treeview.get_children():
            self.treeview.delete(item)

        columns = [desc[0] for desc in self.cursor.description]
        self.treeview["columns"] = columns
        self.treeview["show"] = "headings"  # Это позволяет скрыть пустую колонку слева

        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, anchor=tk.CENTER, width=100)  # Задайте желаемую ширину столбца

        for i, row in enumerate(rows):
            self.treeview.insert("", i, text=row[0], values=row[1:])

    def display_table(self, table_name):
        rows = self.cursor.execute(f'SELECT * FROM {table_name}').fetchall()

        self.cursor.execute(f'PRAGMA table_info({table_name})')
        column_names = [column[1] for column in self.cursor.fetchall()]

        table_window = tk.Toplevel(self.master)
        table_window.title(table_name)

        treeview = ttk.Treeview(table_window)

        treeview["columns"] = column_names
        treeview.column("#0", width=0, stretch="no")
        for col in column_names:
            treeview.heading(col, text=col)
            treeview.column(col, anchor="center", width=100)

        for row in rows:
            values = [str(i) if i is not None else "" for i in row]
            treeview.insert("", "end", values=values)

        treeview.pack(fill="both", expand=True)


root = tk.Tk()
app = DatabaseApp(root)
root.mainloop()
