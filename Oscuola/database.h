#ifndef DATABASE_H
#define DATABASE_H
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <json/json.h>
#include <QJsonObject>
#include <QObject>
class req{
public:
    std::string name;
    std::string aftername;
    std::string classs;
};
class database : public QObject{
    Q_OBJECT
private:
public :
    QMap<QString, double> st1_student_grade(int);
    std::tuple<std::string, std::string, std::string, std::string,int,int,int> login_check(std::string email, std::string passwd);
    void registerr(std::string email, std::string passwd, std::function<void(bool)> callback);
    std::vector<QString> st1_student_alerts(int id);
    std::string fetch_timetable(int year,int classs);
    bool sendpost(QString subject,QString message);
    QVector<QString> get_classes(int id);
    std::vector<req> get_requests(int id);
    bool accept(std::string classs, std::string name,std::string aftername);
    bool deleter(std::string classs, std::string name,std::string aftername);





    database(QObject *parent = nullptr) : QObject(parent)
    {
    }
signals:
    void loginResult(std::vector<std::string> result);
};

#endif // DATABASE_H
