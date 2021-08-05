
"""
作者：luoyu
日期：2021年01月05日
"""
from interval import Interval
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog,QMainWindow
from unit.blood_gas_main_window import *
from unit.setting import *


class BloodGas(Ui_mainWindow):
    """血气分析"""

    def __init__(self):
        super().__init__()
        # 获得吸氧浓度
        self.main_window = None
        self.nd = 0.21

    def setupUi(self, mainWindow):
        """重写父类"""

        super().setupUi(mainWindow)
        # 设置button样式表覆盖
        # border - radius: 0px;
        # border: 1pxsolid  # C0C0C0;
        self.pushButton.setStyleSheet(
            '''
            QPushButton{
                border: 2px groove gray;
                background-color:#FFFFFF;
                border-style: solid;
                border-radius: 5px;  
                width: 100px;
                height:20px;
                padding:0 0px;
            }

            QPushButton:hover{
                border: 2px solid #E3C46F;
                background-color:#FEF4BF;
                border-style: solid;
                border-radius:5px;
                width: 40px;
                height:20px;
                padding:0 0px;
            }
            QPushButton:pressed{
                background-color:#EAF0FF;
                border: 2px solid #AAB4C4;
                width: 40px;
                height:20px;
                padding:0 0px;
                border-radius:3px;
            } ''')
        self.pushButton_2.setStyleSheet(
            '''
            QPushButton{
                border: 2px groove gray;
                background-color:#FFFFFF;
                border-style: solid;
                border-radius: 5px;  
                width: 100px;
                height:20px;
                padding:0 0px;
            }

            QPushButton:hover{
                border: 2px solid #E3C46F;
                background-color:#FEF4BF;
                border-style: solid;
                border-radius:5px;
                width: 40px;
                height:20px;
                padding:0 0px;
            }
            QPushButton:pressed{
                background-color:#EAF0FF;
                border: 2px solid #AAB4C4;
                width: 40px;
                height:20px;
                padding:0 0px;
                border-radius:3px;
            } ''')
        self.main_window = mainWindow
        self.limit_input()
        # 设置窗体调用
        self.actionSetting.triggered.connect(SetDialog)
        # 帮助窗口调用
        self.actionguanyu.triggered.connect(self.show_help_dialog)
        # 开始计算
        self.pushButton.clicked.connect(self.start_cal)
        # 输出内容到text并复制
        self.pushButton_2.clicked.connect(self.convert_out)

    def limit_input(self):
        """输入限限制器"""

        # 整数校验器 [1,99]
        int_validator = QIntValidator(None)
        int_validator.setRange(1, 99)
        # 浮点校验器 [-360,360]，精度：小数点后2位
        double_validator = QDoubleValidator(None)
        double_validator.setRange(-360, 360)
        double_validator.setNotation(QDoubleValidator.StandardNotation)
        # 设置精度，小数点2位
        double_validator.setDecimals(3)
        self.year.setValidator(int_validator)
        self.ph.setValidator(double_validator)
        self.pco2.setValidator(double_validator)
        self.po2.setValidator(double_validator)
        self.hct.setValidator(double_validator)
        self.thb.setValidator(int_validator)
        self.na.setValidator(double_validator)
        self.k.setValidator(double_validator)
        self.cl.setValidator(double_validator)
        self.ca.setValidator(double_validator)
        self.lac.setValidator(double_validator)
        self.glu.setValidator(double_validator)
        self.so2.setValidator(double_validator)
        self.cto2.setValidator(int_validator)
        self.ab.setValidator(double_validator)
        self.sb.setValidator(double_validator)
        self.be.setValidator(double_validator)
        self.ag.setValidator(double_validator)
        self.pop.setValidator(double_validator)
        self.ri.setValidator(double_validator)
        self.tmp.setValidator(double_validator)
        self.pa.setValidator(double_validator)

    def henderseon_hasselbach(self):
        """平衡校验公式"""
        result = "酸碱失衡超出预期，无法根据Henderson-Hasselbach公式校验，请检查结果"
        h = 24 * float(self.pco2.text()) / float(self.ab.text())
        if h in Interval(22, 25, upper_closed=False):
            if float(self.ph.text()) in Interval(7.60, 7.65, lower_closed=False):
                result = "根据Henderson-Hasselbach公式，内在一致性校验通过\n[H+]：%.2f(mmol/L);PH参考区间：[%.2f, %.2f)" % (h, 7.60, 7.65)
            else:
                result = "根据Henderson-Hasselbach公式，内在一致性校验失败，血气结果可能不准确。\n[H+]：%.2f(mmol/L) ;PH参考区间：[%.2f, %.2f)" % (h, 7.60, 7.65)
        elif h in Interval(25, 28, upper_closed=False):
            if float(self.ph.text()) in Interval(7.55, 7.60, lower_closed=False):
                result = "根据Henderson-Hasselbach公式，内在一致性校验通过\n[H+]：%.2f(mmol/L);PH参考区间：[%.2f, %.2f)" % (h, 7.55, 7.60)
            else:
                result = "根据Henderson-Hasselbach公式，内在一致性校验失败，血气结果可能不准确。\n[H+]：%.2f(mmol/L) ;PH参考区间：[%.2f, %.2f)" % (h, 7.55, 7.60)
        elif h in Interval(28, 32, upper_closed=False):
            if float(self.ph.text()) in Interval(7.50, 7.55, lower_closed=False):
                result = "根据Henderson-Hasselbach公式，内在一致性校验通过\n[H+]：%.2f(mmol/L);PH参考区间：[%.2f, %.2f)" % (h, 7.50, 7.55)
            else:
                result = "根据Henderson-Hasselbach公式，内在一致性校验失败，血气结果可能不准确。\n[H+]：%.2f(mmol/L) ;PH参考区间：[%.2f, %.2f)" % (h, 7.50, 7.55)
        elif h in Interval(32, 35, upper_closed=False):
            if float(self.ph.text()) in Interval(7.45, 7.50, lower_closed=False):
                result = "根据Henderson-Hasselbach公式，内在一致性校验通过\n[H+]：%.2f(mmol/L);PH参考区间：[%.2f, %.2f)" % (h, 7.45, 7.50)
            else:
                result = "根据Henderson-Hasselbach公式，内在一致性校验失败，血气结果可能不准确。\n[H+]：%.2f(mmol/L) ;PH参考区间：[%.2f, %.2f)" % (h, 7.45, 7.50)
        elif h in Interval(35, 40, upper_closed=False):
            if float(self.ph.text()) in Interval(7.40, 7.45, lower_closed=False):
                result = "根据Henderson-Hasselbach公式，内在一致性校验通过\n[H+]：%.2f(mmol/L);PH参考区间：[%.2f, %.2f)" % (h, 7.40, 7.45)
            else:
                result = "根据Henderson-Hasselbach公式，内在一致性校验失败，血气结果可能不准确。\n[H+]：%.2f(mmol/L) ;PH参考区间：[%.2f, %.2f)" % (h, 7.40, 7.45)
        elif h in Interval(40, 45, upper_closed=False):
            if float(self.ph.text()) in Interval(7.35, 7.40, lower_closed=False):
                result = "根据Henderson-Hasselbach公式，内在一致性校验通过\n[H+]：%.2f(mmol/L);PH参考区间：[%.2f, %.2f)" % (h, 7.35, 7.40)
            else:
                result = "根据Henderson-Hasselbach公式，内在一致性校验失败，血气结果可能不准确。\n[H+]：%.2f(mmol/L) ;PH参考区间：[%.2f, %.2f)" % (h, 7.35, 7.40)
        elif h in Interval(45, 50, upper_closed=False):
            if float(self.ph.text()) in Interval(7.30, 7.35, upper_closed=False):
                result = "根据Henderson-Hasselbach公式，内在一致性校验通过\n[H+]：%.2f(mmol/L);PH参考区间：[%.2f, %.2f)" % (h, 7.45, 7.30)
            else:
                result = "根据Henderson-Hasselbach公式，内在一致性校验失败，血气结果可能不准确。\n[H+]：%.2f(mmol/L) ;PH参考区间：[%.2f, %.2f)" % (h, 7.45, 7.30)
        elif h in Interval(50, 56, upper_closed=False):
            if float(self.ph.text()) in Interval(7.25, 7.30, lower_closed=False):
                result = "根据Henderson-Hasselbach公式，内在一致性校验通过\n[H+]：%.2f(mmol/L);PH参考区间：[%.2f, %.2f)" % (h, 7.25, 7.30)
            else:
                result = "根据Henderson-Hasselbach公式，内在一致性校验失败，血气结果可能不准确。\n[H+]：%.2f(mmol/L) ;PH参考区间：[%.2f, %.2f)" % (h, 7.25, 7.30)
        elif h in Interval(56, 63, upper_closed=False):
            if float(self.ph.text()) in Interval(7.20, 7.25, lower_closed=False):
                result = "根据Henderson-Hasselbach公式，内在一致性校验通过\n[H+]：%.2f(mmol/L);PH参考区间：[%.2f, %.2f)" % (h, 7.20, 7.25)
            else:
                result = "根据Henderson-Hasselbach公式，内在一致性校验失败，血气结果可能不准确。\n[H+]：%.2f(mmol/L) ;PH参考区间：[%.2f, %.2f)" % (h, 7.20, 7.25)
        elif h in Interval(63, 71, upper_closed=False):
            if float(self.ph.text()) in Interval(7.15, 7.20, lower_closed=False):
                result = "根据Henderson-Hasselbach公式，内在一致性校验通过\n[H+]：%.2f(mmol/L);PH参考区间：[%.2f, %.2f)" % (h, 7.15, 7.20)
            else:
                result = "根据Henderson-Hasselbach公式，内在一致性校验失败，血气结果可能不准确。\n[H+]：%.2f(mmol/L) ;PH参考区间：[%.2f, %.2f)" % (h, 7.15, 7.20)
        elif h in Interval(71, 79, upper_closed=False):
            if float(self.ph.text()) in Interval(7.10, 7.15, lower_closed=False):
                result = "根据Henderson-Hasselbach公式，内在一致性校验通过\n[H+]：%.2f(mmol/L);PH参考区间：[%.2f, %.2f)" % (h, 7.10, 7.15)
            else:
                result = "根据Henderson-Hasselbach公式，内在一致性校验失败，血气结果可能不准确。\n[H+]：%.2f(mmol/L) ;PH参考区间：[%.2f, %.2f)" % (h, 7.10, 7.15)
        elif h in Interval(79, 89, upper_closed=False):
            if float(self.ph.text()) in Interval(7.05, 7.10, lower_closed=False):
                result = "根据Henderson-Hasselbach公式，内在一致性校验通过\n[H+]：%.2f(mmol/L);PH参考区间：[%.2f, %.2f)" % (h, 7.05, 7.10)
            else:
                result = "根据Henderson-Hasselbach公式，内在一致性校验失败，血气结果可能不准确。\n[H+]：%.2f(mmol/L) ;PH参考区间：[%.2f, %.2f)" % (h, 7.05, 7.10)
        elif h in Interval(89, 100):
            if float(self.ph.text()) in Interval(7.00, 7.05):
                result = "根据Henderson-Hasselbach公式，内在一致性校验通过\n[H+]：%.2f(mmol/L);PH参考区间：[%.2f, %.2f)" % (h, 7.00, 7.05)
            else:
                result = "根据Henderson-Hasselbach公式，内在一致性校验失败，血气结果可能不准确。\n[H+]：%.2f(mmol/L);PH参考区间：[%.2f, %.2f)" % (h, 7.00, 7.05)
        split = str("-"*50)
        self.textBrowser.append(result)
        self.textBrowser.append(split)



    def respiratory_failure(self):
        """呼吸衰竭的判断"""

        result = ""
        if float(self.po2.text()) > 60 and float(self.pco2.text()) < 50:
            result = "无呼吸衰竭"
        elif float(self.po2.text()) > 60 and float(self.pco2.text()) >= 50:
            if self.nd == 0.21:
                result = "低通气综合征（高碳酸血症）"
            else:
                result = "II型呼吸衰竭"
        elif float(self.po2.text()) <= 60 and float(self.pco2.text()) < 50:
            result = "I型呼吸衰竭"
        elif float(self.po2.text()) <= 60 and float(self.pco2.text()) >= 50:
            result = "II型呼吸衰竭"
        return result

    def diagnostics(self):
        """酸碱失衡的计算"""

        # 清空输出窗口
        self.textBrowser.clear()

        # 酸碱失衡校验器
        self.henderseon_hasselbach()
        # 获取吸氧浓度
        self.nd = self.oxygen.currentText()
        delta_ag = float(self.ag.text()) - 12
        q_hco3 = delta_ag + float(self.ab.text())
        check_cl_min = float(self.na.text()) - 40 - 2
        check_cl_max = float(self.na.text()) - 40 + 2

        # 定义空值字符串
        var = ""
        var1 = ""

        if float(self.ph.text()) > 7.45:
            if float(self.pco2.text()) > 40:
                delta_hco3 = 24 - float(self.ab.text())
                delta_pco2 = 40 + 0.9 * abs(delta_hco3)
                pco2_hope = Interval(delta_pco2 - 5, delta_pco2 + 5)
                if float(self.pco2.text()) in pco2_hope:
                    var = '代谢性碱中毒'
                elif float(self.pco2.text()) < delta_pco2 - 5:
                    var = '代谢性碱中毒合并呼吸性碱中毒'
                else:  # 代偿极限，55；
                    var = '代谢性碱中毒合并呼吸性酸中毒失代偿'
            else:
                delta_pco2 = 40 - float(self.pco2.text())
                delta_hco3 = 24 - abs(delta_pco2) * 0.2
                hco3_hope = Interval(delta_hco3 - 2.5, delta_hco3 + 2.5)
                if float(self.ab.text()) in hco3_hope:
                    var = '呼吸性碱中毒'
                elif float(self.ab.text()) > delta_hco3 + 2.5:
                    var = '呼吸性碱中毒合并代谢性碱中毒失代偿'
                else:
                    var = '呼吸性碱中毒合并代谢性酸中毒失代偿'

        elif float(self.ph.text()) < 7.35:
            if float(self.pco2.text()) > 40:
                delta_pco2 = float(self.pco2.text()) - 40
                delta_hco3 = 24 + 0.35 * abs(delta_pco2)
                hco3_hope = Interval(delta_hco3 - 5.58, delta_hco3 + 5.58)
                if float(self.ab.text()) in hco3_hope:
                    var = '呼吸性酸中毒'
                elif float(self.ab.text()) > delta_hco3 + 5.58:
                    var = '呼吸性酸中毒合并代谢性碱中毒'
                else:
                    var = '呼吸性酸中毒合并代谢性酸中毒'
            else:
                delta_pco2 = 1.5 * float(self.ab.text()) + 8
                pco2_hope = Interval(delta_pco2 - 2, delta_pco2 + 2)
                if float(self.pco2.text()) in pco2_hope:
                    var = '代谢性酸中毒'
                elif float(self.pco2.text()) < delta_pco2 - 2:
                    var = '代谢性酸中毒合并呼吸性碱中毒'
                else:
                    var = '代谢性酸中毒合并呼吸性酸中毒'

        elif 7.35 <= float(self.ph.text()) < 7.4:
            if float(self.pco2.text()) < 35:
                delta_pco2 = 1.5 * float(self.ab.text()) + 8
                pco2_hope = Interval(delta_pco2 - 2, delta_pco2 + 2)
                if float(self.pco2.text()) in pco2_hope:
                    var = '代谢性酸中毒'
                elif float(self.pco2.text()) < delta_pco2 - 2:
                    var = '代谢性酸中毒合并呼吸性碱中毒'
                else:
                    var = '输入可能有误？'
            elif float(self.pco2.text()) > 45:
                delta_pco2 = float(self.pco2.text()) - 40
                delta_hco3 = 24 + 0.35 * abs(delta_pco2)
                hco3_hope = Interval(delta_hco3 - 5.58, delta_hco3 + 5.58)
                if float(self.ab.text()) in hco3_hope:
                    var = '呼吸性酸中毒'
                elif float(self.ab.text()) > delta_hco3 + 5.58:
                    var = '呼吸性酸中毒合并代谢性碱中毒'
                else:
                    var = '输入可能有误？'

        elif 7.4 <= float(self.ph.text()) <= 7.45:
            if float(self.pco2.text()) < 35:
                delta_pco2 = 40 - float(self.pco2.text())
                delta_hco3 = 24 - abs(delta_pco2) * 0.2
                hco3_hope = Interval(delta_hco3 - 2.5, delta_hco3 + 2.5)
                if float(self.ab.text()) in hco3_hope:
                    var = '呼吸性碱中毒'
                else:
                    var = '呼吸性碱中毒合并代谢性酸中毒代偿期'
            else:
                delta_hco3 = 24 - float(self.ab.text())
                delta_pco2 = 40 + 0.9 * abs(delta_hco3)
                pco2_hope = Interval(delta_pco2 - 5, delta_pco2 + 5)
                if float(self.pco2.text()) in pco2_hope:
                    var = '代谢性碱中毒'
                elif float(self.pco2.text()) < delta_pco2 - 5:
                    var = '数值可能有误？'
                else:  # 代偿极限，55；
                    var = '代谢性碱中毒合并呼吸性酸中毒代偿'
        if float(self.ag.text()) <= 16:
            if 22 <= q_hco3 <= 27:
                var1 = var
            elif q_hco3 < 22:
                if '代谢性酸中毒' in var:
                    var2 = var.replace('代谢性酸中毒', ' ( 高氯）代谢性酸中毒')
                    var1 = var2 + '\r' + '标准氯：' + str(check_cl_min) + 'mmol/L'
                else:
                    var1 = var + '并存 (高氯）代谢性酸中毒' + '\r' + '标准氯：' + str(check_cl_min) + 'mmol/L'
            else:
                if '代谢性碱中毒' in var:
                    pass
                else:
                    var1 = var + '并存代谢性碱中毒'
        else:
            if 22 <= q_hco3 <= 27:  # 判断单纯高AG代酸
                if '代谢性酸中毒' in var:
                    var2 = var.replace('代谢性酸中毒', ' ( 高阴离子间隙）代谢性酸中毒')
                    var1 = var2
                else:
                    var1 = var + '并存 (高阴离子间隙）代谢性酸中毒'
            elif q_hco3 < 22:
                if '代谢性酸中毒' in var:
                    var2 = var.replace('代谢性酸中毒', ' ( 高阴离子间隙）代谢性酸中毒并存（高氯）代谢性酸中毒')

                    var1 = var2 + '\r' + '标准氯：' + str(check_cl_min) + 'mmol/L'
                else:
                    var1 = var + '并存 (高阴离子间隙）代谢性酸中毒并存（高氯）代谢性酸中毒' + '\r' + '标准氯：' + str(check_cl_min) + 'mmol/L'
            else:
                if '代谢性酸中毒' in var:
                    var2 = var.replace('代谢性酸中毒', ' ( 高阴离子间隙）代谢性酸中毒')
                    if '代谢性碱中毒' in var2:
                        var1 = var2
                    else:
                        var1 = var2 + '并存代谢性碱中毒'
                else:
                    if '代谢性碱中毒' in var:
                        var1 = var + '并存（高阴离子间隙）代谢性酸中毒'
                    else:
                        var1 = var + '并存（高阴离子间隙）代谢性酸中毒' + '并存代谢性碱中毒'
        var5 = self.respiratory_failure()
        split = str("-" * 50)
        result = "酸碱平衡计算结果：\n" + var1 + "\n" + split + "\n呼吸衰竭判断结果：\n" + var5
        return result

    def convert_out(self):
        """判断为空字符，整合输入结果，拼接字符串，输出到窗体以供复制"""

        result = []
        self.textBrowser.clear()
        if len(self.ph.text()) != 0:
            v_ph = "PH:%s" % self.ph.text()
            result.append(v_ph)
        if len(self.pco2.text()) != 0:
            v_pco2 = "PCO2:%smmHg" % self.pco2.text()
            result.append(v_pco2)
        if len(self.po2.text()) != 0:
            v_po2 = "PO2:%smmHg" % self.po2.text()
            result.append(v_po2)
        if len(self.hct.text()) != 0:
            v_hct = "Hct:%s%%" % self.hct.text()
            result.append(v_hct)
        if len(self.thb.text()) != 0:
            v_thb = "HGB:%sg/L" % str(float(self.thb.text()) * 10)
            result.append(v_thb)
        if len(self.na.text()) != 0:
            v_na = "Na+:%smmol/L" % self.na.text()
            result.append(v_na)
        if len(self.k.text()) != 0:
            v_k = "K+:%smmol/L" % self.k.text()
            result.append(v_k)
        if len(self.cl.text()) != 0:
            v_cl = "Cl-:%smmol/L" % self.cl.text()
            result.append(v_cl)
        if len(self.ca.text()) != 0:
            v_ca = "Ca2+:%smmol/L" % self.ca.text()
            result.append(v_ca)
        if len(self.lac.text()) != 0:
            v_lac = "Lac:%smmol/L" % self.lac.text()
            result.append(v_lac)
        if len(self.glu.text()) != 0:
            v_glu = "Glu:%smmol/L" % self.glu.text()
            result.append(v_glu)
        if len(self.so2.text()) != 0:
            v_so2 = "SaO2:%s%%" % self.so2.text()
            result.append(v_so2)
        # TODO 这里的ct02 在定义pyqt时应该为ctCo2，现未修改；直接屌用
        if len(self.cto2.text()) != 0:
            v_ctco2 = "CtCO2:%smmol/L" % self.cto2.text()
            result.append(v_ctco2)
        if len(self.ab.text()) != 0:
            v_ab = "AbHCO3+:%smmol/L" % self.ab.text()
            result.append(v_ab)
        if len(self.sb.text()) != 0:
            v_sb = "SbHCO3+:%smmol/L" % self.sb.text()
            result.append(v_sb)
        if len(self.be.text()) != 0:
            v_be = "BE:%smmol/L" % self.be.text()
            result.append(v_be)
        if len(self.ag.text()) != 0:
            v_ag = "AG+:%smmol/L" % self.ag.text()
            result.append(v_ag)
        if len(self.pop.text()) != 0:
            v_pop = "渗透压:%smmol/L" % self.pop.text()
            result.append(v_pop)
        if len(self.ri.text()) != 0:
            v_ri = "呼吸指数：%s" % self.ri.text()
            result.append(v_ri)
        if len(self.tmp.text()) != 0:
            v_t = "T:%s℃" % self.tmp.text()
            result.append(v_t)
        result1 = '、'.join(result)
        # 复制到剪切板
        clipboard = QApplication.clipboard()
        clipboard.setText(result1)
        self.textBrowser.append(str(result1))

    def start_cal(self):
        """开始计算酸碱失衡"""

        if (
                len(self.ph.text()) == 0 or
                len(self.po2.text()) == 0 or
                len(self.po2.text()) == 0 or
                len(self.ag.text()) == 0 or
                len(self.ab.text()) == 0 or
                len(self.cl.text()) == 0 or
                len(self.na.text()) == 0):
            self.show_warning()
        else:
            result = self.diagnostics()
            self.textBrowser.append(str(result))
            split = str("-"*50)
            warning = "计算结果仅供参考"
            self.textBrowser.append(split)
            self.textBrowser.append(warning)

    def show_warning(self):
        warning_text = "<p>PH、PCO2、PO2、Ag、Ab、Na、Cl为必填项目，否则程序无法进行准确计算</p>"
        QMessageBox.warning(self.main_window, '警告', warning_text)

    def show_help_dialog(self):
        """帮助信息窗体"""

        help_text = "<P>这是一个简易的血气分析软件     版本：1.5</P><p> by：十号风球</p><p>" \
                     "项目地址：https://github.com/luoyulong-CQMU</p>"
        QMessageBox.about(self.main_window, '说明', help_text)


