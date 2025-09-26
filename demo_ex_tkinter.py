import tkinter as tk
from tkinter import ttk
import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "1111",
    "port": 5432
}

def fetch_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                type_partner, 
                name_partner, 
                director, 
                phone_partner, 
                rating 
            FROM partners_import
            ORDER BY name_partner;
        """)
        partners = cursor.fetchall()

        cursor.execute("""
            SELECT 
                name_partner,
                MAX(kolvo_product) AS kolvo_product
            FROM partner_products_import
            GROUP BY name_partner;
        """)
        discounts = cursor.fetchall()

        discount_dict = {row[0]: row[1] for row in discounts}

        cursor.close()
        conn.close()
        return partners, discount_dict

    except Exception as e:
        print("Ошибка подключения к БД:", e)
        return [], {}

def format_rating(rating_str):
    try:
        return int(rating_str)
    except (ValueError, TypeError):
        return 0

def create_gui(partners, discount_dict):
    root = tk.Tk()
    root.title("Партнеры и скидки")
    root.geometry("800x600")

    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)


    title_label = tk.Label(main_frame, text="Список партнеров", font=("Arial", 16, "bold"))
    title_label.pack(pady=(0, 20))

    # Область прокрутки
    canvas = tk.Canvas(main_frame)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for partner in partners:
        type_partner, name_partner, director, phone, rating = partner

        total_sales_raw = discount_dict.get(name_partner, 0)
        try:
            total_sales = int(total_sales_raw) if total_sales_raw is not None else 0
        except (ValueError, TypeError):
            total_sales = 0

        # Рассчитываем скидку по правилам
        if total_sales < 10000:
            discount_text = "0%"
        elif total_sales < 50000:
            discount_text = "5%"
        elif total_sales < 300000:
            discount_text = "10%"
        else:
            discount_text = "15%"

        # Карточка партнёра
        card_frame = tk.Frame(scrollable_frame, relief="solid", bd=1, padx=10, pady=10)
        card_frame.pack(fill="x", pady=5)

        left_frame = tk.Frame(card_frame)
        left_frame.pack(side="left", fill="x", expand=True)

        tk.Label(left_frame, text=f"{type_partner} | {name_partner}", font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Label(left_frame, text=f"Директор: {director}").pack(anchor="w")
        tk.Label(left_frame, text=f"Телефон: {phone}").pack(anchor="w")

        rating_value = format_rating(rating)
        tk.Label(left_frame, text=f"Рейтинг: {rating_value}").pack(anchor="w")
        tk.Label(left_frame, text=f"Продано: {total_sales} ед.").pack(anchor="w")

        # Блок скидки справа
        right_frame = tk.Frame(card_frame)
        right_frame.pack(side="right", padx=(10, 0))

        tk.Label(right_frame, text=discount_text, font=("Arial", 10, "bold"), bg="lightgray", width=10, height=2).pack()

    root.mainloop()

if __name__ == "__main__":
    partners, discount_dict = fetch_data()
    create_gui(partners, discount_dict)