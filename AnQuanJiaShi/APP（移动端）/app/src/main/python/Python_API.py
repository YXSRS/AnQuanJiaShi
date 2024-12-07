import pymysql
from sqlalchemy import create_engine
import pandas as pd


def ce_shi_ShuJuKu():
    config = {
        'host': '39.103.177.201',  # 域名
        'port': 3306,  # 端口号
        'user': 'root',
        'password': 'gccgcc',  # 密码
        'database': 'anquan_jiashi',  # 数据库名
        'charset': 'utf8mb4',  # 字符编码
        'cursorclass': pymysql.cursors.Cursor,  # 选择 Cursor 类型
    }

    conn = pymysql.connect(**config)  # 连接数据库
    conn.select_db('anquan_jiashi')  # 定位到数据库的表
    cur = conn.cursor()  # 建立连接

    sql = "insert into zhanghao_biao values(%s,%s,%s)"
    insert = cur.executemany(sql, [("ccc", "123", "3")])  # 数据
    print('shouyingxianghangshu', insert)
    cur.close()
    conn.commit()
    conn.close()
    print('sql succeed')


# 判断账号密码正确
# 参数：
#     zhang_hao：账号
#     mi_ma：密码
# 返回值：
#     0：账号密码正确
#     1：没有该账号
#     2：密码错误
def PanDuan_ZhangHao_MiMa_ZhengQue(zhang_hao, mi_ma):
    engine = create_engine("mysql+pymysql://root:gccgcc@39.103.177.201:3306/anquan_jiashi?charset=utf8mb4")
    data = pd.read_sql_table("zhanghao_biao", con=engine)
    flag = 1
    i = 0
    for temp_ZhangHao in (data['ZhangHao']):
        if temp_ZhangHao == zhang_hao:  # 判断是否存在账号
            flag = 2
            if data['MiMa'][i] == mi_ma:  # 判断密码是否正确
                flag = 0
            break
        i += 1
    return flag


# 查询账号是否存在
# 参数：
#     zhang_hao：账号
# 返回值：
#     1：存在
#     0：不存在
def ChaXun_ZhangHao_ShiFou_CunZai(zhang_hao):
    engine = create_engine("mysql+pymysql://root:gccgcc@39.103.177.201:3306/anquan_jiashi?charset=utf8mb4")
    data = pd.read_sql_table("zhanghao_biao", con=engine)
    flag = 0
    for temp_ZhangHao in (data['ZhangHao']):
        if temp_ZhangHao == zhang_hao:  # 判断是否存在账号
            flag = 1
            break
    return flag


# 修改密码
# 参数：
#     zhang_hao：账号
#     mi_ma：密码
def XiuGai_MiMa(zhang_hao, mi_ma):
    config = {
        'host': '39.103.177.201',  # 域名
        'port': 3306,  # 端口号
        'user': 'root',
        'password': 'gccgcc',  # 密码
        'database': 'anquan_jiashi',  # 数据库名
        'charset': 'utf8mb4',  # 字符编码
        'cursorclass': pymysql.cursors.Cursor,  # 选择 Cursor 类型
    }

    conn = pymysql.connect(**config)  # 连接数据库
    conn.select_db('anquan_jiashi')  # 定位到数据库的表
    cur = conn.cursor()  # 建立连接

    sql = "update zhanghao_biao set MiMa=(%s) where ZhangHao=(%s);"
    cur.executemany(sql, [(mi_ma, zhang_hao)])  # 数据
    cur.close()
    conn.commit()
    conn.close()


# 获取车主名
# 返回值：
#       车主名
def get_CheZhuMing(zhang_hao):
    engine = create_engine("mysql+pymysql://root:gccgcc@39.103.177.201:3306/anquan_jiashi?charset=utf8mb4")
    data = pd.read_sql_table("zhanghao_biao", con=engine)
    i = 0
    for temp_ZhangHao in (data['ZhangHao']):
        if temp_ZhangHao == zhang_hao:  # 判断是否存在账号
            break
        i += 1
    return data['CheZhuMing'][i]


# 修改资料
# 参数：
#     zhang_hao：账号
#     che_zhu_ming：车主名
def XiuGai_ZiLiao(zhang_hao, che_zhu_ming):
    config = {
        'host': '39.103.177.201',  # 域名
        'port': 3306,  # 端口号
        'user': 'root',
        'password': 'gccgcc',  # 密码
        'database': 'anquan_jiashi',  # 数据库名
        'charset': 'utf8mb4',  # 字符编码
        'cursorclass': pymysql.cursors.Cursor,  # 选择 Cursor 类型
    }

    conn = pymysql.connect(**config)  # 连接数据库
    conn.select_db('anquan_jiashi')  # 定位到数据库的表
    cur = conn.cursor()  # 建立连接

    sql = "update zhanghao_biao set CheZhuMing=(%s) where ZhangHao=(%s);"
    cur.executemany(sql, [(che_zhu_ming, zhang_hao)])  # 数据
    cur.close()
    conn.commit()
    conn.close()


# 获取实时数据
# 参数：
#     zhang_hao：账号
# 返回值;
#     str：时间,位置,体温,心率,血氧
def get_ShiShi_ShuJu(zhang_hao):
    engine = create_engine("mysql+pymysql://root:gccgcc@39.103.177.201:3306/anquan_jiashi?charset=utf8mb4")
    data = pd.read_sql_table("shishi_biao", con=engine)
    i = 0
    str = ""
    for temp_ZhangHao in (data['ZhangHao']):
        if temp_ZhangHao == zhang_hao:  # 寻找账号对应的那行实时数据
            str = data['ShiJian'][i] + "," + data['WeiZhi'][i] + "," + data['TiWen'][i] + "," + data['XinLv'][i] + "," + data['XueYang'][i]
            break
        i += 1
    return str


# 获取违规数据表
# 返回值：
#       字符串。格式：xxx,xxx,xxx;xxx,xxx,xxx;xxx,xxx,xxx，每行数据用;分隔，每个数据用,分隔
def get_WeiGui_ShuJuBiao():
    engine = create_engine("mysql+pymysql://root:gccgcc@39.103.177.201:3306/anquan_jiashi?charset=utf8mb4")
    data = pd.read_sql_table("weigui_biao", con=engine)
    Str = ""
    hang = len(data['id']) - 1  # 行
    for i in range(hang, -1, -1):
        str = data['ShiJian'][i] + "," + data['WeiZhi'][i] + "," + data['XingWei'][i] + "," + data['TiWen'][i] + "," + data['XinLv'][i] + "," + data['XueYang'][i]
        if i == 0:
            Str = Str + str
        else:
            Str = Str + str + ";"
    return Str