class SetDialog(QDialog, Ui_Dialog):
    """公式选择器"""

    setting_ui = Ui_Dialog()

    def __init__(self):
        super().__init__()
        self.set_ui()

    def set_ui(self):
        var = "<center>《诊断学》第八版公式</center>" \
              "<p>呼吸性酸中毒：<p>" \
              "<p>急性：ΔHCO<SUB>3</SUB><sup>-</sup>=ΔP<sub>a</sub>CO<sub>2</sub>x0.07±1.5<p>" \
              "<p>慢性：ΔHCO<SUB>3</SUB><sup>-</sup>=ΔP<sub>a</sub>CO<sub>2</sub>x0.35±5.58<p>" \
              "<p>呼吸性碱中毒：</p>" \
              "<p>急性：ΔHCO<SUB>3</SUB><sup>-</sup>=ΔP<sub>a</sub>CO<sub>2</sub>x0.2±2.5<p>" \
              "<p>慢性：ΔHCO<SUB>3</SUB><sup>-</sup>=ΔP<sub>a</sub>CO<sub>2</sub>x0.5±2.5<p>" \
              "<p>代谢性酸中毒：</p>" \
              "P<sub>a</sub>CO<sub>2</sub>=HCO<SUB>3</SUB><sup>-</sup>x1.5+8±2" \
              "<p>代谢性碱中毒：</p>" \
              "ΔP<sub>a</sub>CO<sub>2</sub>=ΔHCO<SUB>3</SUB><sup>-</sup>x0.9±1.5"
        self.setting_ui.setupUi(self)
        self.setting_ui.radioButton.setChecked(True)
        self.setting_ui.textBrowser.append(var)
        self.setting_ui.radioButton_2.toggled.connect(self.message)
        self.setting_ui.radioButton.toggled.connect(self.message)
        self.setting_ui.radioButton_3.toggled.connect(self.message)
        self.exec_()

    def message(self):
        var1 = "<p>《诊断学》第八版公式</p>" \
               "<p>呼吸性酸中毒：<p>" \
               "<p>急性：ΔHCO<SUB>3</SUB><sup>-</sup>=ΔP<sub>a</sub>CO<sub>2</sub>x0.07±1.5<p>" \
               "<p>慢性：ΔHCO<SUB>3</SUB><sup>-</sup>=ΔP<sub>a</sub>CO<sub>2</sub>x0.35±5.58<p>" \
               "<p>呼吸性碱中毒：</p>" \
               "<p>急性：ΔHCO<SUB>3</SUB><sup>-</sup>=ΔP<sub>a</sub>CO<sub>2</sub>x0.2±2.5<p>" \
               "<p>慢性：ΔHCO<SUB>3</SUB><sup>-</sup>=ΔP<sub>a</sub>CO<sub>2</sub>x0.5±2.5<p>" \
               "<p>代谢性酸中毒：</p>" \
               "P<sub>a</sub>CO<sub>2</sub>=HCO<SUB>3</SUB><sup>-</sup>x1.5+8±2" \
               "<p>代谢性碱中毒：</p>" \
               "ΔP<sub>a</sub>CO<sub>2</sub>=ΔHCO<SUB>3</SUB><sup>-</sup>x0.9±1.5"
        var2 = "<center>钟南山《呼吸病学》第二版公式</center>" \
               "<p>呼吸性酸中毒：<p>" \
               "<p>急性：代偿引起HCO<SUB>3</SUB><sup>-</sup>升高3-4mmHg<p>" \
               "<p>慢性：ΔHCO<SUB>3</SUB><sup>-</sup>=ΔP<sub>a</sub>CO<sub>2</sub>x0.35±5.58<p>" \
               "<p>呼吸性碱中毒：</p>" \
               "<p>急性：ΔHCO<SUB>3</SUB><sup>-</sup>=ΔP<sub>a</sub>CO<sub>2</sub>x0.2±2.5<p>" \
               "<p>慢性：ΔHCO<SUB>3</SUB><sup>-</sup>=ΔP<sub>a</sub>CO<sub>2</sub>x0.49±1.72<p>" \
               "<p>代谢性酸中毒：</p>" \
               "P<sub>a</sub>CO<sub>2</sub>=HCO<SUB>3</SUB><sup>-</sup>x1.5+8±2" \
               "<p>代谢性碱中毒：</p>" \
               "ΔP<sub>a</sub>CO<sub>2</sub>=HCO<SUB>3</SUB><sup>-</sup>x0.9±5"
        var3 = "<center>钱桂生《中华肺部疾病杂志》2010.04版公式</center>" \
               "<p>呼吸性酸中毒：<p>" \
               "<p>急性：代偿引起HCO<SUB>3</SUB><sup>-</sup>升高3-4mmHg<p>" \
               "<p>慢性：ΔHCO<SUB>3</SUB><sup>-</sup>=ΔP<sub>a</sub>CO<sub>2</sub>x0.35±5.58<p>" \
               "<p>呼吸性碱中毒：</p>" \
               "<p>急性：ΔHCO<SUB>3</SUB><sup>-</sup>=ΔP<sub>a</sub>CO<sub>2</sub>x0.2±2.5<p>" \
               "<p>慢性：ΔHCO<SUB>3</SUB><sup>-</sup>=ΔP<sub>a</sub>CO<sub>2</sub>x0.5±2.5<p>" \
               "<p>代谢性酸中毒：</p>" \
               "P<sub>a</sub>CO<sub>2</sub>=HCO<SUB>3</SUB><sup>-</sup>x1.5+8±2" \
               "<p>代谢性碱中毒：</p>" \
               "ΔP<sub>a</sub>CO<sub>2</sub>=HCO<SUB>3</SUB><sup>-</sup>x0.9±5"
        if self.setting_ui.radioButton.isChecked():
            self.setting_ui.textBrowser.clear()
            self.setting_ui.textBrowser.append(var1)
        elif self.setting_ui.radioButton_2.isChecked():
            self.setting_ui.textBrowser.clear()
            self.setting_ui.textBrowser.append(var2)
        elif self.setting_ui.radioButton_3.isChecked():
            self.setting_ui.textBrowser.clear()
            self.setting_ui.textBrowser.append(var3)


