import psycopg2

def calculation(type_product, type_material, kolvo, par1,par2):
    try:
        if kolvo > 0 and par1>0 and par2>0:
            conn = psycopg2.connect(dbname="postgres",
                                    user="postgres",
                                    password="1111",
                                    host="localhost",
                                    port="5432")
            cur = conn.cursor()
            cur.execute(f"""Select percent FROM material_type WHERE type_material = '{type_material}'""")
            brak = cur.fetchall()[0][0]
            cur.execute(f"""SELECT k_type_product FROM product_type_import WHERE type_product = '{type_product}'""")
            koaf_type_product = cur.fetchall()[0][0]
            kolvo_1 = par1 * par2 * koaf_type_product
            all_kolvo = kolvo * kolvo_1 + (kolvo_1*kolvo*brak)
            return round(all_kolvo)
        else:
            return -1
    except:
        return -1

a = calculation("Ламинат", "Тип материала 1", 1000, 10, 20)
print(a)