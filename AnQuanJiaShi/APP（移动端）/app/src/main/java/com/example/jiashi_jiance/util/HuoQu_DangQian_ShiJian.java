package com.example.jiashi_jiance.util;

import java.text.SimpleDateFormat;
import java.util.Date;

public class HuoQu_DangQian_ShiJian {
    public static String Get_Now_time() {//获取当前时间
        SimpleDateFormat time = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        return time.format(new Date());
    }
}
