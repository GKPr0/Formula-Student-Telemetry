#ifndef SERVER_H
#define SERVER_H

#include <Arduino.h>
#include <WiFi.h>

void printWifiInfo();

void serverSetup();
void serverSend(String msg);

#endif