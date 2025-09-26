import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import datetime

# Конфигурация подключения к БД
DB_CONFIG = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "1111",
    "port": 5432
}

current_partner_name = None

# ========================
# Функции для работы с БД
# ========================

def fetch_partners():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type_partner, name_partner, director, mail_partner, phone_partner, ur_adress_partner, inn, rating
            FROM partners_import
            ORDER BY name_partner;
        """)
        partners = cursor.fetchall()
        cursor.close()
        conn.close()
        return partners
    except Exception as e:
        messagebox.showerror("Ошибка БД", f"Не удалось загрузить партнёров:\n{e}")
        return []

def fetch_partner_by_name(name):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type_partner, name_partner, director, mail_partner, phone_partner, ur_adress_partner, inn, rating
            FROM partners_import
            WHERE name_partner = %s;
        """, (name,))
        partner = cursor.fetchone()
        cursor.close()
        conn.close()
        return partner
    except Exception as e:
        messagebox.showerror("Ошибка БД", f"Не удалось загрузить данные:\n{e}")
        return None

def save_partner(name, type_partner, rating, address, director, phone, email, inn, partner_name=None):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        if partner_name is None:
            cursor.execute("""
                INSERT INTO partners_import (
                    type_partner, name_partner, director, mail_partner, phone_partner,
                    ur_adress_partner, inn, rating
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (type_partner, name, director, email, phone, address, inn, rating))
        else:
            cursor.execute("""
                UPDATE partners_import
                SET type_partner = %s, name_partner = %s, director = %s, mail_partner = %s,
                    phone_partner = %s, ur_adress_partner = %s, inn = %s, rating = %s
                WHERE name_partner = %s
            """, (type_partner, name, director, email, phone, address, inn, rating, partner_name))

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить данные:\n{e}")
        return False

def validate_rating(rating_str):
    try:
        rating = int(rating_str)
        if rating < 0:
            raise ValueError
        return rating, None
    except:
        return None, "Рейтинг должен быть целым неотрицательным числом"

def fetch_sales_history(partner_name):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product, kolvo_product, date_sale
            FROM partner_products_import
            WHERE name_partner = %s
            ORDER BY date_sale DESC;
        """, (partner_name,))
        history = cursor.fetchall()
        cursor.close()
        conn.close()
        return history
    except Exception as e:
        messagebox.showerror("Ошибка БД", f"Не удалось загрузить историю:\n{e}")
        return []

# ========================
# Форма добавления/редактирования партнёра
# ========================

