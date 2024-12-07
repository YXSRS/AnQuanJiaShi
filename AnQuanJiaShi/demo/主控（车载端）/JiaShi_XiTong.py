# Author:Eric
# -*- codeing = utf-8 -*-
# @Time : 2023-09-16 1:04
# @Author : 86136
# @File : 1.py
# @Software: PyCharm

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import cv2
import os
import pynmea2
import serial  # 获取GPS经纬度数据
import threading  # 导入线程模块
import time
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from mlx90614 import MLX90614  # MLX90614采集体温
import max30102_OrangePi_2  # 心率，血氧
import wiringpi  # GPIO引脚
from wiringpi import GPIO
import pymysql
from dbutils.pooled_db import PooledDB
import base64
import requests

global_Window = None
global_GPS = ""
global_time = ""
global_TiWen = 0.0
global_XinLv = 0.0
global_XueYang = 0.0
global_TuPian = "/home/orangepi/BiShe/JiaShi_XiTong/1.jpg"
global_Time_flag = 0  # 0：初始状态；1：空闲状态；2：写状态；3：读状态

# 行为    使用手机，闭眼，低头，吸烟，打哈欠，酒驾
global_XingWei = ['cellphone', 'eyes_closed', 'head_lowered', 'smoke', 'yawning', 'jiu_jia']
global_XingWei_ZH = ["使用手机", "闭眼", "低头", "吸烟", "打哈欠", "酒驾"]

global_Pool = PooledDB(
    creator=pymysql,  # 数据库驱动
    maxconnections=20,  # 连接池中最大连接数
    mincached=5,  # 初始化时连接池中连接数
    maxcached=10,  # 连接池中最多缓存的连接数
    maxusage=0,  # 每个连接的最大重复使用次数，0表示无限制
    blocking=True,  # 当连接池没有可用连接时是否阻塞等待
    host='39.103.177.201',
    port=3306,
    user='root',
    password='gccgcc',
    database='anquan_jiashi',
    charset='utf8mb4',
)
global_config = {
        'host': '39.103.177.201',  # 域名
        'port': 3306,  # 端口号
        'user': 'root',
        'password': 'gccgcc',  # 密码
        'database': 'anquan_jiashi',  # 数据库名
        'charset': 'utf8mb4',  # 字符编码
        'cursorclass': pymysql.cursors.Cursor,  # 选择 Cursor 类型
    }
global_ZhangHaoBiao = "zhanghao_biao"
global_ShiShiBiao = "shishi_biao"
global_WeiGuiBiao = "weigui_biao"
global_ZhangHao = "aaa"

# 请求地址
global_Request_URL = "https://aip.baidubce.com/rest/2.0/image-classify/v1/driver_behavior"
global_API_Key = "HPRZB8G6O0TyzbkvN29rMgIL"
global_Secret_Key = "smaB6q4TYgnpTIr1XdmiKeRlxnMCHrRC"
global_Token_URL = "https://aip.baidubce.com/oauth/2.0/token"
global_Grant_Type = "client_credentials"
global_Host = "%s?grant_type=%s&client_id=%s&client_secret=%s" % (global_Token_URL, global_Grant_Type, global_API_Key, global_Secret_Key)
global_Headers = {'content-type': 'application/x-www-form-urlencoded'}


