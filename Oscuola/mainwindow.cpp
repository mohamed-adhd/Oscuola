#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include "database.h"
MainWindow::MainWindow(database& dbo,QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow),db(dbo){
    ui->setupUi(this);
    setFixedSize(1280, 720);
    connect(ui->login_but,&QPushButton::clicked,this,[this]() {
        if(ui->login_email->text()==""){
            ui->login_alert->setText("fill all fields please");
        }else{
            if(db.login_check(ui->login_email->text().toStdString(),ui->login_passwd->text().toStdString())){
                switchpg(2);
            }else{
                ui->login_alert->setText("user not found");
            }
        }
    });

    connect(ui->reg_but,&QPushButton::clicked,this,[this]() {
        switchpg(1);
    });














}

MainWindow::~MainWindow()
{
    delete ui;
}
void MainWindow::switchpg(int to){
    ui->pages->setCurrentIndex(to);
}