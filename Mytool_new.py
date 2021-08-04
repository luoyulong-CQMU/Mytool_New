# -*- coding:utf-8 -*-
"""
作者：luoyu
日期：2021年01月05日
"""
import tkinter as tk
from tkinter import messagebox, ttk, Scrollbar
from PIL import Image, ImageTk
# import ctypes
from unit.OutpatientLog import *
from unit.BloodGas import *
from unit.discharge import *
from unit.report_card import *
from unit.settingdiag import *
from unit.database import *
from unit.copd import *
from unit.Card import *
from game_unit.gameModule import *
from update_unit.update_client import Update


class CaseTool(object):
    def __init__(self):
        pass

    def my_case_tool(self, main_window=None):
        # 这里默认设置为None是为了在单个程序调用测试不报错！
        try:
            # 把主窗最小化
            main_window.state('icon')
        except:
            pass
        top_level = tk.Toplevel()
        top_level.wm_attributes('-topmost', 1)
        top_level.title('病案工具')
        top_level.resizable(width=False, height=False)
        screenwidth = top_level.winfo_screenwidth()
        screenheight = top_level.winfo_screenheight()
        width = 570
        height = 250
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)

        top_level.geometry(alignstr)

        out_message = tk.StringVar()
        out_message.set('住院证打印需要填写医生姓名')
        frame1 = tk.Frame(top_level, width=525, height=160, borderwidth=2, padx=0, pady=0, relief="sunken")
        frame1.pack()
        frame1.place(x=20, y=20)
        btn_report = tk.Button(frame1, text='感染病例报卡', font=('Arial', 10), width=15, height=2,
                               activebackground='Lightblue',
                               command=lambda: ReportCard().report_card(out_message))
        btn_quality = tk.Button(frame1, text='病案质量填充', font=('Arial', 10), width=15, height=2,
                                activebackground='Lightblue',
                                command=lambda: ReportCard().quality(out_message))
        btn_printID = tk.Button(frame1, text='住院证打印', font=('Arial', 10), width=15, height=2,
                                activebackground='Lightblue',
                                command=lambda: PrindPainIdCard().draw_mainwindow(out_message))
        btn_Game = tk.Button(frame1, text='GameTest', font=('Arial', 10), width=15, height=2,
                             activebackground='Lightblue', command=lambda: GameSelect().draw_main_window(top_level))
        btn_report.pack()
        btn_quality.pack()
        btn_printID.pack()
        btn_Game.pack()
        btn_report.place(x=50, y=10)
        btn_quality.place(x=330, y=10)
        btn_printID.place(x=50, y=90)
        btn_Game.place(x=330, y=90)

        frame2 = tk.Frame(top_level, width=525, height=40, borderwidth=2, padx=0, pady=0, relief="sunken")
        frame2.pack()
        frame2.place(x=20, y=190)
        message_lab = tk.Label(frame2, width='57', height=1, textvariable=out_message, justify='left')
        message_lab.pack()
        message_lab.place(x=1, y=3)
        top_level.protocol("WM_DELETE_WINDOW", lambda: self.exit_window(main_window=main_window, top_level=top_level))
        top_level.mainloop()

    def exit_window(self, main_window, top_level):
        try:
            main_window.state('normal')
        except:
            pass
        top_level.destroy()


