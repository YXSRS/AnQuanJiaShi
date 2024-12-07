#ifndef XIUGAI_ZILIAO_H
#define XIUGAI_ZILIAO_H

#include <QMainWindow>

namespace Ui {
class XiuGai_ZiLiao;
}

class XiuGai_ZiLiao : public QMainWindow
{
    Q_OBJECT

public:
    explicit XiuGai_ZiLiao(QWidget *parent = nullptr);
    ~XiuGai_ZiLiao();

private:
    Ui::XiuGai_ZiLiao *ui;
};

#endif // XIUGAI_ZILIAO_H
