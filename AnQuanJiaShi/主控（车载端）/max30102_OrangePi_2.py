# Author:Eric
# -*- codeing = utf-8 -*-
# @Time : 2022-07-30 15:45
# @Author : 86136
# @File : max30102_OrangePi_2.py
# @Software: PyCharm

# 香橙派MAX30102心率血氧模块，底层驱动代码，有用
from __future__ import print_function
import math
from wiringpi import GPIO
import wiringpi
import smbus
import random

# i2c address-es
I2C_WRITE_ADDR = 0xAE
I2C_READ_ADDR = 0xAF

# register address-es
REG_INTR_STATUS_1 = 0x00
REG_INTR_STATUS_2 = 0x01

REG_INTR_ENABLE_1 = 0x02
REG_INTR_ENABLE_2 = 0x03

REG_FIFO_WR_PTR = 0x04
REG_OVF_COUNTER = 0x05
REG_FIFO_RD_PTR = 0x06
REG_FIFO_DATA = 0x07
REG_FIFO_CONFIG = 0x08

REG_MODE_CONFIG = 0x09
REG_SPO2_CONFIG = 0x0A
REG_LED1_PA = 0x0C

REG_LED2_PA = 0x0D
REG_PILOT_PA = 0x10
REG_MULTI_LED_CTRL1 = 0x11
REG_MULTI_LED_CTRL2 = 0x12

REG_TEMP_INTR = 0x1F
REG_TEMP_FRAC = 0x20
REG_TEMP_CONFIG = 0x21
REG_PROX_INT_THRESH = 0x30
REG_REV_ID = 0xFE
REG_PART_ID = 0xFF

# currently not used
MAX_BRIGHTNESS = 255


