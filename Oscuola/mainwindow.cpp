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
            loaded_grades=true;
            QMap<QString, double> ss=db.st1_student_grade(std::get<4>(f));
            for (int row = 0; row < ui->grades_table->rowCount(); ++row) {
                QTableWidgetItem *sub = ui->grades_table->item(row, 0);
                if (sub == nullptr) {
                    continue;
                }
                QString subject = sub->text();
                if (ss.contains(subject)) {
                    double value = ss[subject];
                    ui->grades_table->setItem(row, 1, new QTableWidgetItem(QString::number(value)));
                }
            }

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




    QButtonGroup *time_buts_teach= new QButtonGroup(this);
    for(int i=1;i<5;i++){
        QString name=QString("timetable_but_teacher_%1").arg(i);
        QPushButton *button=this->findChild<QPushButton*>(name);
        if(button){
            time_buts_teach->addButton(button);
        }}

    QButtonGroup *grades_buts_teach= new QButtonGroup(this);
    for(int i=1;i<5;i++){
        QString name=QString("grades_button_teacher_%1").arg(i);
        QPushButton *button=this->findChild<QPushButton*>(name);
        if(button){
            grades_buts_teach->addButton(button);
        }}

    QButtonGroup *reqst_buts= new QButtonGroup(this);
    for(int i=1;i<5;i++){
        QString name=QString("requests_button_teacher_%1").arg(i);
        QPushButton *button=this->findChild<QPushButton*>(name);
        if(button){
            reqst_buts->addButton(button);
        }}



    QButtonGroup *back_buts_teach= new QButtonGroup(this);
    for(int i=1;i<5;i++){
        QString name=QString("back_home_btn_teacher_%1").arg(i);
        QPushButton *button=this->findChild<QPushButton*>(name);
        if(button){
            back_buts_teach->addButton(button);
        }}


    connect(back_buts_teach,&QButtonGroup::buttonClicked,this,[this](){
        switchpg(7);


    });




    connect(ui->teacher_timetable_load_btn,&QPushButton::clicked,this,[this]{
        int yeary=ui->teacher_timetable_class_combo->currentText().at(0).digitValue();
        int classs=ui->teacher_timetable_class_combo->currentText().at(2).digitValue();

        std::string  soi=db.fetch_timetable(yeary,classs);
        QByteArray pfp = QByteArray::fromBase64(QString::fromStdString(soi).toUtf8());
        QPixmap p;
        p.loadFromData(pfp);
        QPixmap scaled = p.scaled(
            ui->timetable_picture_label_teacher->size(),
            Qt::KeepAspectRatio,
            Qt::SmoothTransformation
            );
        ui->timetable_picture_label_teacher->setPixmap(scaled);
        ui->timetable_picture_label_teacher->setAlignment(Qt::AlignCenter);

    });

