# -*- coding:utf-8 -*- 

"""
作者：luoyu
日期：2021年01月06日
"""
import time
import win32gui
import win32api
import win32con
import win32print
import win32ui
from tkinter import messagebox
import re
import datetime
import xlrd
import numpy as np
import cv2
import os
from PIL import ImageFont, ImageDraw, Image, ImageWin
from unit.database import *


def get_doctor_info():
    try:
        info = DataBase()
        doctor_name = info.get_name()
    except:
        doctor_name = "医师姓名"
    return doctor_name


def draw_pain_info(name, pain_id, rtime, rm, rd, sex, year, diag1, ctime):
    """
    绘制A4纸大小的图，内容由下列参数照感染病历卡填充
    :param name: 患者姓名
    :param pain_id: 患者住院号
    :param rtime: 入院时间
    :param rm: 入院_月
    :param rd: 入院_天
    :param sex: 性别
    :param year: 年龄
    :param diag1: 诊断
    :param ctime: 出院时间
    """
    # 读取数据库，获取医生姓名
    doctor_name = get_doctor_info()
    # print(diag1)
    img = np.zeros([3508, 2480, 3], np.uint8)
    img[:, :, 0] = np.zeros([3508, 2480]) + 255
    img[:, :, 1] = np.ones([3508, 2480]) + 254
    img[:, :, 2] = np.ones([3508, 2480]) * 255
    img2 = np.zeros([3508, 2480, 3], np.uint8) + 255
    cv2.waitKey(0)
    fontpath = "font/simsun.ttc"
    font = ImageFont.truetype(fontpath, 48)
    img_pil = Image.fromarray(img2)
    draw = ImageDraw.Draw(img_pil)
    draw.text((448, 485), name, font=font, fill=(0, 0, 0))
    draw.text((855, 485), pain_id, font=font, fill=(0, 0, 0))
    draw.text((1380, 477), str(rtime.year), font=font, fill=(0, 0, 0))
    draw.text((1710, 477), str(rm), font=font, fill=(0, 0, 0))
    draw.text((1890, 477), str(rd), font=font, fill=(0, 0, 0))

    draw.text((448, 630), sex, font=font, fill=(0, 0, 0))
    draw.text((855, 630), year, font=font, fill=(0, 0, 0))
    draw.text((1390, 620), "——", font=font, fill=(0, 0, 0))
    draw.text((1710, 620), "—", font=font, fill=(0, 0, 0))
    draw.text((1890, 620), "—", font=font, fill=(0, 0, 0))

    draw.text((420, 760), diag1[0], font=font, fill=(0, 0, 0))
    draw.text((1410, 750), "——", font=font, fill=(0, 0, 0))

    draw.text((500, 895), "——", font=font, fill=(0, 0, 0))
    draw.text((820, 895), "——", font=font, fill=(0, 0, 0))

    draw.text((460, 1315), "——", font=font, fill=(0, 0, 0))
    draw.text((840, 1315), "——", font=font, fill=(0, 0, 0))

    draw.text((420, 1440), "普内科", font=font, fill=(0, 0, 0))
    draw.text((845, 1440), doctor_name, font=font, fill=(0, 0, 0))

    draw.text((1550, 3137), str(ctime.year), font=font, fill=(0, 0, 0))
    draw.text((1760, 3137), str(ctime.month), font=font, fill=(0, 0, 0))
    draw.text((1930, 3137), str(ctime.day), font=font, fill=(0, 0, 0))

    bk_img = np.array(img_pil)
    cv2.waitKey()
    path_ = r'./cache'
    if not os.path.exists(path_):
        print(f"保存路径不存在！创建中. . .")
        os.mkdir(path_)

    cv2.imwrite("./cache/pain.jpg", bk_img)


def draw_quality(name, pain_id):
    """
    绘制A4纸张大小的图，内容由下列参数照病历质量评分标准表格填充
    :param name: 患者姓名
    :param pain_id: 患者住院号
    """
    # print(diag1)
    img = np.zeros([3508, 2480, 3], np.uint8)
    img[:, :, 0] = np.zeros([3508, 2480]) + 255
    img[:, :, 1] = np.ones([3508, 2480]) + 254
    img[:, :, 2] = np.ones([3508, 2480]) * 255
    img2 = np.zeros([3508, 2480, 3], np.uint8) + 255
    cv2.waitKey(0)
    fontpath = "font/simsun.ttc"
    font = ImageFont.truetype(fontpath, 48)
    img_pil = Image.fromarray(img2)
    draw = ImageDraw.Draw(img_pil)
    draw.text((300, 290), "普内科", font=font, fill=(0, 0, 0))
    draw.text((700, 290), name, font=font, fill=(0, 0, 0))
    draw.text((1200, 290), "罗玉龙", font=font, fill=(0, 0, 0))
    draw.text((1550, 290), pain_id, font=font, fill=(0, 0, 0))

    bk_img = np.array(img_pil)
    cv2.waitKey()
    cv2.imwrite("./cache/pain.jpg", bk_img)


