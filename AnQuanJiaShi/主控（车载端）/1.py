# Author:Eric
# -*- codeing = utf-8 -*-
# @Time : 2022-08-03 13:10
# @Author : 86136
# @File : er.py
# @Software: PyCharm

import requests
import base64
import cv2
import pymysql
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import threading  # 导入线程模块
import time
import os  # 语音播报
import wiringpi  # GPIO引脚
from wiringpi import GPIO
import urllib  # 发送短信
import urllib.request
import hashlib
import serial  # 获取GPS经纬度数据
import pynmea2
from mlx90614 import MLX90614  # MLX90614采集体温
import max30102_OrangePi_2  # 心率，血氧

# 调用API部分
# 行为    双手离开方向盘，使用手机，闭眼，低头，未系安全带，吸烟，打哈欠，酒驾，酒精
XingWei = ['both_hands_leaving_wheel', 'cellphone', 'eyes_closed', 'head_lowered', 'not_buckling_up', 'smoke', 'yawning', 'jiu_jia', 'jiu_jing']
XingWei_ZhongWen = ["双手离开方向盘", "使用手机", "闭眼", "低头", "未系安全带", "吸烟", "打哈欠", "酒驾", "酒精"]

# 请求地址
request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/driver_behavior"

# 获取access_token的值
host = '' \
       'https://aip.baidubce.com/oauth/2.0/token?' \
       'grant_type=client_credentials&' \
       'client_id=HPRZB8G6O0TyzbkvN29rMgIL&' \
       'client_secret=smaB6q4TYgnpTIr1XdmiKeRlxnMCHrRC'
access_token = ''
response = requests.get(host)
if response:
    print("access_token: ", response.json()['access_token'])
    access_token = response.json()['access_token']
else:
    print("获取access_token值失败！！！")
    exit(0)

# 调用API的信息整理
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}

# 数据库部分
# 连接信息
config = {
    'host': '39.103.177.201',  # 域名
    'port': 3306,  # 端口号
    'user': 'root',
    'password': 'gccgcc',  # 密码
    'database': 'anquan_jiashi',  # 数据库名
    'charset': 'utf8mb4',  # 字符编码
    'cursorclass': pymysql.cursors.Cursor,  # 选择 Cursor 类型
}
# conn = pymysql.connect(**config)  # 连接数据库
# conn.select_db('anquan_jiashi')  # 定位到数据库的表
# cur = conn.cursor()  # 建立连接
# sql = "insert into CeShi1 values(%s,%s,%s,%s)"  # 数据库添加数据语句

# 摄像头部分
# 采用摄像头
cap = cv2.VideoCapture("/dev/video10")

# GPIO引脚
wiringpi.wiringPiSetup()  # 初始化所有GPIO引脚
wiringpi.pinMode(5, GPIO.INPUT)  # 配置GPIO wPi 5 引脚作为输入模式

Time_flag = 1  # 时间标志位
ti_wen = 0.0  # 体温
xin_lv = 0.0  # 心率
SpO2 = 0.0  # 血氧
GPS_old = ""


# 获取GPS经纬度数据的函数
def gps_get():
    global GPS_old
    # 创建gps串口的句柄
    ser = serial.Serial("/dev/ttyS4", 38400)

    # print("获取句柄成功，进入循环：")
    while (True):
        # 读取一行gps信息
        line = str(str(ser.readline())[2:])  # 将读取到的字节码转化成字符串（去掉前2位的无用字符）
        # print(line)

        # 寻找有地理坐标的那一行数据
        if line.startswith('$GNRMC'):
            line = line.replace('\\r\\n\'', '')  # 字符串结尾的无用换行符
            # print(line)
            try:
                rmc = pynmea2.parse(line)

                GPS_NS_D = str(int(float(rmc.lat) / 100))  # GPS北纬南纬的度
                GPS_NS_F = str(int(float(rmc.lat) % 100))  # GPS北纬南纬的分
                GPS_NS_M = str(int(float(rmc.lat) * 100))[-2:]  # GPS北纬南纬的秒，取rmc.lat字符串的最后两位
                GPS_EW_D = str(int(float(rmc.lon) / 100))  # GPS东经西经的度
                GPS_EW_F = str(int(float(rmc.lon) % 100))  # GPS东经西经的分
                GPS_EW_M = str(float(rmc.lon) * 100)[-2:]  # GPS东经西经的秒
                GPS = str(GPS_NS_D) + "°" + str(GPS_NS_F) + "′" + str(GPS_NS_M) + "″" + str(rmc.lat_dir) + str(GPS_EW_D) + "°" + str(GPS_EW_F) + "′" + str(GPS_EW_M) + "″" + str(rmc.lon_dir)

                return GPS
            except Exception as e:
                return GPS_old


