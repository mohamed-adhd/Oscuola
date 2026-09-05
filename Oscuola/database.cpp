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



void database::login_check(std::string email, std::string passwd, std::function<void(bool)> callback)
{
    QNetworkAccessManager *manager = new QNetworkAccessManager(this);
    QNetworkRequest request(QUrl("https://oscuola-kbqny06rq-midouamdouni4-7219s-projects.vercel.app/login_check"));
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
        bool success = (obj["message"].toString() == "pass");
        res->deleteLater();
        callback(success);
    });
}





void database::registerr(std::string email, std::string passwd, std::function<void(bool)> callback)
{
    QNetworkAccessManager *manager = new QNetworkAccessManager(this);
    QNetworkRequest request(QUrl("https://oscuola-nbp40xlyw-midouamdouni4-7219s-projects.vercel.app/insert_request"));
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



















