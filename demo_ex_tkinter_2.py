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

# Глобальная переменная для хранения выбранного партнёра
current_partner_name = None  # Имя партнёра для редактирования


def fetch_partners():
    """Загружает список партнёров из БД."""
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
        messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить партнёров:\n{e}")
        return []

def fetch_partner_by_name(name):
    """Загружает данные партнёра по имени."""
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
        messagebox.showerror("Ошибка базы данных", f"Не удалось загрузить данные партнёра:\n{e}")
        return None

def save_partner(name, type_partner, rating, address, director, phone, email, inn, partner_name=None):
    """Сохраняет нового партнёра или обновляет существующего."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        if partner_name is None:
            # Добавление
            cursor.execute("""
                INSERT INTO partners_import (
                    type_partner, name_partner, director, mail_partner, phone_partner,
                    ur_adress_partner, inn, rating
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (type_partner, name, director, email, phone, address, inn, rating))
        else:
            # Редактирование
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
    """Проверяет, что рейтинг — неотрицательное целое число."""
    try:
        rating = int(rating_str)
        if rating < 0:
            raise ValueError("Рейтинг не может быть отрицательным")
        return rating, None
    except ValueError as e:
        return None, "Рейтинг должен быть целым неотрицательным числом"


def show_partner_form(root, refresh_callback, partner_name=None):
    """Открывает форму добавления/редактирования партнёра."""

    global current_partner_name
    current_partner_name = partner_name

    form_window = tk.Toplevel(root)
    form_window.title("Добавить партнёра" if partner_name is None else "Редактировать партнёра")
    form_window.geometry("500x600")
    form_window.grab_set()  # Модальное окно

    title = "Добавление нового партнёра" if partner_name is None else "Редактирование партнёра"
    tk.Label(form_window, text=title, font=("Arial", 14, "bold")).pack(pady=10)

    fields_frame = tk.Frame(form_window, padx=20, pady=10)
    fields_frame.pack(fill="both", expand=True)

    # Наименование
    tk.Label(fields_frame, text="Наименование*:", anchor="w").pack(fill="x")
    name_entry = tk.Entry(fields_frame)
    name_entry.pack(fill="x", pady=(0, 10))

    # Тип партнёра
    tk.Label(fields_frame, text="Тип партнёра*:", anchor="w").pack(fill="x")
    type_var = tk.StringVar()
    type_combo = ttk.Combobox(fields_frame, textvariable=type_var, state="readonly")
    type_combo['values'] = ["Поставщик", "Дистрибьютор", "Розничный магазин", "Оптовик"]
    type_combo.pack(fill="x", pady=(0, 10))

    # Рейтинг
    tk.Label(fields_frame, text="Рейтинг* (целое неотрицательное число):", anchor="w").pack(fill="x")
    rating_entry = tk.Entry(fields_frame)
    rating_entry.pack(fill="x", pady=(0, 10))

    # Адрес
    tk.Label(fields_frame, text="Адрес:", anchor="w").pack(fill="x")
    address_entry = tk.Entry(fields_frame)
    address_entry.pack(fill="x", pady=(0, 10))

    # ФИО директора
    tk.Label(fields_frame, text="ФИО директора:", anchor="w").pack(fill="x")
    director_entry = tk.Entry(fields_frame)
    director_entry.pack(fill="x", pady=(0, 10))

    # Телефон
    tk.Label(fields_frame, text="Телефон:", anchor="w").pack(fill="x")
    phone_entry = tk.Entry(fields_frame)
    phone_entry.pack(fill="x", pady=(0, 10))

    # Email
    tk.Label(fields_frame, text="Email:", anchor="w").pack(fill="x")
    email_entry = tk.Entry(fields_frame)
    email_entry.pack(fill="x", pady=(0, 10))

    # INN
    tk.Label(fields_frame, text="ИНН:", anchor="w").pack(fill="x")
    inn_entry = tk.Entry(fields_frame)
    inn_entry.pack(fill="x", pady=(0, 10))

    # Заполнение полей при редактировании
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

        # Валидация обязательных полей
        if not name:
            messagebox.showwarning("Предупреждение", "Поле 'Наименование' обязательно для заполнения.")
            return
        if not type_partner:
            messagebox.showwarning("Предупреждение", "Поле 'Тип партнёра' обязательно для заполнения.")
            return

        # Валидация рейтинга
        rating, error = validate_rating(rating_str)
        if error:
            messagebox.showerror("Ошибка ввода", error)
            return

        action = "добавить нового партнёра" if partner_name is None else "сохранить изменения"
        confirm = messagebox.askyesno(
            "Подтверждение",
            f"Вы уверены, что хотите {action}?",
            icon="question"
        )
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


def create_main_window():
    """Создаёт главное окно со списком партнёров."""

    root = tk.Tk()
    root.title("Управление партнёрами")
    root.geometry("900x600")

    def refresh_partners_list():
        # 1. Очищаем интерфейс
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # 2. Загружаем АКТУАЛЬНЫЕ данные из БД (включая новых партнёров!)
        partners = fetch_partners()

        # 3. Если данных нет — показываем сообщение
        if not partners:
            tk.Label(scrollable_frame, text="Нет данных", font=("Arial", 12)).pack(pady=20)
            return

        # 4. Отображаем всех партнёров
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

            # Кнопки
            btn_frame = tk.Frame(card)
            btn_frame.pack(side="right", padx=10)

            tk.Button(btn_frame, text="✎ Редактировать",
                      command=lambda n=name: show_partner_form(root, refresh_partners_list, n)).pack(pady=2)
            # Если добавили историю продаж — раскомментируйте:

    # Верхняя панель
    top_frame = tk.Frame(root, pady=10)
    top_frame.pack(fill="x")

    tk.Label(top_frame, text="Список партнёров", font=("Arial", 16, "bold")).pack(side="left", padx=20)
    tk.Button(top_frame, text="➕ Добавить партнёра", command=lambda: show_partner_form(root, refresh_partners_list), bg="lightblue").pack(side="right", padx=20)

    # Область прокрутки
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    refresh_partners_list()
    root.mainloop()


if __name__ == "__main__":
    create_main_window()