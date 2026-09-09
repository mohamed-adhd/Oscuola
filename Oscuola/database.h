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
    QMap<QString, double> st1_student_grade(int);
    std::tuple<std::string, std::string, std::string, std::string,int> login_check(std::string email, std::string passwd);
    void registerr(std::string email, std::string passwd, std::function<void(bool)> callback);
    database(QObject *parent = nullptr) : QObject(parent)
    {
    }
signals:
    void loginResult(std::vector<std::string> result);
};

#endif // DATABASE_H
