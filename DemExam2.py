import psycopg2

def db():
    conn = psycopg2.connect(dbname="postgres",
                            user="postgres",
                            password="1111",
                            host="localhost",
                            port="5432")
    print("Подключение установлено")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            p.type, 
            p.name, 
            p.director, 
            p.phone_num, 
            p.rating,
            COALESCE(SUM(ppi.kolvo), 0) AS total_kolvo
        FROM partners p
        LEFT JOIN partner_products_import ppi ON p.name = ppi.name_partner
        GROUP BY p.type, p.name, p.director, p.phone_num, p.rating
        ORDER BY p.name
    """)
    rows = cursor.fetchall()

    info = []
    sale = []
    for row in rows:

        if len(row) != 6:
            print(f"Предупреждение: Некорректная строка: {row}")
            continue

        type_, name, director, phone_num, rating, total_kolvo = row

        if rating is None:
            rating = 0
        if director is None:
            director = "Не указан"
        if phone_num is None:
            phone_num = "Нет телефона"

        info.append((type_, name, director, phone_num, rating))

        if total_kolvo < 10000:
            discount = 0
        elif total_kolvo < 50000:
            discount = 5
        elif total_kolvo < 300000:
            discount = 10
        else:
            discount = 15
        sale.append(discount)

    conn.close()
    return info, sale