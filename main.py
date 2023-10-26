import tkinter as tk
from tkinter import ttk
import sqlite3

# Класс главного окна
class Main (tk.Frame):
    def _init_(self,root):
        super()._init_(root)
        self.init_main()
        self.db = db
        self.viem_records()

##################################################################
    # Саздание и работа с главным окном
    def init_main(self):
        toolbar = tk.Frame(bg="#d7d7d7", bd = 2)
        toolbar.pack(side=tk.TOP,fill=tk.X)
##################################################################

        # ДОБАВИТЬ
        self.add_img = tk.PhotoImage(file="./img/add.png")
        btn_add = tk.button(toolbar,bg="#d7d7d7", bd=1,\
                            image =self.add_img, command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # Обновить
        self.upd_img = tk.PhotoImage(file="./img/update.png")
        btn_upd = tk.Button (toolbar,bg="#d7d7d7",bd=1,
                           image=self.add_img,command=self.open_update_dialoge)
        btn_upd.pack(side=tk.LEFT)

        # Удалить
        self.deg_img = tk.PhotoImage(file="./img/deleate.png")
        btn_del = tk.Button(toolbar,bg="#d7d7d7",bd=1,
                            image=self.del_img,command=self.deleat_records)
        btn_del.pack(side=tk.LEFT)

        # Поиск
        self.search = tk.PhotoImage(file="./img/search.png")
        btn_search = tk.Button(toolbar,bg="#d7d7d7",bd=1,
                            image=self.search_img,command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        # Обновить
        self.refresh_img = tk.PhotoImage(file="./img/refresh.png")
        btn_refresh = tk.Button(toolbar,bg="#d7d7d7", bd=1,
                                image=self.refresh_img,command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

################################################################## Создание Таблицы
        # Добавляем столбцы
        self.tree = ttk.Treeview(self,columns=("id", "name", "phone", "email"),
                                 heigh=45, show="headings")
        
        # Добавить параметры колонкам
        self.tree.column("ID",width=45, anchor=tk.CENTER)
        self.tree.column("name",width=300,anchor=tk.CENTER)
        self.tree.column("phone",width=150, anchore=tk.CENTER)
        self.tree.column("email",width=150,anchore=tk.CENTER)

        # Подписи колонок
        self.tree.heading("ID",text="ID")
        self.tree.heading("name",text="ФИО")
        self.tree.heading("phone",text="Тулуфон")
        self.tree.heading("email", text="E-mail")

        # Упаковка
        self.tree.pack(side=tk.LEFT)
################################################################### ВСЕ МЕТОДЫ

    def records(self,name,phone,email):
        self.db.insert_data(name,phone,email)
        self.view_records()

    # Отображение данных в TreeView
    def view_records(self):
        self.db.cur.execute("""SELECT * FROM users""")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("","end",valumns=row)
        for row in self.db.cur.fetchall()]

    # Метод обновление данных
    def update_records(self,name,phone,email):
        id =self.tree.set(self.tree.selecttion()[0],"1")
        self.db.cur.execute(""" UPDATE users SET name=?, phone=?, email=? WHERE ID=? """
                            (name,phone,email,id))
        self.db.conn.commit()
        self.view_records()

    # Метод для удаления данных
    def deleate_records(self):
        for row in self.tree.selection():
            self.db.cur.execute(""" DELEAT FROM users WHERE ID=?""",
                                (self.tree.set(row,"#1"),))
        self.db.conn.commit()
        self.view_records()

    # Метод поиска данных
    def search_records(self,name):
        name = ("%" + name + "%")
        self.db.cur.execute(""" SELECT * FROM users WHERE name LIKE ?""", (name,))

        [self.tree.deleate(i) for i in self.tree.get_choldren()]
        [self.tree.insert("", "end",values=row)
         for row in self.db.cur.fetchall()]
                         
################################################################### ВЫЗОВ КЛАССОВ

    # Метод вызывающий окно добовления
    def open_child(self):
        Child()
    
    # Метод вызывающий окно обновления
    def open_update_dialog(self):
        Update()
    
    # Метод вызывающий окно поиска
    def open_search(self):
        Search()

###################################################################
# Дочернее  окно+__)
class Child(tk.Toplevel):
    def _init_(self):
        super()._init_(root)
        self.init_child()
        self.view = app

        def init_child(self):
            self.title("Добавить контакт")
            self.geometry("400x200")
            self.resizeble(False,False)
            self.grab_set()
            self.focus_set()
###################################################################
            label_name = tk.label(self,text="ФИО:")
            label_name.place(x=50,y=50)
            label_phone = tk.label(self,text="Телефон")
            label_phone.place(x=50,y=80)
            label_email = tk.label(self,text="E-mail")
            label_email.place(x=50,y=110)
            self.entry_name = ttk.Entry(self)
            self.entry_name.place(x=200,y=50)
            self.entry_phone = ttk.Entry(self)
            self.entry_phone.place(x=200,y=80)
            self.entry_email = ttk.Entry(self)
            self.entry_email.place(x=200,y=110)
###################################################################

            # Кнопка закрытия
            self.btn_cancel = ttk.Button(self,text="Закрыть",command=self.destroy)
            self.btn_cansel.place(x=300,y=170)

            # Кнопка добавления
            self.btn_add = ttk.Button(self,text="Добавить")
            self.btn_add.place(x=220,y=170)
            self.btn_add.bind("<Button-1>",lambda eventy:
                              self.view.records(self.entry_name.get(),
                                                self.entry_phone.get(),
                                                self.entry_emal.get()))
            
###################################################################

# Класс редактирования контактов
class Update(Child):
    def _init_(self):
        super()._init_()
        self.init_updeat()
        self.db = db
        self.defualt_data()

    def init_updeat(self):
      self.title("Редокьтровать позоцию")
      self.btn_add.destroy()

      self.btn_upd = ttk.Button(self,text="Редактировать")
      self.btn_upd.bind("<Button - 1>", lambda event :
                        self.view.update_record(self.entry_name.get(),
                                                self.entry_phone.get(),
                                                self.entry_email.get()))
      self.btn_upd.bind("<Button - 1>", lambda event: self.destroy(), add="+")
      self.btn_upd.place(x=200, y=170)

    def defult_data(self):
        id = self.view.tree.set(self.view.tree.selection([0], "#1"))
        self.db.cur.execute(""" SELECT * FROM users WHERE ID=? """,(id,))

        row = self.db.cur.fetchone()
        self.entry_name.insert(0,row[1])
        self.entry_phone.insert(0,row[2])
        self.entry_email.insert(0,row[3])


#####################################################################                

# Класс поиска контакта
class Search(tk.Toplevel):
    def _init_(self):
      super()._init_(root)
      self.init_search()
      self.view = app

    def init_search(self):
        self.title("Поиск по котнактам")
        self.geometry("300x100")
        self.resible(False,False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self,text="ФИО")
        label_name.place(x=20,y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_name.place(x=70,y=20)

        # Кнопка закрытия
        self.btn_cancel = ttk.Button(self,text="Закрыть", command=self.destroy)
        self.btn_cancel.place(x=200,y=70)

        # Кнопка поиска
        self.btn_search = ttk.Button(self,text="Найти")
        self.btn_search.place(x=70,y=70)
        self.btn_search.bind("<Button>",lambda event:
                             self.view.search_records(self.entry_name.get()))
        self.btn_search.bind("<Button>",lambda event: self.destroy(),add="+")


#######################################################################
# Класс Базы данных
class DB:
    def _init_(self):
        self.conn = sqlite3.connectZ("contacts.db")
        self.cur = self.conn.cursor()
        self.cur.execute(""" CREAT TABLE IF NOT EXISTS users(
                                ID INTEGER PRIMARY KEY NOT NULL,
                                nameTEXT,
                                phone TEXT,
                                email TEXT )""")
        self.cur.commit()

    def insert_data(self, name,phone,email):
        self.cur.execute(""" INSERT INTO users (name,phone,email)
                         VALUES(?,?,?)""",(name,phone,email))
        self.conn.commit()
####################################################################

if __name__=="_main_":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.ttitle("Тедефонная книга")
    root.geometry("645*450")
    root.resizable(False,False)
    root.configure(bg="White")
    root.mainloop()
