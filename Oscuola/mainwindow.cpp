#include "mainwindow.h"
#include "./ui_mainwindow.h"
    : QMainWindow(parent)
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}