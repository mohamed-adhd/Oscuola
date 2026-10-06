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
    std::tuple<std::string, std::string, std::string, std::string,int,int,int> f;
    bool loaded_grades=false,alertsloaded=false,tbloaded=false;
    database& db;
    std::vector<studs> momo;
    explicit MainWindow(database& dbo,QWidget *parent = nullptr);
    ~MainWindow() override;
    void switchpg(int to);
    void fillgradeclasses();
    void fillgradestudents();
    void showgrades(int sid);
    void loadgrades();
    void savegrades();
    void setgradeheaders(int year);

private:
    Ui::MainWindow *ui;
    std::vector<cgr> roster;

};
#endif // MAINWINDOW_H
