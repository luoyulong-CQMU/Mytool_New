# -*- coding:utf-8 -*- 

"""
作者：luoyu
日期：2021年01月06日
"""



class DiagFileModify(object):

    diag_dict = set()
    path = "config/diag.txt"
    def __init__(self):
        pass

    def read_file(self):

        file_dict = set()
        with open(DiagFileModify.path, encoding="utf-8-sig") as fo:
            for line in fo.readlines():
                print(line.strip())
                file_dict.add(line.strip())
                pass
        # file_list = list(file_dict)
    def add_diag_to_file(self):
        head = input("请输入关键词：")



if __name__ == '__main__':
    a = DiagFileModify()
    a.read_file()
