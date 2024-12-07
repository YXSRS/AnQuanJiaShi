#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "zhaohui_mima.h"
#include <QDebug>
#include <QSqlDatabase>
#include <QSqlQuery>
#include <QMessageBox>
#include "zhu_jiamian.h"

/*
 * 登录界面
 */

QString zhang_hao;
QSqlDatabase d;

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    //设置窗口标题
    setWindowTitle("登录界面");

    //背景图片铺满整个窗口
    QPalette PAllbackground = this->palette();
    QImage ImgAllbackground(":/TuPian_ZiYuan/deng_lu_jie_mian.png");
    QImage fitimgpic=ImgAllbackground.scaled(this->width(),this->height(), Qt::IgnoreAspectRatio);
    PAllbackground.setBrush(QPalette::Window, QBrush(fitimgpic));
    this->setPalette(PAllbackground);

    //设置字体颜色
    QPalette ZiTi_YanSe;//字体颜色
    ZiTi_YanSe.setColor(QPalette::WindowText,Qt::white);//白色
    ui->lab_XiTong->setPalette(ZiTi_YanSe);
    ui->lab_YongHuDengLu->setPalette(ZiTi_YanSe);

    //设置字体大小
    QFont ZiTi_DaXiao;//字体大小
    ZiTi_DaXiao.setPointSize(20);
    ui->lab_XiTong->setFont(ZiTi_DaXiao);
    ui->lab_YongHuDengLu->setFont(ZiTi_DaXiao);

    //修改lab背景
    ui->lab_ZhangHao->setStyleSheet("QLabel{background:#ffffff;}");//白色
    ui->lab_MiMa->setStyleSheet("QLabel{background:#ffffff;}");//白色
    ui->lab_XiTong->setStyleSheet("QLabel{background:#000000;}");//黑色
    ui->lab_YongHuDengLu->setStyleSheet("QLabel{background:#000000;}");//黑色

    //数据库初始化
    ShuJuKu_Init();

    //点击登录按钮，判断帐号密码，正确就进入系统
    connect(ui->btn_DengLu,&QPushButton::clicked,[=]()mutable{
        zhang_hao=ui->bjk_ZhangHao->text();//获取用户输入的帐号
        QString mi_ma=ui->bjk_MiMa->text();//获取用户输入的密码

        if(zhang_hao.isEmpty()){
            QMessageBox::warning(this,"警告","帐号不能为空！");
            return ;
        }
        if(mi_ma.isEmpty()){
            QMessageBox::warning(this,"警告","密码不能为空！");
            return ;
        }

        //尝试打开数据库
        if(!d.open()){
            QMessageBox::warning(this,"警告","请检查网络连接！");
            return ;
        }

        QSqlQuery query;
        QString sql = QString("SELECT * FROM zhanghao_biao where ZhangHao = '%1'").arg(zhang_hao);
        if(query.exec(sql)) //执行sql语句是否成功
        {
            if(query.size()){//查询结果记录条数大于0,说明帐号存在
                query.next();
                if(mi_ma==query.value("MiMa").toString()){
                    Zhu_JIaMian *zhu_jiemian=new Zhu_JIaMian();
                    zhu_jiemian->show();
                    this->close();
                    return ;
                }
                else {
                    QMessageBox::warning(this,"警告","密码错误！");
                    return ;
                }
            }
            else {
                QMessageBox::warning(this,"警告","该帐号不存在！");
                return ;
            }
        }
    });

    //点击退出按钮，实现关闭窗口
    connect(ui->btn_TuiChu,&QPushButton::clicked,[=](){
        this->close();
    });

    //点击忘记密码按钮
    connect(ui->btn_WangJiMiMa,&QPushButton::clicked,[=](){
        ZhaoHui_MiMa *zhaohui_mima=new ZhaoHui_MiMa();
        zhaohui_mima->show();
    });
}

void ShuJuKu_Init(){//数据库初始化
    //connect mysql-server
    d = QSqlDatabase::addDatabase("QMYSQL"); //加载mysql驱动，这个字符串是固定的
    d.setHostName("39.103.177.201");
    d.setDatabaseName("anquan_jiashi");        //数据库名称
    d.setPort(3306);                     //数据库端口，如果没有更改/etc/mysql/my.cnf就不用改
    d.setUserName("root");
    d.setPassword("gccgcc");
}

MainWindow::~MainWindow()
{
    delete ui;
}