def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()


# 发送短信
def FaSong_DuanXin():
    global GPS_old
    statusStr = {
        '0': '短信发送成功',
        '-1': '参数不全',
        '-2': '服务器空间不支持,请确认支持curl或者fsocket,联系您的空间商解决或者更换空间',
        '30': '密码错误',
        '40': '账号不存在',
        '41': '余额不足',
        '42': '账户已过期',
        '43': 'IP地址限制',
        '50': '内容含有敏感词'
    }

    smsapi = "http://api.smsbao.com/"
    # 短信平台账号
    user = 'YXSRS'
    # 短信平台密码
    password = md5('690904289cet')
    # 要发送的短信内容
    content = "您好，位于" + GPS_old + "位置！！！"
    # 要发送短信的手机号码
    phone = '13692619214'

    data = urllib.parse.urlencode({'u': user, 'p': password, 'm': phone, 'c': content})
    send_url = smsapi + 'sms?' + data
    response = urllib.request.urlopen(send_url)
    the_page = response.read().decode('utf-8')
    print(statusStr[the_page])


# 上传数据库，危险行为库
def ShangChuan_MySQL(i):
    global config
    global XingWei_ZhongWen
    global XingWei
    global ti_wen
    global xin_lv
    global SpO2
    global GPS_old
    # 获取当前北京时间
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    SHA_TZ = timezone(
        timedelta(hours=8),
        name='Asia/Shanghai',
    )
    ShiJian_GeShi = '%Y-%m-%d %H:%M:%S'  # 时间格式
    beijing_now_time = utc_now.astimezone(SHA_TZ)  # 北京时间
    BeiJing_NowTime_str = beijing_now_time.strftime(ShiJian_GeShi)  # 北京时间字符串

    # 数据库的连接
    conn = pymysql.connect(**config)  # 连接数据库
    conn.select_db('anquan_jiashi')  # 定位到数据库的表
    cur = conn.cursor()  # 建立连接

    # 获取表的行数
    cur.execute('SELECT COUNT(*) FROM weigui_biao')
    row_count = cur.fetchone()[0] + 1

    # 上传数据库
    # sql = "insert into weigui_biao (id,ShiJian,WeiZhi,XingWei,TiWen,XinLv,XueYang) values(1," + BeiJing_NowTime_str + "," + GPS_old + "," + XingWei_ZhongWen[i] + "," + str(ti_wen) + "," + str(xin_lv) + "," + str(SpO2) + ");"  # 数据库添加数据语句
    sql = "insert into weigui_biao values(%s,%s,%s,%s,%s,%s,%s);"  # 数据库添加数据语句
    cur.executemany(sql, [(row_count, BeiJing_NowTime_str, GPS_old, XingWei_ZhongWen[i], str(ti_wen), str(xin_lv), str(SpO2))])  # 数据

    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()

    # 语音播报，执行两遍
    # MingLing = "echo \"orangepi\" | sudo -S aplay -D plughw:0,0 " + XingWei[i] + ".wav"
    MingLing = "aplay -D plughw:0,0 " + XingWei[i] + ".wav"
    os.system(MingLing)

    print("已上传数据库！！！")


