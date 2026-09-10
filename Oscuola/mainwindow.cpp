#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include "database.h"
#include <QButtonGroup>
MainWindow::MainWindow(database& dbo,QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow),db(dbo){
    ui->setupUi(this);
    switchpg(0);
    setFixedSize(1280, 720);

























    QButtonGroup *grades_buts= new QButtonGroup(this);
    for(int i=1;i<5;i++){
        QString name=QString("grades_button_student_%1").arg(i);
        QPushButton *button=this->findChild<QPushButton*>(name);
        if(button){
            grades_buts->addButton(button);
        }}
    connect(grades_buts,&QButtonGroup::buttonClicked,this,[this](QAbstractButton*) {
        if (!loaded_grades){
            QMap<QString, double> ss=db.st1_student_grade(std::get<4>(f));
            for (int row = 0; row < ui->grades_table->rowCount(); ++row) {
                QString subject = ui->grades_table->item(row, 0)->text();
                if (ss.contains(subject)) {
                    double value = ss[subject];
                    ui->grades_table->setItem(row, 1, new QTableWidgetItem(QString::number(value)));
                }
            }
            loaded_grades=true;
        }

        switchpg(3);});



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
    connect(alerts_buts,&QButtonGroup::buttonClicked,this,[this]() {
        if(!alertsloaded){
            std::vector<QString> alerts1st=db.st1_student_alerts(std::get<4>(f));
            for (int i=0;i<alerts1st.size();i++){
                ui->alerts_list_full->addItem(alerts1st[i]);
            }
            alertsloaded=true;

        }








switchpg(4);});



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
        QString name=QString("timeint table_but_student_%1").arg(i);
        QPushButton *button=this->findChild<QPushButton*>(name);
        if(button){
            time_buts->addButton(button);
        }}
    connect(time_buts,&QButtonGroup::buttonClicked,this,[this]() {
        if(!tbloaded){
            std::string  soi=db.fetch_timetable(std::get<5>(f),std::get<6>(f));
            QByteArray pfp = QByteArray::fromBase64(QString::fromStdString(soi).toUtf8());
            QPixmap p;
            QPixmap scaled = p.scaled(
                ui->timetable_picture_label->size(),
                Qt::KeepAspectRatio,
                Qt::SmoothTransformation
                );
            ui->timetable_picture_label->setPixmap(scaled);
            ui->timetable_picture_label->setAlignment(Qt::AlignCenter);
            tbloaded=true;
        }
        switchpg(6);});






    connect(ui->login_but,&QPushButton::clicked,this,[this]() {
        if(ui->login_email->text()==""){
            ui->login_alert->setText("fill all fields please");
        }else{
            std::tuple<std::string, std::string, std::string, std::string,int,int,int> s=db.login_check(ui->login_email->text().toStdString(), ui->login_passwd->text().toStdString());
            f=s;
            if (get<0>(s)!="false") {
                if(get<0>(s)=="student"){


                    std::string soi=db.fetch_timetable(std::get<5>(f),std::get<6>(f));
                    QByteArray pfp = QByteArray::fromBase64(QString::fromStdString(soi).toUtf8());
                    QPixmap p;
                    QPixmap scaled = p.scaled(
                        ui->timetable_picture_label->size(),
                        Qt::KeepAspectRatio,
                        Qt::SmoothTransformation
                        );
                    ui->timetable_picture_label->setPixmap(scaled);
                    ui->timetable_picture_label->setAlignment(Qt::AlignCenter);














                    switchpg(6);
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

















}

MainWindow::~MainWindow()
{
    delete ui;
}
void MainWindow::switchpg(int to){
    ui->pages->setCurrentIndex(to);
}