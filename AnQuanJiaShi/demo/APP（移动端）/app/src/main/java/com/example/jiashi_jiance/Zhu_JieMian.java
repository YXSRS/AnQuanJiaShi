package com.example.jiashi_jiance;

import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.os.Bundle;
import android.widget.RadioButton;
import android.widget.RadioGroup;

/*
    主界面
 */

public class Zhu_JieMian extends AppCompatActivity {

    private RadioGroup rg_DiBu_DaoHangLan;
    private RadioButton rb_ShiShi_ShuJu;
    private RadioButton rb_WeiGui_JiLu;
    private RadioButton rb_GeRen_ZhongXin;
    private fragment_ShiShi_ShuJu fragment_shiShi_shuJu;
    private fragment_WeiGui_JiLu fragment_weiGui_jiLu;
    private fragment_GeRen_ZhongXin fragment_geRen_zhongXin;
    private String zhang_hao;
    private String CheZhuMing;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_zhu_jie_mian);

        // 通过资源标识符获取控件实例
        rg_DiBu_DaoHangLan = findViewById(R.id.rg_DiBu_DaoHangLan);//底部导航栏
        rb_ShiShi_ShuJu = findViewById(R.id.rb_ShiShi_ShuJu);//实时数据
        rb_WeiGui_JiLu = findViewById(R.id.rb_WeiGui_JiLu);//违规记录
        rb_GeRen_ZhongXin = findViewById(R.id.rb_GeRen_ZhongXin);//个人中心

        //从上一个页面获取账号、车主名
        zhang_hao = getIntent().getStringExtra("ZhangHao");
        CheZhuMing = getIntent().getStringExtra("CheZhuMing");


        // 创建三个碎片实例
        fragment_shiShi_shuJu = new fragment_ShiShi_ShuJu(zhang_hao, CheZhuMing);
        fragment_weiGui_jiLu = new fragment_WeiGui_JiLu(zhang_hao);
        fragment_geRen_zhongXin = new fragment_GeRen_ZhongXin(zhang_hao, CheZhuMing);

        // 进行事件处理
        eventHandling();
        // 显示欢迎碎片
        showFragment(fragment_shiShi_shuJu);
    }

    /**
     * 显示碎片
     *
     * @param fragment
     */
    private void showFragment(Fragment fragment) {
        // 创建碎片管理器
        FragmentManager fm = getSupportFragmentManager();
        // 创建碎片事务
        FragmentTransaction ft = fm.beginTransaction();
        // 在容器里显示碎片
        ft.replace(R.id.container, fragment);
        // 提交碎片事务
        ft.commit();
    }

    private void eventHandling() {
        rg_DiBu_DaoHangLan.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup group, int checkedId) {
                switch (checkedId) {
                    case R.id.rb_ShiShi_ShuJu: //实时数据
                        showFragment(fragment_shiShi_shuJu);
                        break;
                    case R.id.rb_WeiGui_JiLu: //违规记录
                        showFragment(fragment_weiGui_jiLu);
                        break;
                    case R.id.rb_GeRen_ZhongXin: //个人中心
                        showFragment(fragment_geRen_zhongXin);
                        break;
                }
            }
        });
    }
}