class widget(QWidget):
    def __init__(self):
        super().__init__()

        self.ZiTi_YanSe_BaiSe = "color:rgb(255, 255, 255)"  # 字体颜色白色
        self.ZiTi_YanSe_HuanSe = "color:rgb(255, 255, 0)"  # 字体颜色黄色
        self.BeiJing_YanSe_HeiSe = "background-color:rgb(0, 0, 0)"  # 背景颜色黑色

        # 设置界面为我们生成的界面
        self.init_ui()

    def init_ui(self):
        self.ui = uic.loadUi("/home/orangepi/BiShe/JiaShi_XiTong/zhu_jie_mian.ui")

        # 设置窗体标题
        self.ui.setWindowTitle("基于智能云API的智能安全驾驶检测系统")

        # 设置图标
        self.ui.setWindowIcon(QIcon("/home/orangepi/BiShe/JiaShi_XiTong/TuBiao.png"))

        # 设置背景
        self.ui.label_BeiJing.setPixmap(QPixmap("/home/orangepi/BiShe/JiaShi_XiTong/BeiJing.png"))
        self.ui.label_BeiJing.setScaledContents(True)  # 自适应QLabel大小

        # 设置项目标题
        self.ui.label_XiangMuMing.setText("基于智能云API的智能安全驾驶检测系统")

        # 设置题目标题字体样式
        font = QFont()  # 实例化字体对象
        font.setFamily("微软雅黑")  # 字体
        font.setBold(True)  # 加粗
        font.setPointSize(28)  # 字体大小
        self.ui.label_XiangMuMing.setStyleSheet(self.ZiTi_YanSe_BaiSe)  # 文本颜色
        self.ui.label_XiangMuMing.setFont(font)

        # 设置信息
        self.ui.label_XinXi.setText("信息技术与工程学院   物联网2001   陈恩泰")

        # 设置信息字体样式
        font.setPointSize(15)  # 字体大小
        self.ui.label_XinXi.setStyleSheet(self.ZiTi_YanSe_BaiSe)  # 文本颜色
        self.ui.label_XinXi.setFont(font)

        # 设置实时信息
        font.setPointSize(17)  # 字体大小

        self.ui.label_CheZhu1.setStyleSheet(self.ZiTi_YanSe_HuanSe)  # 文本颜色
        self.ui.label_CheZhu1.setFont(font)
        self.ui.label_CheZhu1.setText("车主：")

        self.ui.label_CheZhu2.setStyleSheet(self.ZiTi_YanSe_HuanSe)  # 文本颜色
        self.ui.label_CheZhu2.setFont(font)
        self.ui.label_CheZhu2.setText("null")

        self.ui.label_RiQi1.setStyleSheet(self.ZiTi_YanSe_HuanSe)  # 文本颜色
        self.ui.label_RiQi1.setFont(font)
        self.ui.label_RiQi1.setText("日期：")

        self.ui.label_RiQi2.setStyleSheet(self.ZiTi_YanSe_HuanSe)  # 文本颜色
        self.ui.label_RiQi2.setFont(font)
        self.ui.label_RiQi2.setText("null")

        self.ui.label_TiWen1.setStyleSheet(self.ZiTi_YanSe_HuanSe)  # 文本颜色
        self.ui.label_TiWen1.setFont(font)
        self.ui.label_TiWen1.setText("体温：")

        self.ui.label_TiWen2.setStyleSheet(self.ZiTi_YanSe_HuanSe)  # 文本颜色
        self.ui.label_TiWen2.setFont(font)
        self.ui.label_TiWen2.setText("null")

        self.ui.label_XinLv1.setStyleSheet(self.ZiTi_YanSe_HuanSe)  # 文本颜色
        self.ui.label_XinLv1.setFont(font)
        self.ui.label_XinLv1.setText("心率：")

        self.ui.label_XinLv2.setStyleSheet(self.ZiTi_YanSe_HuanSe)  # 文本颜色
        self.ui.label_XinLv2.setFont(font)
        self.ui.label_XinLv2.setText("null")

        self.ui.label_XueYang1.setStyleSheet(self.ZiTi_YanSe_HuanSe)  # 文本颜色
        self.ui.label_XueYang1.setFont(font)
        self.ui.label_XueYang1.setText("血氧：")

        self.ui.label_XueYang2.setStyleSheet(self.ZiTi_YanSe_HuanSe)  # 文本颜色
        self.ui.label_XueYang2.setFont(font)
        self.ui.label_XueYang2.setText("null")

        self.ui.label_WeiZhi1.setStyleSheet(self.ZiTi_YanSe_HuanSe)  # 文本颜色
        self.ui.label_WeiZhi1.setFont(font)
        self.ui.label_WeiZhi1.setText("位置：")

        self.ui.label_WeiZhi2.setStyleSheet(self.ZiTi_YanSe_HuanSe)  # 文本颜色
        self.ui.label_WeiZhi2.setFont(font)
        self.ui.label_WeiZhi2.setText("null")

        # 设置视频默认背景
        self.ui.label_XianShi_ShiPin.setStyleSheet(self.BeiJing_YanSe_HeiSe)

    # 设置车主
    def SheZhi_CheZhu(self, CheZhu):
        self.ui.label_CheZhu2.setText(CheZhu)

    # 设置日期
    def SheZhi_RiQi(self, BeiJing_Time):
        self.ui.label_RiQi2.setText(BeiJing_Time)

    # 设置体温
    def SheZhi_TiWen(self, ti_wen):
        self.ui.label_TiWen2.setText(ti_wen)

    # 设置心率
    def SheZhi_XinLv(self, xin_lv):
        self.ui.label_XinLv2.setText(xin_lv)

    # 设置血氧
    def SheZhi_XueYang(self, xue_yang):
        self.ui.label_XueYang2.setText(xue_yang)

    # 设置位置信息
    def SheZhi_WeiZhi(self, GPS):
        self.ui.label_WeiZhi2.setText(GPS)

    # 显示视频
    def XianShiShiPin(self, img):
        # BGR -> RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        qformat = QImage.Format_Indexed8

        if len(img.shape) == 3:  # rows[0], cols[1], channels[2]
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        outImage = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)

        self.ui.label_XianShi_ShiPin.setPixmap(QPixmap.fromImage(outImage))
        self.ui.label_XianShi_ShiPin.setScaledContents(True)


