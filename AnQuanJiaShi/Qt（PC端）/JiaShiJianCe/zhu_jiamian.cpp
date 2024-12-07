#include "zhu_jiamian.h"
#include "ui_zhu_jiamian.h"
#include <QMenuBar>
#include <QMessageBox>
#include <QDebug>
#include <QSqlDatabase>
#include <QSqlQuery>
#include "xiugai_mima.h"
#include "xiugai_ziliao.h"
#include <QDateTime>

/*
 * 主界面
 */

extern QString zhang_hao;
extern QSqlDatabase d;

Zhu_JIaMian::Zhu_JIaMian(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::Zhu_JIaMian)
{
    ui->setupUi(this);
    //设置窗口标题
    setWindowTitle("智能安全驾驶检测系统");

    //包含菜单栏，只能有一个
    QMenuBar *CaiDanLan=menuBar();//菜单栏

    //将菜单栏放入到窗口中
    this->setMenuBar(CaiDanLan);

    //创建个人中心菜单
    QMenu *CaiDanLan_XuanXiang=CaiDanLan->addMenu("个人中心");//菜单栏选项

    //添加菜单项
    QAction *XiuGai_ZiLiao=CaiDanLan_XuanXiang->addAction("修改资料");
    CaiDanLan_XuanXiang->addSeparator();//添加分割线
    QAction *XiuGai_MiMa=CaiDanLan_XuanXiang->addAction("修改密码");
    CaiDanLan_XuanXiang->addSeparator();//添加分割线
    QAction *LianXi_KeFu=CaiDanLan_XuanXiang->addAction("联系客服");
    CaiDanLan_XuanXiang->addSeparator();//添加分割线
    QAction *GuanYu_WoMen=CaiDanLan_XuanXiang->addAction("关于我们");

    //点击 修改资料
    connect(XiuGai_ZiLiao,SIGNAL(triggered()),this,SLOT(DianJi_XiuGai_ZiLiao()));

    //点击 修改密码
    connect(XiuGai_MiMa,SIGNAL(triggered()),this,SLOT(DianJi_XiuGai_MiMa()));

    //点击 联系客服
    connect(LianXi_KeFu,SIGNAL(triggered()),this,SLOT(DianJi_LianXi_KeFu()));

    //点击 关于我们
    connect(GuanYu_WoMen,SIGNAL(triggered()),this,SLOT(DianJi_GuanYu_WoMen()));

    //启动定时器
    id_ShiShi_ShuJu=startTimer(3000);//每3000ms调用一次
    id_WeiGui_JiLu=startTimer(5000);//每5000ms调用一次

    //实时数据部分
    //设置字体颜色
    QString ZiTi_YanSe="color:#40E0D0;";//字体颜色，青绿色
    ui->lab_CheZhu1->setStyleSheet(ZiTi_YanSe);
    ui->lab_CheZhu2->setStyleSheet(ZiTi_YanSe);
    ui->lab_RiQi1->setStyleSheet(ZiTi_YanSe);
    ui->lab_RiQi2->setStyleSheet(ZiTi_YanSe);
    ui->lab_TiWen1->setStyleSheet(ZiTi_YanSe);
    ui->lab_TiWen2->setStyleSheet(ZiTi_YanSe);
    ui->lab_XinLv1->setStyleSheet(ZiTi_YanSe);
    ui->lab_XinLv2->setStyleSheet(ZiTi_YanSe);
    ui->lab_XueYang1->setStyleSheet(ZiTi_YanSe);
    ui->lab_XueYang2->setStyleSheet(ZiTi_YanSe);
    ui->lab_WeiZhi1->setStyleSheet(ZiTi_YanSe);
    ui->lab_WeiZhi2->setStyleSheet(ZiTi_YanSe);
    ZiTi_YanSe="color:#FF0000;";//字体颜色，红色
    ui->lab_TiShi1->setStyleSheet(ZiTi_YanSe);
    ui->lab_TiShi2->setStyleSheet(ZiTi_YanSe);

    //设置字体大小
    QFont ZiTi_DaXiao;//字体大小
    ZiTi_DaXiao.setPointSize(15);
    ui->lab_CheZhu1->setFont(ZiTi_DaXiao);
    ui->lab_CheZhu2->setFont(ZiTi_DaXiao);
    ui->lab_RiQi1->setFont(ZiTi_DaXiao);
    ui->lab_RiQi2->setFont(ZiTi_DaXiao);
    ui->lab_TiWen1->setFont(ZiTi_DaXiao);
    ui->lab_TiWen2->setFont(ZiTi_DaXiao);
    ui->lab_XinLv1->setFont(ZiTi_DaXiao);
    ui->lab_XinLv2->setFont(ZiTi_DaXiao);
    ui->lab_XueYang1->setFont(ZiTi_DaXiao);
    ui->lab_XueYang2->setFont(ZiTi_DaXiao);
    ui->lab_WeiZhi1->setFont(ZiTi_DaXiao);
    ui->lab_WeiZhi2->setFont(ZiTi_DaXiao);

    //设置按键背景颜色
    ui->btn_ShuaXin->setStyleSheet("background-color: rgb(64, 224, 208)");//青绿色

    //设置实时数据frame背景色
    //ui->frame->setStyleSheet("QFrame{background-color:#F8F8F8}");//

    //刷新按钮被按下
    connect(ui->btn_ShuaXin,&QPushButton::clicked,[=](){
        //尝试打开数据库
        if(!d.open()){
            QMessageBox::warning(this,"警告","请检查网络连接！");
            return ;
        }

        QSqlQuery query;
        QString sql = QString("SELECT * FROM shishi_biao where ZhangHao = '%1'").arg(zhang_hao);
        if(query.exec(sql)) //执行sql语句是否成功
        {
            if(query.size()){//查询结果记录条数大于0,说明帐号的实时数据存在
                query.next();

                //显示实时数据
                ui->lab_RiQi2->setText(query.value("ShiJian").toString());
                ui->lab_TiWen2->setText(query.value("TiWen").toString()+"'C");
                ui->lab_XinLv2->setText(query.value("XinLv").toString()+" bpm");
                ui->lab_XueYang2->setText(query.value("XueYang").toString()+"%");
                ui->lab_WeiZhi2->setText(query.value("WeiZhi").toString());

                //显示提示内容
                QDateTime XianZai_ShiJian = QDateTime::currentDateTime();//获取系统当前的时间
                QDateTime ShiShi_ShiJian = QDateTime::fromString(query.value("ShiJian").toString(), "yyyy-MM-dd hh:mm:ss");//实时时间
                qint64 ShiJian_Cha = XianZai_ShiJian.toTime_t() - ShiShi_ShiJian.toTime_t();//时间差，单位：秒
                if(ShiJian_Cha>5){
                    ui->lab_TiShi2->setText("下位机未开启！");
                }
                else {
                    ui->lab_TiShi2->setText("下位机已开启！");
                }

                //显示车主名
                sql = QString("SELECT * FROM zhanghao_biao where ZhangHao = '%1'").arg(zhang_hao);
                if(query.exec(sql)) //执行sql语句是否成功
                {
                    if(query.size()){//查询结果记录条数大于0,说明帐号数据存在
                        query.next();
                        ui->lab_CheZhu2->setText(query.value("CheZhuMing").toString());
                    }
                    else {
                        QMessageBox::warning(this,"警告","刷新失败！");
                        return ;
                    }
                }
                else {
                    QMessageBox::warning(this,"警告","刷新失败！");
                    return ;
                }

                QMessageBox::information(this,"提示","刷新成功！");
                return ;
            }
            else {
                QMessageBox::warning(this,"警告","该帐号的实时数据不存在！");
                return ;
            }
        }
    });

    //违规记录部分
    QStringList list;
    list<<"时间"<<"位置"<<"行为"<<"体温"<<"心率"<<"血氧";

    //告诉控件，有多少列
    ui->tableWidget->setColumnCount(list.size());

    //设置水平头
    ui->tableWidget->setHorizontalHeaderLabels(list);

    //设置列宽
    ui->tableWidget->setColumnWidth(0, 170);
    ui->tableWidget->setColumnWidth(1, 250);
    ui->tableWidget->setColumnWidth(2, 150);
    ui->tableWidget->setColumnWidth(3, 105);
    ui->tableWidget->setColumnWidth(4, 105);
    ui->tableWidget->setColumnWidth(5, 105);
}

