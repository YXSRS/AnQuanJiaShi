package com.example.jiashi_jiance;

import android.content.Context;
import android.os.Bundle;

import androidx.fragment.app.Fragment;

import android.os.CountDownTimer;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.example.jiashi_jiance.util.HuoQu_DangQian_ShiJian;

/*
    实时数据
 */

public class fragment_ShiShi_ShuJu extends Fragment implements View.OnClickListener {

    String zhang_hao;
    String che_zhu_ming;
    CountDownTimer timer;
    private TextView tv_CheZhu;
    private TextView tv_RiQi;
    private TextView tv_TiWen;
    private TextView tv_XinLv;
    private TextView tv_XueYang;
    private TextView tv_WeiZhi;
    private TextView tv_TiShi;
    private Button btn_ShuaXin;
    private PyObject pyObject;
    String ShiShi_ShuJu;

    public fragment_ShiShi_ShuJu(String ZhangHao, String CheZhuMing) {
        this.zhang_hao = ZhangHao;
        this.che_zhu_ming = CheZhuMing;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        Context context = getContext();
        View view = LayoutInflater.from(context).inflate(R.layout.fragment_shi_shi_shu_ju, container, false);

        Python python = Python.getInstance(); // 初始化Python环境
        pyObject = python.getModule("Python_API");//"Python_API"为需要调用的Python文件名

        tv_CheZhu = view.findViewById(R.id.tv_CheZhu);
        tv_RiQi = view.findViewById(R.id.tv_RiQi);
        tv_TiWen = view.findViewById(R.id.tv_TiWen);
        tv_XinLv = view.findViewById(R.id.tv_XinLv);
        tv_XueYang = view.findViewById(R.id.tv_XueYang);
        tv_WeiZhi = view.findViewById(R.id.tv_WeiZhi);
        tv_TiShi = view.findViewById(R.id.tv_TiShi);

        btn_ShuaXin = view.findViewById(R.id.btn_ShuaXin);
        btn_ShuaXin.setOnClickListener(this);

        timer = new CountDownTimer(Long.MAX_VALUE, 1000) {
            @Override
            public void onTick(long l) {
                // 在这里执行访问云数据库的操作
                // 每隔 1 秒执行一次倒计时
                ShuaXin_ShiShi_ShuJu();
            }

            @Override
            public void onFinish() {
                // 在这里再次启动倒计时
            }
        };

        tv_CheZhu.setText(che_zhu_ming);

        return view;
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

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.btn_ShuaXin:
                ShuaXin_ShiShi_ShuJu();
                break;
        }
    }

    /*
        获取时间差
        参数：
            JieShu_ShiJian：结束时间。格式：yy-mm-dd hh:mm:ss
            KaiShi_ShiJian：开始时间。格式：yy-mm-dd hh:mm:ss
        返回值：
            0-6，单位：s
     */
    public int get_ShiJianCha(String JieShu_ShiJian, String KaiShi_ShiJian) {
        int cha = 6;
        String[] JieShu_ShiJian_s = JieShu_ShiJian.split(" ");
        String[] JieShu_ShiJian_2_s = JieShu_ShiJian_s[1].split(":");
        String[] KaiShi_ShiJian_s = KaiShi_ShiJian.split(" ");
        String[] KaiShi_ShiJian_2_s = KaiShi_ShiJian_s[1].split(":");

        if (JieShu_ShiJian_s[0].equals(KaiShi_ShiJian_s[0])) {//日期相等
            int JieShu_Shi = Integer.parseInt(JieShu_ShiJian_2_s[0]);
            int JieShu_Fen = Integer.parseInt(JieShu_ShiJian_2_s[1]);
            int JieShu_Miao = Integer.parseInt(JieShu_ShiJian_2_s[2]);
            int KaiShi_Shi = Integer.parseInt(KaiShi_ShiJian_2_s[0]);
            int KaiShi_Fen = Integer.parseInt(KaiShi_ShiJian_2_s[1]);
            int KaiShi_Miao = Integer.parseInt(KaiShi_ShiJian_2_s[2]);
            cha = (JieShu_Shi - KaiShi_Shi) * 3600 + (JieShu_Fen - KaiShi_Fen) * 60 + (JieShu_Miao - KaiShi_Miao);
            if (cha >= 6) {
                cha = 6;
            }
        }

        return cha;
    }

    /*
        刷新实时数据
     */
    public void ShuaXin_ShiShi_ShuJu(){
        PyObject ret = pyObject.callAttr("get_ShiShi_ShuJu", zhang_hao);//"get_ShiShi_ShuJu"为需要调用的函数名
        ShiShi_ShuJu = String.valueOf(ret);
        String[] strs = ShiShi_ShuJu.split(",");//分割数据
        tv_RiQi.setText(strs[0]);
        tv_WeiZhi.setText(strs[1]);
        tv_TiWen.setText(strs[2] + "℃");
        tv_XinLv.setText(strs[3] + " bpm");
        tv_XueYang.setText(strs[4] + "%");
        String now_time = HuoQu_DangQian_ShiJian.Get_Now_time();//现在时间
        int ShiJian_cha = get_ShiJianCha(now_time, strs[0]);//时间差
        if (ShiJian_cha>=6){
            tv_TiShi.setText("下位机未开启！");
        }
        else {
            tv_TiShi.setText("下位机已开启！");
        }
    }
}