def show_partner_form(root, refresh_callback, partner_name=None):
    global current_partner_name
    current_partner_name = partner_name

    form_window = tk.Toplevel(root)
    form_window.title("Добавить партнёра" if partner_name is None else "Редактировать партнёра")
    form_window.geometry("500x600")
    form_window.grab_set()

    title = "Добавление нового партнёра" if partner_name is None else "Редактирование партнёра"
    tk.Label(form_window, text=title, font=("Arial", 14, "bold")).pack(pady=10)

    fields_frame = tk.Frame(form_window, padx=20, pady=10)
    fields_frame.pack(fill="both", expand=True)

    tk.Label(fields_frame, text="Наименование*:", anchor="w").pack(fill="x")
    name_entry = tk.Entry(fields_frame)
    name_entry.pack(fill="x", pady=(0, 10))

    tk.Label(fields_frame, text="Тип партнёра*:", anchor="w").pack(fill="x")
    type_var = tk.StringVar()
    type_combo = ttk.Combobox(fields_frame, textvariable=type_var, state="readonly")
    type_combo['values'] = ["Поставщик", "Дистрибьютор", "Розничный магазин", "Оптовик"]
    type_combo.pack(fill="x", pady=(0, 10))

    tk.Label(fields_frame, text="Рейтинг* (целое неотрицательное число):", anchor="w").pack(fill="x")
    rating_entry = tk.Entry(fields_frame)
    rating_entry.pack(fill="x", pady=(0, 10))

    tk.Label(fields_frame, text="Адрес:", anchor="w").pack(fill="x")
    address_entry = tk.Entry(fields_frame)
    address_entry.pack(fill="x", pady=(0, 10))

    tk.Label(fields_frame, text="ФИО директора:", anchor="w").pack(fill="x")
    director_entry = tk.Entry(fields_frame)
    director_entry.pack(fill="x", pady=(0, 10))

    tk.Label(fields_frame, text="Телефон:", anchor="w").pack(fill="x")
    phone_entry = tk.Entry(fields_frame)
    phone_entry.pack(fill="x", pady=(0, 10))

    tk.Label(fields_frame, text="Email:", anchor="w").pack(fill="x")
    email_entry = tk.Entry(fields_frame)
    email_entry.pack(fill="x", pady=(0, 10))

    tk.Label(fields_frame, text="ИНН:", anchor="w").pack(fill="x")
    inn_entry = tk.Entry(fields_frame)
    inn_entry.pack(fill="x", pady=(0, 10))

    if partner_name is not None:
        partner_data = fetch_partner_by_name(partner_name)
        if partner_data:
            type_var.set(partner_data[0])
            name_entry.insert(0, partner_data[1])
            director_entry.insert(0, partner_data[2])
            email_entry.insert(0, partner_data[3])
            phone_entry.insert(0, partner_data[4])
            address_entry.insert(0, partner_data[5])
            inn_entry.insert(0, partner_data[6])
            rating_entry.insert(0, partner_data[7] or 0)

    def on_save():
        name = name_entry.get().strip()
        type_partner = type_var.get().strip()
        rating_str = rating_entry.get().strip()
        address = address_entry.get().strip()
        director = director_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        inn = inn_entry.get().strip()

        if not name:
            messagebox.showwarning("Предупреждение", "Поле 'Наименование' обязательно.")
            return
        if not type_partner:
            messagebox.showwarning("Предупреждение", "Поле 'Тип партнёра' обязательно.")
            return

        rating, error = validate_rating(rating_str)
        if error:
            messagebox.showerror("Ошибка ввода", error)
            return

        action = "добавить нового партнёра" if partner_name is None else "сохранить изменения"
        confirm = messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите {action}?")
        if not confirm:
            return

        if save_partner(name, type_partner, rating, address, director, phone, email, inn, partner_name):
            messagebox.showinfo("Успех", "Данные успешно сохранены!")
            form_window.destroy()
            refresh_callback()

    btn_frame = tk.Frame(form_window)
    btn_frame.pack(pady=20)
    tk.Button(btn_frame, text="Сохранить", command=on_save, bg="lightgreen", width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Назад", command=form_window.destroy, bg="lightgray", width=12).pack(side="left", padx=5)


# ========================
# Основное приложение с вкладками
# ========================

def create_main_app():
    root = tk.Tk()
    root.title("Система управления партнёрами")
    root.geometry("950x650")

    # Создаём вкладки
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # Вкладка 1: Партнёры
    partners_tab = ttk.Frame(notebook)
    notebook.add(partners_tab, text="Управление партнёрами")

    # Заголовок
    tk.Label(partners_tab, text="Список партнёров", font=("Arial", 16, "bold")).pack(pady=10)

    # Кнопка добавления
    top_frame = tk.Frame(partners_tab)
    top_frame.pack(fill="x", padx=20, pady=5)
    tk.Button(top_frame, text="➕ Добавить партнёра", command=lambda: show_partner_form(root, refresh_partners_list), bg="lightblue").pack(side="right")

    # Область прокрутки
    canvas = tk.Canvas(partners_tab)
    scrollbar = ttk.Scrollbar(partners_tab, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=10)
    scrollbar.pack(side="right", fill="y")

    def show_sales_history_window(partner_name):  # ← только partner_name
        history = fetch_sales_history(partner_name)
        if not history:
            messagebox.showinfo("История продаж", f"Нет данных по продажам для партнёра '{partner_name}'.")
            return

        win = tk.Toplevel(root)  # ← root доступен без передачи!
        win.title(f"История продаж: {partner_name}")
        win.geometry("600x500")
        win.grab_set()

        tk.Label(win, text=f"История продаж партнёра: {partner_name}", font=("Arial", 14, "bold")).pack(pady=10)

        tree = ttk.Treeview(win, columns=("product", "quantity", "date"), show="headings", height=15)
        tree.heading("product", text="Продукция")
        tree.heading("quantity", text="Количество")
        tree.heading("date", text="Дата продажи")

        tree.column("product", width=250)
        tree.column("quantity", width=100, anchor="center")
        tree.column("date", width=150, anchor="center")

        tree.pack(fill="both", expand=True, padx=20, pady=10)

        for row in history:
            product, qty, date_str = row
            date_formatted = date_str.strftime("%d.%m.%Y") if isinstance(date_str, datetime.date) else str(date_str)
            tree.insert("", "end", values=(product, qty, date_formatted))

        tk.Button(win, text="Закрыть", command=win.destroy, bg="lightgray", width=15).pack(pady=10)

    def refresh_partners_list():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        partners = fetch_partners()
        if not partners:
            tk.Label(scrollable_frame, text="Нет данных", font=("Arial", 12)).pack(pady=20)
            return

        for partner in partners:
            type_p, name, director, email, phone, address, inn, rating = partner

            card = tk.Frame(scrollable_frame, relief="ridge", bd=1, padx=10, pady=10)
            card.pack(fill="x", pady=5)

            left = tk.Frame(card)
            left.pack(side="left", fill="x", expand=True)

            tk.Label(left, text=f"{type_p} | {name}", font=("Arial", 11, "bold")).pack(anchor="w")
            tk.Label(left, text=f"Директор: {director or '—'}").pack(anchor="w")
            tk.Label(left, text=f"Телефон: {phone or '—'}").pack(anchor="w")
            tk.Label(left, text=f"Email: {email or '—'}").pack(anchor="w")
            tk.Label(left, text=f"Адрес: {address or '—'}").pack(anchor="w")
            tk.Label(left, text=f"ИНН: {inn or '—'}").pack(anchor="w")
            tk.Label(left, text=f"Рейтинг: {rating or 0}").pack(anchor="w")

            btn_frame = tk.Frame(card)
            btn_frame.pack(side="right", padx=10)
            tk.Button(btn_frame, text="✎ Редактировать", command=lambda n=name: show_partner_form(root, refresh_partners_list, n)).pack(pady=2)


    refresh_partners_list()

    # ========================
    # Вкладка 2: История продаж + Расчёт материала
    # ========================
    analytics_tab = ttk.Frame(notebook)
    notebook.add(analytics_tab, text="Аналитика и расчёты")

    # Выбор партнёра
    tk.Label(analytics_tab, text="Выберите партнёра для просмотра истории продаж:", font=("Arial", 12)).pack(pady=10)

    partner_var = tk.StringVar()
    partner_combo = ttk.Combobox(analytics_tab, textvariable=partner_var, state="readonly", width=50)
    partner_combo.pack(pady=5)

    # Заполняем выпадающий список
    partners = fetch_partners()
    partner_names = [p[1] for p in partners]  # name_partner — 2-й элемент
    partner_combo['values'] = partner_names

    # Кнопка "Показать историю"
    tk.Button(analytics_tab, text="Показать историю продаж", command=lambda: load_sales_history(partner_var.get()), bg="lightgreen").pack(pady=10)

    # Таблица истории
    tree_frame = tk.Frame(analytics_tab)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

    tree = ttk.Treeview(tree_frame, columns=("product", "quantity", "date"), show="headings")
    tree.heading("product", text="Продукция")
    tree.heading("quantity", text="Количество")
    tree.heading("date", text="Дата продажи")

    tree.column("product", width=250)
    tree.column("quantity", width=100, anchor="center")
    tree.column("date", width=150, anchor="center")

    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    # Функция загрузки истории
    def load_sales_history(partner_name):
        if not partner_name:
            messagebox.showwarning("Внимание", "Выберите партнёра")
            return

        # Очищаем таблицу
        for item in tree.get_children():
            tree.delete(item)

        history = fetch_sales_history(partner_name)
        for row in history:
            product, qty, date_str = row
            date_formatted = date_str.strftime("%d.%m.%Y") if isinstance(date_str, datetime.date) else str(date_str)
            tree.insert("", "end", values=(product, qty, date_formatted))

    # ========================
    # Расчёт материала
    # ========================
    tk.Label(analytics_tab, text="Расчёт необходимого материала", font=("Arial", 14, "bold")).pack(pady=(30,10))

    calc_frame = tk.Frame(analytics_tab, padx=20, pady=10, relief="groove", bd=1)
    calc_frame.pack(fill="x", padx=20, pady=10)

    # Поля ввода
    tk.Label(calc_frame, text="ID типа продукции:").grid(row=0, column=0, sticky="w", pady=5)
    product_id_entry = tk.Entry(calc_frame, width=10)
    product_id_entry.grid(row=0, column=1, sticky="w", padx=10)

    tk.Label(calc_frame, text="ID типа материала:").grid(row=1, column=0, sticky="w", pady=5)
    material_id_entry = tk.Entry(calc_frame, width=10)
    material_id_entry.grid(row=1, column=1, sticky="w", padx=10)

    tk.Label(calc_frame, text="Количество продукции:").grid(row=2, column=0, sticky="w", pady=5)
    count_entry = tk.Entry(calc_frame, width=10)
    count_entry.grid(row=2, column=1, sticky="w", padx=10)

    tk.Label(calc_frame, text="Параметр 1 (вещ.):").grid(row=3, column=0, sticky="w", pady=5)
    param1_entry = tk.Entry(calc_frame, width=10)
    param1_entry.grid(row=3, column=1, sticky="w", padx=10)

    tk.Label(calc_frame, text="Параметр 2 (вещ.):").grid(row=4, column=0, sticky="w", pady=5)
    param2_entry = tk.Entry(calc_frame, width=10)
    param2_entry.grid(row=4, column=1, sticky="w", padx=10)

    result_label = tk.Label(calc_frame, text="Результат: —", font=("Arial", 10, "bold"))
    result_label.grid(row=5, column=0, columnspan=2, pady=10)

    def calculate_material():
        try:
            p_id = int(product_id_entry.get())
            m_id = int(material_id_entry.get())
            count = int(count_entry.get())
            p1 = float(param1_entry.get())
            p2 = float(param2_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте правильность ввода чисел")
            return

        # Метод расчёта (можно вынести в отдельный модуль)
        PRODUCT_COEFFS = {1: 1.2, 2: 1.5, 3: 0.8}
        DEFECT_RATES = {1: 0.05, 2: 0.10, 3: 0.02}

        if p1 <= 0 or p2 <= 0 or count <= 0:
            result_label.config(text="Результат: -1 (ошибка параметров)")
            return

        if p_id not in PRODUCT_COEFFS or m_id not in DEFECT_RATES:
            result_label.config(text="Результат: -1 (неверный ID)")
            return

        coeff = PRODUCT_COEFFS[p_id]
        defect = DEFECT_RATES[m_id]

        material_per_unit = p1 * p2 * coeff
        total = material_per_unit * count
        total_with_defect = total / (1 - defect)

        import math
        result = math.ceil(total_with_defect)
        result_label.config(text=f"Результат: {result}")

    tk.Button(calc_frame, text="Рассчитать", command=calculate_material, bg="lightblue").grid(row=6, column=0, columnspan=2, pady=10)

    # ========================
    # Запуск
    # ========================
    root.mainloop()

# ========================
# Запуск приложения
# ========================
if __name__ == "__main__":
    create_main_app()