# 获取网络状态
def Get_WangLuoZhuangTai():
    if os.system("ping www.baidu.com -c 1") == 0:
        return True
    else:
        return False


# 获取GPS经纬度数据的函数
def Get_GPS():
    global global_GPS
    # 创建gps串口的句柄
    ser = serial.Serial("/dev/ttyS4", 38400)

    while True:
        # 读取一行gps信息
        line = str(str(ser.readline())[2:])  # 将读取到的字节码转化成字符串（去掉前2位的无用字符）
        # print(line)

        # 寻找有地理坐标的那一行数据
        if line.startswith('$GNRMC'):
            line = line.replace('\\r\\n\'', '')  # 字符串结尾的无用换行符
            try:
                rmc = pynmea2.parse(line)

                GPS_NS_D = str(int(float(rmc.lat) / 100))  # GPS北纬南纬的度
                GPS_NS_F = str(int(float(rmc.lat) % 100))  # GPS北纬南纬的分
                GPS_NS_M = str(int(float(rmc.lat) * 100))[-2:]  # GPS北纬南纬的秒，取rmc.lat字符串的最后两位
                GPS_EW_D = str(int(float(rmc.lon) / 100))  # GPS东经西经的度
                GPS_EW_F = str(int(float(rmc.lon) % 100))  # GPS东经西经的分
                GPS_EW_M = str(float(rmc.lon) * 100)[-2:]  # GPS东经西经的秒

                if "." in GPS_EW_M:
                    GPS_EW_M = GPS_EW_M.replace('.', '')

                GPS = str(GPS_NS_D) + "°" + str(GPS_NS_F) + "′" + str(GPS_NS_M) + "″" + str(rmc.lat_dir) + " " + \
                      str(GPS_EW_D) + "°" + str(GPS_EW_F) + "′" + str(GPS_EW_M) + "″" + str(rmc.lon_dir)

                return GPS
            except Exception as e:
                return global_GPS


def Get_Time():
    # 获取当前北京时间
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    SHA_TZ = timezone(
        timedelta(hours=8),
        name='Asia/Shanghai',
    )
    ShiJian_GeShi = '%Y-%m-%d %H:%M:%S'  # 时间格式
    beijing_now_time = utc_now.astimezone(SHA_TZ)  # 北京时间
    BeiJing_NowTime_str = beijing_now_time.strftime(ShiJian_GeShi)  # 北京时间字符串

    return str(BeiJing_NowTime_str)


# 获取access_token
def Get_Access_Token(host):
    while True:
        response = requests.get(host)
        if response:
            print("获取access_token值成功，access_token: ", response.json()['access_token'])
            access_token = response.json()['access_token']
            return access_token
        else:
            print("获取access_token值失败！！！")


# 获取表行数
def Get_Biao_HangShu(biao):
    sql_biao = "SELECT COUNT(*) FROM %s;" % biao
    while True:
        try:
            conn_biao = global_Pool.connection()  # 从连接池中获取一个连接
            cursor_biao = conn_biao.cursor()
            cursor_biao.execute(sql_biao)  # 执行sql语句，也可执行数据库命令，如：show tables
            HangShu = cursor_biao.fetchone()[0] + 1
            conn_biao.close()
            return HangShu
        except Exception as e:
            conn_biao.close()
            print(e)


