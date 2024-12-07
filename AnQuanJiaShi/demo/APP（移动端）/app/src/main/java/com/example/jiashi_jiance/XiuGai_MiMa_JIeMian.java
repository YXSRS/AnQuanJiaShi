package com.example.jiashi_jiance;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

/*
    修改密码界面
 */

public class XiuGai_MiMa_JIeMian extends AppCompatActivity implements View.OnClickListener {
    private Button btn_QueDing;
    private EditText et_ZhangHao;
    private EditText et_XinMiMa1;
    private EditText et_XinMiMa2;
    private ImageView iv_FanHui;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_xiu_gai_mi_ma_jie_mian);

        // 初始化Python环境
        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }

        iv_FanHui = findViewById(R.id.iv_FanHui);//返回
        iv_FanHui.setOnClickListener(this);

        btn_QueDing = findViewById(R.id.btn_QueDing);//确定按钮
        btn_QueDing.setOnClickListener(this);

        et_ZhangHao = findViewById(R.id.et_ZhangHao);//账号编辑框
        et_XinMiMa1 = findViewById(R.id.et_XinMiMa1);//新密码1编辑框
        et_XinMiMa2 = findViewById(R.id.et_XinMiMa2);//新密码2编辑框
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.iv_FanHui:
                finish();//结束当前活动页面
                break;
            case R.id.btn_QueDing: {
                //确定按钮被按下
                //检索数据库是否存在输入的账号，有：对比两次输入的密码；无：提示
                //两次输入密码一致：修改数据库密码；不一致：提示
                String zhang_hao = et_ZhangHao.getText().toString();
                String xin_MiMa1 = et_XinMiMa1.getText().toString();
                String xin_MiMa2 = et_XinMiMa2.getText().toString();
                if ((!zhang_hao.equals(""))&&(!xin_MiMa1.equals(""))&&(!xin_MiMa2.equals(""))) {//都不为空
                    if (xin_MiMa1.equals(xin_MiMa2)) {//两次输入密码一致
                        Python python = Python.getInstance(); // 初始化Python环境
                        PyObject pyObject = python.getModule("Python_API");//"Python_API"为需要调用的Python文件名
                        PyObject ret = pyObject.callAttr("ChaXun_ZhangHao_ShiFou_CunZai", zhang_hao);//"ChaXun_ZhangHao_ShiFou_CunZai"为需要调用的函数名
                        int flag = Integer.valueOf(String.valueOf(ret));
                        if (flag == 1) {//该账号存在
                            ret = pyObject.callAttr("XiuGai_MiMa", zhang_hao, xin_MiMa1);//"XiuGai_MiMa"为需要调用的函数名，修改密码
                            //弹出提示信息
                            AlertDialog textTips = new AlertDialog.Builder(XiuGai_MiMa_JIeMian.this).setTitle("提示").setMessage("密码修改成功！").create();
                            textTips.show();
                        } else {
                            //弹出提示信息
                            AlertDialog textTips = new AlertDialog.Builder(XiuGai_MiMa_JIeMian.this).setTitle("提示").setMessage("该账号不存在！").create();
                            textTips.show();
                        }
                    } else {
                        //弹出提示信息
                        AlertDialog textTips = new AlertDialog.Builder(XiuGai_MiMa_JIeMian.this).setTitle("提示").setMessage("两次输入的密码不一致！").create();
                        textTips.show();
                    }
                } else {
                    //弹出提示信息
                    AlertDialog textTips = new AlertDialog.Builder(XiuGai_MiMa_JIeMian.this).setTitle("提示").setMessage("请填完整信息，信息不能为空！").create();
                    textTips.show();
                }
                break;
            }
        }
    }
}