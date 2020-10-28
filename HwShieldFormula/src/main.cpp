#include <Arduino.h>
#include <Arduino.h>
#include <WiFi.h>

//#include <server.hpp>
#include <can.hpp>

String canMsg = "Hello computer";

// WiFi credentials
const char* ssid     = "Test_ESP_32";
const char* password = "Fstulracing69";

// Wifi setting
IPAddress local_IP(192, 168, 1, 100);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 0, 0);
int port = 80;

WiFiServer server(port);

void printWiFiInfo(){
  IPAddress IP = WiFi.softAPIP();
  
  Serial.println("Network " + String(ssid) +" is running");
  Serial.print("AP IP address: ");
  Serial.println(IP);
}

void serverSetup() {

  Serial.println("Setting AP (Access Point)…");
  
  if(!WiFi.softAP(ssid, password)){
    Serial.println("Starting AP faild");
  }
  delay(100);
  if(!WiFi.softAPConfig(local_IP, gateway, subnet)){
    Serial.println("AP failed to configurate");
  }

  printWiFiInfo();

  server.begin();
}

void setup() {
  Serial.begin(115200);
  
  serverSetup();
  canSetup();
}

void loop() {
  
  WiFiClient client = server.available();

  if (client) {
    
    Serial.println("New connection");
    while (client.connected()) {
      canDataPack dataPack =  canReceive();
  
      canMsg = convertDataPackToString(dataPack);
      client.print(canMsg);    
      delay(1); 
    }

    client.stop();
    
  }
}