# 上传实时数据库
def ShangChuan_ShiShi_MySQL(ZhangHao, ShiJian, WeiZhi, TiWen, XinLv, XueYang):
    global global_config
    # 数据库的连接
    conn = pymysql.connect(**global_config)  # 连接数据库
    conn.select_db('anquan_jiashi')  # 定位到数据库的表
    cur = conn.cursor()  # 建立连接

    # 上传数据库
    sql = "update shishi_biao set ShiJian=(%s), WeiZhi=(%s), TiWen=(%s), XinLv=(%s), XueYang=(%s) where ZhangHao=(%s);"  # 数据库添加数据语句
    cur.executemany(sql, [(ShiJian, WeiZhi, TiWen, XinLv, XueYang, ZhangHao)])  # 数据

    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()


# 上传违规数据库
def ShangChuan_WeiGui_MySQL(XingWei_ZH):
    global global_WeiGuiBiao
    global global_time
    global global_GPS
    global global_TiWen
    global global_XinLv
    global global_XueYang
    global global_config

    Id = Get_Biao_HangShu(global_WeiGuiBiao)

    # 数据库的连接
    conn = pymysql.connect(**global_config)  # 连接数据库
    conn.select_db('anquan_jiashi')  # 定位到数据库的表
    cur = conn.cursor()  # 建立连接

    # 上传数据库
    sql = "insert into weigui_biao values(%s,%s,%s,%s,%s,%s,%s);"  # 数据库添加数据语句
    cur.executemany(sql, [(str(Id), global_time, global_GPS, XingWei_ZH, str(global_TiWen), str(global_XinLv), str(global_XueYang))])  # 数据

    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()


# 语音播报
def YuYin_BoBao(XingWei):
    MingLing = "aplay -D plughw:0,0 /home/orangepi/BiShe/JiaShi_XiTong/" + XingWei + ".wav"
    os.system(MingLing)


# 调用API识别
def main1():
    global global_Host
    global global_Request_URL
    global global_Headers
    global global_TuPian
    global global_Time_flag
    global global_XingWei
    global global_XingWei_ZH

    access_token = Get_Access_Token(global_Host)

    # 调用API的信息整理
    request_url = global_Request_URL + "?access_token=" + access_token

    while True:
        # time.sleep(0.1)
        if global_Time_flag == 1:
            global_Time_flag = 3  # 开始读取图片
            f = open(global_TuPian, 'rb')  # 二进制方式打开图片文件
            img = base64.b64encode(f.read())  # base64编码
            params = {"image": img}
            global_Time_flag = 1  # 读取完图片，允许写入

            # 获取驾驶行为
            # '''
            response = requests.post(request_url, data=params, headers=global_Headers)
            if response:
                # 将得到的信息进行格式化输出
                # js = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ':'))
                # print(js) #输出得到的驾驶行为信息

                # 输出精度大于0.83的行为，并上传数据库
                for i in range(0, 5):
                    if response.json()['person_info'][0]['attributes'][global_XingWei[i]]['score'] > 0.83:
                        ShangChuan_WeiGui_MySQL(global_XingWei_ZH[i])  # 上传数据库
                        print(global_XingWei[i], global_XingWei_ZH[i], response.json()['person_info'][0]['attributes'][global_XingWei[i]]['score'])

                        YuYin_BoBao(global_XingWei[i])
                        break
            # '''


# 酒精检测
def main2():
    global global_XingWei
    global global_XingWei_ZH
    wiringpi.pinMode(5, GPIO.INPUT)  # 配置GPIO wPi 5 引脚作为输入模式
    while True:
        GPIO_wPi_5 = wiringpi.digitalRead(5)  # 获取GPIO wPi 5引脚的电平
        if GPIO_wPi_5 == 0:  # 检测到酒驾行为
            ShangChuan_WeiGui_MySQL(global_XingWei_ZH[5])  # 上传数据库

            YuYin_BoBao(global_XingWei[6])

            time.sleep(5)


# 获取心率、血氧
def main3():
    global global_XinLv
    global global_XueYang
    global global_Window

    max30102 = max30102_OrangePi_2.MAX30102()  # MAX30102初始化

    while True:
        global_XinLv, global_XueYang = max30102.get_XinLv_SpO2()
        global_Window.SheZhi_XinLv(str(global_XinLv) + " bpm")
        global_Window.SheZhi_XueYang(str(global_XueYang) + "%")


