#ifndef SERVER_H
#define SERVER_H

#include <Arduino.h>
#include <WiFi.h>

extern QueueHandle_t messageQueue;
extern const size_t msg_send_count;

// WiFi credentials
static const char* ssid     = "Krakonos69";
static const char* password = "Fstulracing69";

// Wifi setting
static const IPAddress local_IP(192, 168, 4, 1);
static const IPAddress gateway(192, 168, 4, 100);
static const IPAddress subnet(255, 255, 255, 0);
static const unsigned int port = 23;

static const uint8_t wifi_protocol = 7; //  802.11 available b=1, g=2, n=4 ,lr=8 can be combined as follow 1,3,7,8,15
static const int8_t wifi_tx_power = 82;  // Maximum WiFi transmitting power, unit is 0.25dBm, range is [40, 82] corresponding to 10dBm - 20.5dBm here.

void serverSetup();
void serverHandler(void *parameter);

void printWiFiInfo();

#endif