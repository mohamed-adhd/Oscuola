#include "mainwindow.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    database s;
    MainWindow w(s);
    w.show();
    return QApplication::exec();
}