# 获取体温
def main4():
    global global_TiWen
    global global_Window

    TiWen = MLX90614(0x5a)  # MLX90614初始化

    while True:
        global_TiWen = TiWen.get_TiWen()
        global_Window.SheZhi_TiWen(str(global_TiWen) + "℃")
        time.sleep(1)


# 获取GPS
def main5():
    global global_GPS
    global global_Window

    while True:
        GPS = Get_GPS()
        global_GPS = GPS
        global_Window.SheZhi_WeiZhi(global_GPS)
        time.sleep(1)


# 获取北京时间
def main6():
    global global_Window
    global global_time

    while True:
        global_time = Get_Time()
        global_Window.SheZhi_RiQi(global_time)
        time.sleep(0.5)


# 获取车主
def main7():
    global global_Pool
    global global_ZhangHaoBiao
    global global_Window
    global global_ZhangHao
    conn_zhanghao_biao = None
    sql_zhanghao_biao = "SELECT * FROM " + global_ZhangHaoBiao

    while True:
        try:
            conn_zhanghao_biao = global_Pool.connection()  # 从连接池中获取一个连接
            cursor_zhanghao_biao = conn_zhanghao_biao.cursor()
            cursor_zhanghao_biao.execute(sql_zhanghao_biao)  # 执行sql语句，也可执行数据库命令，如：show tables
            result_zhanghao_biao = cursor_zhanghao_biao.fetchall()  # 所有结果

            for i in range(len(result_zhanghao_biao)):
                if global_ZhangHao == result_zhanghao_biao[i][0]:
                    global_Window.SheZhi_CheZhu(result_zhanghao_biao[i][3])
                    break

            conn_zhanghao_biao.close()
            time.sleep(1)
        except Exception as e:
            conn_zhanghao_biao.close()
            print(e)


# 实时数据上传
def main8():
    global global_ZhangHao
    global global_time
    global global_GPS
    global global_TiWen
    global global_XinLv
    global global_XueYang

    while True:
        ShangChuan_ShiShi_MySQL(global_ZhangHao, global_time, global_GPS, str(global_TiWen), str(global_XinLv), str(global_XueYang))
        time.sleep(1)


if __name__ == '__main__':
    # 检测网络状态
    while Get_WangLuoZhuangTai() == False:
        pass

    # 初始化并展示我们的界面组件
    app = QApplication(sys.argv)
    global_Window = widget()
    global_Window.ui.show()

    wiringpi.wiringPiSetup()  # 初始化所有GPIO引脚

    main_1 = threading.Thread(target=main1)  # 初始化第一个线程，调用API检测行为
    main_2 = threading.Thread(target=main2)  # 初始化第二个线程，检测酒精
    main_3 = threading.Thread(target=main3)  # 初始化第三个线程，获取心率、血氧
    main_4 = threading.Thread(target=main4)  # 初始化第四个线程，获取体温
    main_5 = threading.Thread(target=main5)  # 初始化第五个线程，获取GPS
    main_6 = threading.Thread(target=main6)  # 初始化第六个线程，获取北京时间
    main_7 = threading.Thread(target=main7)  # 初始化第七个线程，获取车主名
    main_8 = threading.Thread(target=main8)  # 初始化第八个线程，上传实时数据

    main_1.start()  # 开启第一个进程
    main_2.start()  # 开启第二个进程
    main_3.start()  # 开启第三个进程
    main_4.start()  # 开启第四个进程
    main_5.start()  # 开启第五个进程
    main_6.start()  # 开启第六个进程
    main_7.start()  # 开启第七个进程
    main_8.start()  # 开启第八个进程

    # 初始化摄像头
    cap = cv2.VideoCapture("/dev/video10")

    # 显示图像
    while True:
        flag, zhen = cap.read()
        if not flag:
            break
        global_Window.XianShiShiPin(zhen)

        # 允许更新图片
        if global_Time_flag == 0 or global_Time_flag == 1:
            global_Time_flag = 2  # 开始写入图片
            # 对每一帧进行处理
            cv2.imwrite(global_TuPian, zhen)  # 注意英文路径，写进内存
            global_Time_flag = 1  # 写入完图片，允许读取

        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()

    # 结束QApplication
    sys.exit(app.exec_())
