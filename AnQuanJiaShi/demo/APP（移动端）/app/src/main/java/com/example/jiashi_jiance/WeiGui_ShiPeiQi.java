package com.example.jiashi_jiance;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

public class WeiGui_ShiPeiQi extends BaseAdapter {
    private final String[] JiLu;
    private Context mContext;
    private String ShuJu;
    private TextView tv_RiQi;
    private TextView tv_WeiZhi;
    private TextView tv_WeiGui_XingWei;
    private TextView tv_TiWen;
    private TextView tv_XinLv;
    private TextView tv_XueYang;
    private List<String> RiQi = new ArrayList<>();//日期
    private List<String> WeiZhi = new ArrayList<>();//位置
    private List<String> XingWei = new ArrayList<>();//行为
    private List<String> TiWen = new ArrayList<>();//体温
    private List<String> XinLv = new ArrayList<>();//心率
    private List<String> XueYang = new ArrayList<>();//血氧

    public WeiGui_ShiPeiQi(Context fragment_weiGui_jiLu, String valueOf) {
        this.mContext = fragment_weiGui_jiLu;
        this.ShuJu = valueOf;
        JiLu = valueOf.split(";");
        JiLu_ChaiFen();
    }

    //得到item的总数
    @Override
    public int getCount() {
        //返回ListView Item条目的总数
        return JiLu.length;
    }

    //得到Item代表的对象
    @Override
    public Object getItem(int i) {
        //返回ListView Item条目代表的对象
        return RiQi.get(i);
    }

    //得到Item的id
    @Override
    public long getItemId(int i) {
        //返回ListView Item的id
        return i;
    }

    @Override
    public View getView(int i, View view, ViewGroup viewGroup) {
        // 获取布局文件item_cart.xml的根视图
        view = LayoutInflater.from(mContext).inflate(R.layout.wei_gui_shi_pei_qi, null);
        tv_RiQi = view.findViewById(R.id.tv_RiQi);
        tv_WeiZhi = view.findViewById(R.id.tv_WeiZhi);
        tv_WeiGui_XingWei = view.findViewById(R.id.tv_WeiGui_XingWei);
        tv_TiWen = view.findViewById(R.id.tv_TiWen);
        tv_XinLv = view.findViewById(R.id.tv_XinLv);
        tv_XueYang = view.findViewById(R.id.tv_XueYang);

        tv_RiQi.setText(RiQi.get(i));
        tv_WeiZhi.setText(WeiZhi.get(i));
        tv_WeiGui_XingWei.setText(XingWei.get(i));
        tv_TiWen.setText(TiWen.get(i) + "℃");
        tv_XinLv.setText(XinLv.get(i) + " bpm");
        tv_XueYang.setText(XueYang.get(i) + "%");
        return view;
    }

    //记录拆分
    public void JiLu_ChaiFen() {
        String[] temp;
        for (int i = 0; i < JiLu.length; i++) {
            temp = JiLu[i].split(",");
            RiQi.add(temp[0]);
            WeiZhi.add(temp[1]);
            XingWei.add(temp[2]);
            TiWen.add(temp[3]);
            XinLv.add(temp[4]);
            XueYang.add(temp[5]);
        }
    }
}
