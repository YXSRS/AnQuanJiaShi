#include "zhaohui_mima.h"
#include "ui_zhaohui_mima.h"
#include <QMessageBox>
#include <QDebug>
#include <QSqlDatabase>
#include <QSqlQuery>

/*
 * 找回密码
 */

extern QSqlDatabase d;

ZhaoHui_MiMa::ZhaoHui_MiMa(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::ZhaoHui_MiMa)
{
    ui->setupUi(this);
    //设置窗口标题
    setWindowTitle("找回密码");

    //确认按钮被按下
    connect(ui->btn_QueRen,&QPushButton::clicked,[=](){
        QString zhang_hao=ui->bjk_ZhangHao->text();//获取用户输入的帐号
        QString mi_ma1=ui->bjk_XinMiMa1->text();//获取用户输入的密码1
        QString mi_ma2=ui->bjk_XinMiMa2->text();//获取用户输入的密码2

        if(zhang_hao.isEmpty()||mi_ma1.isEmpty()||mi_ma2.isEmpty()){
            QMessageBox::warning(this,"警告","内容不能为空！");
            return ;
        }

        if(mi_ma1!=mi_ma2){//两次密码不一致
            QMessageBox::warning(this,"警告","两次输入的密码不一致！");
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
                sql = QString("update zhanghao_biao set MiMa='%1' where ZhangHao='%2'").arg(mi_ma1).arg(zhang_hao);
                if(query.exec(sql)){//执行sql语句是否成功，修改密码成功
                    QMessageBox::information(this,"提示","修改密码成功！");
                    this->close();
                    return ;
                }
                else {//修改密码失败
                    QMessageBox::warning(this,"警告","修改密码失败！");
                    return ;
                }
            }
            else {
                QMessageBox::warning(this,"警告","该帐号不存在！");
                return ;
            }
        }
    });
}

ZhaoHui_MiMa::~ZhaoHui_MiMa()
{
    delete ui;
}
