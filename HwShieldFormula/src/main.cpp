#include <Arduino.h>
#include <Arduino.h>
#include <WiFi.h>

//#include <server.hpp>
#include <can.hpp>

String canMsg = "Hello computer";
uint8_t data[12];
uint32_t id;


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
    ESP.restart();
  }
  delay(50);
  if(!WiFi.softAPConfig(local_IP, gateway, subnet)){
    Serial.println("AP failed to configurate");
    ESP.restart();
  }

  printWiFiInfo();

  server.begin();
}

void setup() {
  Serial.begin(115200);
  /*
  id = (uint32_t) 603;

  for(int i(0); i < 4; i ++){
    data[i] = ((uint8_t*)&id)[3-i];
  }

  data[4] = (uint8_t) 215;
  data[5] = (uint8_t) 196;
  data[6] = (uint8_t) 0;
  data[7] = (uint8_t) 0;
  data[8] = (uint8_t) 128;
  data[9] = (uint8_t) 13;
  data[10] = (uint8_t) 32;
  data[11] = (uint8_t) 64;
  */

  serverSetup();
  canSetup();
}

void loop() {
  
  WiFiClient client = server.available();

  if (client) {
    
    Serial.println("New connection");
    while (client.connected()) {  
      //Byte version
      canDataPack dataPack = canReceive();

      if(dataPack.canID != 0){
        convertDataPackToByteArray(data, dataPack);

        client.write(data, 12); 
      }
      

     //client.write(data, 12);

      delay(1); 
    }

    client.stop();
    
  }
}