# 上传数据库2，实时数据库
def ShangChuan_MySQL_2():
    global config
    global ti_wen
    global xin_lv
    global SpO2
    global GPS_old
    # 获取当前北京时间
    utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
    SHA_TZ = timezone(
        timedelta(hours=8),
        name='Asia/Shanghai',
    )
    ShiJian_GeShi = '%Y-%m-%d %H:%M:%S'  # 时间格式
    beijing_now_time = utc_now.astimezone(SHA_TZ)  # 北京时间
    BeiJing_NowTime_str = beijing_now_time.strftime(ShiJian_GeShi)  # 北京时间字符串

    # 数据库的连接
    conn = pymysql.connect(**config)  # 连接数据库
    conn.select_db('anquan_jiashi')  # 定位到数据库的表
    cur = conn.cursor()  # 建立连接

    # 上传数据库
    # sql = "update shishi_biao set ShiJian=" + BeiJing_NowTime_str + ", WeiZhi=" + GPS_old + ", TiWen=" + str(ti_wen) + ", XinLv=" + str(xin_lv) + ", XueYang=" + str(SpO2) + " where ZhangHao=aaa;"  # 数据库添加数据语句
    sql = "update shishi_biao set ShiJian=(%s), WeiZhi=(%s), TiWen=(%s), XinLv=(%s), XueYang=(%s) where ZhangHao=\"aaa\";"  # 数据库添加数据语句
    cur.executemany(sql, [(BeiJing_NowTime_str, GPS_old, str(ti_wen), str(xin_lv), str(SpO2))])  # 数据

    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()


# 多线程，计时、识别程序
def main2():
    global Time_flag
    global XingWei_ZhongWen
    global XingWei
    while True:
        time.sleep(0.1)
        if Time_flag == 0:
            f = open('1.jpg', 'rb')  # 二进制方式打开图片文件
            img = base64.b64encode(f.read())  # base64编码
            params = {"image": img}
            Time_flag = 1  # 读取完图片，允许写入

            # 获取驾驶行为
            # '''
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                # 将得到的信息进行格式化输出
                # js = json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ':'))
                # print(js) #输出得到的驾驶行为信息

                # 输出精度大于0.93的行为，并上传数据库
                for i in range(0, 7):
                    if response.json()['person_info'][0]['attributes'][XingWei[i]]['score'] > 0.83:
                        ShangChuan_MySQL(i)  # 上传数据库
                        print(XingWei[i], XingWei_ZhongWen[i], response.json()['person_info'][0]['attributes'][XingWei[i]]['score'])
                        break
            # '''


# 酒精检测
def main3():
    while True:
        GPIO_wPi_5 = wiringpi.digitalRead(5)  # 获取GPIO wPi 5引脚的电平
        if GPIO_wPi_5 == 0:  # 检测到酒驾行为
            # 发送短信
            FaSong_DuanXin()

            ShangChuan_MySQL(7)  # 上传数据库

            time.sleep(5)


# 体温、心率、血氧数据获取，上传
def main4():
    global ti_wen
    global xin_lv
    global SpO2
    TiWen = MLX90614(0x5a)  # MLX90614初始化
    m = max30102_OrangePi_2.MAX30102()  # MAX30102初始化
    while True:
        ti_wen = TiWen.get_TiWen()
        xin_lv, SpO2 = m.get_XinLv_SpO2()


# 获取GPS
def main5():
    global GPS_old
    global ti_wen
    global xin_lv
    global SpO2
    while True:
        GPS = gps_get()
        GPS_old = GPS
        ShangChuan_MySQL_2()  # 上传数据库，CeShi3
        print("体温：", ti_wen, "℃   心率：", xin_lv, "bpm   血氧：", SpO2, "%   已更新到数据库！")
        time.sleep(1)


# 程序运行
k = 1
main_2 = threading.Thread(target=main2)  # 初始化第二个线程
main_3 = threading.Thread(target=main3)  # 初始化第三个线程
main_4 = threading.Thread(target=main4)  # 初始化第四个线程
main_5 = threading.Thread(target=main5)  # 初始化第五个线程
print("程序启动：")
main_2.start()  # 开启第二个线程，进行计时
main_3.start()  # 开启第三个进程，进行酒驾检测
main_4.start()  # 开启第四个进程，进行体温、心率、血氧数据获取，上传
main_5.start()  # 开启第五个进程
while True:
    flag, zhen = cap.read()  # 获取每一帧
    if not flag:
        break
    cv2.imshow('xian_shi', zhen)  # 显示每一帧

    # 计时到了1.5秒，开始识别
    if Time_flag == 1:
        # 对每一帧进行处理
        cv2.imwrite("1.jpg", zhen)  # 注意英文路径，写进内存
        Time_flag = 0  # 写入完图片，允许读取

    cv2.waitKey(1)

# 程序结束，关闭所有东西
cap.release()
cv2.destroyAllWindows()
cur.close()
conn.commit()
conn.close()
