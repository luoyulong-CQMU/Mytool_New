import os
import threading
import tkinter as tk
import io
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
from game_unit.ManAndMachine import *
# from mineblock import *
from game_unit.MineSweeping import *
from game_unit.simpleSnake import *


def resize(w, h, w_box, h_box, pil_image):
  '''
  resize a pil_image object so it will fit into
  a box of size w_box times h_box, but retain aspect ratio
  对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例
  '''
  f1 = 1.0*w_box/w # 1.0 forces float division in Python2
  f2 = 1.0*h_box/h
  factor = min([f1, f2])
  #print(f1, f2, factor) # test
  # use best down-sizing filter
  width = int(w*factor)
  height = int(h*factor)
  return pil_image.resize((width, height), Image.ANTIALIAS)


class GameSelect(object):
    def __init__(self):
        # self.select_info_print()
        pass

    def draw_main_window(self, father_window=None):
        try:
            # 把主窗最小化
            father_window.state('icon')
        except:
            pass
        self.top_level = tk.Toplevel()
        self.top_level.wm_attributes('-topmost', 1)
        self.top_level.title('GameTest')
        # top_level.wm_attributes('-topmost', 1)
        self.top_level.resizable(width=False, height=False)
        screenwidth = self.top_level.winfo_screenwidth()
        screenheight = self.top_level.winfo_screenheight()
        width = 400
        height = 200
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.top_level.geometry(alignstr)
        frame1 = tk.Frame(self.top_level, width=360, height=120, borderwidth=2, padx=0, pady=0, relief="sunken")
        frame1.pack()
        frame1.place(x=20,y=20)

        # 期望图像显示的大小
        w_box = 96
        h_box = 96
        # 以一个PIL图像对象打开
        pil_image_sweep = Image.open(r'resources/sweeping.png')

        # get the size of the image
        # 获取图像的原始大小
        w, h = pil_image_sweep.size

        # resize the image so it retains its aspect ration
        # but fits into the specified display box
        # 缩放图像让它保持比例，同时限制在一个矩形框范围内
        pil_image_resized = resize(w, h, w_box, h_box, pil_image_sweep)

        # convert PIL image object to Tkinter PhotoImage object
        # 把PIL图像对象转变为Tkinter的PhotoImage对象
        sweep_pic = ImageTk.PhotoImage(pil_image_resized)

        # sweep_pic = tk.PhotoImage(file="ico/sweeping.png")
        sweep_pic_lab = tk.Button(frame1,width=96,height=96,image=sweep_pic,compound = tk.CENTER,command=self.start_sweep,relief='flat')
        sweep_pic_lab.place(x=10, y=10)
        # 五指棋
        pil_image_five = Image.open(r'resources/five.png')
        w1, h1 = pil_image_five.size
        resize(w1, h1, w_box, h_box, pil_image_five)
        five_pic = ImageTk.PhotoImage(resize(w1, h1, w_box, h_box, pil_image_five))
        five_pic_lab = tk.Button(frame1,width=96,height=96,image=five_pic,compound = tk.CENTER,command=self.start_five,relief='flat')
        five_pic_lab.pack()
        five_pic_lab.place(x=125, y=10)
        # 贪食蛇
        pil_image_snake = Image.open(r'resources/snake.png')
        w2, h2 = pil_image_snake.size
        resize(w2, h2, w_box, h_box, pil_image_snake)
        snake_pic = ImageTk.PhotoImage(resize(w2, h2, w_box, h_box, pil_image_snake))
        snake_pic_lab = tk.Button(frame1, width=96, height=96, image=snake_pic, compound=tk.CENTER,command=self.start_snake,relief='flat')
        snake_pic_lab.pack()
        snake_pic_lab.place(x=245, y=10)
        # 绘制标签frame
        frame2 = tk.Frame(self.top_level, width=360, height=30, borderwidth=2, padx=0, pady=0, relief="sunken")
        frame2.pack()
        frame2.place(x=20, y=150)
        # 绘制游戏标签
        sweep_lab = tk.Label(frame2,width=10,height=1,text='扫雷')
        sweep_lab.pack()
        sweep_lab.place(x=15,y=3)
        five_lab = tk.Label(frame2,width=10,height=1,text='五指棋')
        five_lab.pack()
        five_lab.place(x=135,y=3)
        snake_lab = tk.Label(frame2,width=10,height=1,text='Snake')
        snake_lab.pack()
        snake_lab.place(x=260,y=3)
        # 重写退出事件,还原主窗口
        self.top_level.protocol("WM_DELETE_WINDOW", lambda: self.exit_window(main_window=father_window, top_level=self.top_level))
        self.top_level.mainloop()

    def exit_window(self,main_window, top_level):
        try:
            main_window.state('normal')
        except:
            pass
        top_level.destroy()

    def start_sweep(self):
        self.top_level.state('icon')
        # 启用多线程，避免主窗口无响应
        new_t = threading.Thread(target=Sweeping().main,args=(self.top_level,))
        new_t.setDaemon(True)
        new_t.start()


    def start_five(self):
        self.top_level.state('icon')
        # 启用多线程，避免主窗口无响应
        new_t = threading.Thread(target=FiveInARow().main,args=(self.top_level,))
        new_t.setDaemon(True)
        new_t.start()

    def start_snake(self):
        self.top_level.state('icon')
        # 启用多线程，避免主窗口无响应
        new_t = threading.Thread(target=mySnake().main,args=(self.top_level,))
        new_t.setDaemon(True)
        new_t.start()

if __name__ == '__main__':
    GameSelect().draw_main_window()
