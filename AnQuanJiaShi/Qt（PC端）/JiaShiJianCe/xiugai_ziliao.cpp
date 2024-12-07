#include "xiugai_ziliao.h"
#include "ui_xiugai_ziliao.h"
#include <QMessageBox>
#include <QDebug>
#include <QSqlDatabase>
#include <QSqlQuery>

/*
 * 修改资料
 */

extern QSqlDatabase d;
extern QString zhang_hao;

XiuGai_ZiLiao::XiuGai_ZiLiao(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::XiuGai_ZiLiao)
{
    ui->setupUi(this);
    //设置窗口标题
    setWindowTitle("修改资料");

    //确定按键被点击
    connect(ui->btn_QueDing,&QPushButton::clicked,[=](){
        QString CheZhuMing=ui->bjk_CheZhuMing->text();//获取用户输入的车主名

        if(CheZhuMing.isEmpty()){
            QMessageBox::warning(this,"警告","内容不能为空！");
            return ;
        }

        //尝试打开数据库
        if(!d.open()){
            QMessageBox::warning(this,"警告","请检查网络连接！");
            return ;
        }

        QSqlQuery query;
        QString sql = QString("update zhanghao_biao set CheZhuMing='%1' where ZhangHao='%2'").arg(CheZhuMing).arg(zhang_hao);
        if(query.exec(sql)) //执行sql语句是否成功
        {
            QMessageBox::information(this,"提示","修改资料成功！");
            this->close();
            return ;
        }
    });
}

XiuGai_ZiLiao::~XiuGai_ZiLiao()
{
    delete ui;
}
