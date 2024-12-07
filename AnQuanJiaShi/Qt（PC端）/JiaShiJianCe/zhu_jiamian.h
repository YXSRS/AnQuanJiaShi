#ifndef ZHU_JIAMIAN_H
#define ZHU_JIAMIAN_H

#include <QMainWindow>

namespace Ui {
class Zhu_JIaMian;
}

class Zhu_JIaMian : public QMainWindow
{
    Q_OBJECT

public:
    explicit Zhu_JIaMian(QWidget *parent = nullptr);
    ~Zhu_JIaMian();

public slots:
    void DianJi_XiuGai_ZiLiao();      //点击修改资料的槽函数
    void DianJi_XiuGai_MiMa();      //点击修改密码的槽函数
    void DianJi_LianXi_KeFu();      //点击联系客服的槽函数
    void DianJi_GuanYu_WoMen();      //点击关于我们的槽函数

private:
    Ui::Zhu_JIaMian *ui;
    //定时器事件
    void timerEvent(QTimerEvent *);

    //定时器标识号
    int id_ShiShi_ShuJu,id_WeiGui_JiLu;
};
#endif // ZHU_JIAMIAN_H
