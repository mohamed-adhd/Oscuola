#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include "database.h"
#include <QButtonGroup>
MainWindow::MainWindow(database& dbo,QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow),db(dbo){
    ui->setupUi(this);
    switchpg(2);
    setFixedSize(1280, 720);
    db.st1_student_grade(1);
    QButtonGroup *grades_buts= new QButtonGroup(this);
    for(int i=1;i<5;i++){
        QString name=QString("grades_button_student_%1").arg(i);
        QPushButton *button=this->findChild<QPushButton*>(name);
        if(button){
            grades_buts->addButton(button);
        }}
    connect(grades_buts,&QButtonGroup::buttonClicked,this,[this]() {switchpg(3);});



    QButtonGroup *back_buts= new QButtonGroup(this);
    for(int i=1;i<5;i++){
        QString name=QString("back_home_btn_%1").arg(i);
        QPushButton *button=this->findChild<QPushButton*>(name);
        if(button){
            back_buts->addButton(button);
        }}
    connect(back_buts,&QButtonGroup::buttonClicked,this,[this]() {switchpg(2);});




    QButtonGroup *alerts_buts= new QButtonGroup(this);
    for(int i=1;i<5;i++){
        QString name=QString("alerts_student_but_%1").arg(i);
        QPushButton *button=this->findChild<QPushButton*>(name);
        if(button){
            alerts_buts->addButton(button);
        }}
    connect(alerts_buts,&QButtonGroup::buttonClicked,this,[this]() {switchpg(4);});



    QButtonGroup *post_buts= new QButtonGroup(this);
    for(int i=1;i<5;i++){
        QString name=QString("post_button_student_%1").arg(i);
        QPushButton *button=this->findChild<QPushButton*>(name);
        if(button){
            post_buts->addButton(button);
        }}
    connect(post_buts,&QButtonGroup::buttonClicked,this,[this]() {switchpg(5);});



    QButtonGroup *time_buts= new QButtonGroup(this);
    for(int i=1;i<5;i++){
        QString name=QString("timetable_but_student_%1").arg(i);
        QPushButton *button=this->findChild<QPushButton*>(name);
        if(button){
            time_buts->addButton(button);
        }}
    connect(time_buts,&QButtonGroup::buttonClicked,this,[this]() {switchpg(6);});






    connect(ui->login_but,&QPushButton::clicked,this,[this]() {
        if(ui->login_email->text()==""){
            ui->login_alert->setText("fill all fields please");
        }else{
            std::tuple<std::string, std::string, std::string, std::string> s=db.login_check(ui->login_email->text().toStdString(), ui->login_passwd->text().toStdString());
            if (get<0>(s)!="false") {
                if(get<0>(s)=="student"){
                    switchpg(2);
                }
                QByteArray pfp = QByteArray::fromBase64(QString::fromStdString(std::get<3>(s)).toUtf8());
                QPixmap p;
                if (!p.loadFromData(pfp, "JPEG")) {
                    qDebug() << "pix map failed ma guy!";
                } else {
                    QPixmap scaled = p.scaled(
                        ui->pfp->size(),
                        Qt::KeepAspectRatio,
                        Qt::SmoothTransformation
                        );

                    ui->pfp->setPixmap(scaled);
                    ui->pfp->setAlignment(Qt::AlignCenter);

                }} else {
                ui->login_alert->setText("user not found");
            }
        }});
    connect(ui->reg_but,&QPushButton::clicked,this,[this]() {
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