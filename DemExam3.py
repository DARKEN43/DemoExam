import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showwarning, showerror
import psycopg2
from psycopg2 import Error


def window_edit(a=None):
    root = tk.Tk()
    root.title("Редактирование партнера")
    root.geometry("700x540")
    root.iconbitmap(default="Мастер пол.ico")
    root.resizable(width=False, height=False)
    font_text = "Segoe UI"
    colors = ["#FFFFFF", "#F4E8D3", "#67BA80"]
    root.config(bg=colors[0])


    style = ttk.Style()
    style.theme_use('default')

    style.configure("TCombobox",
                    fieldbackground=colors[1],  # Цвет фона выпадающего списка
                    background=colors[1],  # Цвет фона поля
                    )

    frame = tk.Frame(root, background="#e3be7d")
    frame.grid(row=0, column=0, padx=10, pady=10)

    type_lbl = tk.Label(frame, text="Тип партнера", font=(font_text, 20, "bold"), background="#e3be7d")
    type_lbl.grid(row=0, column=0, padx=20)
    types = ["ЗАО", "ООО", "ПАО", "ОАО"]
    type_entry = ttk.Combobox(frame, font=(font_text, 20), width=29, values=types,  state="readonly")
    type_entry.grid(row=0, column=1, pady=20)

    name_lbl = tk.Label(frame, text="Имя партнера", font=(font_text, 20, "bold"), background="#e3be7d")
    name_lbl.grid(row=1, column=0)
    name_entry = tk.Entry(frame, font=(font_text, 20), width=30, background=colors[1])
    name_entry.grid(row=1, column=1)

    name_director_lbl = tk.Label(frame, text="Директор", font=(font_text, 20, "bold"), background="#e3be7d")
    name_director_lbl.grid(row=2, column=0)
    name_director_entry = tk.Entry(frame, font=(font_text, 20), width=30, background=colors[1])

    name_director_entry.grid(row=2, column=1, pady=20)

    phone_num_lbl = tk.Label(frame, text="Телефон", font=(font_text, 20, "bold"), background="#e3be7d")
    phone_num_lbl.grid(row=4, column=0)
    phone_num_entry = tk.Entry(frame, font=(font_text, 20), width=30, background=colors[1])
    phone_num_entry.grid(row=3, column=1)

    email_lbl = tk.Label(frame, text="email", font=(font_text, 20, "bold"), background="#e3be7d")
    email_lbl.grid(row=3, column=0)
    email_entry = tk.Entry(frame, font=(font_text, 20), width=30, background=colors[1])
    email_entry.grid(row=4, column=1, pady=20)

    address_lbl = tk.Label(frame, text="Адрес", font=(font_text, 20, "bold"), background="#e3be7d")
    address_lbl.grid(row=5, column=0)
    address_entry = tk.Entry(frame, font=(font_text, 20), width=30, background=colors[1])
    address_entry.grid(row=5, column=1)

    rating_lbl = tk.Label(frame, text="Рейтинг", font=(font_text, 20, "bold"), background="#e3be7d")
    rating_lbl.grid(row=6, column=0)
    rating_entry = tk.Entry(frame, font=(font_text, 20), width=30, background=colors[1])
    rating_entry.grid(row=6, column=1, pady=20)


    def save_btn():
        try:
            b = (type_entry.get(), name_entry.get(), name_director_entry.get(), phone_num_entry.get(), email_entry.get(), address_entry.get(), int(rating_entry.get()))
            if b[6] < 0:
                showerror(title="Предупреждение", message="Рейтинг должен быть положительным целым числом")
                return "Отрицательное значение"
        except:
            showerror(title="Предупреждение", message="Рейтинг должен быть положительным целым числом")
            return 1
        if a == b:
            showwarning(title="Предупреждение", message="Данные не были изменены")
        else:
            conn = psycopg2.connect(dbname="postgres",
                                    user="postgres",
                                    password="1111",
                                    host="localhost",
                                    port="5432")
            print("Подключение установлено")

            cursor = conn.cursor()
            if a:
                try:
                    cursor.execute(f"""UPDATE partners SET type = '{b[0]}', name = '{b[1]}', director = '{b[2]}', email = '{b[3]}',
                                            phone_num = '{b[4]}', adres = '{b[5]}', rating = {b[6]} WHERE name = '{a[1]}'""")

                    conn.commit()
                    print("данные сохранены")
                except Error as e:
                    print(f"Transaction failed: {e.pgcode} - {e.pgerror}")
            else:
                try:
                    cursor.execute(
                        f"""INSERT INTO partners (type, name, director, email, phone_num, adres, rating) VALUES ('{b[0]}', '{b[1]}', '{b[2]}', '{b[3]}',
                                            '{b[4]}', '{b[5]}', {b[6]})""")
                    cursor.execute(
                        f"""INSERT INTO partner_products_import (products, name_partner, kolvo, date) VALUES (null, '{b[1]}', 0, null)""")

                    conn.commit()
                    print("данные сохранены")
                except Error as e:
                    print(f"Transaction failed: {e.pgcode} - {e.pgerror}")

    save_button = tk.Button(frame, text="Добавить", font=(font_text, 20, "bold"), background="#e3be7d", command=save_btn)
    save_button.grid(row=7, column=0, columnspan=2)

    if a:
        rating_entry.insert(tk.END, a[6])
        address_entry.insert(tk.END, a[5])
        email_entry.insert(tk.END, a[4])
        phone_num_entry.insert(tk.END, a[3])
        name_director_entry.insert(tk.END, a[2])
        name_entry.insert(tk.END, a[1])
        type_entry.set(a[0])
        save_button.config(text="Сохранить")

    root.mainloop()

if __name__ == "__main__":
    window_edit(('ЗАО', 'База Строитель', 'Иванова Александра Ивановна', 'aleksandraivanova@ml.ru', '493 123 45 67', '652050, Кемеровская область, город Юрга, ул. Лесная, 15', 7))