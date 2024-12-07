package com.example.jiashi_jiance;

import android.content.Context;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.os.CountDownTimer;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.example.jiashi_jiance.util.HuoQu_DangQian_ShiJian;

/*
    违规记录
 */

public class fragment_WeiGui_JiLu extends Fragment {
    String zhang_hao;
    CountDownTimer timer;
    private PyObject pyObject;
    private ListView lv_JiLu;

    public fragment_WeiGui_JiLu(String ZhangHao) {
        this.zhang_hao = ZhangHao;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        Context context = getContext();
        View view = LayoutInflater.from(context).inflate(R.layout.fragment_wei_gui_ji_lu, container, false);

        Python python = Python.getInstance(); // 初始化Python环境
        pyObject = python.getModule("Python_API");//"Python_API"为需要调用的Python文件名

        lv_JiLu = view.findViewById(R.id.lv_JiLu);

        timer = new CountDownTimer(Long.MAX_VALUE, 3000) {
            @Override
            public void onTick(long l) {
                // 在这里执行访问云数据库的操作
                // 每隔 3 秒执行一次倒计时
                ShuaXin_WeiGui_JiLu();
            }

            @Override
            public void onFinish() {
                // 在这里再次启动倒计时
            }
        };

        return view;
    }

    /*
        刷新违规记录
     */
    public void ShuaXin_WeiGui_JiLu() {
        PyObject ret = pyObject.callAttr("get_WeiGui_ShuJuBiao");//"get_WeiGui_ShuJuBiao"为需要调用的函数名
        WeiGui_ShiPeiQi weiGui_shiPeiQi = new WeiGui_ShiPeiQi(getContext(), String.valueOf(ret));
        lv_JiLu.setAdapter(weiGui_shiPeiQi);
    }

    @Override
    public void onPause() {
        super.onPause();
        //本方法被调用的情况
        //碎片被其他碎片覆盖，例如用户在两个不同的碎片之间切换。
        //碎片所在的活动被其他活动覆盖，例如用户启动了另一个应用程序。
        //碎牌所在的活动被暂停，例如用户按下了电源键。

        // 停止倒计时
        timer.cancel();
    }

    @Override
    public void onResume() {
        super.onResume();
        //本方法被调用的情况
        //碎片被其他碎片覆盖，然后用户返回到这个碎片。
        //碎片所在的活动被其他活动覆盖，然后用户返回到这个活动。
        //碎片所在的活动被暂停，然后恢复运行。

        // 重新启动倒计时
        timer.start();
    }
}