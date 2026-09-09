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



std::tuple<std::string, std::string, std::string, std::string> database::login_check(std::string email, std::string passwd)
{
    QNetworkAccessManager *manager = new QNetworkAccessManager(this);
    QNetworkRequest request(QUrl("https://oscuola-cfrspd9cj-midouamdouni4-7219s-projects.vercel.app/login_check"));
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");

    QMap<QString, QString> bs = loadEnvResolved();
    QString dakey = bs.value("API_KEY");
    qDebug() << dakey;
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
        qDebug() << obj["success"].toString();
        qDebug() << obj["role"].toString();
        qDebug() << obj["name"].toString();
        qDebug() << obj["pfp"].toString();
        if(obj["success"].toBool()==true){
            std::tuple<std::string, std::string, std::string, std::string> temp;
            std::get<0>(temp) =obj["role"].toString().toStdString();
            std::get<1>(temp) =obj["name"].toString().toStdString();
            std::get<2>(temp) =obj["aftername"].toString().toStdString();
            std::get<3>(temp) = obj["pfp"].toString().toStdString();
            res->deleteLater();
            manager->deleteLater();
            return temp;
        }else{
            std::tuple<std::string, std::string, std::string, std::string> temp;
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
    qDebug() << json["email"].toString();
    qDebug() << json["passwd"].toString();
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







std::vector<int> database::st1_student_grade(int id)
{
    QNetworkAccessManager *manager = new QNetworkAccessManager(this);
    QNetworkRequest request(QUrl("https://oscuola-7mjaohwl9-midouamdouni4-7219s-projects.vercel.app/s1t_year_student"));
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
    qDebug() << obj["success"].toString();
    qDebug() << obj["math"].toString();
    qDebug() << obj["cs"].toString();
    std::vector<int> temp;
    temp.push_back(obj["math"].toInt());
    temp.push_back(obj["french"].toInt());
    temp.push_back(obj["english"].toInt());
    temp.push_back(obj["cs"].toInt());
    temp.push_back(obj["ph"].toInt());
    temp.push_back(obj["scvt"].toInt());
    temp.push_back(obj["og"].toInt());
    return temp;




};






;














