# -*- coding:utf-8 -*- 

"""
作者：luoyu
日期：2021年01月14日
"""

import sqlite3
from tkinter import messagebox
import tkinter as tk


class DataBase(object):
    """数据库操作"""
    doctor_name = ""

    def __init__(self):
        pass

    def get_input_name(self):
        self.doctor_name = self.modify_enty.get('0.0', 'end')
        self.write_database()
        self.top_level.destroy()

    def draw_input_window(self):
        self.top_level = tk.Toplevel()
        # self.top_level.wm_attributes('-topmost', 1)
        self.top_level.title('输入姓名')
        self.top_level.resizable(width=False, height=False)
        screenwidth = self.top_level.winfo_screenwidth()
        screenheight = self.top_level.winfo_screenheight()
        width = 300
        height = 150
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.top_level.geometry(alignstr)
        self.modify_enty = tk.Text(self.top_level, width=20, height=2)
        self.modify_enty.pack()
        self.modify_enty.place(x=50, y=60)

        modify_btn = tk.Button(self.top_level, width=10, height=1, text="修    改",
                               command=self.get_input_name)
        modify_btn.pack()
        modify_btn.place(x=200, y=60)
        self.top_level.mainloop()

    def write_database(self):
        conn = sqlite3.connect("doctor.db")
        cursor = conn.cursor()
        cursor.execute("create table user (id varchar(20) primary key , name varchar (20))")
        cursor.execute("insert into user (id,name ) values (?, ?)", ('1', self.doctor_name))
        cursor.rowcount
        cursor.close()
        conn.commit()
        conn.close()

    @staticmethod
    def read_data():
        conn = sqlite3.connect("doctor.db")
        cursor = conn.cursor()
        cursor.execute("select * from user where  id=?", ('1',))
        value = cursor.fetchall()
        doctor_name = tuple(value[0])
        cursor.close()
        return doctor_name[1]

    @staticmethod
    def update_data(new_name="猪"):
        conn = sqlite3.connect("doctor.db")
        cursor = conn.cursor()
        cursor.execute("update user set name = ? where id = 1 ", (new_name,))
        cursor.rowcount
        cursor.close()
        conn.commit()
        messagebox.showinfo(title="提示", message='信息更新成功!')
        conn.close()

    def get_name(self):
        try:
            return self.read_data()
        except Exception as e:
            messagebox.showwarning(title="注意！", message='数据库未创建!')
            self.draw_input_window()
            return self.read_data()


class DiagMatch(object):
    def __init__(self):
        pass

    @staticmethod
    def read_db(diag_key="心悸"):
        conn = sqlite3.connect("diag.db")
        cursor = conn.cursor()
        cursor.execute("select * from diag")
        value = cursor.fetchall()
        # print(value)
        cursor.close()
        return value

    @staticmethod
    def add_key_words(keywords):
        conn = sqlite3.connect("diag.db")
        cursor = conn.cursor()
        cursor.execute("insert into diag (diag,choice) values (?,?)", (keywords, ""))
        cursor.close()
        conn.commit()
        conn.close()

    @staticmethod
    def add_chief(keywords, new_chief):
        conn = sqlite3.connect("diag.db")
        cursor = conn.cursor()
        cursor.execute("select choice from diag where diag=?", (keywords,))
        value = cursor.fetchall()
        cursor.rowcount
        # print(keywords,value,new_chief)
        try:
            choices = value[0][0] + '|' + new_chief
            if value[0][0] is "" or value[0][0] is None:
                choices = new_chief
        except:
            choices = new_chief
        # print(choices)
        cursor.execute("update diag set choice = ? where diag = ? ", (choices, keywords))
        cursor.rowcount
        cursor.close()
        conn.commit()
        conn.close()

    @staticmethod
    def del_keywords(keywords):
        conn = sqlite3.connect("diag.db")
        cursor = conn.cursor()
        cursor.execute("delete from diag where diag = ? ", (keywords,))
        cursor.close()
        conn.commit()
        conn.close()

    @staticmethod
    def del_chief(keywords, chief):
        conn = sqlite3.connect("diag.db")
        cursor = conn.cursor()
        cursor.execute("select choice from diag where diag=?", (keywords,))
        value = cursor.fetchall()
        cursor.rowcount
        choices = value[0][0]
        count = 0
        for item in choices:
            if item == "|":
                count += 1
        if count > 0:
            choices = choices.replace(f'|{chief}', "")
        else:
            choices = choices.replace(f'{chief}', "")

        cursor.execute("update diag set choice = ? where diag = ? ", (choices, keywords))
        cursor.rowcount
        cursor.close()
        conn.commit()
        conn.close()

    @staticmethod
    def update_keywords(old_string, new_string):
        conn = sqlite3.connect("diag.db")
        cursor = conn.cursor()
        cursor.execute("update diag set diag = ? where diag = ? ", (new_string, old_string))
        # cursor.execute("update user set name = ? where id = 1 ", (new_name,))
        cursor.rowcount
        cursor.close()
        conn.commit()
        # messagebox.showinfo(title="提示", message='信息更新成功!')
        # print("*" * 50)
        conn.close()

    @staticmethod
    def update_chief(keywords, old_string, new_string):
        conn = sqlite3.connect("diag.db")
        cursor = conn.cursor()
        cursor.execute("select choice from diag where diag=?", (keywords,))
        value = cursor.fetchall()
        cursor.rowcount
        # print(keywords, value, new_string)
        try:
            choices = value[0][0]
            if value[0][0] is "" or value[0][0] is None:
                choices = new_string
            else:
                choices = choices.replace(old_string, new_string)
        except:
            choices = new_string
        # print(choices)
        # print(f"keyw{keywords}--old{old_string}--new{new_string}")
        cursor.execute("update diag set choice = ? where diag = ? ", (choices, keywords))
        # cursor.execute("update user set name = ? where id = 1 ", (new_name,))
        cursor.rowcount
        cursor.close()
        conn.commit()
        # messagebox.showinfo(title="提示", message='信息更新成功!')
        # print("*" * 50)
        conn.close()

    @staticmethod
    def create_db():
        conn = sqlite3.connect("diag.db")
        cursor = conn.cursor()
        cursor.execute("create table diag (diag varchar(255) primary key , choice varchar (255))")
        # cursor.execute("insert into user (id,name ) values (?, ?)", ('1', self.doctor_name))
        cursor.rowcount
        cursor.close()
        conn.commit()
        conn.close()


if __name__ == '__main__':
    name = DiagMatch()
    # name.update_data()
    name.update_chief('测试1', 'NMB', 'NMafsdfB')