class Setting_window(object):
    """
    程序设置界面
    """

    def __init__(self):
        pass

    def draw_main_window(self, main_window):
        """

        :param main_window: 父窗口，其目的在于点开设置最小化父窗口以及关闭设置自动还原父窗口
        :return:
        """
        self.database = DataBase()
        try:
            # 尝试调用 数据库 读取医生信息，如不存在，会自动创建，
            name = self.database.get_name()
        except:
            name = "默认姓名"
        try:
            # 把主窗最小化
            main_window.state('icon')
        except:
            pass
        # 绘制toplevel部件
        top_level = tk.Toplevel()
        top_level.title('程序设置')
        top_level.resizable(width=False, height=False)
        screenwidth = top_level.winfo_screenwidth()
        screenheight = top_level.winfo_screenheight()
        width1 = 700
        height1 = 500
        alignstr = '%dx%d+%d+%d' % (width1, height1, (screenwidth - width1) / 2, (screenheight - height1) / 2)
        top_level.geometry(alignstr)
        fram1 = tk.Frame(top_level, borderwidth=2, width=500, height=50, relief="sunken")
        fram2 = tk.Frame(top_level, borderwidth=2, width=500, height=370, relief="sunken")
        fram3 = tk.Frame(top_level, borderwidth=2, width=130, height=420, relief="sunken")
        fram1.place(x=30, y=30)
        fram2.place(x=30, y=100)
        fram3.place(x=550, y=30)
        doctor_name = tk.StringVar()
        doctor_name.set(f'默认姓名(输入要修改的内容点击修改):')
        name_lab = tk.Label(fram1, width=30, height=1, textvariable=doctor_name)
        name_lab.place(relx=0.02, rely=0.1)
        modify_enty = tk.Text(fram1, width=20, height=1)
        modify_enty.insert('end', name)
        modify_enty.place(relx=0.6, rely=0.2)
        modify_btn = tk.Button(fram3, width=10, height=1, text="修改姓名",
                               command=lambda: self.update_name(modify_enty))
        modify_btn.place(relx=0.1, rely=0.01)
        update_btn = tk.Button(fram3, width=10, height=1, text="检查更新",
                               command=Update().check_version)
        update_btn.place(relx=0.1, rely=0.15)

        add_keywords_btn = tk.Button(fram3, width=10, height=1, text="增加关键字", command=self.add_key_words)
        add_keywords_btn.place(relx=0.1, rely=0.3)

        add_chief_btn = tk.Button(fram3, width=10, height=1, text="增加主诉", command=self.add_chief)
        add_chief_btn.place(relx=0.1, rely=0.45)

        modify_chief_btn = tk.Button(fram3, width=10, height=1, text="修改", command=self.modify)
        modify_chief_btn.place(relx=0.1, rely=0.6)

        del_chief_btn = tk.Button(fram3, width=10, height=1, text="删除", command=self.del_)
        del_chief_btn.place(relx=0.1, rely=0.75)

        save_btn = tk.Button(fram3, width=10, height=1, text="帮助", command=self.help)
        save_btn.place(relx=0.1, rely=0.9)

        self.tree = ttk.Treeview(fram2, height=16)
        self.tree.column("#0", width=465, anchor="center")
        keywords_and_chief = DiagMatch().read_db()  # keywords_and_chief 为数据库返回的列表;包含多个元组（keywords,chief）
        sum = len(keywords_and_chief)
        for i, each in enumerate(keywords_and_chief):
            # 通过遍历上述列表，把关键词及主诉添加到tree
            diag = each[0]
            father_tree = self.tree.insert("", 0, diag, text=f'{sum - i}.{diag}', values=(i))
            try:
                # 调用try是避免只有关键词没有主诉的情况程序报错
                choice_lst = each[1].split('|')
                for index, choice in enumerate(choice_lst):
                    self.tree.insert(father_tree, 1, text=f'{choice}', values=(f"{index}"))
            except:
                messagebox.showwarning('警告', f'【{diag}】还没有添加随机主诉！')
        # 滚动条
        vbar = Scrollbar(fram2, orient='vertical', command=self.tree.yview, width=20)
        self.tree.configure(yscrollcommand=vbar.set)
        # # 选中行
        self.tree.bind('<<TreeviewSelect>>', self.selectTree(self.tree))
        s = ttk.Style()
        s.configure('Treeview', rowheight=20)
        self.tree.pack(side='left')
        vbar.pack(side='right', fill='y')
        top_level.protocol("WM_DELETE_WINDOW", lambda: self.exit_window(main_window=main_window, top_level=top_level))
        top_level.mainloop()

    def update_name(self, Edit):
        '''
        调用get方法获取输入值，因text控件为多行，需要strip取掉\n
        :param Edit: tk.Text控件
        :return:
        '''
        new_name = Edit.get('0.0', 'end').strip()
        self.database.update_data(new_name=new_name)

    def help(self):
        messagebox.showinfo('提示', '1.   对关键字的解释\n'
                                  '1.1 关键字是对应匹配（门诊日志[诊断印象]）的字符串\n'
                                  '      比如关键字"AB"能匹配到"ABCD",\r\n'
                                  '      也能匹配到"DDABD",但无法匹配到"DADB"\n'
                                  '1.2 关键字应尽量精短，匹配范围则更广\r\n\r\n'
                                  '2.   对主诉的解释\n'
                                  '2.1 主诉则是由多个完整的随机主诉组成。\n'
                                  '2.2 其内容是根据关键字在门诊日志[诊断印象]中匹配出来的\n'
                                  '2.3 为避免出现重复，每个关键字应设置尽量多的主诉短语\n'
                                  '')

    def add_key_words(self):
        '''
        添加关键词
        :return:
        '''
        top_level = tk.Toplevel()
        top_level.title('增加关键字')
        top_level.resizable(width=False, height=False)
        screenwidth = top_level.winfo_screenwidth()
        screenheight = top_level.winfo_screenheight()
        width1 = 400
        height1 = 100
        alignstr = '%dx%d+%d+%d' % (width1, height1, (screenwidth - width1) / 2, (screenheight - height1) / 2)
        top_level.geometry(alignstr)
        lab = tk.Label(top_level, text='输入匹配关键字(根据关键字匹配主诉)', width=30, height=1)
        lab.grid(row=0, column=0)
        text = tk.Text(top_level, width=20, height=1)
        text.grid(row=1, column=0)
        client_btn = tk.Button(top_level, width=10, height=1, text='确定',
                               command=lambda: self.add_key_words_client(text, top_level))
        client_btn.grid(row=1, column=1)
        top_level.mainloop()

    def add_key_words_client(self, Edit, window):
        '''

        :param Edit: tk.Text控件；
        :param window: 当前窗口，以调用销毁事件
        :return:
        '''
        key_words = Edit.get('0.0', 'end').strip()
        self.tree.insert("", 0, key_words, text=key_words)
        DiagMatch().add_key_words(key_words)
        self.tree.update()
        window.destroy()

    def add_chief(self):
        '''
        添加随机主诉
        :return:
        '''
        curItem = self.tree.focus()  # 获取当前选择的节点
        father_item = self.tree.parent(curItem)  # 获取父节点
        if father_item == "" or father_item is None:  # 如果为空，则判断为根节点，则选中的是关键词
            top_level = tk.Toplevel()
            # top_level.wm_attributes('-topmost', 1)
            top_level.title('增加主诉')
            # top_level.geometry('400x200+300+300')
            top_level.resizable(width=False, height=False)
            screenwidth = top_level.winfo_screenwidth()
            screenheight = top_level.winfo_screenheight()
            width1 = 400
            height1 = 100
            alignstr = '%dx%d+%d+%d' % (width1, height1, (screenwidth - width1) / 2, (screenheight - height1) / 2)
            top_level.geometry(alignstr)
            lab = tk.Label(top_level, text='输入随机主诉(根据列表随机选取，建议>2个)', width=40, height=1)
            lab.place(relx=0.01, rely=0.1)
            text = tk.Text(top_level, width=20, height=2)
            text.place(relx=0.1, rely=0.4)
            client_btn = tk.Button(top_level, width=10, height=1, text='确定',
                                   command=lambda: self.add_chief_client(text, top_level))
            client_btn.place(relx=0.6, rely=0.4)
            top_level.mainloop()
        else:
            messagebox.showwarning('警告', '请选择父节点再添加主诉！')

    def add_chief_client(self, Edit, window):
        '''

        :param Edit: tk.Text控件
        :param window: 当前窗口
        :return:
        '''
        curItem = self.tree.focus()  # 获取当前选中节点
        # print(f"当前选中节点：{curItem}")
        father_item = self.tree.parent(curItem)  # 获取节点的父节点
        if father_item == "" or father_item is None:  # 判断是否为根节点，如果父节点为空则是跟节点
            new_chief = Edit.get('0.0', 'end').strip()
            DiagMatch().add_chief(curItem, new_chief)
            self.tree.insert(curItem, 0, text=new_chief)
        else:
            messagebox.showwarning('警告', '请选择父节点再添加主诉！')
        window.destroy()

    def modify(self):
        '''
        修改节点内容，包含修改关键词以及主诉
        :return:
        '''
        curItem = self.tree.focus()
        lab_text = "关键字" if self.tree.parent(curItem) == "" else "随机主诉"
        top_level = tk.Toplevel()
        # top_level.wm_attributes('-topmost', 1)
        top_level.title(f'修改{lab_text}')
        top_level.resizable(width=False, height=False)
        screenwidth = top_level.winfo_screenwidth()
        screenheight = top_level.winfo_screenheight()
        width1 = 500
        height1 = 100
        alignstr = '%dx%d+%d+%d' % (width1, height1, (screenwidth - width1) / 2, (screenheight - height1) / 2)
        top_level.geometry(alignstr)
        lab = tk.Label(top_level, text='在下方输入要修改的内容', width=40, height=1)
        lab.place(relx=0.01, rely=0.1)
        text = tk.Text(top_level, width=20, height=2)
        text.place(relx=0.1, rely=0.4)
        client_btn = tk.Button(top_level, width=10, height=1, text='确定',
                               command=lambda: self.modify_client(text, top_level))
        client_btn.place(relx=0.6, rely=0.4)
        top_level.mainloop()

    def modify_client(self, Edit, window):
        '''

        :param Edit: Text控件
        :param window: 当前窗体
        :return:
        '''
        curItem = self.tree.focus()
        item_text = self.tree.item(curItem)['text'] # 这里需要调用item方法才能获取到text内容，原因次节点不能直接获取text；
        father_item = self.tree.parent(curItem)  # 获取节点的父节点
        new_item = Edit.get('0.0', 'end').strip()
        self.tree.item(curItem, text=new_item)
        if father_item == "" or father_item is None:  # 如果为空，则判断为根节点，则选中的是关键词
            DiagMatch().update_keywords(curItem, new_item)
        else:
            DiagMatch().update_chief(father_item, item_text, new_item)
        window.destroy()

    def del_(self):
        '''
        删除内容
        :return:
        '''
        select_item = self.tree.focus()
        father_item = self.tree.parent(select_item)
        if father_item == "" or father_item is None: # 为空则表示选中的是跟节点
            choice = messagebox.askyesno("警告！", "确定删除关键字？删除关键字会将其下所有的随机主诉删除！")
            # 删除关键字及下所有的内容
            if choice:
                self.tree.delete(select_item)
                DiagMatch().del_keywords(select_item)
            else:
                pass
        else:
            select_item = self.tree.focus()
            select_item_text = self.tree.item(select_item)['text']
            self.tree.delete(select_item)
            print(father_item,select_item_text)
            DiagMatch().del_chief(father_item,select_item_text)

    def exit_window(self, main_window, top_level):
        try:
            main_window.state('normal')
        except:
            pass
        top_level.destroy()

    # 鼠标选中一行回调
    def selectTree(self, tree):
        for item in tree.selection():
            item_text = tree.item(item, "values")
            print(item_text)


