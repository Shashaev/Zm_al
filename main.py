import random as rn
import sqlite3 as sql

from tkinter import *


win = Tk()
win.title('Snake')
u_nik = ''
ob = []
rek = 0
tb = sql.connect('Snake.db')
cur = tb.cursor()

ex = 'CREATE TABLE IF NOT EXISTS users (nik TEXT NOT NULL PRIMARY KEY, password TEXT NOT NULL, rec INTEGER NOT NULL)'
cur.execute(ex)

n_l = Label(text="Ник:")
s_l = Label(text="Пароль:")

n_l.grid(row=0, column=0, padx='10', pady='5')
s_l.grid(row=1, column=0, padx='10', pady='5')

nik = Entry()
pas = Entry()
nik.grid(row=0, column=1, columnspan=3, padx='10')
pas.grid(row=1, column=1, columnspan=3, padx='10')


def r_tb():
    global rek
    global u_nik

    en_pas = pas.get()
    ni_pas = nik.get()

    er_nik = Label(text='Введите ник')
    er_pas = Label(text='Введите пароль')
    er_n = Label(text='Неверный логин или пароль')
    er_n.grid_forget()
    er_nik.grid_forget()
    er_pas.grid_forget()
    if len(nik.get()) == 0:
        er_nik.grid(row=3, column=0, columnspan=2)
        ob.append(er_nik)
    elif len(pas.get()) == 0:
        er_pas.grid(row=3, column=0, columnspan=2)
        ob.append(er_pas)
    else:
        pas_ = cur.execute(f'SELECT password FROM users WHERE nik = "{ni_pas}"').fetchone()
        if pas_ == None:
            cur.execute(f'INSERT INTO users VALUES ("{ni_pas}", "{en_pas}", {0})')
            u_nik = ni_pas
            reg()
            tb.commit()
        else:
            if pas_[0] == en_pas:
                u_nik = ni_pas
                rek = cur.execute(f'SELECT rec FROM users WHERE nik = "{ni_pas}"').fetchone()[0]
                reg()
            else:
                er_n.grid(row=3, column=0, columnspan=2)
                ob.append(er_n)


def reg():
    n_l.destroy()
    s_l.destroy()
    nik.destroy()
    pas.destroy()
    fx.destroy()
    if len(ob) > 0:
        for i in ob:
            i.destroy()
    win.geometry("440x440")
    li.grid(row=1, column=0, pady='200', padx='35')
    kn.grid(row=1, column=2, pady='200', padx='35')


def w_li():
    li.grid_forget()
    if len(ob) > 0:
        for i in ob:
            i.destroy()
    lis.delete(0, END)
    bl = cur.execute('SELECT nik, rec FROM users').fetchall()
    for i in range(len(bl)):
        bl[i] = list(bl[i])
        a = bl[i][0]
        bl[i][0] = bl[i][1]
        bl[i][1] = a
    bl.sort(reverse=True)
    for i in range(len(bl)):
        lis.insert(END, f'{bl[i][1]}:     {bl[i][0]}')

    kn.grid(row=1, column=1, pady='20', padx='35')
    lis.grid(row=0, column=1, padx='105')