def print_pain_info():
    """
    调用系统默认打印机，传入./cache/pain.jpg文件打印
    :return:
    """
    # Constants for GetDeviceCaps
    #
    #
    # HORZRES / VERTRES = printable area
    #
    HORZRES = 8
    VERTRES = 10
    #
    # LOGPIXELS = dots per inch
    #
    LOGPIXELSX = 88
    LOGPIXELSY = 90
    #
    # PHYSICALWIDTH/HEIGHT = total area
    #
    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111
    #
    # PHYSICALOFFSETX/Y = left / top margin
    #
    PHYSICALOFFSETX = 112
    PHYSICALOFFSETY = 50  # 113

    printer_name = win32print.GetDefaultPrinter()
    file_name = "./cache/pain.jpg"

    # You can only write a Device-independent bitmap
    # directly to a Windows device context; therefore
    # we need (for ease) to use the Python Imaging
    # Library to manipulate the image.
    #
    # Create a device context from a named printer
    # and assess the printable size of the paper.
    #
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)
    printable_area = hDC.GetDeviceCaps(HORZRES), hDC.GetDeviceCaps(VERTRES)
    printer_size = hDC.GetDeviceCaps(PHYSICALWIDTH), hDC.GetDeviceCaps(PHYSICALHEIGHT)
    printer_margins = hDC.GetDeviceCaps(PHYSICALOFFSETX), hDC.GetDeviceCaps(PHYSICALOFFSETY)

    #
    # Open the image, rotate it if it's wider than
    # it is high, and work out how much to multiply
    # each pixel by to get it as big as possible on
    # the page without distorting.
    #
    bmp = Image.open(file_name)
    # if bmp.size[0] > bmp.size[1]:
    #     bmp = bmp.rotate(90,expand=True)

    ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
    scale = min(ratios)

    #
    # Start the print job, and draw the bitmap to
    # the printer device at the scaled size.
    #
    hDC.StartDoc(file_name)
    hDC.StartPage()

    dib = ImageWin.Dib(bmp)
    scaled_width, scaled_height = [int(scale * i) for i in bmp.size]
    x1 = int((printer_size[0] - scaled_width) / 2)
    y1 = int((printer_size[1] - scaled_height) / 2)
    x2 = x1 + scaled_width
    y2 = y1 + scaled_height
    dib.draw(hDC.GetHandleOutput(), (x1, y1, x2, y2))

    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()


def show_window_attr(hWnd):
    '''
    显示窗口的属性
    :return:
    '''

    if not hWnd:
        return

    # 中文系统默认title是gb2312的编码
    title = win32gui.GetWindowText(hWnd)
    # title = gbk2utf8(title)
    clsname = win32gui.GetClassName(hWnd)


def show_windows(hWndList):
    for h in hWndList:
        show_window_attr(h)


def data_base(name="张三", gender="男", id_="123456", rtime_=None, ctime_=None, diag_=None):
    # print("信息写入数据库")
    # print(rtime_,type(rtime_))
    # print(diag_,type(diag_))
    diag_ = "|".join(diag_)
    conn = sqlite3.connect("pain_info.db")
    cursor = conn.cursor()
    try:
        cursor.execute("create table info(name, gender, id_  primary key,rtime,ctime,diag_ varchar(255))")
    except:
        # print('table 已存在')
        pass
    try:
        cursor.execute("insert into info (name, gender, id_,rtime,ctime,diag_) values (?, ?,?,?,?,?)",
                       (name.strip(b'\x00'.decode()), gender.strip(b'\x00'.decode()), id_.strip(b'\x00'.decode()), rtime_, ctime_, diag_.strip(b'\x00'.decode())))
        # print(f"-->{name} 信息写入成功！")
    except Exception as e:
        # print(e)
        pass
    conn.commit()
    # print("*" * 50)
    conn.close()


