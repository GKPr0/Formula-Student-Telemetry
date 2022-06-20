#ifndef WIFI_CLIENT_H
#define WIFI_CLIENT_H

#include <Arduino.h>
#include <Wifi.h>

extern QueueHandle_t messageQueue;

// WiFi credentials
static const char* ssid     = "Klarka69";
static const char* password = "Fstulracing69";

// Wifi setting
static const IPAddress server_IP(192, 168, 4, 1);
static const unsigned int port = 49696;

extern uint8_t wifi_protocol;  //  802.11 available b=1, g=2, n=4 ,lr=8 can be combinedas follow 1,2,3,4,7,8
static const int8_t wifi_tx_power = 82;  // Maximum WiFi transmitting power, unit is 0.25dBm, range is [40, 82] corresponding to 10dBm - 20.5dBm here.

void wifiSetupOrReconnect();
void connectToFormula();

void wifiHandler(void *parameter);

#endif