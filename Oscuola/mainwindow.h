#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "database.h"
QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    database& db;
    explicit MainWindow(database& dbo,QWidget *parent = nullptr);
    ~MainWindow() override;
    void switchpg(int to);

private:
    Ui::MainWindow *ui;

};
#endif // MAINWINDOW_H
