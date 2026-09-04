#include "mainwindow.h"
#include "./ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow){
    ui->setupUi(this);
    setFixedSize(1280, 720);
    connect(ui->login_but,&QPushButton::clicked,this,[this]() {
        if(ui->login_email->text()==""){
            ui->login_alert->setText("fill all fields please");
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