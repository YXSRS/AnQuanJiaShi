#include "mainwindow.h"
#include <QApplication>
#include <QIcon>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QApplication::setWindowIcon(QIcon(":/TuPian_ZiYuan/TuBiao.ico"));
    MainWindow w;
    w.show();
    return a.exec();
}
