#ifndef XIUGAI_MIMA_H
#define XIUGAI_MIMA_H

#include <QMainWindow>

namespace Ui {
class XiuGai_MiMa;
}

class XiuGai_MiMa : public QMainWindow
{
    Q_OBJECT

public:
    explicit XiuGai_MiMa(QWidget *parent = nullptr);
    ~XiuGai_MiMa();

private:
    Ui::XiuGai_MiMa *ui;
};

#endif // XIUGAI_MIMA_H
