#ifndef DATABASE_H
#define DATABASE_H
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QJsonObject>
#include <QObject>
class req{
public:
    std::string name;
    std::string aftername;
    std::string classs;
};



class studs{
public:
    std::string name;
    std::string aftername;
    int id;
};



class cgr{
public:
    int id;
    int year;
    std::string name;
    std::string aftername;
    QMap<QString, double> grades;
};

class reports{
public:
    std::string name;
    std::string classs;
};




class users{
public :
    std::string name;
    std::string gmail;
    std::string role;
};










class database : public QObject{
    Q_OBJECT
private:
public :
    QMap<QString, double> st1_student_grade(int);
    std::tuple<std::string, std::string, std::string, std::string,int,int,int> login_check(std::string email, std::string passwd);
    void registerr(std::string email, std::string passwd,std::string classy,std::string name,std::string aftername, std::function<void(bool)> callback);
    std::vector<QString> st1_student_alerts(int id);
    std::string fetch_timetable(int year,int classs);
    bool sendpost(QString subject,QString message);
    QVector<QString> get_classes(int id);
    QVector<QString> list_classes();
    std::vector<studs> get_students(std::string classs);
    std::vector<req> get_requests(int id);
    bool accept(std::string classs, std::string name,std::string aftername);
    bool deleter(std::string classs, std::string name,std::string aftername);
    QMap<QString, double> get_grades(int id);
    std::vector<cgr> get_class_grades(std::string classs);
    int post_grades(int id, QMap<QString, double> g, int *year);
    bool generate_rapport(QString classs,int id,int teid);
    std::vector<reports> loadreports(int id);
    QString rep_content(QString name,QString classs);
    bool update_timetable(QString content,int year,int classs);
    std::vector<users> list_users();







    database(QObject *parent = nullptr) : QObject(parent)
    {
    }
signals:
    void loginResult(std::vector<std::string> result);
};

#endif // DATABASE_H
