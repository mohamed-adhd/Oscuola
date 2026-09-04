#ifndef DATABASE_H
#define DATABASE_H
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <json/json.h>
#include <QJsonObject>
class database{
private:
public :
        bool login_check(std::string email,std::string passwd){
            QNetworkAccessManager *manager = new QNetworkAccessManager(this);
            QNetworkRequest request(QUrl("https://oscuola-git-develop-midouamdouni4-7219s-projects.vercel.app/login_check"));
            request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
            request.setRawHeader("Authorization", "Bearer YOUR_TOKEN");
            QJsonObject json;
            json["email"] =   QString::fromStdString(email);
            json["passwd"] =  QString::fromStdString(passwd);
            QJsonDocument doc(json);
            QByteArray data = doc.toJson();
            QNetworkReply *res = manager->post(request, data);
            QByteArray responseData = res->readAll();
            QJsonDocument docs = QJsonDocument::fromJson(responseData);
            QJsonObject obj = docs.object();
            if(obj["status"]=="pass"){
                return true;
            }
            return false;


        }

};

#endif // DATABASE_H
