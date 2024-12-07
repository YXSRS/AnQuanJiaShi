package com.example.jiashi_jiance;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

/*
    修改资料界面
 */

public class XiuGai_ZiLiao_JieMian extends AppCompatActivity implements View.OnClickListener {

    private ImageView iv_FanHui;
    private TextView tv_CheZhuMing;
    private Button btn_QueDing;
    private String zhang_hao;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_xiu_gai_zi_liao_jie_mian);

        // 初始化Python环境
        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }

        //从上一个页面获取账号
        zhang_hao = getIntent().getStringExtra("ZhangHao");

        iv_FanHui = findViewById(R.id.iv_FanHui);//返回
        tv_CheZhuMing = findViewById(R.id.tv_CheZhuMing);//车主名编辑框
        btn_QueDing = findViewById(R.id.btn_QueDing);//确定

        iv_FanHui.setOnClickListener(this);
        btn_QueDing.setOnClickListener(this);
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.iv_FanHui:
                finish();//结束当前活动页面
                break;
            case R.id.btn_QueDing:
                String che_zhu_ming = tv_CheZhuMing.getText().toString();

                Python python = Python.getInstance(); // 初始化Python环境
                PyObject pyObject = python.getModule("Python_API");//"Python_API"为需要调用的Python文件名
                PyObject ret = pyObject.callAttr("XiuGai_ZiLiao", zhang_hao, che_zhu_ming);//"XiuGai_ZiLiao"为需要调用的函数名

                //以下弹出对话框
                AlertDialog.Builder builder = new AlertDialog.Builder(this);
                builder.setTitle("提示");
                builder.setMessage("资料修改完成！");
                builder.setPositiveButton("好的", null);
                AlertDialog dialog = builder.create();
                dialog.show();
                break;
        }
    }
}