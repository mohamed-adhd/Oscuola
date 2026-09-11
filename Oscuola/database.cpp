#include "database.h"
#include <QNetworkAccessManager>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <json/json.h>
#include <QJsonObject>
#include <QFile>
#include <QTextStream>
#include <QMap>
#include <QString>
#include <stdio.h>
#include <iostream>
#include <QDir>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <stdlib.h>
#include<QCoreApplication>
using namespace std;
QMap<QString, QString> loadEnv(const QString &path = ".env")
{
    QMap<QString, QString> env;
    QFile file(path);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qDebug() << "Working dir:" << QDir::currentPath();
        qWarning() << "Couldnt open that shi:" << path;
        return env;
    }

    QTextStream in(&file);
    while (!in.atEnd()) {
        QString line = in.readLine().trimmed();
        if (line.isEmpty() || line.startsWith('#'))
            continue;

        int eqIndex = line.indexOf('=');
        if (eqIndex == -1)
            continue;

        QString key = line.left(eqIndex).trimmed();
        QString value = line.mid(eqIndex + 1).trimmed();
                if (value.startsWith('"') && value.endsWith('"'))
            value = value.mid(1, value.length() - 2);

        env[key] = value;
    }

    return env;
}

QMap<QString, QString> loadEnvResolved()
{
    QDir dir(QCoreApplication::applicationDirPath());
    for (int i = 0; i < 5; ++i) {
        if (dir.exists(".env")) {
            return loadEnv(dir.filePath(".env"));
        }
        dir.cdUp();
    }
    qWarning() << ".env not found gang";
    return {};
}



std::tuple<std::string, std::string, std::string, std::string,int,int,int > database::login_check(std::string email, std::string passwd)
{
    QNetworkAccessManager *manager = new QNetworkAccessManager(this);
    QNetworkRequest request(QUrl("https://oscuola-b72k84s73-midouamdouni4-7219s-projects.vercel.app/login_check"));
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QMap<QString, QString> bs = loadEnvResolved();
    QString dakey = bs.value("API_KEY");
    //qDebug() << dakey;
    QByteArray auth = "Bearer " + dakey.toUtf8();
    request.setRawHeader("Authorization", auth);
    QJsonObject json;
    json["gmail"] = QString::fromStdString(email);
    json["passwd"] = QString::fromStdString(passwd);
    qDebug() << json["email"].toString();
    qDebug() << json["passwd"].toString();
    QJsonDocument doc(json);
    QByteArray data = doc.toJson();
    QNetworkReply *res = manager->post(request, data);
    QEventLoop loop;

    connect(
        res,
        &QNetworkReply::finished,
        &loop,
        &QEventLoop::quit
        );

    loop.exec();
        QByteArray responseData = res->readAll();
        QJsonDocument docs = QJsonDocument::fromJson(responseData);
        QJsonObject obj = docs.object();
        //qDebug() << obj["success"].toString();
        //qDebug() << "year:" << obj["year"];
        //qDebug() << "year string:" << obj["year"].toString();
        //qDebug() << "year int:" << obj["year"].toInt();

        //qDebug() << "class:" << obj["class"];
        //qDebug() << "class string:" << obj["class"].toString();
        //qDebug() << "class int:" << obj["class"].toInt();
        //qDebug() << "the role   : " +obj["role"].toString();
        //qDebug() << "the name   : " +obj["name"].toString();
        //qDebug() << "the aftername   : " +obj["aftername"].toString();
        //qDebug() << obj["pfp"].toString();qDebug() << obj["ids"].toString();
        if(obj["success"].toBool()==true){
            std::tuple<std::string, std::string, std::string, std::string,int,int,int> temp;
            std::get<0>(temp) =obj["role"].toString().toStdString();
            std::get<1>(temp) =obj["name"].toString().toStdString();
            std::get<2>(temp) =obj["aftername"].toString().toStdString();
            std::get<3>(temp) = obj["pfp"].toString().toStdString();
            std::get<4>(temp) = obj["ids"].toInt();
            std::get<5>(temp) = obj["year"].toInt();
            std::get<6>(temp) = obj["class"].toInt();
            res->deleteLater();
            manager->deleteLater();
            return temp;
        }else{
            std::tuple<std::string, std::string, std::string, std::string,int,int,int> temp;
            std::get<0>(temp) ="false";
            res->deleteLater();
            manager->deleteLater();
            return temp;
        }

    };






    ;




void database::registerr(std::string email, std::string passwd, std::function<void(bool)> callback)
{
    QNetworkAccessManager *manager = new QNetworkAccessManager(this);
    QNetworkRequest request(QUrl("https://oscuola-65alqz1pf-midouamdouni4-7219s-projects.vercel.app/insert_request"));
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QMap<QString, QString> bs = loadEnvResolved();
    QString dakey = bs.value("API_KEY");
    qDebug() << dakey;
    QByteArray auth = "Bearer " + dakey.toUtf8();
    request.setRawHeader("Authorization", auth);
    QJsonObject json;
    json["gmail"] = QString::fromStdString(email);
    json["passwd"] = QString::fromStdString(passwd);
    //qDebug() << json["email"].toString();
    //qDebug() << json["passwd"].toString();
    QJsonDocument doc(json);
    QByteArray data = doc.toJson();
    QNetworkReply *res = manager->post(request, data);
    connect(res, &QNetworkReply::finished, this, [res, callback]() {
        QByteArray responseData = res->readAll();
        QJsonDocument docs = QJsonDocument::fromJson(responseData);
        QJsonObject obj = docs.object();
        std::cout << obj["message"].toString().toStdString() << std::endl;
        qDebug() << obj["message"].toString();
        bool success = (obj["message"].toString() == "inserted");
        res->deleteLater();
        callback(success);
    });
}



