import psycopg2
from tkinter import *
from tkinter import ttk

def history_story():
    conn = psycopg2.connect(dbname="postgres",
                            user="postgres",
                            password="1111",
                            host="localhost",
                            port="5432")
    print("Подключение установлено")
    cursor = conn.cursor()
    cursor.execute("""Select * FROM partner_products_import WHERE kolvo >0 """)
    a = cursor.fetchall()
    cursor.execute("""Select name FROM partners""")
    b = cursor.fetchall()
    val = []
    for i in range(len(b)):
        val.append(b[i][0])

    root_1 = Tk()
    root_1.title("Продажи")
    root_1.geometry("900x600")

    def combo_filter(event):
        name = filtr.get()
        tree.delete(*tree.get_children())
        cursor.execute(f"""Select * FROM partner_products_import WHERE kolvo >0 and name_partner = '{name}'""")
        c = cursor.fetchall()
        for i in c:
            tree.insert("", END, values=i)

    filtr = ttk.Combobox(root_1, values=val,  state="readonly")
    filtr.bind("<<ComboboxSelected>>", combo_filter)
    filtr.pack()

    columns = ("product", "name_partner", "kolvo", "date")
    tree = ttk.Treeview(root_1, columns=columns, show="headings")
    tree.pack(fill=BOTH, expand=1)
    tree.heading("product", text="Продукт")
    tree.heading("name_partner", text="Партнер")
    tree.heading("kolvo", text="Количество")
    tree.heading("date", text="Дата")


    for partner in a:
        tree.insert("", END, values=partner)

    root_1.mainloop()