def blood_gas():
    # 自适应dpi缩放
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    ui = BloodGas()
    ui.setupUi(main_window)
    main_window.show()
    # sys.exit(app.exec_())
    app.exec_()


def clean_cache():
    dirpath = "./cache/"
    # 判断文件是否存在
    files = os.listdir(dirpath)
    for file in files:
        try:
            file_path = dirpath + file
            os.remove(file_path)
        except:
            pass
    os._exit(1)


def change_arrow(button):
    button.configure(cursor='hand2')
    window.update()


if __name__ == '__main__':
    Update().check_version()
    window = tk.Tk()
    window.configure(bg='#393939')
    window.title('Mytool4.0')
    window.resizable(width=False, height=False)
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    width = 570
    height = 250
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    window.geometry(alignstr)
    img_1 = tk.PhotoImage(file="resources/main_1.png")
    img_2 = tk.PhotoImage(file="resources/main_2.png")
    img_3 = tk.PhotoImage(file="resources/main_3.png")
    img_4 = tk.PhotoImage(file="resources/main_4.png")
    img_5 = tk.PhotoImage(file="resources/main_5.png")
    img_6 = tk.PhotoImage(file="resources/main_6.png")
    bt1 = tk.Button(window, text='门诊日志格式化工具', width=200, height=50, image=img_1,
                    relief='sunken', bg='#282828',
                    activebackground='#1f5383',
                    command=lambda: OutPaintLog().draw_main_top_level(window))
    bt2 = tk.Button(window, text='出院随访格式化工具', width=200, height=50, image=img_2,
                    relief='sunken', bg='#282828',
                    activebackground='#1f5383',
                    command=lambda: DisCharge().draw_main_window(window))
    bt3 = tk.Button(window, text='重庆居民慢阻肺报告卡', width=200, height=50, image=img_3,
                    relief='sunken', bg='#282828',
                    activebackground='#1f5383',
                    command=lambda: GetMessage().draw_main_window(window))
    bt4 = tk.Button(window, text='病案工具', width=200, height=50, image=img_4, relief='sunken',
                    bg='#282828',
                    activebackground='#1f5383',
                    command=lambda: CaseTool().my_case_tool(window))
    bt5 = tk.Button(window, text='血气分析工具', width=200, height=50, image=img_5,
                    relief='sunken', bg='#282828',
                    activebackground='#1f5383',
                    command=blood_gas)
    bt6 = tk.Button(window, text='程序设置', width=200, height=50, image=img_6, relief='sunken',
                    bg='#282828',
                    activebackground='#1f5383',
                    command=lambda: Setting_window().draw_main_window(main_window=window))
    bt1.place(x=50, y=20)
    bt2.place(x=50, y=90)
    bt3.place(x=50, y=160)
    bt4.place(x=300, y=20)
    bt5.place(x=300, y=90)
    bt6.place(x=300, y=160)
    bt1.bind("<Enter>", change_arrow(bt1))
    bt2.bind("<Enter>", change_arrow(bt2))
    bt3.bind("<Enter>", change_arrow(bt3))
    bt4.bind("<Enter>", change_arrow(bt4))
    bt5.bind("<Enter>", change_arrow(bt5))
    bt6.bind("<Enter>", change_arrow(bt6))
    window.protocol("WM_DELETE_WINDOW", clean_cache)
    window.mainloop()
