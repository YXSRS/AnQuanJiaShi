#ifndef ZHAOHUI_MIMA_H
#define ZHAOHUI_MIMA_H

#include <QWidget>

namespace Ui {
class ZhaoHui_MiMa;
}

class ZhaoHui_MiMa : public QWidget
{
    Q_OBJECT

public:
    explicit ZhaoHui_MiMa(QWidget *parent = nullptr);
    ~ZhaoHui_MiMa();

private:
    Ui::ZhaoHui_MiMa *ui;
};

#endif // ZHAOHUI_MIMA_H