// yea after all , coding is all i have , like fr , nobody is here at 10 pm , just me and the github , man i love this, euphoric ass feeling




    connect(time_buts_teach,&QButtonGroup::buttonClicked,this,[this](){
        ui->teacher_timetable_class_combo->clear();
        QVector<QString> classes = db.get_classes(std::get<4>(f));
        for (const QString &c : classes)
            ui->teacher_timetable_class_combo->addItem(c);







        switchpg(8);


    });



    connect(grades_buts_teach,&QButtonGroup::buttonClicked,this,[this](){
        fillgradeclasses();
        switchpg(9);
    });


    connect(ui->teacher_grades_class_combo,&QComboBox::currentIndexChanged,this,[this](int){
        fillgradestudents();
    });


    connect(ui->teacher_grades_student_combo,&QComboBox::currentIndexChanged,this,[this](int){
        showgrades(ui->teacher_grades_student_combo->currentData().toInt());
    });


    connect(ui->teacher_grades_load_btn,&QPushButton::clicked,this,[this]{
        loadgrades();
    });


    connect(ui->teacher_grades_save_btn,&QPushButton::clicked,this,[this]{
        savegrades();
    });









    connect(reqst_buts,&QButtonGroup::buttonClicked,this,[this](){

        QList<QFrame*> oldRows = ui->panel_requests_teacher->findChildren<QFrame*>(
            QRegularExpression("^request_row_.*"));
        for (QFrame *f : oldRows) {
            f->deleteLater();}
        int y = 50;
        const int rowh = 64;
        const int spacing = 8;
        int index = 1;
        std::vector<req> temp = db.get_requests(std::get<4>(f));
        for (const req &r : temp) {
            QFrame *row = new QFrame(ui->panel_requests_teacher);
            row->setObjectName(QString("request_row_%1").arg(index));
            row->setGeometry(16, y, 908, rowh);

            QLabel *label = new QLabel(row);
            label->setGeometry(16, 8, 550, 48);
            label->setText(QString("%1 %2 (%3)").arg(QString::fromStdString(r.name)).arg(QString::fromStdString(r.aftername)).arg(QString::fromStdString(r.classs)));

            QPushButton *acceptBtn = new QPushButton("✅  Accept", row);
            acceptBtn->setGeometry(590, 12, 140, 40);
            acceptBtn->setCursor(Qt::PointingHandCursor);

            QPushButton *declineBtn = new QPushButton("❌  Decline", row);
            declineBtn->setGeometry(740, 12, 140, 40);
            declineBtn->setCursor(Qt::PointingHandCursor);

            std::string reqn = r.name;
            std::string reqaf = r.aftername;
            std::string reqcs = r.classs;

            connect(acceptBtn, &QPushButton::clicked, this, [this, reqn,reqaf,reqcs, row]() {
                db.accept(reqn,reqaf,reqcs);
                row->deleteLater();
            });

            connect(declineBtn, &QPushButton::clicked, this, [this, reqn,reqaf,reqcs, row]() {
                db.deleter(reqn,reqaf,reqcs);
                row->deleteLater();
            });

            row->show();
            y += rowh + spacing;
            index++;
        }











        switchpg(10);

    });



















    QButtonGroup *alerts_buts= new QButtonGroup(this);
    for(int i=1;i<5;i++){
        QString name=QString("alerts_student_but_%1").arg(i);
        QPushButton *button=this->findChild<QPushButton*>(name);
        if(button){
            alerts_buts->addButton(button);
        }}
    connect(alerts_buts,&QButtonGroup::buttonClicked,this,[this]() {
        if(!alertsloaded){
            alertsloaded=true;
            std::vector<QString> alerts1st=db.st1_student_alerts(std::get<4>(f));
            for (int i=0;i<alerts1st.size();i++){
                ui->alerts_list_full->addItem(alerts1st[i]);
            }


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
    connect(ui->btn_send_request,&QPushButton::clicked,this,[this](){
        if(db.sendpost(ui->request_subject->text(),ui->request_message->toPlainText())){
            ui->post_res->setText("request submitted");
        }else{
            ui->post_res->setText("something went wrong");
        }


        ;
    });


    QButtonGroup *time_buts= new QButtonGroup(this);
    for(int i=1;i<5;i++){
        QString name=QString("timetable_but_student_%1").arg(i);
        QPushButton *button=this->findChild<QPushButton*>(name);
        if(button){
            time_buts->addButton(button);
        }}

    connect(time_buts,&QButtonGroup::buttonClicked,this,[this]() {
        if(!tbloaded){
            tbloaded=true;
            std::string  soi=db.fetch_timetable(std::get<5>(f),std::get<6>(f));
            QByteArray pfp = QByteArray::fromBase64(QString::fromStdString(soi).toUtf8());
            QPixmap p;
            p.loadFromData(pfp,"JPEG");
            QPixmap scaled = p.scaled(
                ui->timetable_picture_label->size(),
                Qt::KeepAspectRatio,
                Qt::SmoothTransformation
                );
            ui->timetable_picture_label->setPixmap(scaled);
            ui->timetable_picture_label->setAlignment(Qt::AlignCenter);

        }
        switchpg(6);});

    QButtonGroup *logout_buts= new QButtonGroup(this);
    for(int i=1;i<6;i++){
        QString name=QString("logout_but_%1").arg(i);
        QPushButton *button=this->findChild<QPushButton*>(name);
        if(button){
            logout_buts->addButton(button);
        }}
    connect(logout_buts,&QButtonGroup::buttonClicked,this,[this]{
        switchpg(0);
    });



    connect(ui->login_but,&QPushButton::clicked,this,[this]() {
        if(ui->login_email->text()==""){
            ui->login_alert->setText("fill all fields please");
        }else{
            std::tuple<std::string, std::string, std::string, std::string,int,int,int> s=db.login_check(ui->login_email->text().toStdString(), ui->login_passwd->text().toStdString());
            qDebug()<<"the role recieved is "+get<0>(s);
            f=s;
            if (get<0>(s)!="false") {
                ui->user_name_label->setText(QString::fromStdString(std::get<1>(f))+" "+QString::fromStdString(std::get<2>(f)));
                if(get<0>(s)=="student"){

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

                    }













                }

                else if (get<0>(s)=="teacher"){
                    QByteArray pfp = QByteArray::fromBase64(QString::fromStdString(std::get<3>(s)).toUtf8());
                    QPixmap p;
                    if (!p.loadFromData(pfp, "JPEG")) {
                        qDebug() << "pix map failed ma guy!";
                    } else {
                        QPixmap scaled = p.scaled(
                            ui->teacher_pfp->size(),
                            Qt::KeepAspectRatio,
                            Qt::SmoothTransformation
                            );

                        ui->teacher_pfp->setPixmap(scaled);
                        ui->teacher_pfp->setAlignment(Qt::AlignCenter);

                    }





                    switchpg(7);
                }
                } else {
                ui->login_alert->setText("user not found");
            }
        }});
    connect(ui->btn_create_account,&QPushButton::clicked,this,[this]() {
        if(ui->reg_aftername->text()=="" || ui->reg_pswd->text()=="" || ui->pswd_conf->text()==""){
            ui->login_alert->setText("fill all fields please(reg)");
        }else if(ui->reg_pswd->text()!= ui->pswd_conf->text()){
            ui->login_alert->setText("passwords must match");
        }
        else{
            db.registerr(ui->reg_email->text().toStdString(),ui->reg_pswd->text().toStdString(),ui->classy->text().toStdString(),ui->reg_name->text().toStdString(),ui->reg_aftername->text().toStdString(),[this](bool success){
                if (success) {
                    ui->reg_alert->setText("we have submitted you account request , you will be notified by email when done ");
                } else {
                    ui->reg_alert->setText("something went wrong , try again later");
                }
            });}});



    connect(ui->reg_but,&QPushButton::clicked,this,[this]() {
        switchpg(1);});













}

MainWindow::~MainWindow()
{
    delete ui;
}
void MainWindow::switchpg(int to){
    ui->pages->setCurrentIndex(to);
}
void MainWindow::setgradeheaders(int year){
    QString sixth;
    if(year==1){
        sixth = "Life & Earth Sciences";
    }else if(year==2){
        sixth = "History & Geography";
    }else {
        sixth = "Philosophy";
    }
    QStringList headers = {
        "Student", "Mathematics", "French", "English",
        "Computer Science", "Physics", sixth, "Overall Grade"
    };
    ui->teacher_grades_list->setColumnCount(headers.size());
    ui->teacher_grades_list->setHorizontalHeaderLabels(headers);
    ui->teacher_grades_list->setRowCount(0);
}
void MainWindow::fillgradeclasses(){
    ui->teacher_grades_class_combo->blockSignals(true);
    ui->teacher_grades_class_combo->clear();
    QVector<QString> classes = db.get_classes(std::get<4>(f));
    for (const QString &c : classes){
        ui->teacher_grades_class_combo->addItem(c, c);
    }
    ui->teacher_grades_class_combo->blockSignals(false);
    fillgradestudents();
}
void MainWindow::fillgradestudents(){
    ui->teacher_grades_student_combo->blockSignals(true);
    ui->teacher_grades_student_combo->clear();
    roster.clear();
    if(ui->teacher_grades_class_combo->count()==0){
        ui->teacher_grades_student_combo->blockSignals(false);
        ui->teacher_grades_list->setRowCount(0);
        return;
    }
    roster = db.get_class_grades(ui->teacher_grades_class_combo->currentText().toStdString());
    ui->teacher_grades_student_combo->addItem("whole class", 0);
    for (const cgr &c : roster){
        ui->teacher_grades_student_combo->addItem(
            QString::fromStdString(c.aftername+" "+c.name+"; id : ")+QString::number(c.id), c.id);
    }
    ui->teacher_grades_student_combo->blockSignals(false);
    showgrades(ui->teacher_grades_student_combo->currentData().toInt());
}
void MainWindow::showgrades(int sid){
    int year = 1;
    for (const cgr &c : roster){
        if(c.year>0){
            year = c.year;
            break;
        }
    }
    setgradeheaders(year);
    QStringList keys = {"math","french","english","cs","ph","scvt"};
    int r = 0;
    for (const cgr &c : roster){
        if(sid!=0 && c.id!=sid){
            continue;
        }
        ui->teacher_grades_list->insertRow(r);
        QTableWidgetItem *who = new QTableWidgetItem(
            QString::fromStdString(c.aftername+" "+c.name));
        who->setFlags(who->flags() & ~Qt::ItemIsEditable);
        who->setData(Qt::UserRole, c.id);
        ui->teacher_grades_list->setItem(r,0,who);
        for(int k=0;k<keys.size();k++){
            ui->teacher_grades_list->setItem(r,k+1,
                new QTableWidgetItem(QString::number(c.grades.value(keys[k]),'f',2)));
        }
        QTableWidgetItem *ov = new QTableWidgetItem(QString::number(c.grades.value("overallg"),'f',2));
        ov->setFlags(ov->flags() & ~Qt::ItemIsEditable);
        ui->teacher_grades_list->setItem(r,7,ov);
        r++;
    }
    ui->teacher_grades_list->resizeColumnsToContents();
}
void MainWindow::loadgrades(){
    if(ui->teacher_grades_class_combo->count()==0){
        ui->teacher_grades_res->setText("no class picked");
        return;
    }
    fillgradestudents();
    ui->teacher_grades_res->setText(roster.size()==0 ? "no students in that class" : "loaded");
}
void MainWindow::savegrades(){
    QTableWidget *tbl = ui->teacher_grades_list;
    if(tbl->rowCount()==0){
        ui->teacher_grades_res->setText("nothing to save");
        return;
    }
    QStringList keys = {"math","french","english","cs","ph","scvt"};
    int done = 0;
    int year = 0;
    for(int r=0;r<tbl->rowCount();r++){
        QTableWidgetItem *who = tbl->item(r,0);
        if(who==nullptr){
            continue;
        }
        int id = who->data(Qt::UserRole).toInt();
        QMap<QString,double> g;
        for(int k=0;k<keys.size();k++){
            QTableWidgetItem *cell = tbl->item(r,k+1);
            bool good = false;
            double v = cell==nullptr ? 0.0 : cell->text().toDouble(&good);
            if(cell!=nullptr && !good){
                ui->teacher_grades_res->setText("bad number on row "+QString::number(r+1));
                return;
            }
            g[keys[k]] = v;
        }
        if(db.post_grades(id,g,&year)){
            done++;
        }
    }
    if(done>0){
        fillgradestudents();
    }
    ui->teacher_grades_res->setText("saved "+QString::number(done)+" student(s)");
}