def in_sn():
    lis.grid_forget()
    kn.grid_forget()
    li.grid_forget()
    if len(ob) > 0:
        for i in ob:
            i.destroy()
    can = Canvas(width=440, height=440, bg='white', bd=0)
    can.focus_set()
    can.pack()

    v = can.create_rectangle(200, 200, 240, 240, fill='green', outline='green')
    d_z = [[200, 200, 240, 240]]
    ind = [v]
    pos_wish = []
    t = 0
    x = 0
    y = 0
    e = 0
    r = 0

    def los():
        global rek
        global u_nik
        p = 'проиграл'
        can.destroy()
        la = Label(win, text=f"Ты {p}! \n\n Набраные очки - {len(d_z)}", font='30')
        la.grid(row=0, column=0, columnspan=2, pady='10')
        ob.append(la)
        if rek < len(d_z):
            lp = Label(win, text=f"Новый рекорд !!!", font='30')
            lp.grid(row=1, column=0, columnspan=2, pady='10')
            ob.append(lp)
            rek = len(d_z)
            cur.execute(f'Update users set rec = {rek} where nik = "{u_nik}"')
            tb.commit()
        kn.grid(row=2, column=1, pady='160', padx='35')
        li.grid(row=2, column=0, pady='160', padx='35')

    def wish():
        ex = 0
        nonlocal pos_wish
        cor_x = rn.randint(0, 10) * 40
        cor_y = rn.randint(0, 10) * 40
        c_wish = [cor_x, cor_y, cor_x + 40, cor_y + 40]

        for j in range(len(d_z)):
            if c_wish == d_z[j]:
                wish()
                ex = 1
        if ex == 0:
            can.create_oval(c_wish[0], c_wish[1], c_wish[2], c_wish[3],
                            width=0, outline='white', fill='red', tags='cherry')
            pos_wish = c_wish

    wish()

    def pr():
        cor = d_z[-1]
        if cor[0] < 0 or cor[1] < 0 or cor[2] > 440 or cor[3] > 440:
            los()
        else:
            for j in range(0, len(d_z) - 2):
                if cor == d_z[j]:
                    los()

    def ren(_x, _y, x_w, y_w):
        nonlocal e
        e += 1

        cor = d_z[-1]
        can.coords(ind[-1], cor[0] + _x, cor[1] + _y, cor[2] + _x, cor[3] + _y)
        d_z[-1] = [cor[0] + _x, cor[1] + _y, cor[2] + _x, cor[3] + _y]

        cor_w = d_z[0]
        can.coords(ind[0], cor_w[0] + x_w, cor_w[1] + y_w, cor_w[2] + x_w, cor_w[3] + y_w)
        d_z[0] = [cor_w[0] + x_w, cor_w[1] + y_w, cor_w[2] + x_w, cor_w[3] + y_w]

        if e != 10:
            win.after(25, lambda: ren(_x, _y, x_w, y_w))
        else:
            e = 0
            win.after(25, per)

    def per():
        nonlocal r
        nonlocal pos_wish
        nonlocal t

        if r == 1:
            can.delete(ind[0])
            d_z.pop(0)
            ind.pop(0)

        cor = d_z[-1]

        c = can.create_rectangle(cor[0], cor[1], cor[2], cor[3], fill='green', outline='green')

        ind.append(c)
        d_z.extend([cor])

        x_w = int((d_z[1][0] - d_z[0][0]) / 10)
        y_w = int((d_z[1][1] - d_z[0][1]) / 10)
        pr()
        if len(d_z) < 3:
            can.delete(ind[0])

        ren(x, y, x_w, y_w)

        if cor == pos_wish:
            can.delete('cherry')
            wish()
            r = 0
        else:
            r = 1
        if len(d_z) == 120:
            can.destroy()
            la = Label(text=f"Ты выграл!!! \n За игру ты прошёл "
                       f"{t} клеток \n Сможешь справиться за меньшее колтчество?", font='30')
            la.grid()
            ob.append(la)
            kn.grid(row=2, column=1, pady='160', padx='35')
            li.grid(row=2, column=0, pady='160', padx='35')
        t += 1

    def izm_poz(_x=0, _y=0):
        nonlocal y
        nonlocal x
        y = _y
        x = _x
        if t == 0:
            per()

    can.bind('<Up>', lambda event: izm_poz(_y=-4))
    can.bind('<Down>', lambda event: izm_poz(_y=4))
    can.bind('<Left>', lambda event: izm_poz(_x=-4))
    can.bind('<Right>', lambda event: izm_poz(_x=4))


kn = Button(text='Начать игру', command=in_sn, font='30')
fx = Button(text='Войти', command=r_tb)
fx.grid(row=2, column=2, pady='5')
li = Button(text='Таблица лидеров', command=w_li, font=30)
lis = Listbox(font=30)
win.mainloop()
