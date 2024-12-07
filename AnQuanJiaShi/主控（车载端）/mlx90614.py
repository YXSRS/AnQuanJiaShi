# Author:Eric
# -*- codeing = utf-8 -*-
# @Time : 2022-07-28 15:42
# @Author : 86136
# @File : mlx90614.py
# @Software: PyCharm

# MLX90614采集体温，都可用
import smbus
from time import sleep


class MLX90614():
    MLX90614_RAWIR1 = 0x04
    MLX90614_RAWIR2 = 0x05
    MLX90614_TA = 0x06
    MLX90614_TOBJ1 = 0x07
    MLX90614_TOBJ2 = 0x08

    MLX90614_TOMAX = 0x20
    MLX90614_TOMIN = 0x21
    MLX90614_PWMCTRL = 0x22
    MLX90614_TARANGE = 0x23
    MLX90614_EMISS = 0x24
    MLX90614_CONFIG = 0x25
    MLX90614_ADDR = 0x0E
    MLX90614_ID1 = 0x3C
    MLX90614_ID2 = 0x3D
    MLX90614_ID3 = 0x3E
    MLX90614_ID4 = 0x3F

    comm_retries = 50
    comm_sleep_amount = 0.001

    def __init__(self, address=0x5a, bus_num=3):
        self.bus_num = bus_num
        self.address = address
        self.bus = smbus.SMBus(bus=bus_num)

    def read_reg(self, reg_addr):
        err = None
        # for i in range(self.comm_retries):
        while True:
            try:
                data = self.bus.read_word_data(self.address, reg_addr)
                return data
            except Exception as e:
                err = e
                # "Rate limiting" - sleeping to prevent problems with sensor
                # when requesting data too quickly
                sleep(self.comm_sleep_amount)
        # By this time, we made a couple requests and the sensor didn't respond
        # (judging by the fact we haven't returned from this function yet)
        # So let's just re-raise the last IOError we got
        # raise err

    def data_to_temp(self, data):
        temp = (data * 0.02) - 273.15
        return temp

    # 获取环境温度
    def get_amb_temp(self):
        data = self.read_reg(self.MLX90614_TA)
        return self.data_to_temp(data)

    # 获取物体温度
    def get_obj_temp(self):
        data = self.read_reg(self.MLX90614_TOBJ1)
        return self.data_to_temp(data)

    # 获取体温
    def get_TiWen(self):
        data = self.read_reg(self.MLX90614_TOBJ1)
        temp = (data * 0.02) - 273.15
        wen_du = 0.7797 * temp + 9.727 + 5
        wen_du = round(wen_du, 2)  # 保留2位小数
        return wen_du


if __name__ == "__main__":
    sensor = MLX90614()  # MLX90614初始化
    print(sensor.get_amb_temp())
    print(sensor.get_obj_temp())
    print(sensor.get_TiWen())