void Zhu_JIaMian::DianJi_XiuGai_ZiLiao(){//点击修改资料
    XiuGai_ZiLiao *xiugai_ziliao=new XiuGai_ZiLiao();
    xiugai_ziliao->show();
    return;
}

void Zhu_JIaMian::DianJi_XiuGai_MiMa(){//点击修改密码
    XiuGai_MiMa *xiugai_mima=new XiuGai_MiMa();
    xiugai_mima->show();
    return;
}

void Zhu_JIaMian::DianJi_LianXi_KeFu(){//点击联系客服
    QMessageBox::information(this,"提示","电话：12345678901");
    return;
}

void Zhu_JIaMian::DianJi_GuanYu_WoMen(){//点击关于我们
    QMessageBox::information(this,"提示","智能安全驾驶检测系统Qt1.0版，我们是专业团队！");
    return;
}
//定时器事件
void Zhu_JIaMian::timerEvent(QTimerEvent *e){
    static int JiLu_num=0;//记录的条数
    static int JiLu_num_old=0;//旧的记录的条数

    if(e->timerId()==id_ShiShi_ShuJu){//实时数据
        //尝试打开数据库
        if(!d.open()){
            QMessageBox::warning(this,"警告","请检查网络连接！");
            return ;
        }

        QSqlQuery query;
        QString sql = QString("SELECT * FROM shishi_biao where ZhangHao = '%1'").arg(zhang_hao);
        if(query.exec(sql)) //执行sql语句是否成功
        {
            if(query.size()){//查询结果记录条数大于0,说明帐号的实时数据存在
                query.next();

                //显示实时数据
                ui->lab_RiQi2->setText(query.value("ShiJian").toString());
                ui->lab_TiWen2->setText(query.value("TiWen").toString()+"'C");
                ui->lab_XinLv2->setText(query.value("XinLv").toString()+" bpm");
                ui->lab_XueYang2->setText(query.value("XueYang").toString()+"%");
                ui->lab_WeiZhi2->setText(query.value("WeiZhi").toString());

                //显示提示内容
                QDateTime XianZai_ShiJian = QDateTime::currentDateTime();//获取系统当前的时间
                QDateTime ShiShi_ShiJian = QDateTime::fromString(query.value("ShiJian").toString(), "yyyy-MM-dd hh:mm:ss");//实时时间
                qint64 ShiJian_Cha = XianZai_ShiJian.toTime_t() - ShiShi_ShiJian.toTime_t();//时间差，单位：秒
                if(ShiJian_Cha>5){
                    ui->lab_TiShi2->setText("下位机未开启！");
                }
                else {
                    ui->lab_TiShi2->setText("下位机已开启！");
                }

                //显示车主名
                sql = QString("SELECT * FROM zhanghao_biao where ZhangHao = '%1'").arg(zhang_hao);
                if(query.exec(sql)) //执行sql语句是否成功
                {
                    if(query.size()){//查询结果记录条数大于0,说明帐号数据存在
                        query.next();
                        ui->lab_CheZhu2->setText(query.value("CheZhuMing").toString());
                    }
                }
            }
        }
    }

    if(e->timerId()==id_WeiGui_JiLu){//违规记录
        //尝试打开数据库
        if(!d.open()){
            QMessageBox::warning(this,"警告","请检查网络连接！");
            return ;
        }

        QSqlQuery query;
        QString sql = QString("SELECT * FROM weigui_biao");
        if(query.exec(sql)) //执行sql语句是否成功
        {
            JiLu_num_old=JiLu_num;
            JiLu_num=query.size();
            if(JiLu_num>0&&JiLu_num_old!=JiLu_num){//查询结果记录条数大于0,说明帐号的违规记录数据存在，两次的记录数不一致，说明有新的违规记录
                ui->tableWidget->clearContents();//清空表格内容
                ui->tableWidget->setRowCount(0);//删除表格线

                //设置列宽
                ui->tableWidget->setColumnWidth(0, 170);
                ui->tableWidget->setColumnWidth(1, 250);
                ui->tableWidget->setColumnWidth(2, 150);
                ui->tableWidget->setColumnWidth(3, 105);
                ui->tableWidget->setColumnWidth(4, 105);
                ui->tableWidget->setColumnWidth(5, 105);

                //将违规记录填入表格
                while (query.next()) {
                    ui->tableWidget->insertRow(0);
                    ui->tableWidget->setItem(0,0,new QTableWidgetItem(query.value("ShiJian").toString()));
                    ui->tableWidget->setItem(0,1,new QTableWidgetItem(query.value("WeiZhi").toString()));
                    ui->tableWidget->setItem(0,2,new QTableWidgetItem(query.value("XingWei").toString()));
                    ui->tableWidget->setItem(0,3,new QTableWidgetItem(query.value("TiWen").toString()+"'C"));
                    ui->tableWidget->setItem(0,4,new QTableWidgetItem(query.value("XinLv").toString()+" bpm"));
                    ui->tableWidget->setItem(0,5,new QTableWidgetItem(query.value("XueYang").toString()+"%"));
                }
            }
            else {
                return;
            }
        }
        else {
            return;
        }
    }
}

Zhu_JIaMian::~Zhu_JIaMian()
{
    delete ui;
}