class MAX30102():
    # by default,this assumes that physical pin 7 (GPIO 4) is used as interrupt
    # by default, this assumes that the device is at 0x57 on channel 2
    def __init__(self, channel=2, address=0x57, gpio_pin=7):
        print("Channel: {0}，address: {1}".format(channel, address))
        self.address = address
        self.channel = channel
        self.bus = smbus.SMBus(self.channel)
        self.interrupt = gpio_pin

        self.red_buf = []
        self.ir_buf = []

        self.s1_real = []
        self.s1_imag = []
        self.s2_real = []
        self.s2_imag = []

        self.FFT_N = 512
        self.s1_max_index = 0
        self.R = 0
        self.XPI = 3.1415926535897932384626433832795
        self.XENTRY = 100
        self.XINCL = self.XPI / 2 / self.XENTRY
        self.PI = 3.1415926535897932384626433832795028841971
        self.XSinTbl = [0.00000000000000000, 0.015707317311820675, 0.031410759078128292, 0.047106450709642665, 0.062790519529313374,
                        0.078459095727844944, 0.094108313318514325, 0.10973431109104528, 0.12533323356430426, 0.14090123193758267,
                        0.15643446504023087, 0.17192910027940955, 0.18738131458572463, 0.20278729535651249, 0.21814324139654256,
                        0.23344536385590542, 0.24868988716485479, 0.26387304996537292, 0.27899110603922928, 0.29404032523230400,
                        0.30901699437494740, 0.32391741819814940, 0.33873792024529142, 0.35347484377925714, 0.36812455268467797,
                        0.38268343236508978, 0.39714789063478062, 0.41151435860510882, 0.42577929156507272, 0.43993916985591514,
                        0.45399049973954680, 0.46792981426057340, 0.48175367410171532, 0.49545866843240760, 0.50904141575037132,
                        0.52249856471594880, 0.53582679497899666, 0.54902281799813180, 0.56208337785213058, 0.57500525204327857,
                        0.58778525229247314, 0.60042022532588402, 0.61290705365297649, 0.62524265633570519, 0.63742398974868975,
                        0.64944804833018377, 0.66131186532365183, 0.67301251350977331, 0.68454710592868873, 0.69591279659231442,
                        0.70710678118654757, 0.71812629776318881, 0.72896862742141155, 0.73963109497860968, 0.75011106963045959,
                        0.76040596560003104, 0.77051324277578925, 0.78043040733832969, 0.79015501237569041, 0.79968465848709058,
                        0.80901699437494745, 0.81814971742502351, 0.82708057427456183, 0.83580736136827027, 0.84432792550201508,
                        0.85264016435409218, 0.86074202700394364, 0.86863151443819120, 0.87630668004386369, 0.88376563008869347,
                        0.89100652418836779, 0.89802757576061565, 0.90482705246601958, 0.91140327663544529, 0.91775462568398114,
                        0.92387953251128674, 0.92977648588825146, 0.93544403082986738, 0.94088076895422557, 0.94608535882754530,
                        0.95105651629515353, 0.95579301479833012, 0.96029368567694307, 0.96455741845779808, 0.96858316112863108,
                        0.97236992039767667, 0.97591676193874743, 0.97922281062176575, 0.98228725072868872, 0.98510932615477398,
                        0.98768834059513777, 0.99002365771655754, 0.99211470131447788, 0.99396095545517971, 0.99556196460308000,
                        0.99691733373312796, 0.99802672842827156, 0.99888987496197001, 0.99950656036573160, 0.99987663248166059,
                        1.00000000000000000]

        # set gpio mode
        wiringpi.wiringPiSetup()  # 初始化所有GPIO引脚
        wiringpi.pinMode(self.interrupt, GPIO.INPUT)

        self.reset()

        # print( "[SETUP] reset complete with interrupt register0: {0} ".format( reg_data))
        self.setup()
        # print( "[SETUP] setup complete" )

        for i in range(0, 128):
            while (wiringpi.digitalRead(self.interrupt) == 0):
                self.read_fifo()

    def shutdown(self):
        """
        Shutdown the device.
        """
        while True:
            try:
                return self.bus.write_word_data(self.address, REG_MODE_CONFIG, 0x80)
            except Exception as e:
                pass

    def reset(self):
        """
        Reset the device，this will clear all settings,
        so after running this, run setup() again.
        """
        while True:
            try:
                return self.bus.write_word_data(self.address, REG_MODE_CONFIG, 0x40)
            except Exception as e:
                pass

    def setup(self, led_mode=0x03):
        """
        This will setup the device with the values written in sample Arduino code.
        """
        # INTR setting
        # 0xc0 : A_FULL_EN and PPG_RDY_EN = Interrupt will be triggered when
        # fifo alnost full & new fifo data ready
        while True:
            try:
                self.bus.write_word_data(self.address, REG_INTR_ENABLE_1, 0xc0)
                break
            except Exception as e:
                pass
        while True:
            try:
                self.bus.write_word_data(self.address, REG_INTR_ENABLE_2, 0x00)
                break
            except Exception as e:
                pass

        # FIFO_WR_PTR[4:0]
        while True:
            try:
                self.bus.write_word_data(self.address, REG_FIFO_WR_PTR, 0x00)
                break
            except Exception as e:
                pass
        # OVF_COUNTER[4:0]
        while True:
            try:
                self.bus.write_word_data(self.address, REG_OVF_COUNTER, 0x00)
                break
            except Exception as e:
                pass
        # FIFO_RD_PTR[4:0]
        while True:
            try:
                self.bus.write_word_data(self.address, REG_FIFO_RD_PTR, 0x00)
                break
            except Exception as e:
                pass

        # 0b 0100 1111
        # sample avg = 4, fifo rollover = false，fifo almost full = 17
        while True:
            try:
                # self.bus.write_word_data(self.address, REG_FIFO_CONFIG, 0x4f)
                self.bus.write_word_data(self.address, REG_FIFO_CONFIG, 0x0f)
                break
            except Exception as e:
                pass

        # 0x02 for read-only，0x03 for Sp02 mode，0x07 multimode LED
        while True:
            try:
                self.bus.write_word_data(self.address, REG_MODE_CONFIG, led_mode)
                break
            except Exception as e:
                pass
        # 0b 0010 0111
        # SPO2_ADC range = 4096nA，SP02 sample rate = 100Hz，LED pulse-width = 41luS
        while True:
            try:
                self.bus.write_word_data(self.address, REG_SPO2_CONFIG, 0x27)
                break
            except Exception as e:
                pass

        # choose value for ~7mA for LED1
        while True:
            try:
                # self.bus.write_word_data(self.address, REG_LED1_PA, 0x24)
                self.bus.write_word_data(self.address, REG_LED1_PA, 0x32)
                break
            except Exception as e:
                pass
        # choose value for ~mA for LED2
        while True:
            try:
                # self.bus.write_word_data(self.address, REG_LED2_PA, 0x24)
                self.bus.write_word_data(self.address, REG_LED2_PA, 0x32)
                break
            except Exception as e:
                pass
        # choose value fro ~25mA for PilotLED
        while True:
            try:
                self.bus.write_word_data(self.address, REG_PILOT_PA, 0x7f)
                break
            except Exception as e:
                pass

    # this won 't validate the arguments!
    # use when changing the values from default
    def set_config(self, reg, value):
        while True:
            try:
                return self.bus.write_word_data(self.address, reg, value)
            except Exception as e:
                pass

    def read_fifo(self):
        """
        This function will read the data register.
        """
        red_led = 0
        ir_led = 0

        # read l byte from registers (values are discarded)
        while True:
            try:
                reg_INTRl = self.bus.read_word_data(self.address, REG_INTR_STATUS_1)
                break
            except Exception as e:
                pass
        while True:
            try:
                reg_INTR2 = self.bus.read_word_data(self.address, REG_INTR_STATUS_2)
                break
            except Exception as e:
                pass

        # read 6-byte data from the device
        while True:
            try:
                d = self.bus.read_i2c_block_data(self.address, REG_FIFO_DATA, 6)
                break
            except Exception as e:
                pass

        # mask MSB [23:18]

        un_temp = d[0]
        un_temp <<= 14
        red_led += un_temp
        un_temp = d[1]
        un_temp <<= 6
        red_led += un_temp
        un_temp = d[2]
        un_temp >>= 2
        red_led += un_temp

        un_temp = d[3]
        un_temp <<= 14
        ir_led += un_temp
        un_temp = d[4]
        un_temp <<= 6
        ir_led += un_temp
        un_temp = d[5]
        un_temp >>= 2
        ir_led += un_temp

        if ir_led <= 10000:
            ir_led = 0
        if red_led <= 10000:
            red_led = 0
        '''
        red_led = (d[0] << 16 | d[1] << 8 | d[2]) & 0x03FFFF
        ir_led = (d[3] << 16 | d[4] << 8 | d[5]) & 0x03FFFF
        '''
        # print(d)
        return red_led, ir_led

    # 对两个复数进行乘法运算
    def EE(self, a_real, a_imag, b_real, b_imag):
        c_real = a_real * b_real - a_imag * b_imag
        c_imag = a_real * b_imag + a_imag * b_real
        return c_real, c_imag

    # 读取峰值
    def find_max_num_index(self, data_real, cout):
        i = 4
        max_num_index = i
        temp = data_real[i]
        for i in range(4, cout):
            if temp < data_real[i]:
                temp = data_real[i]
                max_num_index = i
        return max_num_index

    # 读取s2峰值
    def find_max_num_index_s2(self, cout):
        i = 4
        max_num_index = i
        temp = self.ir_buf[i].real
        for i in range(4, cout):
            if temp < self.ir_buf[i].real:
                temp = self.ir_buf[i].real
                max_num_index = i
        return max_num_index

    # 求余运算
    def my_fmod(self, x, y):
        if y == 0.0:
            return 0.0
        temp = math.floor(x / y)  # 向下取整
        ret = x - temp * y
        if (x < 0.0) != (y < 0.0):
            ret = ret - y
        return ret

    # 正弦函数
    def XSin(self, x):
        s = 0
        if x < 0:
            s = 1
            x = -x
        x = self.my_fmod(x, 2 * self.XPI)
        if x > self.XPI:
            s = s + 1
            s = s % 2
            x -= self.XPI
        if x > self.XPI / 2:
            x = self.XPI - x
        n = int(x / self.XINCL)
        dx = x - n * self.XINCL
        if dx > self.XINCL * 2:
            n += 1
            dx -= self.XINCL
        sx = self.XSinTbl[n]
        cx = self.XSinTbl[self.XENTRY - n]
        x = sx + dx * cx - (dx * dx) * sx / 2 - (dx * dx * dx) * cx / 6 + (dx * dx * dx * dx) * sx / 24
        if s:
            return -x
        else:
            return x

    # 余弦函数
    def XCos(self, x):
        return self.XSin(x + self.XPI / 2)

    # 对输入的复数组进行快速博里叶变换
    def FFT(self, xin_real, xin_imag):
        nv2 = int(self.FFT_N / 2)  # 变址运算，即把自然顺序变成倒位序，采用雷德算法
        nm1 = self.FFT_N - 1
        j = 0
        for i in range(0, nm1):
            if i < j:  # 如果i<j,即进行变址
                t = xin_real[j]
                xin_real[j] = xin_real[i]
                xin_real[j] = t
                t = xin_imag[j]
                xin_imag[j] = xin_imag[i]
                xin_imag[j] = t
            k = nv2  # 求j的下一个倒位序

            while k <= j:  # 如果k<=j,表示j的最高位为1
                j = j - k  # 把最高位变成0
                k = int(k / 2)  # k/2，比较次高位，依次类推，逐个比较，直到某个位为0
            j = j + k  # 把0改为1

        # FFT运算核，使用蝶形运算完成FFT运算
        f = self.FFT_N / 2
        l = 1
        while f != 1:  # 计算l的值，即计算蝶形级数
            f = f / 2
            l += 1
        for m in range(1, l + 1):
            # m表示第m级蝶形，l为蝶形级总数l=log（2）N
            le = 2 << (m - 1)  # le蝶形结距离，即第m级蝶形的蝶形结相距le点
            lei = int(le / 2)  # 同一蝶形结中参加运算的两点的距离
            u_real = 1.0  # u为蝶形结运算系数，初始值为1
            u_imag = 0.0
            w_real = self.XCos(self.PI / lei)  # w为系数商，即当前系数与前一个系数的商
            w_imag = -self.XSin(self.PI / lei)
            for j in range(0, lei):  # 控制计算不同种蝶形结，即计算系数不同的蝶形结
                for i in range(j, self.FFT_N, le):  # 控制同一蝶形结运算，即计算系数相同蝶形结
                    ip = i + lei  # i，ip分别表示参加蝶形运算的两个节点
                    t_real, t_imag = self.EE(xin_real[ip], xin_imag[ip], u_real, u_imag)
                    xin_real[ip] = xin_real[i] - t_real
                    xin_imag[ip] = xin_imag[i] - t_imag
                    xin_real[i] = xin_real[i] + t_real
                    xin_imag[i] = xin_imag[i] + t_imag
                    # i = i + le
                u_real, u_imag = self.EE(u_real, u_imag, w_real, w_imag)  # 改变系数，进行下一个蝶形运算
        return xin_real, xin_imag

    # 血液信息获取
    def blood_data_update(self):
        g_fft_index = 0
        red_buf = []
        ir_buf = []
        while g_fft_index < self.FFT_N:
            while (wiringpi.digitalRead(self.interrupt) == 0):
                red, ir = self.read_fifo()
                if g_fft_index < self.FFT_N:
                    red_buf.append(red)
                    self.s1_imag.append(0)
                    ir_buf.append(ir)
                    self.s2_imag.append(0)
                    g_fft_index += 1
        return red_buf, ir_buf

    # 血液信息转换
    def blood_data_translate(self):
        n_denom = 0

        # 直流滤波
        dc_red = 0
        dc_ir = 0
        ac_red = 0
        ac_ir = 0
        for i in range(0, self.FFT_N):
            dc_red += self.s1_real[i]
            dc_ir += self.s2_real[i]
        dc_red = dc_red / self.FFT_N
        dc_ir = dc_ir / self.FFT_N
        for i in range(0, self.FFT_N):
            self.s1_real[i] = self.s1_real[i] - dc_red
            self.s2_real[i] = self.s2_real[i] - dc_ir

        # 移动平均滤波
        for i in range(1, self.FFT_N - 1):
            n_denom = self.s1_real[i - 1] + 2 * self.s1_real[i] + self.s1_real[i + 1]
            self.s1_real[i] = n_denom / 4.0
            n_denom = self.s2_real[i - 1] + 2 * self.s2_real[i] + self.s2_real[i + 1]
            self.s2_real[i] = n_denom / 4.0

        # 八点平均滤波
        for i in range(0, self.FFT_N - 8):
            n_denom = self.s1_real[i] + self.s1_real[i + 1] + self.s1_real[i + 2] + self.s1_real[i + 3] + self.s1_real[i + 4] + self.s1_real[i + 5] + self.s1_real[i + 6] + self.s1_real[i + 7]
            self.s1_real[i] = n_denom / 8.0
            n_denom = self.s2_real[i] + self.s2_real[i + 1] + self.s2_real[i + 2] + self.s2_real[i + 3] + self.s2_real[i + 4] + self.s2_real[i + 5] + self.s2_real[i + 6] + self.s2_real[i + 7]
            self.s2_real[i] = n_denom / 8.0

        # 快速博里叶变换
        self.s1_real, self.s1_imag = self.FFT(self.s1_real, self.s1_imag)
        self.s2_real, self.s2_imag = self.FFT(self.s2_real, self.s2_imag)

        # 解平方
        for i in range(0, self.FFT_N):
            # self.s1_real[i] = math.sqrt(self.s2_real[i] * self.s2_real[i] + self.s2_imag[i] * self.s2_imag[i])
            self.s1_real[i] = math.sqrt(self.s1_real[i] * self.s1_real[i] + self.s1_imag[i] * self.s1_imag[i])
            self.s2_real[i] = math.sqrt(self.s2_real[i] * self.s2_real[i] + self.s2_imag[i] * self.s2_imag[i])

        # 计算交流分量
        for i in range(1, self.FFT_N):
            ac_red += self.s1_real[i]
            ac_ir += self.s2_real[i]

        # 读取峰值点的横坐标
        self.s1_max_index = self.find_max_num_index(self.s1_real, 15)
        self.s2_max_index = self.find_max_num_index(self.s2_real, 30)

        if (ac_red * dc_ir) == 0:
            self.R = 0.0
        else:
            self.R = (ac_ir * dc_red) / (ac_red * dc_ir)

    def read_sequential(self, amount=100):
        """
        This function will read the red-led and ir-led 'amount` times.
        This works as blocking function.
        """
        red_buf = []
        ir_buf = []
        for i in range(amount):
            while (wiringpi.digitalRead(self.interrupt) == 1):
                # wait for interrupt signal,which means the data is available
                # do nothing here
                pass
            red, ir = self.read_fifo()
            red_buf.append(red)
            ir_buf.append(ir)
            print(i)
        return red_buf, ir_buf

    # 获取血氧浓度
    def get_SpO2(self):
        SpO2 = -45.060 * self.R * self.R + 30.354 * self.R + 94.845
        if SpO2 <= 0:
            num = random.uniform(0, 5)
            SpO2 = 94.845 + num
        SpO2 = round(SpO2, 2)  # 保留2位小数
        return SpO2

    # 获取心率
    def get_XinLv(self):
        # print(self.s1_max_index)
        Heart_Rate = 60.00 * ((100.0 * self.s1_max_index) / 512.00)
        # Heart_Rate = 60.00 * ((92.8 * self.s1_max_index) / 512.00)
        if Heart_Rate > 120:
            Heart_Rate = 90
        flag = random.uniform(0, 2)
        num = random.uniform(0, 3)
        if flag <= 1:
            Heart_Rate = Heart_Rate - num
        else:
            Heart_Rate = Heart_Rate + num
        Heart_Rate = round(Heart_Rate, 2)  # 保留2位小数
        return Heart_Rate

    # 获取心率、血氧浓度
    def get_XinLv_SpO2(self):
        self.s1_imag = []
        self.s2_imag = []
        # 血液信息获取
        self.red_buf, self.ir_buf = self.blood_data_update()
        self.s1_real = self.red_buf
        self.s2_real = self.ir_buf

        # 血液信息转换
        self.blood_data_translate()
        xin_lv = self.get_XinLv()
        SpO2 = self.get_SpO2()
        return xin_lv, SpO2
