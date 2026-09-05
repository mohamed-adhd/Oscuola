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
            db.login_check(ui->login_email->text().toStdString(), ui->login_passwd->text().toStdString(), [this](bool success) {
                if (success) {
                    switchpg(2);
                } else {
                    ui->login_alert->setText("user not found");
                }
            });}
    });
    connect(ui->submit,&QPushButton::clicked,this,[this]() {
        if(ui->reg_email->text()=="" || ui->reg_pswd->text()=="" || ui->pswd_conf->text()==""){
            ui->login_alert->setText("fill all fields please(reg)");
        }else if(ui->reg_pswd->text()!= ui->pswd_conf->text()){
            ui->login_alert->setText("passwords must match");
        }
        else{
            db.registerr(ui->reg_email->text().toStdString(),ui->reg_pswd->text().toStdString(),[this](bool success){
                       if (success) {
                            ui->reg_alert->setText("we have submitted you account request , you will be notified by email when done ");
                       } else {
                           ui->reg_alert->setText("something went wrong , try again later");
                       }
                                                                   });}});


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