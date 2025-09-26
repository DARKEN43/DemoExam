import tkinter as tk
from tkinter import ttk
from DemExam2 import db
from DemExam4 import view_partner
from DemExam5 import history_story  # <-- Добавили импорт

def window():
    a = db()
    info = a[0]
    sale = a[1]

    root = tk.Tk()
    root.title("Партнеры и скидки")
    root.geometry("910x900")
    root.iconbitmap(default="Мастер пол.ico")
    root.config(bg="#FFFFFF")

    font_text = "Segoe UI"
    colors = ["#FFFFFF", "#F4E8D3", "#67BA80"]

    # Кнопки управления вверху
    top_frame = tk.Frame(root, bg=colors[0])
    top_frame.pack(fill="x", side="top")

    add_btn = tk.Button(top_frame, text="Добавить", font=(font_text, 12, 'bold'), bg=colors[1], fg=colors[2], command=lambda: view_partner(None))
    add_btn.pack(side="left", fill="x", expand=True)

    history_btn = tk.Button(top_frame, text="История продаж", font=(font_text, 12, 'bold'), bg=colors[1], fg=colors[2], command=history_story)
    history_btn.pack(side="left", fill="x", expand=True)

    can = tk.Canvas(root, bg="white", highlightthickness=0)
    can.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=can.yview)
    scrollbar.pack(side="right", fill="y")
    can.configure(yscrollcommand=scrollbar.set)

    main_frame = tk.Frame(can, bg=colors[0])
    can.create_window((0, 0), window=main_frame, anchor="nw")

    def on_configure(event):
        can.configure(scrollregion=can.bbox('all'))

    main_frame.bind("<Configure>", on_configure)

    type_lbls = []
    sale_lbls = []
    name_lbls = []
    phone_nums_lbls = []
    rating_lbls = []
    btns = []

    for i in range(len(info)):
        frame_1 = tk.Frame(main_frame, bg=colors[1], borderwidth=2, relief='groove', width=800, height=200)
        frame_1.grid(row=i, column=0, pady=5, sticky="ew")

        type_lbl = tk.Label(frame_1, text=f'{info[i][0]} | {info[i][1]}', font=(font_text, 16, 'bold'), bg=colors[1], fg=colors[2], width=20, anchor="w")
        type_lbl.grid(row=0, column=0, columnspan=2, sticky="w")
        type_lbls.append(type_lbl)

        sale_lbl = tk.Label(frame_1, text=f'{sale[i]}%', font=(font_text, 24, 'bold'), bg=colors[1], fg=colors[2])
        sale_lbl.grid(row=0, column=2, padx=200, sticky="e")
        sale_lbls.append(sale_lbl)

        name_director = tk.Label(frame_1, text=info[i][2], font=(font_text, 12, 'bold'), bg=colors[1], fg=colors[2])
        name_director.grid(row=1, column=0, columnspan=3, sticky="w")
        name_lbls.append(name_director)

        phone_num = tk.Label(frame_1, text=info[i][3], font=(font_text, 12, 'bold'), bg=colors[1], fg=colors[2])
        phone_num.grid(row=2, column=0, columnspan=3, sticky="w")
        phone_nums_lbls.append(phone_num)

        rating_lbl = tk.Label(frame_1, text=f'Рейтинг: {info[i][4]}', font=(font_text, 12, 'bold'), bg=colors[1], fg=colors[2])
        rating_lbl.grid(row=3, column=0, columnspan=3, sticky="w")
        rating_lbls.append(rating_lbl)

        btn = tk.Button(frame_1, text="Редактировать", font=(font_text, 12, 'bold'), bg=colors[1], fg=colors[2], command=lambda ind=i: view_partner(info[ind][1]))
        btn.grid(row=4, column=0, columnspan=3, sticky="se")
        btns.append(btn)

    def update():
        b = db()
        info = b[0]
        sale = b[1]
        print(len(b[0]), len(type_lbls))
        for i in range(len(type_lbls)):
            type_lbls[i].config(text=f'{info[i][0]} | {info[i][1]}')
            sale_lbls[i].config(text=f'{sale[i]}%')
            name_lbls[i].config(text=info[i][2])
            phone_nums_lbls[i].config(text=info[i][3])
            rating_lbls[i].config(text=f'Рейтинг: {info[i][4]}')
            btns[i].config(command=lambda ind=i: view_partner(info[ind][1]))
        if len(b[0]) > len(type_lbls):
            type_lbls.clear()
            sale_lbls.clear()
            name_lbls.clear()
            phone_nums_lbls.clear()
            rating_lbls.clear()
            btns.clear()
            for i in range(len(info)):
                frame_1 = tk.Frame(main_frame, bg=colors[1], borderwidth=2, relief='groove', width=800, height=200)
                frame_1.grid(row=i, column=0, pady=5, sticky="ew")

                type_lbl = tk.Label(frame_1, text=f'{info[i][0]} | {info[i][1]}', font=(font_text, 16, 'bold'),
                                    bg=colors[1], fg=colors[2], width=20, anchor="w")
                type_lbl.grid(row=0, column=0, columnspan=2, sticky="w")
                type_lbls.append(type_lbl)

                sale_lbl = tk.Label(frame_1, text=f'{sale[i]}%', font=(font_text, 24, 'bold'), bg=colors[1],
                                    fg=colors[2])
                sale_lbl.grid(row=0, column=2, padx=200, sticky="e")
                sale_lbls.append(sale_lbl)

                name_director = tk.Label(frame_1, text=info[i][2], font=(font_text, 12, 'bold'), bg=colors[1],
                                         fg=colors[2])
                name_director.grid(row=1, column=0, columnspan=3, sticky="w")
                name_lbls.append(name_director)

                phone_num = tk.Label(frame_1, text=info[i][3], font=(font_text, 12, 'bold'), bg=colors[1], fg=colors[2])
                phone_num.grid(row=2, column=0, columnspan=3, sticky="w")
                phone_nums_lbls.append(phone_num)

                rating_lbl = tk.Label(frame_1, text=f'Рейтинг: {info[i][4]}', font=(font_text, 12, 'bold'),
                                      bg=colors[1], fg=colors[2])
                rating_lbl.grid(row=3, column=0, columnspan=3, sticky="w")
                rating_lbls.append(rating_lbl)

                btn = tk.Button(frame_1, text="Редактировать", font=(font_text, 12, 'bold'), bg=colors[1], fg=colors[2],
                                command=lambda ind=i: view_partner(info[ind][1]))
                btn.grid(row=4, column=0, columnspan=3, sticky="se")
                btns.append(btn)

        root.after(100, update)

    update()
    root.mainloop()
window()