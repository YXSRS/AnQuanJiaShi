package com.example.jiashi_jiance;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Toast;

import com.example.jiashi_jiance.util.ViewUtil;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.Kwarg;
import com.chaquo.python.android.AndroidPlatform;

/*
    登录界面
 */

public class DengLu_JieMian extends AppCompatActivity implements View.OnClickListener {

    private Button btn_DengLu;
    private Button btn_WangJi_MiMa;
    private EditText et_ZhangHao;
    private EditText et_MiMa;
    private SharedPreferences preferences;
    private CheckBox ck_JiZhu_MiMa;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_deng_lu_jie_mian);

        // 初始化Python环境
        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }

        btn_DengLu = findViewById(R.id.btn_DengLu);//登录按钮
        btn_DengLu.setOnClickListener(this);//监听登录按钮按下

        btn_WangJi_MiMa = findViewById(R.id.btn_WangJi_MiMa);//忘记密码按钮
        btn_WangJi_MiMa.setOnClickListener(this);

        et_ZhangHao = findViewById(R.id.et_ZhangHao);//账号编辑框
        et_ZhangHao.addTextChangedListener(new HideTextWatcher(et_ZhangHao, 11));//添加文本变更监听器
        et_MiMa = findViewById(R.id.et_MiMa);//密码编辑框

        //记住密码部分
        ck_JiZhu_MiMa = findViewById(R.id.ck_JiZhu_MiMa);//记住密码单选框
        preferences = getSharedPreferences("BenDi_ZhangHao_MiMa", Context.MODE_PRIVATE);//本地账号密码
        DuQu_BaoCun_ZhangHao_MiMa();
    }

    //读取保存账号密码
    private void DuQu_BaoCun_ZhangHao_MiMa() {
        boolean gou_xuan_ji_zhu_mi_ma = preferences.getBoolean("GouXuan_JiZhu_MiMa", false);//勾选记住密码
        if (gou_xuan_ji_zhu_mi_ma) {
            String zhang_hao = preferences.getString("ZhangHao", "");
            et_ZhangHao.setText(zhang_hao);

            String mi_ma = preferences.getString("MiMa", "");
            et_MiMa.setText(mi_ma);
            ck_JiZhu_MiMa.setChecked(true);
        }
    }


    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.btn_DengLu: {
                //ShuJuKu.LianJie_ShuJuKu();

                String zhang_hao = et_ZhangHao.getText().toString();
                String mi_ma = et_MiMa.getText().toString();

                Python python = Python.getInstance(); // 初始化Python环境
                PyObject pyObject = python.getModule("Python_API");//"Python_API"为需要调用的Python文件名
                PyObject ret = pyObject.callAttr("PanDuan_ZhangHao_MiMa_ZhengQue", zhang_hao, mi_ma);//"PanDuan_ZhangHao_MiMa_ZhengQue"为需要调用的函数名

                String str = "";
                int flag = Integer.valueOf(String.valueOf(ret));
                if (flag == 0) {
                    //勾选了记住密码，保存到本地
                    if (ck_JiZhu_MiMa.isChecked()) {
                        SharedPreferences.Editor editor = preferences.edit();
                        editor.putString("ZhangHao", zhang_hao);
                        editor.putString("MiMa", mi_ma);
                        editor.putBoolean("GouXuan_JiZhu_MiMa", ck_JiZhu_MiMa.isChecked());//勾选记住密码
                        editor.commit();
                    }

                    //获取车主名
                    ret = pyObject.callAttr("get_CheZhuMing", zhang_hao);//"PanDuan_ZhangHao_MiMa_ZhengQue"为需要调用的函数名
                    String CheZhuMing = String.valueOf(ret);//车主名

                    //跳转到主界面
                    Intent intent = new Intent(this, Zhu_JieMian.class);
                    intent.putExtra("ZhangHao", zhang_hao);
                    intent.putExtra("CheZhuMing", CheZhuMing);
                    intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                    startActivity(intent);
                } else {
                    if (flag == 1) {
                        str = "没有该账号！";
                    } else if (flag == 2) {
                        str = "密码错误！";
                    }

                    //以下弹出对话框
                    AlertDialog.Builder builder = new AlertDialog.Builder(this);
                    builder.setTitle("提示");
                    builder.setMessage(str);
                    builder.setPositiveButton("好的", null);
                    AlertDialog dialog = builder.create();
                    dialog.show();
                }
                break;
            }
            case R.id.btn_WangJi_MiMa: {
                //跳转到找回密码的界面
                Intent intent = new Intent(this, ZhaoHui_MiMa_JieMian.class);
                intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                startActivity(intent);
                break;
            }
        }
    }

    //定义一个编辑框监听器，在输入文本达到指定长度时，自动隐藏输入法
    private class HideTextWatcher implements TextWatcher {
        private EditText mView;
        private int mMaxLength;

        public HideTextWatcher(EditText v, int maxLength) {
            this.mView = v;
            this.mMaxLength = maxLength;
        }

        @Override
        public void beforeTextChanged(CharSequence charSequence, int i, int i1, int i2) {

        }

        @Override
        public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) {

        }

        @Override
        public void afterTextChanged(Editable editable) {
            if (editable.toString().length() == mMaxLength) {
                //隐藏输入法软键盘
                ViewUtil.hideOneInputMethod(DengLu_JieMian.this, mView);
            }
        }
    }
}