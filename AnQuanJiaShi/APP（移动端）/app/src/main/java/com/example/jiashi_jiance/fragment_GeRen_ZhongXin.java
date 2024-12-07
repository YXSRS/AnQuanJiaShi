package com.example.jiashi_jiance;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;

import androidx.appcompat.app.AlertDialog;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;

/*
    个人中心碎片
 */

public class fragment_GeRen_ZhongXin extends Fragment implements View.OnClickListener {
    String zhang_hao;
    String che_zhu_ming;
    private Button btn_TuiChu_DengLu;
    private TextView tv_cheZhuMing;
    private Button btn_XiuGai_ZiLiao;
    private Button btn_XiuGai_MiMa;
    private Button btn_LianXi_KeFu;
    private Button btn_GuanYu_WoMen;

    public fragment_GeRen_ZhongXin(String ZhangHao, String CheZhuMing) {
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
        View view = LayoutInflater.from(context).inflate(R.layout.fragment_ge_ren_zhong_xin, container, false);

        tv_cheZhuMing = view.findViewById(R.id.tv_CheZhuMing);//车主名
        btn_TuiChu_DengLu = view.findViewById(R.id.btn_TuiChu_DengLu);//退出登录
        btn_XiuGai_ZiLiao = view.findViewById(R.id.btn_XiuGai_ZiLiao);//修改资料
        btn_XiuGai_MiMa = view.findViewById(R.id.btn_XiuGai_MiMa);//修改密码
        btn_LianXi_KeFu = view.findViewById(R.id.btn_LianXi_KeFu);//联系客服
        btn_GuanYu_WoMen = view.findViewById(R.id.btn_GuanYu_WoMen);//关于我们

        btn_TuiChu_DengLu.setOnClickListener(this);
        btn_XiuGai_ZiLiao.setOnClickListener(this);
        btn_XiuGai_MiMa.setOnClickListener(this);
        btn_LianXi_KeFu.setOnClickListener(this);
        btn_GuanYu_WoMen.setOnClickListener(this);

        tv_cheZhuMing.setText(che_zhu_ming);

        return view;
    }

    @Override
    public void onClick(View view) {
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        AlertDialog dialog;
        Intent intent;
        switch (view.getId()) {
            case R.id.btn_TuiChu_DengLu:
                Activity activity = getActivity();
                activity.finish();//结束当前活动页面
                break;
            case R.id.btn_XiuGai_ZiLiao:
                //跳转到修改资料界面
                intent = new Intent(getActivity(), XiuGai_ZiLiao_JieMian.class);
                intent.putExtra("ZhangHao", zhang_hao);
                intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                startActivity(intent);
                break;
            case R.id.btn_XiuGai_MiMa:
                //跳转到修改密码界面
                intent = new Intent(getActivity(), XiuGai_MiMa_JIeMian.class);
                intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                startActivity(intent);
                break;
            case R.id.btn_LianXi_KeFu:
                //以下弹出对话框
                builder.setTitle("联系客服");
                builder.setMessage("电话：12345678901");
                builder.setPositiveButton("好的", null);
                dialog = builder.create();
                dialog.show();
                break;
            case R.id.btn_GuanYu_WoMen:
                //以下弹出对话框
                builder.setTitle("关于我们");
                builder.setMessage("这是智能安全驾驶检测系统上位机1.0版本，我们是专业团队。");
                builder.setPositiveButton("好的", null);
                dialog = builder.create();
                dialog.show();
                break;
        }
    }
}