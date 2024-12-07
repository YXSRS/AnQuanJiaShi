package com.example.jiashi_jiance;

import com.chaquo.python.Kwarg;
import com.chaquo.python.PyObject;
import com.chaquo.python.android.AndroidPlatform;
import com.chaquo.python.Python;

public class Diao_Python {
    public static void temp(){
        // 初始化Python环境
        if (!Python.isStarted()){
            //Python.start(new AndroidPlatform(this));
        }
        Python python=Python.getInstance(); // 初始化Python环境
        PyObject pyObject=python.getModule("CeShi1");//"text"为需要调用的Python文件名
        PyObject res1=pyObject.callAttr("ce_shi_ShuJuKu");//"sayHello"为需要调用的函数名
    }
}
