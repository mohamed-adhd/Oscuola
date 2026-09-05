#ifndef DATABASE_H
#define DATABASE_H
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <json/json.h>
#include <QJsonObject>
#include <QObject>
class database : public QObject{
    Q_OBJECT
private:
public :
    void login_check(std::string email, std::string passwd, std::function<void(bool)> callback);
    void registerr(std::string email, std::string passwd, std::function<void(bool)> callback);
    database(QObject *parent = nullptr) : QObject(parent)
    {
    }

};

#endif // DATABASE_H