bool database::sendpost(QString subject,QString message){
    QNetworkAccessManager *manager = new QNetworkAccessManager(this);
    QNetworkRequest request(QUrl("https://oscuola-aeggv6ler-midouamdouni4-7219s-projects.vercel.app/post_request"));
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QMap<QString, QString> bs = loadEnvResolved();
    QString dakey = bs.value("API_KEY");
    qDebug() << dakey;
    QByteArray auth = "Bearer " + dakey.toUtf8();
    request.setRawHeader("Authorization", auth);
    QJsonObject json;
    json["subject"] = QString::fromStdString(subject.toStdString());
    json["message"] = QString::fromStdString(message.toStdString());
    //qDebug() << json["email"].toString();
    //qDebug() << json["passwd"].toString();
    QJsonDocument doc(json);
    QByteArray data = doc.toJson();
    QNetworkReply *res = manager->post(request, data);
    QEventLoop loop;
    connect(res,&QNetworkReply::finished,&loop,&QEventLoop::quit);
    loop.exec();
    QByteArray responseData = res->readAll();
    qDebug().noquote() << responseData;
    QJsonDocument docs = QJsonDocument::fromJson(responseData);
    QJsonObject obj = docs.object();
    qDebug()<<obj["message"].toBool();
    return obj["message"].toBool();

}
 QMap<QString, double> database::st1_student_grade(int id)
{
    QNetworkAccessManager *manager = new QNetworkAccessManager(this);
    QNetworkRequest request(QUrl("https://oscuola-cnb10ca6y-midouamdouni4-7219s-projects.vercel.app/s1t_year_student"));
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QMap<QString, QString> bs = loadEnvResolved();
    QString dakey = bs.value("API_KEY");
    qDebug() << dakey;
    QByteArray auth = "Bearer " + dakey.toUtf8();
    request.setRawHeader("Authorization", auth);
    QJsonObject json;
    json["id"] = QString::fromStdString(std::to_string(id));
    QJsonDocument doc(json);
    QByteArray data = doc.toJson();
    QNetworkReply *res = manager->post(request, data);
    QEventLoop loop;

    connect(res,&QNetworkReply::finished,&loop,&QEventLoop::quit);

    loop.exec();
    QByteArray responseData = res->readAll();
    QJsonDocument docs = QJsonDocument::fromJson(responseData);
    QJsonObject obj = docs.object();
    //qDebug() << obj["success"].toString();
    //qDebug() << obj["math"].toString();
    //qDebug() << obj["cs"].toString();

    QMap<QString, double> temp = {
        {"math", obj["math"].toDouble()},
        {"french", obj["french"].toDouble()},
        {"english", obj["english"].toDouble()},
        {"cs", obj["cs"].toDouble()},
        {"ph",obj["ph"].toDouble()},
        {"scvt", obj["scvt"].toDouble()},
        {"overallg",obj["og"].toDouble()}
    };

    return temp;



};

std::string database::fetch_timetable(int year,int classs)
{
    QNetworkAccessManager *manager = new QNetworkAccessManager(this);
    QNetworkRequest request(QUrl("https://oscuola-b72k84s73-midouamdouni4-7219s-projects.vercel.app/timetable"));
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QMap<QString, QString> bs = loadEnvResolved();
    QString dakey = bs.value("API_KEY");
    //qDebug() << dakey;
    QByteArray auth = "Bearer " + dakey.toUtf8();
    request.setRawHeader("Authorization", auth);
    QJsonObject json;
    qDebug()<<year;
    qDebug()<<classs;
    json["classs"] = QString::fromStdString(std::to_string(classs));
    json["year"] = QString::fromStdString(std::to_string(year));

    QJsonDocument doc(json);
    QByteArray data = doc.toJson();
    QNetworkReply *res = manager->post(request, data);
    QEventLoop loop;

    connect(res,&QNetworkReply::finished,&loop,&QEventLoop::quit);

    loop.exec();
    QByteArray responseData = res->readAll();
    qDebug().noquote() << responseData;
    QJsonDocument docs = QJsonDocument::fromJson(responseData);
    QJsonObject obj = docs.object();
    qDebug() << obj["tb"].toString();
    return obj["tb"].toString().toStdString();

}



std::vector<QString> database::st1_student_alerts(int id)
{
    QNetworkAccessManager *manager = new QNetworkAccessManager(this);
    QNetworkRequest request(QUrl("https://oscuola-jka2tv75x-midouamdouni4-7219s-projects.vercel.app/s1t_alerts"));
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QMap<QString, QString> bs = loadEnvResolved();
    QString dakey = bs.value("API_KEY");
    //qDebug() << dakey;
    QByteArray auth = "Bearer " + dakey.toUtf8();
    request.setRawHeader("Authorization", auth);
    QJsonObject json;
    json["id"] = QString::fromStdString(std::to_string(id));
    QJsonDocument doc(json);
    QByteArray data = doc.toJson();
    QNetworkReply *res = manager->post(request, data);
    QEventLoop loop;

    connect(res,&QNetworkReply::finished,&loop,&QEventLoop::quit);

    loop.exec();
    QByteArray responseData = res->readAll();
    QJsonDocument docs = QJsonDocument::fromJson(responseData);
    QJsonObject obj = docs.object();
    QJsonArray dataArray = obj.value("data").toArray();
    std::vector<QString> temp;
    for (const QJsonValue &enntry : dataArray){
        if (enntry.isArray()){
            QJsonArray inner = enntry.toArray();
            for (const QJsonValue &ennntry : inner){
                temp.push_back(ennntry.toString());
            }
        }
    }


    return temp;



};






















;