class ReportCard(object):

    def __init__(self):
        self.pain_name = ""
        self.pain_gender = ""
        self.pain_year = ""
        self.pain_in_time = ""
        self.pain_bed = ""
        self.pain_days = ""
        self.pain_id = ""
        self.pain_diag = ""
        self.rY = ""
        self.rm = ""
        self.rd = ""
        self.rtime = datetime.datetime
        self.ctime = datetime.datetime
        self.diag1 = ""

    def format_pain_message(self):
        """
        病例报告卡处理程序
        1.从pain_message从窗体查找信息；
        2.出院信息填入pain_info列表中；
        3.通过遍历列表，取出为空的字符及转义字符；
        4.赋值给参数；
        :return:
        """

        pain_info = self.pain_message()
        pain_message = []
        for i in pain_info:
            if i == "\x00":
                pass
            else:
                pain_message.append(i)
        self.pain_name = pain_message[0]
        self.pain_gender = pain_message[1]
        self.pain_year = pain_message[2]
        self.pain_in_time = pain_message[3]
        self.pain_bed = pain_message[7]
        self.pain_days = pain_message[8]
        self.pain_id = pain_message[11][-8:]
        self.pain_diag = pain_message[12][3:].split(',')
        if len(self.pain_in_time) <= 6:
            self.out_message.set('你似乎选错了对象！')
            # print("Error:你似乎选错了对象，请确认\n")
        else:
            # print("\n-----------------------------------")
            # print('找到患者信息：')
            # # print(self.pain_name)
            #
            # print("姓名：%s" % self.pain_name, "性别：%s" % self.pain_gender, "年龄：%s" % self.pain_year,
            #       "住院号：%s" % self.pain_id)
            self.out_message.set(f'姓名:{self.pain_name.ljust(8," ")}||ID:{self.pain_id}"')

            #      f'|  住院号:{self.pain_id} |年龄:{self.pain_year}\t|\r\n'
            #      # f'|  住院号:{self.pain_id} \t|\r\n'
            #       '+-------------------------------+'
            # )

            # print(f'''
            # +-------------------------------+
            # |  找到患者信息：                  |
            # +-------------------------------+
            # |  姓名:{self.pain_name}                    |
            # |  性别:{self.pain_gender}                       |
            # |  年龄:{self.pain_year}                       |
            # |  住院号:{self.pain_id}                |
            # +-------------------------------+
            # ''')
            # 处理年、月、日格式格式；
            self.rY = int(self.pain_in_time[0:4])
            self.rm = int(self.pain_in_time[5:7])
            self.rd = int(self.pain_in_time[8:10])
            find = re.findall(r"\d+", self.pain_days)
            day = find[0]
            self.rtime = datetime.date(self.rY, self.rm, self.rd)
            self.ctime = self.rtime + datetime.timedelta(days=int(day))
            # print(
            #     # '+-------------------------------+\r\n'
            #     f'|  入院时间：{str(self.rtime).ljust(19," ")}|\r\n'
            #     f'|  出院时间：{str(self.ctime).ljust(19," ")}|\r\n'
            #     '+-------------------------------+'
            # )
            # print("入院时间：", self.rtime)
            # print("出院时间：", self.ctime)
            # print("-----------------------------------\n")
            icd = 'config/ICD10.xls'
            icd10 = []
            workbook = xlrd.open_workbook(icd)
            worksheet = workbook.sheet_by_index(0)

            for i in range(worksheet.nrows):
                bm = worksheet.cell_value(worksheet.nrows - i - 1, 0)
                icd10.append(bm)
                self.diag1 = []
            for i in range(len(self.pain_diag)):
                var = self.pain_diag[i]
                for j in range(len(icd10)):
                    var1 = icd10[j]
                    if var1 in var:
                        # print(f'|  找到编码:{var[:12].ljust(15,".")}|')
                        var3 = var.replace(var1, '')
                        self.diag1.append(var3)
                    j += 1
                i += 1
            data_base(name=self.pain_name, gender=self.pain_gender, id_=self.pain_id, rtime_=str(self.rtime),
                      ctime_=str(self.ctime), diag_=self.diag1)
            # print('+-------------------------------+')
            if len(self.diag1) == 0:
                self.out_message.set('未完成首页填写，或填写后未刷新界面，请重试')
                # print("Error:似乎未完成首页填写，或填写后未刷新界面，请重试\n")
            else:
                pass

    def report_card(self, out_message=None):
        """
        感染病例报告卡打印调用程序
        :return:
        """
        # 调用格式化信息
        self.out_message = out_message
        self.format_pain_message()
        draw_pain_info(self.pain_name, self.pain_id,
                       self.rtime, self.rm, self.rd,
                       self.pain_gender, self.pain_year,
                       self.diag1, self.ctime)
        select = messagebox.askyesno(title='请确认',message=f'准备打印，请放入纸张，并确认信息【{self.pain_name}】是否正确？')
        # select = input("准备打印，请放入纸张，并确认信息是否正确？ [Y/n]: ")
        # if select == "n" or select == "no" or select == "N":
        if select:
            print_pain_info()
        else:
            self.out_message.set('你取消了打印！')


    def quality(self,outmessage=None):
        """
        病历质量评分标准卡打印系统
        :return:
        """
        self.out_message = outmessage
        # 调用信息格式化程序
        self.format_pain_message()
        draw_quality(self.pain_name, self.pain_id)
        select = messagebox.askyesno('请选择',f'准备打印，请放入纸张，并确认信息【{self.pain_name}】是否正确？')
        # select = input("准备打印，请放入纸张，并确认信息是否正确？ [Y/n]: ")
        if select:
            print_pain_info()
        else:
            self.out_message.set('你取消了打印!')


    def get_child_windows(self, parent):
        """
        演示如何列出所有的子窗口
        :param parent: 父窗口句柄
        :return:
        """
        if not parent:
            return
        hwnd_child_list = []
        win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwnd_child_list)
        show_windows(hwnd_child_list)
        return hwnd_child_list

    @staticmethod
    def get_text(number):
        """
        获取edit 窗体的内容信息，非窗体标题；注意：中文字符2字节；
        :param number: edit 窗体句柄id
        :return:
        """
        lens = win32gui.SendMessage(number, win32con.WM_GETTEXTLENGTH) + 1
        new_lens = lens * 2 + 2
        buffer = win32gui.PyMakeBuffer(new_lens)
        win32api.SendMessage(number, win32con.WM_GETTEXT, new_lens, buffer)
        address, result_lens = win32gui.PyGetBufferAddressAndLen(buffer)
        text = win32gui.PyGetString(address, result_lens)
        return text[:lens]

    def pain_message(self):
        """
        获取患者信息
        :return:
        """
        """
        ###########
        windowname = '中联基层医疗卫生机构综合信息系统'
        hwnd = win32gui.FindWindow(0, windowname)
        zhwnd = win32gui.FindWindowEx(hwnd, 0, 0, None)
        for i in range(2):
            zhwnd = win32gui.FindWindowEx(zhwnd, 0, 0, None)

        zhwnd = win32gui.FindWindowEx(zhwnd, 0, 0, "住院医生站")

        zhwnd = win32gui.FindWindowEx(zhwnd, 0, 0, None)

        designHostid = win32gui.FindWindowEx(zhwnd, 0, 0, None)

        hWndChildList = get_child_windows(designHostid)
        ###########
        """
        window_title = "中联基层医疗卫生机构综合信息系统"
        hwnd = win32gui.FindWindow(0, window_title)
        z_hwnd = win32gui.FindWindowEx(hwnd, 0, 0, None)
        for i in range(2):
            z_hwnd = win32gui.FindWindowEx(z_hwnd, 0, 0, None)
        z_hwnd = win32gui.FindWindowEx(z_hwnd, 0, 0, "住院医生站")
        z_hwnd = win32gui.FindWindowEx(z_hwnd, 0, 0, None)
        design_host_id = win32gui.FindWindowEx(z_hwnd, 0, 0, None)
        hwnd_child_list = self.get_child_windows(design_host_id)
        for i in range(len(hwnd_child_list)):
            pain = win32gui.GetWindowText(hwnd_child_list[i])
            if pain == '病人信息':
                break
        layout_id = win32gui.FindWindowEx(hwnd_child_list[i], 0, 0, None)
        layout_id_childs = self.get_child_windows(layout_id)
        pain_info = []
        for i in range(15, len(layout_id_childs)):
            message = self.get_text(layout_id_childs[i])
            if message == '':
                pass
            else:
                pain_info.append(message)
        return pain_info


if __name__ == '__main__':
    a = ReportCard()
    a.report_card()
