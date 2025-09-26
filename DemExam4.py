from DemExam3 import window_edit
import psycopg2


def view_partner(name=None):
    if name:
        conn = psycopg2.connect(dbname="postgres",
                                user="postgres",
                                password="1111",
                                host="localhost",
                                port="5432")
        print("Подключение установлено")

        cursor = conn.cursor()
        cursor.execute(f"""Select type, name, director,email, phone_num, adres, rating FROM partners WHERE name = '{name}' ORDER BY name """)
        a = cursor.fetchall()[0]
        print(a)
        conn.close()
        window_edit(a)
    else:
        window_edit()


if __name__ == "__main__":
    view_partner("Паркет 29")