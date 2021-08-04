# -*- coding:utf-8 -*- 

"""
作者：luoyu
日期：2021年07月30日
"""

# -*- coding:utf-8 -*-

"""
作者：luoyu
日期：2021年07月30日
"""
import time
import os
import requests
import tkinter as tk
from tkinter import messagebox
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


class Update(object):
    def __init__(self):
        self.tree = ET.parse("./config/information.xml")
        self.root = self.tree.getroot()  # 获得root节点
        self.ip, self.port = self.get_ip_port()

    def check_version(self):
        # tree = ET.parse("./config/information.xml")
        # root = tree.getroot()  # 获得root节点
        local_ver = self.root.findall('application')[0].find('ver').text
        server_url = f'http://{self.ip}:{self.port}/information.xml'
        server_ver = 'EMPTY'
        try:
            xml = requests.get(server_url,timeout=1)
            bs = BeautifulSoup(xml.text, 'lxml')
            server_ver = bs.find_all('ver')[0].text
        except Exception as error:
            print(error)
        if local_ver == server_ver:
            print("未发现更新！")
        elif server_ver == "EMPTY":
            print("获取版本信息失败！")
        else:
            self.start_update()

    def start_update(self):
        self.window = tk.Tk()
        self.window.title('自动更新')
        self.window.geometry('300x150')
        lable1 = tk.Label(self.window, text='发现新版本，是否更新？', font=('Arial', 12), width=50, height=2)
        lable1.pack()
        button1 = tk.Button(self.window, text="确定", width=10, height=1, command=self.start_download)
        button2 = tk.Button(self.window, text="取消", width=10, height=1, command=self.quit_tk)
        button1.place(x=20, y=80)
        button2.place(x=180, y=80)
        self.var = tk.StringVar()
        tk.Label(self.window, textvariable=self.var, font=('Arial', 10), width=30, height=1).place(x=10, y=120)
        self.window.mainloop()

    def get_ip_port(self):
        ip = self.root.findall('application')[0].find('host').text
        port = self.root.findall('application')[0].find('port').text
        print(f"HOST:{ip} {port}")
        print(ip,port)
        return ip, port
        #
        # config_path = "config/"
        # cfg = ConfigParser()
        # cfg.read(config_path + "server.ini", encoding="utf-8")
        # configs = dict(cfg._sections)
        # ip_port = dict(configs['server'])
        # return ip_port['host'], ip_port['port']

    def start_download(self):
        # ip, port = self.get_ip_port()
        url = f'http://{self.ip}:{self.port}/update.exe'
        path = "d:\\tmp"
        if not os.path.exists(path):  # 看是否有该文件夹，没有则创建文件夹
            os.mkdir(path)
        start = time.time()  # 下载开始时间
        response = requests.get(url, stream=True)  # stream=True必须写上
        size = 0  # 初始化已下载大小
        chunk_size = 1024  # 每次下载的数据大小
        content_size = int(response.headers['content-length'])  # 下载文件总大小
        try:
            if response.status_code == 200:  # 判断是否响应成功
                si = content_size / chunk_size / 1024
                self.var.set('开始下载,文件大小：.2fMB'.format(size=si))
                # mw.lblInfo.setText()
                # mw.lblInfo.setVisible(True)
                filepath = path + '\\update.exe'
                with open(filepath, 'wb') as file:  # 显示进度条
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        rate = float(size / content_size * 100)
                        self.var.set('下载进度：%.2f%%' % rate)
                        self.window.update()
                        # mw.lblInfo.setText('下载进度：%.2f%%' % rate)
            end = time.time()  # 下载结束时间
            # mw.lblInfo.setText('下载完成，耗时：%.2f秒' % (end - start))
            self.var.set('下载完成，耗时：%.2f秒' % (end - start))
            self.window.update()
            time.sleep(1)
            self.is_open_exe()
            self.close_mainAPP()
        except Exception as e:
            # mw.lblInfo.setText('下载失败：%s' % e)
            self.var.set('下载失败：%s' % e)
            self.window.update()

    def close_mainAPP(self):
        os.sys.exit(0)

    def is_open_exe(self):
        cmd = "d:\\tmp\\update.exe"
        os.startfile(cmd)
        self.window.destroy()

    def show_error(self):
        tk.messagebox.showwarning('Update Error!')

    def quit_tk(self):
        self.window.destroy()


if __name__ == '__main__':
    Update().check_version()
